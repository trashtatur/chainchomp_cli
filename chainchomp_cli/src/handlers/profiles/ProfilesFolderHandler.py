import os
from typing import List

from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class ProfilesFolderHandler:

    @staticmethod
    def provide_list_of_profiles() -> List[str]:
        path_to_profiles_folder = PathProvider.profiles_folder()
        if not path_to_profiles_folder.is_dir():
            return []

        return [str(filename) for filename in path_to_profiles_folder if filename.is_file()]

    @staticmethod
    def create_profiles_folder():
        if PathProvider.profiles_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.profiles_folder())
        except OSError as exception:
            LoggerInterface.error(f'Failed to create profiles directory with exception: {exception}')
        return True
