# Called once at the start of the simulation.
def initialize(context):
	#choose the benchmark you want to compare your trades too
    set_benchmark(sid())
    # Reference to the security.
    context.myStock = sid()

    #meant for scheduling a function to run.
    schedule_function(makeStartingTrade, date_rules.every_day(), time_rules.market_open())
    #sets the commission model in Quantopian
    set_commission(commission.PerShare(cost=0, min_trade_cost=0))
#    set_slippage(slippage.FixedSlippage(spread=0))


#gets the previous days Close
def getPrevClose(context, data):
    close = data.history(context.myStock, 'price', 1, '1d')
    log.info('close = {}', close[0])
    return close[0]

#gets the previous days High
def getPrevHigh(context, data):
    high = data.history(context.myStock, 'high', 1, '1d')
    log.info('High = {}', high[0])
    return high[0]

#gets the previous days Low
def getPrevLow(context, data):
    low = data.history(context.myStock, 'low', 1, '1d')
    log.info('Low = {}', low[0])
    return low[0]

#this method will get the available funds from a portfolio
def getAvailableFunds(context, data):
    cash = context.portfolio.cash
    return cash

#this method gets the number of shares we own
def getNumberOfShares(context, data):
    stock = context.myStock
    numShares = context.portfolio.positions[stock].amount    
    return numShares

#gets the number of shares from an open order
def getOpenOrderAmount(context, data):
    stock = context.myStock
    numShares = 0
    ordersList = get_open_orders(stock)
    for x in ordersList:
        numShares = numShares + x.amount

    return numShares
    
#this method makes the sell transactions
def makeSellTransaction(context, data):
    log.info('we are making a sell order')
    asset = context.myStock
    orderHighAmount = context.high
    numShares = getNumberOfShares(context, data)
    log.info('numShares in sell order = {}',numShares)
    order(asset, -numShares, style=LimitOrder(orderHighAmount))

def closeAnyOpenOrders(stock):  
    orders = get_open_orders(stock)  
    if orders:  
        for order in orders:  
             message = 'Canceling order for {amount} shares in {stock}'  
             message = message.format(amount=order.amount, stock=stock)  
             #log.debug(message)  
             cancel_order(order)

#this runs ever minute 
def handle_data(context, data):
	#insert your methods to make the orders here

# handles historical stuff once per day
def before_trading_start(context, data):
    context.low = getPrevLow(context, data)
    context.high = getPrevHigh(context, data)