from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q, Sum
from datetime import datetime
from decimal import Decimal

from rest_framework.decorators import action
from .models import Project, Area, Installment
from .serializers import ProjectSerializer, AreaSerializer, InstallmentSerializer, OverviewSerializer

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

    @action(detail=False, methods=['get'])
    def overview(self, request):
        year = request.query_params.get('year', None)
        if not year:
            return Response({'error': 'Year parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
            start_of_year = datetime(year, 1, 1)
            end_of_year = datetime(year, 12, 31)
        except ValueError:
            return Response({'error': 'Invalid year format'}, status=status.HTTP_400_BAD_REQUEST)

        # Get projects active in the specified year
        projects = self.get_queryset().filter(
            Q(start_date__lte=end_of_year) & 
            (Q(end_date__gte=start_of_year) | Q(end_date__isnull=True))
        )

        # Get all installments for these projects with estimated_date in the selected year
        installments = Installment.objects.filter(
            project__in=projects,
            estimated_date__gte=start_of_year,
            estimated_date__lte=end_of_year
        )

        # Calculate totals based on installments
        total_expected = float(sum(installment.amount or 0 for installment in installments))
        
        # Calculate executed amount (installments with effective_date)
        total_executed = float(sum(
            installment.amount or 0 
            for installment in installments 
            if installment.effective_date is not None
        ))
        
        # Calculate pending amount (installments without effective_date and not overdue)
        total_pending = float(sum(
            installment.amount or 0 
            for installment in installments 
            if installment.effective_date is None and installment.status != 'Atrasada'
        ))
        
        # Calculate overdue amount (installments with status 'Atrasada')
        total_overdue = float(sum(
            installment.amount or 0 
            for installment in installments 
            if installment.status == 'Atrasada'
        ))

        # Calculate projects summary
        projects_summary = []
        for project in projects:
            project_installments = installments.filter(project=project)
            project_expected = float(sum(installment.amount or 0 for installment in project_installments))
            project_executed = float(sum(
                installment.amount or 0 
                for installment in project_installments 
                if installment.effective_date is not None
            ))
            project_pending = float(sum(
                installment.amount or 0 
                for installment in project_installments 
                if installment.effective_date is None and installment.status != 'Atrasada'
            ))
            project_overdue = float(sum(
                installment.amount or 0 
                for installment in project_installments 
                if installment.status == 'Atrasada'
            ))

            projects_summary.append({
                'name': project.name,
                'expected': project_expected,
                'executed': project_executed,
                'pending': project_pending,
                'overdue': project_overdue
            })

        # Calculate area summaries
        areas_summary = []
        for project in projects:
            project_installments = installments.filter(project=project)
            
            for project_area in project.projectarea_set.all():
                area_name = project_area.area.name
                area_data = next((item for item in areas_summary if item['name'] == area_name), None)
                
                if not area_data:
                    area_data = {
                        'name': area_name,
                        'budget': 0,
                        'executed': 0,
                        'pending': 0,
                        'overdue': 0,
                        'progress': 0
                    }
                    areas_summary.append(area_data)

                # Calculate area values based on installments and percentage
                for installment in project_installments:
                    amount = installment.amount or 0
                    area_amount = Decimal(str(amount)) * (project_area.percentage / Decimal('100'))
                    
                    area_data['budget'] += float(area_amount)
                    
                    if installment.effective_date is not None:
                        area_data['executed'] += float(area_amount)
                    elif installment.status == 'Atrasada':
                        area_data['overdue'] += float(area_amount)
                    else:
                        area_data['pending'] += float(area_amount)
                
                area_data['progress'] = (area_data['executed'] / area_data['budget'] * 100) if area_data['budget'] > 0 else 0

        # Calculate monthly summary
        monthly_summary = {}
        for month in range(1, 13):
            month_start = datetime(year, month, 1)
            month_end = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            month_installments = installments.filter(
                effective_date__gte=month_start,
                effective_date__lt=month_end
            )
            monthly_summary[month] = float(sum(installment.amount or 0 for installment in month_installments))

        # Calculate institution summary (FCTE)
        institution_summary = {'FCTE': float(sum(installment.amount or 0 for installment in installments))}

        # Calculate year summary
        year_summary = {}
        for installment in installments:
            year = installment.estimated_date.year
            if year not in year_summary:
                year_summary[year] = 0
            year_summary[year] += float(installment.amount or 0)

        # Calculate destination summary
        destination_summary = {}
        for installment in installments:
            destination = installment.destination or 'Não especificado'
            if destination not in destination_summary:
                destination_summary[destination] = 0
            destination_summary[destination] += float(installment.amount or 0)

        data = {
            'total_expected': total_expected,
            'total_executed': total_executed,
            'total_pending': total_pending,
            'total_overdue': total_overdue,
            'areas_summary': areas_summary,
            'institution_summary': institution_summary,
            'year_summary': year_summary,
            'destination_summary': destination_summary,
            'projects_summary': projects_summary,
            'monthly_summary': monthly_summary
        }

        serializer = OverviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class InstallmentViewSet(viewsets.ModelViewSet):
    serializer_class = InstallmentSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        queryset = Installment.objects.filter(project_id=project_id)
        
        year = self.request.query_params.get('year', None)
        if year:
            try:
                year = int(year)
                start_of_year = datetime(year, 1, 1)
                end_of_year = datetime(year, 12, 31)
                queryset = queryset.filter(
                    estimated_date__gte=start_of_year,
                    estimated_date__lte=end_of_year
                )
            except ValueError:
                # If year is not a valid integer, return all installments
                pass
                
        return queryset.order_by('estimated_date')