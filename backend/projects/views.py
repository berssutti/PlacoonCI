from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q, Exists, OuterRef, Case, When, Value, BooleanField, QuerySet
from django.utils import timezone
from datetime import datetime, timedelta

from rest_framework.decorators import action
from .models import Project, Area, Installment
from .serializers import (
    ProjectSerializer,
    AreaSerializer,
    InstallmentSerializer,
    OverviewSerializer,
)
from .services import overview as overview_service
from .services import project as project_service


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("start_date")
    serializer_class = ProjectSerializer

    def get_queryset(self) -> QuerySet:
        """Override get_queryset to apply alerts annotation and active year filtering."""
        queryset = super().get_queryset().prefetch_related("projectarea_set__area")
        queryset = self._annotate_project_alerts(queryset)

        active_year = self.request.query_params.get("active_year")
        if active_year:
            queryset = self._filter_projects_by_active_year(queryset, active_year)

        return queryset

    def _annotate_project_alerts(self, queryset: QuerySet) -> QuerySet:
        """Annotate projects with a boolean flag indicating if they have any active alerts."""
        today = timezone.now().date()
        one_week_from_now = today + timedelta(days=7)

        overdue_installments = Installment.objects.filter(
            project=OuterRef("pk"), status="Atrasada"
        )

        return queryset.annotate(
            has_alerts=Case(
                When(
                    Q(end_date__lte=one_week_from_now) | Exists(overdue_installments),
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

    def _filter_projects_by_active_year(self, queryset: QuerySet, year_str: str) -> QuerySet:
        """Filter projects based on their activity within the specified year."""
        try:
            year = int(year_str)
            start_of_year = datetime(year, 1, 1)
            end_of_year = datetime(year, 12, 31)

            return queryset.filter(
                Q(start_date__lte=end_of_year)
                & (Q(end_date__gte=start_of_year) | Q(end_date__isnull=True))
            )
        except ValueError:
            return queryset

    @action(detail=False, methods=["get"], url_path="available-years")
    def available_years(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = project_service.get_available_years(queryset)
        return Response(data)

    @action(detail=False, methods=["get"])
    def alerts(self, request):
        alerts = project_service.get_active_alerts()
        return Response(alerts)

    @action(detail=False, methods=["get"])
    def overview(self, request):
        year_str = request.query_params.get("year")
        if not year_str:
            return Response(
                {"error": "Year parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            year = int(year_str)
        except ValueError:
            return Response(
                {"error": "Invalid year format"}, status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.filter_queryset(self.get_queryset())
        data = overview_service.get_overview_data(queryset, year)

        serializer = OverviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class InstallmentViewSet(viewsets.ModelViewSet):
    serializer_class = InstallmentSerializer

    def get_queryset(self) -> QuerySet:
        """Override get_queryset to filter installments by project and optionally by year."""
        project_id = self.kwargs.get("project_pk")
        queryset = (
            Installment.objects.filter(project_id=project_id)
            .select_related("project")
            .prefetch_related("project__projectarea_set__area")
        )

        year_str = self.request.query_params.get("year")
        if year_str:
            queryset = self._filter_installments_by_year(queryset, year_str)

        return queryset.order_by("estimated_date")

    def _filter_installments_by_year(self, queryset: QuerySet, year_str: str) -> QuerySet:
        """Filter installments based on their estimated date within the specified year."""
        try:
            year = int(year_str)
            start_of_year = datetime(year, 1, 1)
            end_of_year = datetime(year, 12, 31)
            return queryset.filter(
                estimated_date__gte=start_of_year, estimated_date__lte=end_of_year
            )
        except ValueError:
            return queryset
