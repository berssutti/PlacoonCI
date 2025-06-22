from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ProjectViewSet, AreaViewSet, InstallmentViewSet, UserManagementViewSet

router = DefaultRouter()
router.register(r'manage-users', UserManagementViewSet, basename='manage-users')
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"areas", AreaViewSet, basename="area")

projects_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
projects_router.register(
    r"installments", InstallmentViewSet, basename="project-installment"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
]
