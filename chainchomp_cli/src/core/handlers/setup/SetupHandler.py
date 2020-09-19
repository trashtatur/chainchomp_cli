import os

from chainchomplib.data import PathProvider


class SetupHandler:

    @staticmethod
    def is_setup() -> bool:
        return PathProvider.base_config_folder().is_dir() \
               and PathProvider.projects_folder().is_dir() \
               and PathProvider.env_var_folder().is_dir() \
               and PathProvider.profiles_folder().is_dir()

    @staticmethod
    def create_base_folder():
        if PathProvider.base_config_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.base_config_folder())
        except OSError:
            # TODO Proper exception
            print('Failed to create base dir')

        return True
