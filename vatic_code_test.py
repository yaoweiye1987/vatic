from sys import argv
from collections import deque

class Bookparser:
    def __init__(self, fname):
        self.fname = fname
    def __enter__(self):
        self.ifile = open(fname)
        self.end = False
        self.header = self.ifile.readline().strip().split(',')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ifile.close()
    def eof(self):
        return self.end
    def read_orders(self, n): # read n orders from the file
        orders = []
        for i in xrange(n):
            ol = self.ifile.readline().strip().split(',')
            if ol == ['']:
                self.end = True
                break
            order = [int(ol[0]), ol[1], ol[2]=='B', float(ol[3]), int(ol[4])]
            orders.append(order)
        return orders
    def print_all_lines(self):
        print self.header
        for line in self.ifile:
            print line

class OrderMatch:
    def __init__(self):
        self.opens = {}
        self.printbf = "OPEN_TIME,CLOSE_TIME,SYMBOL,QUANTITY,PNL,OPEN_SIDE,CLOSE_SIDE,OPEN_PRICE,CLOSE_PRICE"
    def log_record(self, order, orderop, size):
        key = order[1]
        openp = orderop[3]
        closep = order[3] 
        pnl = closep - openp
        if order[2]:
            pnl = -pnl
        pnl *= size
        side = 'B' if order[2] else 'S'
        sideop = 'B' if orderop[2] else 'S'
        records = [str(orderop[0]),str(order[0]),key,str(size),"{0:.2f}".format(pnl),\
                   sideop,side,"{0:.2f}".format(openp), "{0:.2f}".format(closep)]
        record = ",".join(records)
        self.printbf += "\n"+record
    def output(self):
        print self.printbf
        self.printbf = ""
    def process_orders(self, orders):
        for order in orders:
            key = order[1]
            if key not in self.opens: #first time key encountered
                self.opens[key] = deque()
                self.opens[key].append(order)
            else: # not first time key is encountered
                d = self.opens[key]
                if not d: # empty, no openning order
                    d.append(order)
                else:
                    orderop = d.popleft()
                    if (orderop[2] == order[2]): #same add the new order to end of queue
                        d.appendleft(orderop)
                        d.append(order)
                    else: # match order and create the residual order if any
                        size, sizeop = order[4], orderop[4]
                        while size > sizeop:
                            self.log_record(order, orderop, sizeop)
                            #finished check next order
                            size -= sizeop # must >0
                            order[4] = size
                            if d:
                                orderop = d.popleft()
                                sizeop = orderop[4]
                            else:# order book empty put the remaining unmarched order to top of order book
                                d.append(order)
                                orderop = None
                                sizeop = 0
                                break
                        if orderop is not None: # size <= sizeop the top of the order book will be matched
                            self.log_record(order, orderop, size)
                            if size < sizeop: # partial match
                                orderop[4] -= size
                                d.appendleft(orderop)


fname = argv[1]
with Bookparser(fname) as bp:
    om = OrderMatch()
    while not bp.eof():
        orders = bp.read_orders(3000000)
        om.process_orders(orders)
        om.output()
#book = pd.read_csv(fname, nrows = 3)
