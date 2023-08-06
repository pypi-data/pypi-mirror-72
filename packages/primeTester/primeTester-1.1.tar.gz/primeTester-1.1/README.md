# primeTester
primeTester is a collection of Python modules consisting different [primality tests](https://en.wikipedia.org/wiki/Primality_test).

Link to package on PyPI: [primeTester](https://pypi.org/project/primeTester/).

## Tests Included 
- Fermat Test
- Miller Rabin Test
- Solovay Strassen
- AKS Test
- Trial Division

## Install
``
pip3 install PrimeTester
``

## Usage
Import the test function from the python modules installed. Camel case is used for the functions names. 

``
from millerRabin import millerRabin 
``

For probability based tests (Fermat, Miller Rabin, Solovay Strassen) those functions take in two arguments.
The first argument takes in a number to be tested as prime, the second is the number of test iterations. 

``
print(fermat(5,100))
``

All the test functions will return a true or false value. A returned true value indicates that the inputted number is a prime. A returned false value indicates that the inputted number is not a prime. 

