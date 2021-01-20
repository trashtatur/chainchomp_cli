import os

import yaml
from chainchomplib import LoggerInterface
from chainchomplib.configlayer.model.AdapterFileModel import AdapterFileModel
from chainchomplib.data import PathProvider


class AdapterRegistrationHandler:

    @staticmethod
    def register_adapter(adapter_model: AdapterFileModel) -> bool:
        if os.path.isfile(os.path.join(PathProvider.installed_adapters_folder(), f'{adapter_model.name}.yml')):
            LoggerInterface.error(
                f'An adapter with the name {adapter_model.name} is already registered. Aborting!'
            )
            return False

        with open(os.path.join(
                PathProvider.installed_adapters_folder(),
                f'{adapter_model.name}.yml'
        ), 'x') as new_adapter:
            try:
                yaml.safe_dump(adapter_model.get_serialized(), new_adapter)
            except yaml.YAMLError as exception:
                LoggerInterface.error(
                    f'Data for adapter {adapter_model.name} could not be written. Exception: {exception}'
                )
            else:
                return True
            finally:
                new_adapter.close()

