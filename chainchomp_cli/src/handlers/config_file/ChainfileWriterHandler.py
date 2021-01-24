import os

import yaml
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel


class ChainfileWriterHandler:

    @staticmethod
    def write_chainfile(chainlink_model: ChainfileModel, path: str, force):
        if not os.path.isdir(path):
            return False

        if not force and os.path.exists(os.path.join(path, 'chainfile.yml')):
            return

        with open(os.path.join(path, 'chainfile.yml'), 'w') as new_chainfile:
            try:
                return yaml.safe_dump(chainlink_model.get_serialized(), new_chainfile, default_flow_style=False)
            finally:
                new_chainfile.close()
                if os.path.isfile(os.path.join(path, 'chainfile.yml')):
                    return True
                return False
