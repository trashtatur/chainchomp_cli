import os

import yaml
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel


class ChainfileWriterHandler:

    @staticmethod
    def write_chainfile(chainlink_model: ChainfileModel, path: str, force):
        config_dict = {
            'project': chainlink_model.project_name,
            'chainlink': {
                'name': chainlink_model.chainlink_name,
                'next': chainlink_model.next_link if chainlink_model.next_link != '' else 'NONE',
                'previous': chainlink_model.previous_link if chainlink_model.previous_link != '' else 'NONE',
            },
            'start': chainlink_model.start,
            'stop': chainlink_model.stop,
            'profile': chainlink_model.profile
        }
        if not os.path.isdir(path):
            return False

        if not force and os.path.exists(os.path.join(path, 'chainfile.yml')):
            return

        with open(os.path.join(path, 'chainfile.yml'), 'w') as new_chainfile:
            try:
                return yaml.dump(config_dict, new_chainfile, default_flow_style=False)
            finally:
                new_chainfile.close()
                if os.path.isfile(os.path.join(path, 'chainfile.yml')):
                    return True
                return False
