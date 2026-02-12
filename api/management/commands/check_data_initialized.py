import sys

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Check if the database is initialized with users'

    def handle(self, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'htmt_api_user'
                    );
                """)
                table_exists = cursor.fetchone()[0]
                
                if not table_exists:
                    self.stdout.write(self.style.ERROR('User table does not exist. Data should be initialized.'))
                    sys.exit(1)
                
                cursor.execute("SELECT COUNT(*) FROM htmt_api_user;")
                user_count = cursor.fetchone()[0]
                
                if user_count > 0:
                    self.stdout.write(self.style.SUCCESS('Users found in the database.'))
                    sys.exit(0)
                else:
                    self.stdout.write(self.style.ERROR('No users found in the database. Data should be initialized.'))
                    sys.exit(1)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error checking database initialization: {e}'))
            sys.exit(1)
