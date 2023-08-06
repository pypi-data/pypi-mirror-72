
import click
from . import *

@click.group()
def cli():
    pass

@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--interactive', is_flag=True)
def rebalance(verbose, interactive):
    ''' Rebalances your portfolio '''
    rebalance_portfolio(verbose, interactive)

@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--interactive', is_flag=True)
def cancel_all(verbose, interactive):
    ''' Cancels all orders '''
    cancel_all_orders(verbose, interactive)

cli.add_command(rebalance)
cli.add_command(cancel_all)
