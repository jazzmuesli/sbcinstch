# based on http://journals.bmj.com/site/microlives/main.js
class MicrolifeCalculator:

  def __init__(self):
    self.is_male = False

  def gender(self,x):
    if x == "male":
      self.is_male=True
      return -4
    return 0

  def smoking(self,x):
     return (-10 if self.is_male else -9) if x > 15 else 0

  def alcohol(self,x):
    if x < 2:
      return x
    # TODO: really? you can drink 1130 units and it's the same damage as 5 units?
    return 1.0 - min(x-1,5) * (0.5 if self.is_male else 1)

import unittest

calc = MicrolifeCalculator()
class MicrolifeCalculatorTest(unittest.TestCase):
  def test_gender(self): 
    self.assertEquals(calc.gender('male'), -4)

  def test_smoking(self):
    self.assertEquals(calc.smoking(17), -10)

  def test_alcohol(self):
    self.assertEquals(calc.alcohol(1130), -4)

unittest.main()
