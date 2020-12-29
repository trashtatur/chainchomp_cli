import os
from typing import List

from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class ChainlinkFolderHandler:

    @staticmethod
    def provide_list_of_registered_chainlinks() -> List[str]:
        path_to_registered_chainlinks_folder = PathProvider.chainlinks_folder()
        if not path_to_registered_chainlinks_folder.is_dir():
            return []

        return [str(os.path.basename(filename))
                for filename in path_to_registered_chainlinks_folder.glob('**/*') if filename.is_file()]

    @staticmethod
    def create_chainlinks_folder():
        if PathProvider.chainlinks_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.chainlinks_folder())
        except OSError as exception:
            LoggerInterface.error(f'Failed to create registered chainlinks directory with exception: {exception}')
        return True
