import click

from chainchomp_cli.src.commands.chainlink_create import chainlink_create_command
from chainchomp_cli.src.commands.chainlink_edit import chainlink_edit_command
from chainchomp_cli.src.commands.chainchomp_adapter_list import chainlink_adapters_list_command
from chainchomp_cli.src.commands.chainchomp_adapter_register import chainchomp_adapter_register_command
from chainchomp_cli.src.commands.chainchomp_project_new import chainchomp_project_new_command
from chainchomp_cli.src.commands.chainlink_start import chainlink_start_command
from chainchomp_cli.src.commands.chainlink_stop import chainlink_stop_command
from chainchomp_cli.src.commands.setup import setup_command
from chainchomp_cli.src.commands.chainchomp_create_env_var import chainchomp_create_env_var_command


@click.group()
def chainchomp():
    pass


def add_sub_commands():
    chainchomp.add_command(setup_command.setup)
    chainchomp.add_command(chainlink_create_command.chainlink_create)
    chainchomp.add_command(chainlink_edit_command.chainlink_edit)
    chainchomp.add_command(chainlink_start_command.chainlink_start)
    chainchomp.add_command(chainlink_stop_command.chainlink_stop)
    chainchomp.add_command(chainchomp_project_new_command.chainchomp_project_new)
    chainchomp.add_command(chainlink_adapters_list_command.adapter_list)
    chainchomp.add_command(chainchomp_adapter_register_command.adapter_register)
    chainchomp.add_command(chainchomp_create_env_var_command.create_environment_variable)


def main():
    add_sub_commands()
    chainchomp()


if __name__ == '__main__':
    main()
