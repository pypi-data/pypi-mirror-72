"""
Extension for File to handle xxx files
"""
class FileXXX:
    """
    Extension for File to handle xxx files
    """
    @classmethod
    def _write_xxx(cls, textIO, obj):
        """
        Method that does the writing for this filetype.
        Add documentation to File.write()

        :param generalfile.base.classfile.File cls:
        :param textIO:
        :param obj:
        :return:
        """
        path = cls.toPath(textIO.name)
        textIO.write(str(obj))
        return obj

    @classmethod
    def _read_xxx(cls, textIO):
        """
        Method that does the reading for this filetype.
        Add documentation to File.read()

        :param generalfile.base.classfile.File cls:
        :param textIO:
        :return:
        """
        return textIO.read()

# Replace xxx with filetype, has to match


