from typing import List


class ProjectFileHandler:

    def add_chainlink_to_project(self, chainlink_name: str, project_name: str):
        pass

    def create_new_project(self, project_name: str, chainlink_names=None):
        if chainlink_names is None:
            chainlink_names = []