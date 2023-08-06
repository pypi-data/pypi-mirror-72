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

    def test__write_tsv(self):
        df = pd.DataFrame({
            "a": {"color": "red", "value": 5},
            "b": {"color": "blue", "value": 2}
        })
        File.write("df.tsv", df)
        read = File.read("df.tsv")
        # self.assertTrue(df.equals(read))

        # HERE **
        # pd.testing.assert_frame_equal(df, read)

    def test__read_tsv(self):
        pass

