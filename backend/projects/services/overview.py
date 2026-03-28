from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Tuple
from django.db.models import Q, QuerySet
from ..models import Project, Installment


def sum_amounts(inst_list: List[Installment]) -> Decimal:
    """Sum amounts of a list of installments returning Decimal."""
    return sum((Decimal(str(inst.amount or 0)) for inst in inst_list), Decimal("0"))


def distribute_to_areas(
    installs: List[Installment],
    field_key: str,
    p_areas: List[Any],
    areas_summary_map: Dict[str, Dict[str, Any]],
) -> None:
    """Distribute installment amounts to project areas in the summary map."""
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


def _get_projects_and_installments(
    queryset: QuerySet, start_of_year: datetime, end_of_year: datetime
) -> Tuple[List[Project], List[int], QuerySet]:
    """Fetch projects and relevant installments for the year."""
    projects = list(
        queryset.order_by("start_date").filter(
            Q(start_date__lte=end_of_year)
            & (Q(end_date__gte=start_of_year) | Q(end_date__isnull=True))
        )
    )

    project_ids = [p.id for p in projects]

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

    return projects, project_ids, all_installments


def _categorize_installments(
    all_installments: QuerySet,
    project_ids: List[int],
    start_of_year: datetime,
    end_of_year: datetime,
) -> Tuple[
    List[Installment],
    List[Installment],
    List[Installment],
    Dict[int, List[Installment]],
    Dict[int, List[Installment]],
    Dict[int, List[Installment]],
]:
    """Categorize installments into executed, pending, and overdue."""
    installments_executed = []
    installments_pending = []
    installments_overdue = []

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

    return (
        installments_executed,
        installments_pending,
        installments_overdue,
        project_executed_map,
        project_pending_map,
        project_overdue_map,
    )


def _build_projects_summary(
    projects: List[Project],
    project_executed_map: Dict[int, List[Installment]],
    project_pending_map: Dict[int, List[Installment]],
    project_overdue_map: Dict[int, List[Installment]],
) -> List[Dict[str, Any]]:
    """Build the detailed projects summary list."""
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
                "expected": float(val_executed + val_pending + val_overdue),
                "executed": float(val_executed),
                "pending": float(val_pending),
                "overdue": float(val_overdue),
                "coordinator": project_coordinator,
                "start_date": project_start_date,
                "areas": areas_name_list,
                "total_installments": total_installments_count,
            }
        )
    return projects_summary


def _build_areas_summary(
    projects: List[Project],
    project_executed_map: Dict[int, List[Installment]],
    project_pending_map: Dict[int, List[Installment]],
    project_overdue_map: Dict[int, List[Installment]],
) -> List[Dict[str, Any]]:
    """Build the areas summary list."""
    areas_summary_map = {}
    for project in projects:
        p_areas = project.projectarea_set.all()
        if not p_areas:
            continue

        distribute_to_areas(
            project_executed_map[project.id], "executed", p_areas, areas_summary_map
        )
        distribute_to_areas(
            project_pending_map[project.id], "pending", p_areas, areas_summary_map
        )
        distribute_to_areas(
            project_overdue_map[project.id], "overdue", p_areas, areas_summary_map
        )

    areas_summary = []
    for name, data in areas_summary_map.items():
        data["budget"] = data["executed"] + data["pending"] + data["overdue"]
        data["progress"] = (
            (data["executed"] / data["budget"] * 100) if data["budget"] > 0 else 0
        )
        areas_summary.append(data)
    return areas_summary


def _build_monthly_summaries(
    installments_executed: List[Installment],
    projects: List[Project],
    project_executed_map: Dict[int, List[Installment]],
) -> Tuple[Dict[int, float], Dict[int, Dict[str, float]]]:
    """Build monthly totals and monthly area summaries."""
    monthly_summary = {month: 0.0 for month in range(1, 13)}
    for inst in installments_executed:
        m = inst.effective_date.month
        monthly_summary[m] += float(inst.amount or 0)

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
                    monthly_area_summary[m][area_name] = 0.0

                share = amount * (pa.percentage / Decimal("100"))
                monthly_area_summary[m][area_name] += float(share)

    return monthly_summary, monthly_area_summary


def _build_aggregated_summaries(
    installments_executed: List[Installment], total_executed: Decimal
) -> Tuple[Dict[str, float], Dict[int, float], Dict[str, float]]:
    """Build institution, year, and destination summaries."""
    institution_summary = {"FCTE": float(total_executed)}

    year_summary = {}
    for inst in installments_executed:
        y = inst.effective_date.year
        if y not in year_summary:
            year_summary[y] = 0.0
        year_summary[y] += float(inst.amount or 0)

    destination_summary = {}
    for inst in installments_executed:
        destination = inst.destination or "Não especificado"
        if destination not in destination_summary:
            destination_summary[destination] = 0.0
        destination_summary[destination] += float(inst.amount or 0)

    return institution_summary, year_summary, destination_summary


def get_overview_data(queryset: QuerySet, year: int) -> Dict[str, Any]:
    """
    Main entry point for retrieving overview data for a specific year.
    Orchestrates data fetching, categorization, and summary building.
    """
    start_of_year = datetime(year, 1, 1)
    end_of_year = datetime(year, 12, 31)

    projects, project_ids, all_installments = _get_projects_and_installments(
        queryset, start_of_year, end_of_year
    )

    (
        installments_executed,
        installments_pending,
        installments_overdue,
        project_executed_map,
        project_pending_map,
        project_overdue_map,
    ) = _categorize_installments(all_installments, project_ids, start_of_year, end_of_year)

    total_executed = sum_amounts(installments_executed)
    total_pending = sum_amounts(installments_pending)
    total_overdue = sum_amounts(installments_overdue)
    total_expected = total_executed + total_pending + total_overdue

    projects_summary = _build_projects_summary(
        projects, project_executed_map, project_pending_map, project_overdue_map
    )

    areas_summary = _build_areas_summary(
        projects, project_executed_map, project_pending_map, project_overdue_map
    )

    monthly_summary, monthly_area_summary = _build_monthly_summaries(
        installments_executed, projects, project_executed_map
    )

    institution_summary, year_summary, destination_summary = _build_aggregated_summaries(
        installments_executed, total_executed
    )

    return {
        "total_expected": float(total_expected),
        "total_executed": float(total_executed),
        "total_pending": float(total_pending),
        "total_overdue": float(total_overdue),
        "areas_summary": areas_summary,
        "institution_summary": institution_summary,
        "year_summary": year_summary,
        "destination_summary": destination_summary,
        "projects_summary": projects_summary,
        "monthly_summary": monthly_summary,
        "monthly_area_summary": monthly_area_summary,
    }
