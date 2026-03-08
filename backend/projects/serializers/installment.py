from rest_framework import serializers
from decimal import Decimal
from ..models import Installment, Project


class InstallmentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    area_values = serializers.SerializerMethodField()

    class Meta:
        model = Installment
        fields = "__all__"

    def get_area_values(self, obj):
        project_areas = obj.project.projectarea_set.all()
        area_values = {}
        for project_area in project_areas:
            amount_decimal = Decimal(str(obj.amount))
            area_values[project_area.area.name] = amount_decimal * (
                project_area.percentage / Decimal("100")
            )
        return area_values
