"""
Extension for File to handle tsv files
"""
import csv
import pandas as pd
from generallibrary.types import typeChecker

class FileTSV:
    """
    Extension for File to handle tsv files
    """
    @classmethod
    def _write_tsv(cls, textIO, df):
        """

        :param generalfile.File cls: test
        :param textIO:
        :param pd.DataFrame df:
        :return:
        """
        typeChecker(df, pd.DataFrame)

        path = cls.toPath(textIO.name)
        df.to_csv(path, sep="\t", quoting=csv.QUOTE_NONNUMERIC)

        # writer = csv.DictWriter(textIO, fieldnames=tuple(df.keys()), delimiter="\t", lineterminator="\n")
        # writer.writerows(df)

    @classmethod
    def _read_tsv(cls, textIO):
        """

        :param generalfile.File cls: test
        :param textIO:
        :return:
        """
        path = cls.toPath(textIO.name)
        df = pd.read_csv(path, sep="\t", index_col=0, quoting=csv.QUOTE_NONNUMERIC)
        return df




