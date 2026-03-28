from datetime import datetime, timedelta
from django.utils import timezone
from ..models import Project, Installment


def get_available_years(queryset) -> dict:
    years = set()
    for project in queryset:
        if project.start_date:
            start_year = project.start_date.year
            end_year = (
                project.end_date.year if project.end_date else datetime.now().year
            )
            for year in range(start_year, end_year + 1):
                years.add(year)

    sorted_years = sorted(list(years), reverse=True)
    if not sorted_years:
        sorted_years = [datetime.now().year]

    return {"years": sorted_years, "count": queryset.count()}


def get_active_alerts():
    today = timezone.now().date()
    one_week_from_now = today + timedelta(days=7)
    alerts = []

    # 1. Projects ending within a week or already overdue
    # We define "active" projects as those not "Concluído" in the frontend logic.
    # Frontend says "Concluído" if today > end_date.
    # The user wants alerts for "chegar no prazo" (within 1 week) or "passou do prazo".
    projects_with_deadline_alerts = Project.objects.filter(
        end_date__lte=one_week_from_now
    )

    for project in projects_with_deadline_alerts:
        if project.end_date < today:
            message = f"Projeto '{project.name}' está com o prazo vencido ({project.end_date.strftime('%d/%m/%Y')})."
            alert_type = "deadline_overdue"
        else:
            message = f"Projeto '{project.name}' vence em breve ({project.end_date.strftime('%d/%m/%Y')})."
            alert_type = "deadline_near"

        alert_id = f"{project.id}_{alert_type}_{project.end_date}"
        alerts.append(
            {
                "id": alert_id,
                "project_id": project.id,
                "project_name": project.name,
                "type": alert_type,
                "message": message,
                "date": project.end_date,
            }
        )

    # 2. Overdue installments
    overdue_installments = Installment.objects.filter(status="Atrasada").select_related(
        "project"
    )
    for installment in overdue_installments:
        alert_id = f"inst_{installment.id}_overdue"
        alerts.append(
            {
                "id": alert_id,
                "project_id": installment.project.id,
                "project_name": installment.project.name,
                "installment_id": installment.id,
                "type": "installment_overdue",
                "message": f"Parcela de {installment.amount} do projeto '{installment.project.name}' está atrasada.",
                "date": installment.estimated_date,
            }
        )

    # Sort alerts by date (most recent/urgent first)
    alerts.sort(key=lambda x: x["date"], reverse=True)

    return alerts
