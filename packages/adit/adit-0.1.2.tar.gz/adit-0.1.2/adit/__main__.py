import click
from adit import starter, installer
from adit import constants as const
from adit import shutdown_handler


@click.group()
def cli() -> None:
    pass


@cli.command("Setup working directory for Adit")
@click.argument('workdir', help='Setting up working directory for Adit with default config, '
                                'logging config and directories.', default=const.DEFAULT_WORK_DIR)
def install(workdir: str = const.DEFAULT_WORK_DIR) -> None:
    installer.install(workdir=workdir)


@cli.command(help="Start Adit server")
def server() -> None:
    starter.start(mode=const.SERVER_MODE, args=None)


@cli.command(help="Start Adit client")
@click.option('-s', '--server-ip', help='TEXT = IP address of server node.', required=True)
def client(server_ip: str = None) -> None:
    starter.start(mode=const.CLIENT_MODE, args=dict({'server_ip': server_ip}))


if __name__ == "__main__":
    shutdown_handler.init()
    cli()
