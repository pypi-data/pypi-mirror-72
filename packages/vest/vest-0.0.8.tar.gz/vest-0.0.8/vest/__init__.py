
import click
import json
import os
import pprint as pp
from tabulate import tabulate
import robin_stocks as rs

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from . import data


class AssetClass():
    def __init__(self, name, setting, holdings):
        self.name = name
        self.ticker = setting['Ticker']
        self.equity = 0 if self.ticker not in holdings \
                else float(holdings[self.ticker]['equity'])
        self.allocation = 0
        self.target_allocation = float(setting['Target allocation'])
        self.target_equity = 0
        self.underfunded = True

class Portfolio():
    def __init__(self, asset_classes, cash_allocation):
        self.holdings = []
        holdings = rs.build_holdings()
        for name, setting in asset_classes.items():
            self.holdings.append(AssetClass(name, setting, holdings))
        self.total_equity = sum([ac.equity for ac in self.holdings])
        self.total_alloc = sum([ac.target_allocation for ac in self.holdings])
        self.normalize_allocations()
        self.cash = max(0,
                float(rs.load_account_profile()['buying_power']) 
                - 0.01 - cash_allocation)
        self.find_target_equities(self.total_equity + self.cash, 1)
        self.orders = self.generate_orders()
    def normalize_allocations(self):
        for ac in self.holdings:
            ac.target_allocation /= self.total_alloc
    def find_target_equities(self, available_cash, available_allocation):
        for ac in self.holdings:
            if ac.underfunded:
                ac.target_equity = available_cash * ac.target_allocation \
                        / available_allocation
        collar = min([ac.target_equity - ac.equity for ac in self.holdings
            if ac.underfunded]) * 0.07
        for ac in self.holdings:
            if ac.underfunded:
                ac.target_equity -= collar * ac.target_allocation \
                        / available_allocation 
        complete = True
        for ac in self.holdings:
            if ac.equity > ac.target_equity:
                ac.target_equity = ac.equity
                ac.underfunded = False
                available_cash -= ac.equity
                available_allocation -= ac.target_allocation
                complete = False
        if not complete:
            self.find_target_equities(available_cash, available_allocation)
    def generate_orders(self):
        orders = [{'Ticker': ac.ticker, 'Amount': ac.target_equity - ac.equity}
            for ac in self.holdings if ac.target_equity - ac.equity >= 1]
        assert(sum([order['Amount'] for order in orders]) 
                <= self.total_equity + self.cash)
        return sorted(orders, key=lambda x: x['Amount'], reverse=True)
    def show(self):
        for ac in self.holdings:
            ac.allocation = round(100 * ac.equity / self.total_equity, 2)
        print(tabulate({
            'Category': [ac.name for ac in self.holdings], 
            'Ticker': [ac.ticker for ac in self.holdings], 
            'Equity': [ac.equity for ac in self.holdings],
            'Target allocation': [round(100 * ac.target_allocation) 
                for ac in self.holdings],
            'Current allocation': [ac.allocation for ac in self.holdings]},
            headers='keys'))
        print(f'Cash: {round(self.cash, 2)}')

def get_config():
    with pkg_resources.open_text(data, 'config.json') as f:
        return json.load(f)

def log_in():
    username = os.environ.get('RH_USERNAME')
    password = os.environ.get('RH_PASS')
    rs.login(username, password)

def rebalance_portfolio():
    ''' Rebalances your portfolio '''
    config = get_config()
    log_in()
    portfolio = Portfolio(config['Asset classes'], 
            float(config['Cash allocation']))
    open_orders = rs.get_all_open_stock_orders()
    if len(open_orders) > 0:
        click.echo(f'There are already {len(open_orders)} open orders.')
        if click.confirm('Show existing orders?'):
            pp.pprint(open_orders)
    if len(open_orders) == 0 or click.confirm(f'Continue?'):
        pp.pprint(portfolio.orders)
        for i, order in enumerate(portfolio.orders):
            if click.confirm('Execute order for ' 
                    f'{order["Ticker"]}? ({i+1}/{len(portfolio.orders)})'):
                result = rs.order_buy_fractional_by_price(
                    order['Ticker'], order['Amount'], timeInForce='gfd')
                pp.pprint(result)

def cancel_all_orders():
    ''' Cancels all orders '''
    config = get_config()
    log_in()
    if not click.confirm('Cancel all orders?'):
        return
    result = rs.cancel_all_stock_orders()
    pp.pprint(result)

def show_allocation():
    log_in()
    config = get_config()
    portfolio = Portfolio(config['Asset classes'],
            float(config['Cash allocation']))
    portfolio.show()
