import os

import yaml
from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class ProjectFileHandler:

    @staticmethod
    def add_chainlink_to_project(chainlink_name: str, project_name: str):
        projects_folder = PathProvider.projects_folder()

        if not os.path.isfile(os.path.join(projects_folder, project_name)):
            LoggerInterface.warning(
                f'The project with the name {project_name} does not exist yet. You can\t add anything to it'
            )
            return False

        with open(os.path.join(projects_folder, project_name), 'w') as existing_project_file:
            try:
                existing_data = yaml.safe_load(existing_project_file)
            except yaml.YAMLError as exception:
                LoggerInterface.error(
                    f'Could not load the project file for project {project_name} with exception: {exception}'
                )
            else:
                existing_chainlink_data: list = existing_data.get('chainlinks', [])
                if len([elem for elem in existing_chainlink_data if elem == chainlink_name]) is not 0:
                    LoggerInterface.warning(
                        f'The chainlink with the name {chainlink_name} is already registered to project {project_name}.'
                        f' No further operation will be performed'
                    )
                    return False

                existing_chainlink_data.append(chainlink_name)
                yaml.safe_dump(
                    {'name': existing_data.get('name'), 'chainlinks': existing_chainlink_data},
                    existing_project_file,
                    default_flow_style=False
                )
                LoggerInterface.info(f'Added {chainlink_name} to project "{project_name}" successfully')
                return True
            finally:
                existing_project_file.close()

    @staticmethod
    def remove_chainlink_from_all_projects(chainlink_name: str):
        projects_folder = PathProvider.projects_folder()
        times_removed = 0
        for filename in os.listdir(projects_folder):

            with open(os.path.join(projects_folder, filename), 'w') as existing_project_file:
                try:
                    existing_data = yaml.safe_load(existing_project_file)
                except yaml.YAMLError as exception:
                    LoggerInterface.error(
                        f'Could not load the project file for project to remove a chainlink from it {filename}'
                        f' with exception: {exception}'
                    )
                else:
                    existing_chainlink_data: list = existing_data.get('chainlinks', [])
                    if len([elem for elem in existing_chainlink_data if elem == chainlink_name]) is 0:
                        break

                    if len([elem for elem in existing_chainlink_data if elem == chainlink_name]) is 2:
                        LoggerInterface.warning(
                            f'The chainlink {chainlink_name} seems to registered more than once '
                            f'To the project "{filename}". Chainchomp will only remove one occurrence.'
                            f'Please run this again until this error message does not show up'
                            f'Or solve the problem manually.'
                        )

                    existing_chainlink_data.remove(chainlink_name)
                    times_removed += 1
                    if times_removed > 1:
                        LoggerInterface.debug(
                            f'It seems the chainlink {chainlink_name} was registered to multiple projects'
                            f'It will be removed from all of them.'
                        )
                    yaml.safe_dump(
                        {'name': existing_data.get('name'), 'chainlinks': existing_chainlink_data},
                        existing_project_file,
                        default_flow_style=False
                    )
                    LoggerInterface.info(f'Removed {chainlink_name} from project "{filename}" successfully')
                    return True
                finally:
                    existing_project_file.close()

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
            finally:
                new_project_file.close()
