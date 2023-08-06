import random

#Calculate (a^n)%p in 0(logy)
def power(a,n,p):
  res = 1
  a = a % p

  while(n > 0):
    if(n & 1):
      res = (res*a) % p
    n = n>>1
    a = (a*a) % p 
  return res

#Calculate gcd of 2 numbers
def gcd(a,b):
  if(a < b):
    return gcd(b,a)

  elif (a%b ==  0):
    return b

  else:
    return gcd(b,a%b)

#Returns true is n is prime. Returns false if n is
#composite with high probability. Higher K value 
#increases probability of correct result
def fermat(n,k):
  #corner cases
  if(n <= 1 or n == 4):
    return False
  if(n <= 3):
    return True

  while(k>0):
    #pick a random number between 2 and n - 2
    a = random.randint(2,n-2) 

    #check if a and n are co-prime
    if(gcd(n,a) != 1):
      return False
    
    #Fermat's little theorem
    if(power(a,n-1,n) != 1):
     return False

    k = k - 1

  return True
