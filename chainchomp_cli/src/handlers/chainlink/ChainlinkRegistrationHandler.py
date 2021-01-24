import os

import yaml
from chainchomplib import LoggerInterface
from chainchomplib.configlayer.resolver.ChainfileResolver import ChainfileResolver
from chainchomplib.data import PathProvider


class ChainlinkRegistrationHandler:

    @staticmethod
    def register_chainlink(path: str) -> bool:
        if not os.path.isfile(os.path.join(path, 'chainfile.yml')):
            LoggerInterface.error('Can not find a chainfile at the given path. Aborting!')
            return False

        chainlink_model = ChainfileResolver.resolve(
            os.path.join(path, 'chainfile.yml')
        )

        if chainlink_model is None:
            LoggerInterface.error(f'Chainfile at path {path} is not valid. Aborting!')
            return False

        data_dict = {
            'name': chainlink_model.chainlink_name,
            'path': path
        }

        if os.path.isfile(os.path.join(PathProvider.chainlinks_folder(), f'{chainlink_model.chainlink_name}.yml')):
            LoggerInterface.error(
                f'A chainlink with the name {chainlink_model.chainlink_name} is already registered. Aborting!'
            )
            return False

        with open(os.path.join(
                PathProvider.chainlinks_folder(),
                f'{chainlink_model.chainlink_name}.yml',
        ), 'x') as new_chainlink:
            try:
                yaml.safe_dump(data_dict, new_chainlink)
            except yaml.YAMLError as exception:
                LoggerInterface.error(
                    f'Data for chainlink {chainlink_model.chainlink_name} could not be written. Exception: {exception}'
                )
            else:
                return True
            finally:
                new_chainlink.close()
