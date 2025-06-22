from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from projects.models import Project


@receiver(post_migrate)
def create_default_areas(sender, **kwargs):
    if sender.name == "projects":
        print("\nSignal post_migrate received. Creating default areas...")
        from projects.models import Area

        default_areas = [
            "Engenharia de Software",
            "Engenharia Eletrônica",
            "Engenharia Automotiva",
            "Engenharia Aeroespacial",
            "Engenharia de Energia",
        ]

        if Area.objects.count() == 0:
            for area_name in default_areas:
                print(f'Area "{area_name}" created.')

                Area.objects.create(nome=area_name)
            print("Default areas created.")


@receiver(post_migrate)
def create_default_groups_and_permissions(sender, **kwargs):
    if sender.name == "projects":
        print("\nSignal post_migrate received. Creating groups and permissions...")

        default_groups = [
            "Administrador",
            "Financeiro",
            "Professor",
            "Gestor"
        ]

        for group_name in default_groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f'Group "{group_name}" created.')

            group.permissions.clear()
            print(f'Permissions updated for group "{group_name}".')
