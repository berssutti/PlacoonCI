from datetime import datetime
from ..models import Project


def get_available_years(queryset) -> dict:
    
    # We need to filter by permissions if needed, but original code 
    # used `self.filter_queryset(self.get_queryset())`. 
    # If there's no custom filter backend that relies on request, we are safe.
    # The original view used `ProjectViewSet.queryset = Project.objects.all().order_by("start_date")`
    # and `get_queryset` added prefetch.
    # `filter_queryset` loops through filter backends.
    # Assuming standard DRF behavior, if we want to extract this completely, 
    # we might lose some filtering if it was applied via URL params on `available_years` endpoint (unlikely for this specific endpoint logic)
    # However, the original code:
    # `def available_years(self, request): queryset = self.filter_queryset(self.get_queryset())`
    # It seems `available_years` might be affected by filters on `ProjectViewSet`?
    # But `available_years` is a list of ALL years available in the system, usually.
    # Let's assume for now we want all projects. 
    # If the user filters projects by something, `available_years` might respect that?
    # The original implementation calls `filter_queryset`. 
    # If I move this to service, I should probably pass the queryset?
    # For now, I'll just query all.
    
    years = set()
    for project in queryset:
        if project.start_date:
            start_year = project.start_date.year
            end_year = project.end_date.year if project.end_date else datetime.now().year
            for year in range(start_year, end_year + 1):
                years.add(year)
    
    sorted_years = sorted(list(years), reverse=True)
    if not sorted_years:
        sorted_years = [datetime.now().year]
        
    return {
        "years": sorted_years,
        "count": queryset.count()
    }
