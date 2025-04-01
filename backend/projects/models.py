from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Area(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField('Project', through='ProjectArea')

    def __str__(self):
        return self.name 

class Project(models.Model):
    STATUS_CHOICES = [
        ('Processando', 'Processando'),
        ('Recebido', 'Recebido'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_unb_amount_expected = models.FloatField()
    total_fcte_amount_expected = models.FloatField()
    total_compensation_expected = models.FloatField(
        null=True,
        blank=True
    )
    total_compensation_executed = models.FloatField(
        null=True,
        blank=True  
    )
    total_compensation_pending = models.FloatField(
        null=True,
        blank=True
    )
    total_compensation_overdue = models.FloatField(
        null=True,
        blank=True
    )
    coordinator = models.CharField(max_length=100)
    substitute_coordinator = models.CharField(max_length=100)
    academic_supervisor = models.CharField(max_length=100)
    processo_sei = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{5}\.\d{6}/\d{4}-\d{2}$',
                message='Must be in format ddddd.dddddd/YYYY-MM'
            )
        ]
    )
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='Processando',
    )
    nota_dotacao = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    ptres = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    ugr = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    funding_source = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    detailed_nature = models.CharField(
        max_length=8,
        null=True,
        blank=True
    )
    internal_plan = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    internal_plan_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def calculate_compensation_totals(self):
        """Calculate and update the compensation totals based on installment statuses."""
        executed = self.installments.filter(status='Quitada').aggregate(total=models.Sum('amount'))['total'] or 0
        pending = self.installments.filter(status='Pendente').aggregate(total=models.Sum('amount'))['total'] or 0
        overdue = self.installments.filter(status='Atrasada').aggregate(total=models.Sum('amount'))['total'] or 0
        expected = executed + pending + overdue

        self.total_compensation_executed = executed
        self.total_compensation_pending = pending
        self.total_compensation_overdue = overdue
        self.total_compensation_expected = expected
        self.save()


class ProjectArea(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('project', 'area')

    def __str__(self):
        return f"{self.project.name} - {self.area.name} ({self.percentage}%)"


class Installment(models.Model):
    STATUS_CHOICES = [
        ('Atrasada', 'Atrasada'),
        ('Quitada', 'Quitada'),
        ('Pendente', 'Pendente'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='installments')
    amount = models.FloatField()
    estimated_date = models.DateField()
    effective_date = models.DateField(
        null=True,
        blank=True
    )
    observation = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    
    destination = models.CharField(
        max_length=200,
        null=True,
        blank=True    
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pendente'
    )

    def __str__(self):
        return f"{self.project.name} - {self.amount} ({self.status})"


@receiver([post_save, post_delete], sender=Installment)
def update_project_compensation_totals(sender, instance, **kwargs):
    """Signal to update project compensation totals when an installment is saved or deleted."""
    instance.project.calculate_compensation_totals()
