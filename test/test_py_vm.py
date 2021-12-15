from unittest import TestCase

from pysh.py_vm.types import Primatives, UserType, UserValue


class TestUserValues(TestCase):

  def setUp(self):
    self.s = UserType(Primatives.String)
    self.i = UserType(Primatives.Int)
    self.f = UserType(Primatives.Float)
    self.b = UserType(Primatives.Bool)
    self.ls = UserType(Primatives.Array, Primatives.String)
    self.li = UserType(Primatives.Array, Primatives.Int)
    self.lf = UserType(Primatives.Array, Primatives.Float)
    self.lb = UserType(Primatives.Array, Primatives.Bool)
    self.di = UserType(Primatives.Dict, Primatives.Int)
    self.df = UserType(Primatives.Dict, Primatives.Float)
    self.ds = UserType(Primatives.Dict, Primatives.String)
    self.db = UserType(Primatives.Dict, Primatives.Bool)

  def testPrimativesEquality(self):
    self.assertTrue(Primatives.String == Primatives.String)
    self.assertFalse(Primatives.String == Primatives.Int)
    self.assertEqual(Primatives.String, Primatives.String)
    self.assertNotEqual(Primatives.String, Primatives.Float)
    self.assertEqual(Primatives.String, Primatives.String)
    self.assertNotEqual(Primatives.String, Primatives.Bool)
    self.assertNotEqual(Primatives.Array, Primatives.Dict)
    self.assertEqual(Primatives.Array, Primatives.Array)

  def testCanInstantiateAllPrimativeTypes(self):
    self.assertTrue(self.s.convertable(self.i))
    self.assertTrue(self.s.convertable(self.f))
    self.assertTrue(self.s.convertable(self.b))
    self.assertTrue(self.s.convertable(self.s))
    self.assertTrue(self.ls.convertable(self.li))
    self.assertTrue(self.ls.convertable(self.ls))
    self.assertTrue(self.ls.convertable(self.lf))
    self.assertTrue(self.ls.convertable(self.lb))
    self.assertFalse(self.ls.convertable(self.f))
    self.assertFalse(self.ls.convertable(self.ds))

  def testCanConvertBetweenUserValues(self):
    string5 = UserValue("5", UserType(Primatives.String))
    int5 = string5.convert_type(UserType(Primatives.Int))
    intArray = UserValue([1, 2, 3], UserType(Primatives.Array, Primatives.Int))
    self.assertEqual(int5.value, int(string5.value))
    self.assertRaises(ValueError, lambda: intArray.convert_type(UserType(Primatives.Dict, Primatives.Int)))
    stringArray = intArray.convert_type(UserType(Primatives.Array, Primatives.String))
    self.assertEqual(stringArray.value, ["1", "2", "3"])
    self.assertEqual(intArray.value, [1, 2, 3])
    intDict = UserValue({"Key1": 1, "Key2": 2, "Key3": 4}, UserType(Primatives.Dict, Primatives.Int))
    strDict = intDict.convert_type(UserType(Primatives.Dict, Primatives.String))
    self.assertEqual({"Key1": 1, "Key2": 2, "Key3": 4}, intDict.value)
    self.assertEqual({"Key1": "1", "Key2": "2", "Key3": "4"}, strDict.value)

