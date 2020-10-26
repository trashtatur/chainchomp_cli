import click

from chainchomp_cli.src.core.commands.chainlink_create import chainlink_create_command
from chainchomp_cli.src.core.commands.chainlink_edit import chainlink_edit_command
from chainchomp_cli.src.core.commands.adapter_list import chainlink_mq_command
from chainchomp_cli.src.core.commands.chainlink_ping import chainlink_ping_command
from chainchomp_cli.src.core.commands.chainlink_profile import chainlink_profile_command
from chainchomp_cli.src.core.commands.chainchomp_project import chainchomp_project_new_command
from chainchomp_cli.src.core.commands.chainlink_start import chainlink_start_command
from chainchomp_cli.src.core.commands.chainlink_stop import chainlink_stop_command
from chainchomp_cli.src.core.commands.setup import setup_command


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
    chainchomp.add_command(chainlink_mq_command.adapter_list)
    chainchomp.add_command(chainlink_ping_command.chainlink_ping)
    chainchomp.add_command(chainlink_profile_command.chainchomp_profile)


def main():
    add_sub_commands()
    chainchomp()


if __name__ == '__main__':
    main()
