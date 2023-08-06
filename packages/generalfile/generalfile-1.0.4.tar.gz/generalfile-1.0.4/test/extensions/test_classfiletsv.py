"""
Tests for class FileTSV
"""
import unittest
import pandas as pd

from generalfile.base.classfile import File
from test.base.setUpWorkDir import SetUpWorkDir

class FileTSVTest(unittest.TestCase):
    def setUp(self):
        """Set working dir and clear folder"""
        SetUpWorkDir.activate()

    def compareFrames(self, df1, df2):
        self.assertEqual(df1.shape, df2.shape)
        self.assertTrue(df1.columns.equals(df2.columns))
        self.assertTrue(df1.index.equals(df2.index))

    def writeAndReadDF(self, df):
        header, column = File.write("df.tsv", df, overwrite=True)
        read = File.read("df.tsv", header=header, column=column)
        return read

    def appendAndReadDF(self, obj):
        File.write("df.tsv", pd.DataFrame(), overwrite=True)
        File.tsvAppend("df.tsv", obj)
        read = File.read("df.tsv", header=False, column=False)
        return read

    def doTestsOnDataFrame(self, obj):
        df = pd.DataFrame(obj)
        self.compareFrames(df, self.writeAndReadDF(df))
        self.compareFrames(df.T, self.writeAndReadDF(df.T))

    def test_tsvWriteAndRead(self):
        self.doTestsOnDataFrame({"a": {"color": "red", "value": 5}, "b": {"color": "blue", "value": 2}})
        self.doTestsOnDataFrame([{"color": "red", "value": 5}, {"color": "blue", "value": 2}])
        self.doTestsOnDataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        self.doTestsOnDataFrame([[1, 2, 3], [4, 5, 6]])

    def test_tsvAppend(self):
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
        self.compareFrames(df, self.appendAndReadDF([[1, 2, 3], [4, 5, 6]]))
        self.compareFrames(df, self.appendAndReadDF([{"a": 1, "b": 2, "c": 3}, {"d": 4, "e": 5, "f": 6}]))
        self.compareFrames(df, self.appendAndReadDF({1: {"b": 2, "c": 3}, 4: {"e": 5, "f": 6}}))
        self.compareFrames(df, self.appendAndReadDF({1: [2, 3], 4: [5, 6]}))

        df = pd.DataFrame(["hello"])
        self.compareFrames(df, self.appendAndReadDF("hello"))




































