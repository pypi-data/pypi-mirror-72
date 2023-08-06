from decimal import *
from math import sqrt
def squ(a):
  return a*a
def nilakantha(digs,precs,outputiters):
  getcontext().prec = precs
  f = Decimal(3)
  a,b,c=2,3,4
  m = False
  for i in range(digs):
    if(m == False):
      f += Decimal(4/(a*b*c))
    elif(m == True):
      f -= Decimal(4/(a*b*c))
    a,b,c=a+2,b+2,c+2
    if(m==True):
      m=False
    elif(m==False):
      m=True
    if(i%1000 and outputiters):
      print("Iteration " + str(i) + ": " + str(Decimal((squ(a+b))/(4*t))))
  return f
def gregoryleibniz(digs,precs,outputiters):
  getcontext().prec = precs
  n = 1
  f = Decimal(0)
  m = True
  for i in range(digs):
    if(m==True):
      m=False
    elif(m==False):
      m=True
    if(m == False):
      f += Decimal(4/n)
    elif(m == True):
      f -= Decimal(4/n)
    n+=2
    if(i%10 and outputiters):
      print("Iteration " + str(i) + ": " + str(Decimal((squ(a+b))/(4*t))))
  return f
def gausslegendre(digs,precs,outputiters=True):
  getcontext().prec = precs
  a = Decimal(1)
  b = Decimal(1/Decimal(2).sqrt())
  t = Decimal(1/4)
  x = Decimal(1)
  f = 0
  for i in range(digs):
    y = Decimal(a)
    a = Decimal((a+b)/2)
    b = Decimal(sqrt(b*y))
    t = Decimal(t - x * squ((y-a)))
    x = Decimal(2* x)
    if(i%10 == 0 and outputiters):
      print("Iteration " + str(i) + ": " + str(Decimal((squ(a+b))/(4*t))))
  f = Decimal((squ(a+b))/(4*t))
  return f
def archimedes(digs,precs,outputiters=True):
  getcontext().prec = precs
  x=Decimal(4)
  y=2*sqrt(2)
  for i in range(digs):
    xn=Decimal((Decimal(2)*Decimal(x)*Decimal(y))/(Decimal(x)+Decimal(y)))
    y=sqrt(Decimal(xn)*Decimal(y))
    x = xn
    if(i%10 == 0 and outputiters):
      print("Iteration " + str(i) + ": " + str(Decimal((Decimal(x)+Decimal(y))/Decimal(2))))
  f=Decimal((Decimal(x)+Decimal(y))/Decimal(2))
  return f
def dotests(iters,digs):
    print("Archimedes: " + str(archimedes(iters, digs, outputiters=False)))
    print("Gauss-Legendre: " + str(gausslegendre(iters, digs, outputiters=False)))
    print("Gregory-Leibniz: " + str(gregoryleibniz(iters, digs, outputiters=False)))
    print("Nilakantha: " + str(nilakantha(iters, digs, outputiters=False)))
    print("Actual Pi: " + str(3.141592653))
