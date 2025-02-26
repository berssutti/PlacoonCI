from django.db import models
from django.core.validators import RegexValidator

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
        default='Pendente',
    )
