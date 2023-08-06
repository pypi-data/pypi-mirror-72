"""
Extension for File to handle tsv files
"""
import csv
import pandas as pd
from generallibrary.types import typeChecker
from generallibrary.iterables import getRows

class FileTSV:
    """
    Extension for File to handle tsv files
    """

    @staticmethod
    def _indexIsNamed(index):
        """
        Simple version to see if a DataFrame index is named or not
        :param index: DataFrame's index (columns or index)
        """
        if str(index[0]) == "0" or str(index[0]) == "1":
            return False
        else:
            return True

    @classmethod
    def _write_tsv(cls, textIO, df):
        """
        Can write a bunch of different DataFrames to a TSV file.
        Doesn't support advanced pandas functionality.
        Should work with: Keys, Index and Transposed (8 combinations)
        If DataFrame has both keys and index then cell A1 becomes NaN

        TODO: Make it order columns if there are any so that they line up with append.

        :param generalfile.base.classfile.File cls: File inherits FileTSV
        :param textIO: Tsv file
        :param pd.DataFrame df: Generic df
        """

        typeChecker(df, pd.DataFrame)
        path = cls.toPath(textIO.name)

        if df.empty:
            with open(path, "w"):
                pass
            return False, False

        useHeader = cls._indexIsNamed(df.columns)
        useIndex = cls._indexIsNamed(df.index)

        df.to_csv(path, sep="\t", header=useHeader, index=useIndex)

        return useHeader, useIndex

    @classmethod
    def _read_tsv_helper(cls, path, header, column):
        return pd.read_csv(path, sep="\t", header=header, index_col=column).convert_dtypes()

    @classmethod
    def _read_tsv(cls, textIO, header=False, column=False):
        """
        If any cell becomes NaN then the header and column parameters are overriden silently.

        Can read a bunch of different DataFrames to a TSV file.
        Doesn't support advanced pandas functionality.
        Should work with: Keys, Index, Transposed, Header, Column (32 combinations).
        DataFrame in file can have a NaN A1 cell.

        :param generalfile.base.classfile.File cls:
        :param textIO:
        :param bool header: Use headers or not, overriden if any top left cell is NaN
        :param bool column: Use columns or not, overriden if any top left cell is NaN
        :rtype: pd.DataFrame
        """

        path = cls.toPath(textIO.name)

        header = "infer" if header else None
        column = 0 if column else None

        try:
            df = cls._read_tsv_helper(path, header, column)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()

        # Get rid of empty cell (Happens if file was written with header=True, column=True)
        headerFalseColumnFalse = pd.isna(df.iat[0, 0])
        headerFalseColumnTrue = pd.isna(df.index[0])
        headerTrueColumnFalse = str(df.columns[0]).startswith("Unnamed: ")
        if headerFalseColumnFalse or headerFalseColumnTrue or headerTrueColumnFalse:
            header = "infer"
            column = 0
            df = cls._read_tsv_helper(path, header, column)
        else:
            # Get rid of name in index (Happens if file doesn't have an index and column=True)
            # Doesn't happen other way around for some reason, guess it's the internal order in pandas
            if df.index.name is not None:
                if header is None and column == 0:
                    df.index.rename(None, inplace=True)
                else:
                    header = None
                    column = None
                    df = cls._read_tsv_helper(path, header, column)

        if not cls._indexIsNamed(df.columns):
            df.columns = pd.RangeIndex(len(df.columns))
        if not cls._indexIsNamed(df.index):
            df.index = pd.RangeIndex(len(df.index))

        return df.convert_dtypes()

    @staticmethod
    def _tsvAppend_getRow(iterableObj, key=None):
        """
        Takes an object and returns a list of rows to use for appending.

        :param iterableObj: Iterable
        :param key: If iterableObj had a key to assigned it it's given here
        :return: A
        """
        row = [key] if key else []
        if isinstance(iterableObj, (list, tuple)):
            row.extend(iterableObj)
        elif isinstance(iterableObj, dict):
            for _, value in sorted(iterableObj.items()):
                row.append(value)
        return row

    @classmethod
    def tsvAppend(cls, path, obj):
        """
        Append an obj to the end of a TSV file.
        If a dict is given and there are iterables as values then the keys of the dict are the first value in each row.
        Otherwise keys in dicts are ignored.

        Identical append objects
         | [[1, 2, 3], [4, 5, 6]]
         | [{"a": 1, "b": 2, "c": 3}, {"d": 4, "e": 5, "f": 6}]
         | {1: {"b": 2, "c": 3}, 4: {"e": 5, "f": 6}}
         | {1: [2, 3], 4: [5, 6]}

        :param generalfile.base.classfile.File cls:
        :param path:
        :param obj: Iterable (Optionally inside another iterable) or a value for a single cell
        :raises AttributeError: If obj is empty
        """
        path = cls.toPath(path, requireFiletype="tsv", requireExists=True)
        if not obj and obj != 0:
            raise AttributeError("obj is empty")

        with open(path, 'a') as tsvfile:
            writer = csv.writer(tsvfile, delimiter = "\t", lineterminator = "\n")
            for row in getRows(obj):
                writer.writerow(row)













































