from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from messapp.models import User

class Command(BaseCommand):
    help = "Migrates old plain-text passwords to hashed Django format"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        updated = 0

        for user in users:
            # Check if password is already hashed
            if not user.password.startswith('pbkdf2_'):
                raw = user.password  # plain text
                user.password = make_password(raw)
                user.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Passwords migrated: {updated}"))
