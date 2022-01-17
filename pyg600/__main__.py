import click

from .pyg600 import start

@click.command()
def main():
    start()

if __name__ == '__main__':
    main()
