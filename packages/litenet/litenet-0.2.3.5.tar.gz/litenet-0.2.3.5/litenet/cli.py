import click
from litenet.server import LiteNetServer
from litenet.client import LiteNetClient


@click.group()
def cli():
    pass


@click.command(help="Launch a LiteNet Server")
@click.option("-h", "--host", required=True, type=str, help="The ip to run the server on. (Must have access to it.)")
@click.option("-p", "--port", default=5050, type=int, help="The port to run the server on. (Must be a valid port.)")
@click.option("--header", "header", default=64, type=int, help="The size of the server message header.")
@click.option("-d", "--debug", is_flag=True, help="Enters debug mode.")
def server(host, port, header, debug):
    litenet = LiteNetServer(host, port, header, debug=debug)
    litenet.start()


@click.command(help="Launch the LiteNet Client")
@click.option("-h", "--host", required=True, type=str, help="The ip the server's running on. (Must have access to it.)")
@click.option("-p", "--port", default=5050, type=int, help="The port the server's running on. (Must be a valid port.)")
@click.option("--header", "header", default=64, type=int, help="The size of the server message header. (Must match the server's.)")
@click.option("-d", "--debug", is_flag=True, help="Enters debug mode.")
def client(host, port, header, debug):
    client = LiteNetClient(host, port, header, debug=debug)
    client.start()


cli.add_command(server)
cli.add_command(client)

if __name__ == '__main__':
    cli()
