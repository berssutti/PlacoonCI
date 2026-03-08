from rest_framework import serializers


class ProjectSummarySerializer(serializers.Serializer):
    name = serializers.CharField()
    expected = serializers.FloatField()
    executed = serializers.FloatField()
    pending = serializers.FloatField()
    overdue = serializers.FloatField()
    coordinator = serializers.CharField()
    start_date = serializers.CharField()
    areas = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    total_installments = serializers.IntegerField()


class OverviewSerializer(serializers.Serializer):
    total_expected = serializers.FloatField()
    total_executed = serializers.FloatField()
    total_pending = serializers.FloatField()
    total_overdue = serializers.FloatField()
    areas_summary = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), allow_empty=True)
    )
    institution_summary = serializers.DictField(
        child=serializers.FloatField(), allow_empty=True
    )
    year_summary = serializers.DictField(
        child=serializers.FloatField(), allow_empty=True
    )
    destination_summary = serializers.DictField(
        child=serializers.FloatField(), allow_empty=True
    )
    projects_summary = ProjectSummarySerializer(many=True)
    monthly_summary = serializers.DictField(
        child=serializers.FloatField(), allow_empty=True
    )
    monthly_area_summary = serializers.DictField(
        child=serializers.DictField(child=serializers.FloatField(), allow_empty=True)
    )
