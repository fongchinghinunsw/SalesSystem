"""Entry CLI module for Sales System"""

import click
from app.core import create_app

app = create_app('app.settings')


@click.group()
def main():
  pass


@main.command()
def createdb():
  app.system.InitializeDb()


@main.command()
def run():
  app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
  main()
