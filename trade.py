class Trade(object):
  def __init__(self, name):
    self.buy = []
    self.sell = []
    self.name = name 
  def buyitem(self,item):
    while self.sell:
      if self.sell[0].quantity > item.quantity:
        self.sell[0].quantity -= item.quantity
        print (self.sell[0].time, item.time,self.name, item.quantity, item.quantity * (self.sell[0].price - item.price),'S', 'B', self.sell[0].price, item.price) 
        break
      else:
        item.quantity -= self.sell[0].quantity 
        print (self.sell[0].time, item.time, self.name, self.sell[0].quantity, self.sell[0].quantity * (self.sell[0].price - item.price),'S', 'B', self.sell[0].price, item.price)
        self.sell.pop(0)
        if item.quantity == 0: break
    if item.quantity != 0: self.buy.append(item)
    
  def sellitem(self,item):
#    print (self.buy)
    while self.buy:
      if self.buy[0].quantity > item.quantity:
         self.buy[0].quantity -= item.quantity
         print (self.buy[0].time, item.time,self.name,item.quantity, item.quantity * (item.price - self.buy[0].price), 'B', 'S', self.buy[0].price, item.price)
         break
      else:
        item.quantity -= self.buy[0].quantity
        print (self.buy[0].time, item.time,self.name, self.buy[0].quantity, self.buy[0].quantity * (item.price - self.buy[0].price), 'B', 'S', self.buy[0].price, item.price)
        self.buy.pop(0)
        if item.quantity == 0: break
    if item.quantity != 0: self.sell.append(item)


class Item(object):
  def __init__(self, l):
    self.time = int(l[0]) 
    self.name = l[1] 
    self.side = l[2] 
    self.price = float(l[3])
    self.quantity = int(l[4])


if __name__ == '__main__':
  market = {}
  f = open('test.csv', 'r')
  x = f.readline()
  while True: 
    l = f.readline().split(', ')
#    print(l)
    item = Item(l)
    if item.name not in market:
      trade =  Trade(item.name)
      market[item.name] = trade
    else:
      trade = market[item.name] 
#    print(trade)
    if item.side == 'B':
      trade.buyitem(item)
    elif item.side == 'S':
      trade.sellitem(item)
    else:
      print ('wrong input')
      break



