from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed, tusharefeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.technical import cross


class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
        self.__entrySMA = ma.SMA(self.__priceDS, entrySMA)
        self.__exitSMA = ma.SMA(self.__priceDS, exitSMA)
        self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
        self.__overBoughtThreshold = overBoughtThreshold
        self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None

    def getPrice(self):
        return self.__priceDS

    def getEntrySMA(self):
        return self.__entrySMA

    def getExitSMA(self):
        return self.__exitSMA

    def getRSI(self):
        return self.__rsi

    def onEnterCanceled(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitOk(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__exitSMA[-1] is None or self.__entrySMA[-1] is None or self.__rsi[-1] is None:
            return

        bar = bars[self.__instrument]
        if self.__longPos is not None:
            if self.exitLongSignal():
                self.__longPos.exitMarket()
                print 'exitMarket long'
        elif self.__shortPos is not None:
            if self.exitShortSignal():
                self.__shortPos.exitMarket()
                print 'exitMarket short'
        else:
            if self.enterLongSignal(bar):
#                 print 'stragety'+str(bars[self.__instrument].getPrice())
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                print 'enterLong shares'+str(shares)+'self.getBroker().getCash():'+str(self.getBroker().getCash())
                self.__longPos = self.enterLong(self.__instrument, shares, True)
                
            elif self.enterShortSignal(bar):
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                print 'enterShort shares'+str(shares)+'self.getBroker().getCash():'+str(self.getBroker().getCash())
                self.__shortPos = self.enterShort(self.__instrument, shares, True)

    def enterLongSignal(self, bar):
        return bar.getPrice() > self.__entrySMA[-1] and self.__rsi[-1] <= self.__overSoldThreshold

    def exitLongSignal(self):
        return cross.cross_above(self.__priceDS, self.__exitSMA) and not self.__longPos.exitActive()

    def enterShortSignal(self, bar):
        return bar.getPrice() < self.__entrySMA[-1] and self.__rsi[-1] >= self.__overBoughtThreshold
 
    def exitShortSignal(self):
        return cross.cross_below(self.__priceDS, self.__exitSMA) and not self.__shortPos.exitActive()





# Load the yahoo feed from the CSV file
# feed = yahoofeed.Feed()toting
# feed.addBarsFromCSV("orcl", "orcl-2000.csv")

feed = tusharefeed.Feed()
feed.addBarsFromCSV("orcl", "002151.csv")

# Evaluate the strategy with the feed's bars.
#(self, feed, instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
myStrategy = MyStrategyRSI(feed, "orcl", 150, 6, 3, 95, 13)

# Attach a returns analyzers to the strategy. 
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.

# plt.getInstrumentSubplot("orcl").addDataSeries("price", myStrategy.getPrice())
plt.getInstrumentSubplot("orcl").addDataSeries("entrySMA", myStrategy.getEntrySMA())
plt.getInstrumentSubplot("orcl").addDataSeries("exitSMA", myStrategy.getExitSMA())
# plt.getInstrumentSubplot("orcl").addDataSeries("RSI", myStrategy.getRSI())

# Plot the simple returns on each bar.
# plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

# Run the strategy. 
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

# Plot the strategy.
plt.plot() 
