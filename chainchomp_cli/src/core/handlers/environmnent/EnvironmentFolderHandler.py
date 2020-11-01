import os
from typing import List

from chainchomplib.data import PathProvider


class EnvironmentFolderHandler:

    def provide_list_of_environments(self) -> List[str]:
        path_to_env_vars_folder = PathProvider.env_var_folder()
        if not path_to_env_vars_folder.is_dir():
            return []

        return [str(os.path.basename(filename))
                for filename in path_to_env_vars_folder.glob('**/*') if filename.is_file()]

    @staticmethod
    def create_environments_folder():
        if PathProvider.env_var_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.env_var_folder())
        except OSError:
            # TODO Proper exception
            print('Failed to create environments dir')

        return True
