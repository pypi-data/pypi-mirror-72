from margot.backtest import BackTest


class Strategy(object):
 
    def __init__ (self, algo, recent_vol, target_vol):   # noqa: D107
        self.__dict__.update(locals())  # TODO: lazy / loose


class Portfolio(object):

    def __init__ (self, account_size, target_vol):  # noqa: D107
        self.account_size = account_size
        self.target_vol = target_vol
        self.strategies = list()

    def add_strategy(self, algo, target_vol):
        """Add a strategy to the portfolio.

        Args:
            algo (Algo): A Margot Trading Algorithm
            target_vol (float): the vol were aiming for
        """
        bt = BackTest(algo)

        #TODO: periods assumes we're looking at days.
        bt.run(periods=30)  

        self.strategies.append(
            Strategy(algo, bt.volatility(), target_vol)
            )
        