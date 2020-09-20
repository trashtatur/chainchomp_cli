import os

from chainchomplib.data import PathProvider


class AdapterFolderHandler:

    @staticmethod
    def provide_list_of_installed_adapters():
        path_to_adapters_folder = PathProvider.installed_adapters_folder()
        if not path_to_adapters_folder.is_dir():
            return []

        return [str(os.path.basename(filename))
                for filename in path_to_adapters_folder.glob('**/*') if filename.is_file()]

    @staticmethod
    def create_adapter_folder():
        if PathProvider.installed_adapters_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.installed_adapters_folder())
        except OSError:
            # TODO Proper exception
            print('Failed to create installed adapters dir')

        return True
