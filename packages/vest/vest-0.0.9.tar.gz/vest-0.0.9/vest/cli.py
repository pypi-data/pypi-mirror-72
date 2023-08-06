
import click
from . import *

@click.group()
def cli():
    pass

@click.command()
@click.option('--execute_all', is_flag=True)
def rebalance(execute_all):
    ''' Rebalances your portfolio '''
    rebalance_portfolio(execute_all)

@click.command()
def cancel_all():
    ''' Cancels all orders '''
    cancel_all_orders()

@click.command()
def show():
    ''' Shows current portfolio '''
    show_allocation()

cli.add_command(rebalance)
cli.add_command(cancel_all)
cli.add_command(show)
