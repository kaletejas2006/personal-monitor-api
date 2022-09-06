"""
Test custom Django management commands.
"""
from unittest.mock import patch

# A possible error that might be seen if we connect to the database before
# it is ready.
from psycopyg2 import OperationalError as Psycopyg2Error

from django.core.management import call_command
# Another possible error that can be thrown by the database server depending
# on the state of connection.
from django.db.utils import OperationalError
from django.test import SimpleTestCase

import core.management.commands.wait_for_db


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self):
        """Test waiting for database if database is ready."""
