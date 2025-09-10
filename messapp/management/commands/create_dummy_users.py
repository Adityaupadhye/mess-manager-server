from django.core.management.base import BaseCommand
from messapp.models import User

class Command(BaseCommand):
    help = 'Create 10 dummy users for each user role (student, admin, staff)'

    def handle(self, *args, **options):
        roles = ['student', 'admin', 'staff']
        created = 0
        for role in roles:
            for i in range(1, 11):
                username = f'{role}{i}'
                roll_no = f'{role[:4].upper()}2025{i:02d}'
                name = f'{role.capitalize()} User {i}'
                password = 'password123'  # In production, use proper password hashing
                hostel = f'Hostel-{i}' if role == 'student' else ''
                if not User.objects.filter(username=username).exists():
                    User.objects.create(
                        username=username,
                        name=name,
                        password=password,
                        hostel=hostel,
                        roll_no=roll_no,
                        role=role
                    )
                    created += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} dummy users.'))
