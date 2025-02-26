from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == 'projects':
        from projects.models import Area
        if Area.objects.count() == 0:
            call_command('loaddata', 'initial_data.json')