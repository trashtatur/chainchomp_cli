import os
import unittest

from chainchomplib.data import PathProvider
from click import Command
from parameterized import parameterized

from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


class SetupHandlerTest(unittest.TestCase):

    def tearDown(self) -> None:
        try:
            os.rmdir(PathProvider.env_var_folder())
        except OSError:
            pass
        try:
            os.rmdir(PathProvider.fixtures_folder())
        except OSError:
            pass
        try:
            os.rmdir(PathProvider.installed_adapters_folder())
        except OSError:
            pass
        try:
            os.rmdir(PathProvider.profiles_folder())
        except OSError:
            pass
        try:
            os.rmdir(PathProvider.projects_folder())
        except OSError:
            pass

    @parameterized.expand([
        (False, False, False, False, False, False, False),
        (True, False, False, False, False, False, False),
        (True, True, False, False, False, False, False),
        (True, True, True, False, False, False, False),
        (True, True, True, True, False, False, False),
        (True, True, True, True, True, False, False),
        (True, True, True, True, True, True, True),
    ])
    def test_that_setup_check_works(
            self,
            create_env: bool,
            create_fixtures: bool,
            create_adapters: bool,
            create_profiles: bool,
            create_projects: bool,
            create_chainlinks: bool,
            expected: bool
    ):
        if create_env:
            os.mkdir(PathProvider.env_var_folder())
        if create_fixtures:
            os.mkdir(PathProvider.fixtures_folder())
        if create_adapters:
            os.mkdir(PathProvider.installed_adapters_folder())
        if create_profiles:
            os.mkdir(PathProvider.profiles_folder())
        if create_projects:
            os.mkdir(PathProvider.projects_folder())
        if create_chainlinks:
            os.mkdir(PathProvider.chainlinks_folder())

        def success():
            return True
        result = SetupHandler.is_setup(success)
        assert isinstance(result, Command) is not expected
        if not isinstance(result, Command):
            assert result() is expected


if __name__ == '__main__':
    unittest.main()
