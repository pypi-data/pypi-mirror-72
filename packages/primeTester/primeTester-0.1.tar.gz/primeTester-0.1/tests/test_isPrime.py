import sys
import unittest
sys.path.append('/home/avrha/Desktop/Prime-Tests/src')
from trialDivision import trialDivision
from fermat import fermat
from millerRabin import millerRabin
from solovayStrassen import solovayStrassen
from aks import aks

class Test(unittest.TestCase):
  def test_trialDivision(self):
    result = trialDivision(5)
    self.assertTrue(result)

    result = trialDivision(7)
    self.assertTrue(result)

    result = trialDivision(10)
    self.assertFalse(result)

  def test_fermat(self):
    result = fermat(5, 100)
    self.assertTrue(result) 

    result = fermat(14, 100)
    self.assertFalse(result) 

    result = fermat(17, 100)
    self.assertTrue(result) 

  def test_millerRabin(self):
    result = millerRabin(5, 100)
    self.assertTrue(result)

    result = millerRabin(14, 100)
    self.assertFalse(result) 

    result = millerRabin(17, 100)
    self.assertTrue(result)

  def test_solovayStrassen(self):
    result = solovayStrassen(5, 100)
    self.assertTrue(result)

    result = solovayStrassen(14, 100)
    self.assertFalse(result) 

    result = solovayStrassen(17, 100)
    self.assertTrue(result)
 
  def test_aks(self):
    result = aks(5)
    self.assertTrue(result)

    result = aks(7)
    self.assertTrue(result)

    result = aks(10)
    self.assertFalse(result)
    
if __name__ == "__main__":
  unittest.main()
