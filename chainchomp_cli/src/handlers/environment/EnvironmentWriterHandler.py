import os

from chainchomplib.data import PathProvider


class EnvironmentWriterHandler:
    @staticmethod
    def create_environment_variable(name: str, value: str) -> bool:
        if os.path.isfile(os.path.join(PathProvider.environment_variables_folder(), name)):
            return False

        with open(os.path.join(PathProvider.environment_variables_folder(), name)) as new_environment_variable:
            new_environment_variable.write(value)
            new_environment_variable.close()
            return True
