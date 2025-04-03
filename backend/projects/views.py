from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime

from rest_framework.decorators import action
from .models import Project, Area, Installment
from .serializers import ProjectSerializer, AreaSerializer, InstallmentSerializer 

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('start_date')
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.request.query_params.get('active_year', None)
        
        if year:
            try:
                year = int(year)
                start_of_year = datetime(year, 1, 1)
                end_of_year = datetime(year, 12, 31)
                
                # Filter projects that were active during the specified year
                queryset = queryset.filter(
                    Q(start_date__lte=end_of_year) &  # Started before or during the year
                    (Q(end_date__gte=start_of_year) | Q(end_date__isnull=True))  # Ended after or during the year
                )
            except ValueError:
                # If year is not a valid integer, return all projects
                pass
                
        return queryset

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class InstallmentViewSet(viewsets.ModelViewSet):
    serializer_class = InstallmentSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Installment.objects.filter(project_id=project_id).order_by('estimated_date')