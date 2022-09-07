"""
Test custom Django management commands.
"""
from unittest.mock import patch

# A possible error that might be seen if we connect to the database before
# it is ready.
from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
# Another possible error that can be thrown by the database server depending
# on the state of connection.
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready.

        :param patched_check:
        :return:
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError.
        With the side effect code written below, we define that:
        - The first two times that the mocked `check` function is executed,
        `Psycopg2Error` is thrown.
        - The next three times that the mocked `check` function is executed,
        `OperationalError` is thrown.
        - A `True` is returned when `check` is called for the last time.

        The motivation is that initially, `psycopg2` will return an exception
        as the service (database server) has not started. Once it is up and
        running, some time might be required to set up the test database
        which in turn can lead to `OperationalError`.

        In the `wait_for_db` method, we wait for a second after every
        check to prevent overloading the database server with status
        requests. As we are mocking the database connection check call here,
        it does not make sense to wait for outputs were already know hence
        we mock the sleep method as well.

        :param patched_sleep:
        :param patched_check:
        :return:
        """
        patched_check.side_effect = ([Psycopg2OpError] * 2 +
                                     [OperationalError] * 3 +
                                     [True])

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
