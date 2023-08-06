"""
Extension for File to handle xxx files
"""
from base.classfile import File

class FileXXX(File):
    """
    Extension for File to handle xxx files
    """
    @staticmethod
    def _write_xxx(textIO, obj):
        path = File.toPath(textIO.name)
        textIO.write(str(obj))
        return obj

    @staticmethod
    def _read_xxx(textIO):
        return textIO.read()

# Replace xxx with filetype, has to match


