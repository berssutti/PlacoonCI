from datetime import datetime, timedelta
from typing import Any, Dict, List
from django.utils import timezone
from django.db.models import QuerySet
from ..models import Project, Installment


def get_available_years(queryset: QuerySet) -> Dict[str, Any]:
    """Retrieve all years in which projects in the queryset were active."""
    years = set()
    current_year = datetime.now().year

    for project in queryset:
        if project.start_date:
            start_year = project.start_date.year
            end_year = project.end_date.year if project.end_date else current_year
            years.update(range(start_year, end_year + 1))

    sorted_years = sorted(list(years), reverse=True)
    if not sorted_years:
        sorted_years = [current_year]

    return {"years": sorted_years, "count": queryset.count()}


def _get_project_deadline_alerts(today: datetime.date, one_week_from_now: datetime.date) -> List[Dict[str, Any]]:
    """Generate alerts for projects with approaching or passed deadlines."""
    alerts = []
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
    return alerts


def _get_overdue_installment_alerts() -> List[Dict[str, Any]]:
    """Generate alerts for installments that are overdue."""
    alerts = []
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
    return alerts


def get_active_alerts() -> List[Dict[str, Any]]:
    """Retrieve all active alerts for projects and installments."""
    today = timezone.now().date()
    one_week_from_now = today + timedelta(days=7)

    alerts = _get_project_deadline_alerts(today, one_week_from_now)
    alerts.extend(_get_overdue_installment_alerts())

    # Sort alerts by date (most recent/urgent first)
    alerts.sort(key=lambda x: x["date"], reverse=True)

    return alerts
