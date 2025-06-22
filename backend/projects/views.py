from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User, Group
from rest_framework.decorators import action
from .permissions import IsProfessor, IsFinanceiro, IsGestor, IsAdmin
from .models import Project, Area, Installment
from .serializers import (
    ProjectSerializer,
    AreaSerializer,
    InstallmentSerializer,
    OverviewSerializer,
)

from .serializers import UserSerializer 

class UserManagementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar e gerenciar usuários por um Admin.
    'ReadOnlyModelViewSet' permite apenas listar e ver detalhes, não editar diretamente.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['post'], url_path='set-group')
    def set_group(self, request, pk=None):
        """
        Ação customizada para definir o grupo de um usuário.
        Acessível via POST /api/manage-users/{user_id}/set-group/
        """
        user = self.get_object()
        group_name = request.data.get('group_name')

        if not group_name:
            return Response({'error': 'O nome do grupo (group_name) é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({'error': f'O grupo "{group_name}" não existe.'}, status=status.HTTP_400_BAD_REQUEST)

        user.groups.set([group])

        return Response({'status': f'Usuário {user.username} movido para o grupo {group.name}.'}, status=status.HTTP_200_OK)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("start_date")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsFinanceiro]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsFinanceiro | IsGestor]
        elif self.action == "destroy":
            permission_classes = [IsFinanceiro]
        else:
            permission_classes = [IsProfessor | IsFinanceiro | IsGestor]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.request.query_params.get("active_year", None)

        if year:
            try:
                year = int(year)
                start_of_year = datetime(year, 1, 1)
                end_of_year = datetime(year, 12, 31)

                queryset = queryset.filter(
                    Q(start_date__lte=end_of_year)  # Started before or during the year
                    & (
                        Q(end_date__gte=start_of_year) | Q(end_date__isnull=True)
                    )  # Ended after or during the year
                )
            except ValueError:
                pass

        return queryset

    @action(detail=False, methods=["get"])
    def overview(self, request):
        year = request.query_params.get("year", None)
        if not year:
            return Response(
                {"error": "Year parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            year = int(year)
            start_of_year = datetime(year, 1, 1)
            end_of_year = datetime(year, 12, 31)
        except ValueError:
            return Response(
                {"error": "Invalid year format"}, status=status.HTTP_400_BAD_REQUEST
            )

        projects = self.get_queryset().filter(
            Q(start_date__lte=end_of_year)
            & (Q(end_date__gte=start_of_year) | Q(end_date__isnull=True))
        )

        installments = Installment.objects.filter(
            project__in=projects,
            effective_date__gte=start_of_year,
            effective_date__lte=end_of_year,
            status="Quitada",
        )

        total_expected = float(
            sum(installment.amount or 0 for installment in installments)
        )

        total_executed = float(
            sum(installment.amount or 0 for installment in installments)
        )

        pending_installments = Installment.objects.filter(
            project__in=projects,
            estimated_date__gte=start_of_year,
            estimated_date__lte=end_of_year,
            effective_date__isnull=True,
            status__in=["Pendente"],
        )
        total_pending = float(
            sum(installment.amount or 0 for installment in pending_installments)
        )

        overdue_installments = Installment.objects.filter(
            project__in=projects,
            estimated_date__gte=start_of_year,
            estimated_date__lte=end_of_year,
            status="Atrasada",
        )
        total_overdue = float(
            sum(installment.amount or 0 for installment in overdue_installments)
        )

        total_expected = total_executed + total_pending + total_overdue

        projects_summary = []
        for project in projects:
            project_installments = installments.filter(project=project)
            project_pending_installments = pending_installments.filter(project=project)
            project_overdue_installments = overdue_installments.filter(project=project)

            total_installments = (
                project_installments.count()
                + project_pending_installments.count()
                + project_overdue_installments.count()
            )

            project_executed = float(
                sum(installment.amount or 0 for installment in project_installments)
            )
            project_pending = float(
                sum(
                    installment.amount or 0
                    for installment in project_pending_installments
                )
            )
            project_overdue = float(
                sum(
                    installment.amount or 0
                    for installment in project_overdue_installments
                )
            )
            project_expected = project_executed + project_pending + project_overdue
            project_coordinator = (
                project.coordinator if project.coordinator else "Não especificado"
            )
            project_start_date = (
                project.start_date.strftime("%d/%m/%Y")
                if project.start_date
                else "Não especificado"
            )
            areas_name_list = [
                project_area.area.name for project_area in project.projectarea_set.all()
            ]

            projects_summary.append(
                {
                    "name": project.name,
                    "expected": project_expected,
                    "executed": project_executed,
                    "pending": project_pending,
                    "overdue": project_overdue,
                    "coordinator": project_coordinator,
                    "start_date": project_start_date,
                    "areas": areas_name_list,
                    "total_installments": total_installments,
                }
            )

        areas_summary = []
        for project in projects:
            project_installments = installments.filter(project=project)
            project_pending_installments = pending_installments.filter(project=project)
            project_overdue_installments = overdue_installments.filter(project=project)

            for project_area in project.projectarea_set.all():
                area_name = project_area.area.name
                area_data = next(
                    (item for item in areas_summary if item["name"] == area_name), None
                )

                if not area_data:
                    area_data = {
                        "name": area_name,
                        "budget": 0,
                        "executed": 0,
                        "pending": 0,
                        "overdue": 0,
                        "progress": 0,
                    }
                    areas_summary.append(area_data)

                for installment in project_installments:
                    amount = installment.amount or 0
                    area_amount = Decimal(str(amount)) * (
                        project_area.percentage / Decimal("100")
                    )
                    area_data["executed"] += float(area_amount)

                for installment in project_pending_installments:
                    amount = installment.amount or 0
                    area_amount = Decimal(str(amount)) * (
                        project_area.percentage / Decimal("100")
                    )
                    area_data["pending"] += float(area_amount)

                for installment in project_overdue_installments:
                    amount = installment.amount or 0
                    area_amount = Decimal(str(amount)) * (
                        project_area.percentage / Decimal("100")
                    )
                    area_data["overdue"] += float(area_amount)

                area_data["budget"] = (
                    area_data["executed"] + area_data["pending"] + area_data["overdue"]
                )
                area_data["progress"] = (
                    (area_data["executed"] / area_data["budget"] * 100)
                    if area_data["budget"] > 0
                    else 0
                )

        monthly_summary = {}
        for month in range(1, 13):
            month_start = datetime(year, month, 1)
            month_end = (
                datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            )
            month_installments = installments.filter(
                effective_date__gte=month_start,
                effective_date__lt=month_end,
                status="Quitada",  # Apenas parcelas quitadas
            )
            monthly_summary[month] = float(
                sum(installment.amount or 0 for installment in month_installments)
            )

        monthly_area_summary = {}
        for month in range(1, 13):
            month_start = datetime(year, month, 1)
            month_end = (
                datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            )

            month_installments = installments.filter(
                effective_date__gte=month_start,
                effective_date__lt=month_end,
                status="Quitada",  # Apenas parcelas quitadas
            )

            monthly_area_summary[month] = {}

            for project in projects:
                project_installments = month_installments.filter(project=project)

                for project_area in project.projectarea_set.all():
                    area_name = project_area.area.name

                    area_amount = sum(
                        Decimal(str(installment.amount or 0))
                        * (project_area.percentage / Decimal("100"))
                        for installment in project_installments
                    )

                    if area_name not in monthly_area_summary[month]:
                        monthly_area_summary[month][area_name] = 0
                    monthly_area_summary[month][area_name] += float(area_amount)

        executed_installments = installments.filter(
            effective_date__isnull=False, status="Quitada"
        )
        institution_summary = {
            "FCTE": float(
                sum(installment.amount or 0 for installment in executed_installments)
            )
        }

        year_summary = {}
        for installment in executed_installments:
            year = installment.effective_date.year
            if year not in year_summary:
                year_summary[year] = 0
            year_summary[year] += float(installment.amount or 0)

        destination_summary = {}
        for installment in executed_installments:
            destination = installment.destination or "Não especificado"
            if destination not in destination_summary:
                destination_summary[destination] = 0
            destination_summary[destination] += float(installment.amount or 0)

        data = {
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

        serializer = OverviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]


class InstallmentViewSet(viewsets.ModelViewSet):
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        queryset = Installment.objects.filter(project_id=project_id)

        year = self.request.query_params.get("year", None)
        if year:
            try:
                year = int(year)
                start_of_year = datetime(year, 1, 1)
                end_of_year = datetime(year, 12, 31)
                queryset = queryset.filter(
                    estimated_date__gte=start_of_year, estimated_date__lte=end_of_year
                )
            except ValueError:
                pass

        return queryset.order_by("estimated_date")
