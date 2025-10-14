from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create default roles/groups: ADMIN, MANAGER, EMPLOYEE"

    def handle(self, *args, **options):
        for name in ['ADMIN', 'MANAGER', 'EMPLOYEE']:
            Group.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Roles created/verified: ADMIN, MANAGER, EMPLOYEE"))
