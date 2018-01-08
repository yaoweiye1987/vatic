import string 
import random

def id_generator(size = 6, chars = string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

print(id_generator())

tickers = [] 
for i in range(1000):
  tickers.append(id_generator())

side = ['B', 'S'] 


f = open('testfile.csv', 'w')

for i in range(10000):
  price = random.uniform(0,50)
  f.write(str(i) +', '+ tickers[random.randint(0,999)]+ ', '+ side[random.randint(0,1)] +', '+ str(price) +', '+ str(random.randint(0,100))+ '\n')

