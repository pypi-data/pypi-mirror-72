"""
Module by Mandera
Generalfile is made for windows path and file management.
It's relatively easily extended with any filetype by inheriting the File baseclass.

TODO: Try another approach for backup by using "x" mode and not copying
TODO: Remove backup
TODO: Fix thread test, getting PermissionError
TODO: Add a time limit to our infinite loops, import Timer from generallibrary
TODO: Docstring and tests for rename
TODO: Catch if trying to use "CON" in rename, write and copy
TODO: Allow paths to start with "../" to go to parent folder - Actually not Pythonic, we already have Path.getParent() to do that
done
TODO: classfiletsv
TODO: Change suffix, "suffix" is apparently already used for filetype
TODO: Multiple dots are actually allowed
TODO: pip install flynt to convert format() to f strings
TODO: Remove File.getAbsolute(Path) to only use Path.getAbsolute() - Not Pythonic to have two ways to do same thing
"""

from base.classfile import File, Path, PathList
import test

