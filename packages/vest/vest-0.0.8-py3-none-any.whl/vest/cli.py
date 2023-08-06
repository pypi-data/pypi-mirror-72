
import click
from . import *

@click.group()
def cli():
    pass

@click.command()
def rebalance():
    ''' Rebalances your portfolio '''
    rebalance_portfolio()

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
