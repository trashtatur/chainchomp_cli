import os

import yaml
from chainchomplib.configlayer.model.ChainlinkConfigModel import ChainlinkConfigModel
from chainchomplib.configlayer.verify.SchemaVerifier import SchemaVerifier
from chainchomplib.configlayer.verify.schema.ChainfileSchema import ChainfileSchema


class ConfigReadHandler:

    @staticmethod
    def read_config_file(path: str) -> ChainlinkConfigModel or None:

        if os.path.isfile(path) and os.path.basename(path) is not 'chainfile':
            return None

        if not os.path.isdir(path) and not os.path.isfile(f'{os.path.join(path,"chainfile.yml")}'):
            return None

        with open(os.path.join(path, 'chainfile.yml'), 'r') as chainfile:
            try:
                chainfile_data = yaml.safe_load(chainfile)
            except yaml.YAMLError as exception:
                print(exception)

        if chainfile_data:
            try:
                SchemaVerifier.verify(chainfile_data, ChainfileSchema)
            except Exception as exception:
                print(exception)
            else:
                return ChainlinkConfigModel(
                    chainfile_data['project'],
                    chainfile_data['chainlink']['name'],
                    chainfile_data['chainlink']['next'] or '',
                    chainfile_data['chainlink']['previous'] or '',
                    chainfile_data['start'] or 'echo "No start script provided"',
                    chainfile_data['stop'] or 'echo "No stop script provided"',
                    chainfile_data['masterLink'] or False,
                    chainfile_data['adapter'] or 'rabbitmq',
                    chainfile_data['profile'] or 'default'
                )
