import numpy as np
from scipy import stats
from scipy.special import comb
import runTestArgs
import myPythonCheck

#
# Implement a "run test" using information on the sign and ordering of 
# the bin-by-bin residuals read from a file. 
# This test is complementary to and independent from the chi-squared test.  
# It uses the signs of the deviations and the ordering of such deviations; both
# are absent from the chi-squared statistic definition.
#
# The underlying original reference appears to be 
# A. Wald and J. Wolfowitz (1940), "On a test whether two samples are from the 
# same population", Ann. Math. Statist. 11, 147-162. 
# There seem be a number of related applications 
# (like heads/tails or runs of increasing/decreasing values). 
# Here I focused simply on whether the bin deviation was +ve or -ve.
# The books by Barlow, James, and Behnke have good introductory discussions.
#
# Note that this statistical test should only be used in principle for 
# simple hypotheses. Example: those with no parameters being fitted to the data.
# In practice it is likely a very useful/pragmatic additional tool even if this 
# theoretical condition is violated.
#
#              Graham W. Wilson,  24-NOV-2021
#

myPythonCheck.Check()                         # Enforce use of python3

filename, infolevel = runTestArgs.getArguments(None)
runTestArgs.showArgs(filename, infolevel)

# Read residuals data into numpy array
residuals = np.genfromtxt(filename,usecols=(0),unpack=True)
if infolevel > 0: 
    print(residuals)

# Count runs
npos=0
nrun=0
previous = -2
for i in range(0,residuals.size):
    residual = residuals[i]
    if residual > 0.0:
       npos += 1
       value = 1
    else:
       value = 0
    if value != previous:
       nrun += 1
       previous = value
    if infolevel > 1:
       print(i,residual,nrun)       
       
# Summarize observations
print('Nbins                     : ',residuals.size)
print('npos                      : ',npos)
print('number of runs, r         : ',nrun)

# Expectations etc
r = nrun
N = residuals.size
NA = npos
NB = N-NA
expectedr = 1 + (2*NA*NB/N)
variancer = 2*NA*NB*(2*NA*NB-N)/(N*N*(N-1))
sdr=np.sqrt(variancer)
print('E(r)                      : ',expectedr)
print('V(r)                      : ',variancer,', sd(r) :',sdr)

#
# Do exact confidence levels 
# using Wald-Wolfowitz run-test expressions using binomial coefficients.
#
# These expressions could have exceeded the range that is correctly represented 
# using eg. float64 numbers when N is large (eg. N=300). With scipy.special.comb 
# and exact=True, the arbitrary precision integers avoid this pitfall.
#
# Evaluate run test p-value. See Eadie, p263.
# comb(n,k) = Binomial(n,k) is the binomial coefficient, n!/(k! (n-k)!)
# Calculations were verified with Mathematica for test case of (N,NA,robs) = (100,49,56)
#
psum = 0.0
denom = comb(N,NA,exact=True)
for i in range(0,r+1):
    if i%2 == 0:          #even
       s = int(i/2)
       p = float(2*comb(NA-1,s-1,True)*comb(NB-1,s-1,True)/denom)
       if infolevel>2:
          print('Even: i,s,p = ',i,s,p)
       psum += p
    else:                 #odd
       s = int((i+1)/2)
       p = float((comb(NA-1,s-2,True)*comb(NB-1,s-1,True) + comb(NA-1,s-1,True)*comb(NB-1,s-2,True))/denom)
       if infolevel>2:
          print('Odd : i,s,p = ',i,s,p)
       psum += p
print('Run test p-value for robs <= ',r,' is ',100.0*psum,'(%)')
print(' ')
