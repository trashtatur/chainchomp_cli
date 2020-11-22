import os
from typing import List

from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class ProjectsFolderHandler:

    @staticmethod
    def provide_list_of_projects() -> List[str]:
        path_to_projects_folder = PathProvider.projects_folder()
        if not path_to_projects_folder.is_dir():
            return []

        return [str(os.path.basename(filename))
                for filename in path_to_projects_folder.glob('**/*') if filename.is_file()]

    @staticmethod
    def create_projects_folder():
        if PathProvider.projects_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.projects_folder())
        except OSError as exception:
            LoggerInterface.error(f'Failed to create projects directory with exception: {exception}')
        return True
