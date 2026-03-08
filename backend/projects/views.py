from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime

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

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("projectarea_set__area")
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

    @action(detail=False, methods=["get"], url_path="available-years")
    def available_years(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = project_service.get_available_years(queryset)
        return Response(data)

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

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        queryset = (
            Installment.objects.filter(project_id=project_id)
            .select_related("project")
            .prefetch_related("project__projectarea_set__area")
        )

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
