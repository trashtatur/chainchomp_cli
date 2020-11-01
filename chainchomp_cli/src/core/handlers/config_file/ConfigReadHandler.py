import os

import yaml
from chainchomplib.configlayer.model.ChainlinkConfigModel import ChainlinkConfigModel
from chainchomplib.configlayer.verify.SchemaVerifier import SchemaVerifier
from chainchomplib.configlayer.verify.schema.ChainfileSchema import ChainfileSchema


class ConfigReadHandler:

    @staticmethod
    def read_config_file(path: str) -> ChainlinkConfigModel or None:

        if not os.path.exists(path):
            return None

        if os.path.isfile(path) and os.path.basename(path) != 'chainfile.yml':
            return None

        if os.path.isdir(path) and not os.path.isfile(f'{os.path.join(path,"chainfile.yml")}'):
            return None

        file_path = os.path.join(path)
        if not os.path.isfile(path):
            file_path = os.path.join(path, 'chainfile.yml')

        with open(file_path, 'r') as chainfile:
            try:
                chainfile_data = yaml.safe_load(chainfile)
            except yaml.YAMLError as exception:
                print(exception)

        if chainfile_data:
            try:
                SchemaVerifier.verify(chainfile_data, ChainfileSchema().init_schema())
            except Exception as exception:
                print(exception)
            else:
                return ChainlinkConfigModel(
                    chainfile_data.get('project'),
                    chainfile_data.get('chainlink').get('name'),
                    chainfile_data.get('chainlink').get('next', ''),
                    chainfile_data.get('chainlink').get('previous', ''),
                    chainfile_data.get('start', 'echo "No start script provided"'),
                    chainfile_data.get('stop', 'echo "No stop script provided"'),
                    chainfile_data.get('masterLink', False),
                    chainfile_data.get('adapter', 'rabbitmq'),
                    chainfile_data.get('profile', 'default')
                )
