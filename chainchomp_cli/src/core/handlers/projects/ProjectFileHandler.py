import os

import yaml
from chainchomplib.data import PathProvider


class ProjectFileHandler:

    @staticmethod
    def add_chainlink_to_project(self, chainlink_name: str, project_name: str):
        pass

    @staticmethod
    def create_new_project(project_name: str, chainlink_names=None) -> bool:
        if chainlink_names is None:
            chainlink_names = []

        projects_folder = PathProvider.projects_folder()

        if os.path.isfile(os.path.join(projects_folder, project_name)):
            return False

        project_dict = {'name': project_name, 'chainlinks': chainlink_names}

        with open(os.path.join(projects_folder, project_name), 'x') as new_project_file:
            try:
                yaml.safe_dump(project_dict, new_project_file, default_flow_style=False)
            except yaml.YAMLError as exception:
                return False
            else:
                return True
