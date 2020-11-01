import os
import shutil
import unittest

import yaml
from chainchomplib.data import PathProvider
from parameterized import parameterized

from chainchomp_cli.src.core.handlers.projects.ProjectFileHandler import ProjectFileHandler


class ProjectFileHandlerTest(unittest.TestCase):

    def setUp(self) -> None:
        os.mkdir(PathProvider.projects_folder())

    def tearDown(self) -> None:
        try:
            shutil.rmtree(PathProvider.projects_folder())
        except OSError:
            pass

    @parameterized.expand([
        ('test project', ['test'], {'name': 'test project', 'chainlinks': ['test']}, True),
        ('test project2', ['test1', 'test2'], {'name': 'test project2', 'chainlinks': ['test1', 'test2']}, True)
    ])
    def test_that_project_gets_created_correctly(self, project_name, chainlink_names, content, expected):
        result = ProjectFileHandler.create_new_project(project_name, chainlink_names)

        assert result is expected
        assert os.path.isfile(os.path.join(PathProvider.projects_folder(), project_name)) is expected

        with open(os.path.join(PathProvider.projects_folder(), project_name)) as project_file:
            loaded_dict = yaml.safe_load(project_file)
            assert loaded_dict == content

    def test_that_project_wont_be_overwritten(self):
        file = open(os.path.join(PathProvider.projects_folder(), 'test'), 'x')
        file.close()

        result = ProjectFileHandler.create_new_project('test', [])
        assert result is False

if __name__ == '__main__':
    unittest.main()
