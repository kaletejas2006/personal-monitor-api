"""
Django command to wait for the database to be available.
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **kwargs):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up: bool = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, '
                                  'waiting for a second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Databases available!'))
