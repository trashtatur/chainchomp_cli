import os
from typing import List

from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class EnvironmentFolderHandler:

    @staticmethod
    def provide_list_of_environment_variables() -> List[str]:
        path_to_env_vars_folder = PathProvider.environment_variables_folder()
        if not path_to_env_vars_folder.is_dir():
            return []

        return [str(os.path.basename(filename))
                for filename in path_to_env_vars_folder.glob('**/*') if filename.is_file()]

    @staticmethod
    def create_environments_folder():
        if PathProvider.environment_variables_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.environment_variables_folder())
        except OSError as exception:
            LoggerInterface.error(f'Failed to create environments dir with exception: {exception}')

        return True
