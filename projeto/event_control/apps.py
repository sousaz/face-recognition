from django.apps import AppConfig
from django.db.models.signals import post_migrate

class EventControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event_control'

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)

def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    
    groups = {
        'admin': "__all__",
        'student': ["view_student"]
    }

    for group_name, permissions in groups.items():
        group, create = Group.objects.get_or_create(name=group_name)

        if permissions == "__all__":
            all_permissions = Permission.objects.all()
            group.permissions.set(all_permissions)
        elif permissions:
            for codename in permissions:
                permission = Permission.objects.filter(codename=codename).first()
                if permission:
                    group.permissions.add(permission)
