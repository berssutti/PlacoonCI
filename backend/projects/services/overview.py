from datetime import datetime
from decimal import Decimal
from django.db.models import Q
from ..models import Project, Installment


def get_overview_data(queryset, year: int) -> dict:
    start_of_year = datetime(year, 1, 1)
    end_of_year = datetime(year, 12, 31)

    # Optimization: Fetch projects with their areas in one query
    projects = list(
        queryset
        .order_by("start_date")
        .filter(
            Q(start_date__lte=end_of_year)
            & (Q(end_date__gte=start_of_year) | Q(end_date__isnull=True))
        )
    )

    project_ids = [p.id for p in projects]

    # Optimization: Fetch all relevant installments in one query
    # We fetch a superset of installments needed for all metrics to avoid multiple DB hits
    all_installments = (
        Installment.objects.filter(project_id__in=project_ids)
        .filter(
            Q(effective_date__range=(start_of_year, end_of_year), status="Quitada")
            | Q(
                estimated_date__range=(start_of_year, end_of_year),
                status__in=["Pendente", "Atrasada"],
            )
        )
        .select_related("project")
    )

    # In-memory categorization
    installments_executed = []
    installments_pending = []
    installments_overdue = []

    # Maps for quick lookup per project
    project_executed_map = {p_id: [] for p_id in project_ids}
    project_pending_map = {p_id: [] for p_id in project_ids}
    project_overdue_map = {p_id: [] for p_id in project_ids}

    for inst in all_installments:
        is_in_executed_range = (
            inst.effective_date
            and start_of_year.date() <= inst.effective_date <= end_of_year.date()
        )
        is_in_estimated_range = (
            inst.estimated_date
            and start_of_year.date() <= inst.estimated_date <= end_of_year.date()
        )

        if inst.status == "Quitada" and is_in_executed_range:
            installments_executed.append(inst)
            project_executed_map[inst.project_id].append(inst)

        elif (
            inst.status == "Pendente"
            and is_in_estimated_range
            and inst.effective_date is None
        ):
            installments_pending.append(inst)
            project_pending_map[inst.project_id].append(inst)

        elif inst.status == "Atrasada" and is_in_estimated_range:
            installments_overdue.append(inst)
            project_overdue_map[inst.project_id].append(inst)

    # Helper to sum amounts
    def sum_amounts(inst_list):
        return float(sum(inst.amount or 0 for inst in inst_list))

    total_executed = sum_amounts(installments_executed)
    total_pending = sum_amounts(installments_pending)
    total_overdue = sum_amounts(installments_overdue)
    total_expected = total_executed + total_pending + total_overdue

    # Projects Summary
    projects_summary = []
    for project in projects:
        p_exec = project_executed_map[project.id]
        p_pend = project_pending_map[project.id]
        p_over = project_overdue_map[project.id]

        val_executed = sum_amounts(p_exec)
        val_pending = sum_amounts(p_pend)
        val_overdue = sum_amounts(p_over)

        total_installments_count = len(p_exec) + len(p_pend) + len(p_over)

        project_coordinator = (
            project.coordinator if project.coordinator else "Não especificado"
        )
        project_start_date = (
            project.start_date.strftime("%d/%m/%Y")
            if project.start_date
            else "Não especificado"
        )
        # No DB hit here due to prefetch
        areas_name_list = [
            project_area.area.name for project_area in project.projectarea_set.all()
        ]

        projects_summary.append(
            {
                "name": project.name,
                "expected": val_executed + val_pending + val_overdue,
                "executed": val_executed,
                "pending": val_pending,
                "overdue": val_overdue,
                "coordinator": project_coordinator,
                "start_date": project_start_date,
                "areas": areas_name_list,
                "total_installments": total_installments_count,
            }
        )

    # Areas Summary
    areas_summary_map = {}  # name -> data dict

    # We reuse the previously categorized lists
    # But we need to iterate projects to get area percentages

    # To avoid N*M complexity, we can iterate projects and their specific installs
    for project in projects:
        p_areas = project.projectarea_set.all()
        if not p_areas:
            continue

        # Function to distribute amount to areas
        def distribute_to_areas(installs, field_key):
            for inst in installs:
                amount = Decimal(str(inst.amount or 0))
                for pa in p_areas:
                    area_name = pa.area.name
                    if area_name not in areas_summary_map:
                        areas_summary_map[area_name] = {
                            "name": area_name,
                            "budget": 0.0,
                            "executed": 0.0,
                            "pending": 0.0,
                            "overdue": 0.0,
                            "progress": 0.0,
                        }

                    share = amount * (pa.percentage / Decimal("100"))
                    areas_summary_map[area_name][field_key] += float(share)

        distribute_to_areas(project_executed_map[project.id], "executed")
        distribute_to_areas(project_pending_map[project.id], "pending")
        distribute_to_areas(project_overdue_map[project.id], "overdue")

    # Calculate budget and progress for areas
    areas_summary = []
    for name, data in areas_summary_map.items():
        data["budget"] = data["executed"] + data["pending"] + data["overdue"]
        data["progress"] = (
            (data["executed"] / data["budget"] * 100) if data["budget"] > 0 else 0
        )
        areas_summary.append(data)

    # Monthly Summary
    monthly_summary = {}
    for month in range(1, 13):
        monthly_summary[month] = 0.0

    for inst in installments_executed:
        m = inst.effective_date.month
        monthly_summary[m] += float(inst.amount or 0)

    # Monthly Area Summary
    monthly_area_summary = {m: {} for m in range(1, 13)}

    for project in projects:
        p_exec = project_executed_map[project.id]
        p_areas = project.projectarea_set.all()

        for inst in p_exec:
            m = inst.effective_date.month
            amount = Decimal(str(inst.amount or 0))

            for pa in p_areas:
                area_name = pa.area.name
                if area_name not in monthly_area_summary[m]:
                    monthly_area_summary[m][area_name] = 0

                share = amount * (pa.percentage / Decimal("100"))
                monthly_area_summary[m][area_name] += float(share)

    institution_summary = {"FCTE": total_executed}  # Sum of execution for this year

    # Year Summary
    year_summary = {}
    for inst in installments_executed:
        y = inst.effective_date.year
        if y not in year_summary:
            year_summary[y] = 0
        year_summary[y] += float(inst.amount or 0)

    # Destination Summary
    destination_summary = {}
    for inst in installments_executed:
        destination = inst.destination or "Não especificado"
        if destination not in destination_summary:
            destination_summary[destination] = 0
        destination_summary[destination] += float(inst.amount or 0)

    return {
        "total_expected": total_expected,
        "total_executed": total_executed,
        "total_pending": total_pending,
        "total_overdue": total_overdue,
        "areas_summary": areas_summary,
        "institution_summary": institution_summary,
        "year_summary": year_summary,
        "destination_summary": destination_summary,
        "projects_summary": projects_summary,
        "monthly_summary": monthly_summary,
        "monthly_area_summary": monthly_area_summary,
    }
