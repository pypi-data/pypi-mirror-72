"""
Base component of generalfile.
Path is unaware and ignorant of environment.
"""

class Path(str):
    """
    Immutable.
    Path inherits string and makes manipulating paths easy.
    All path parameters used in File are converted to Paths.
    Three stages of scrubbing:
        1. Checking for illegal characters in Path:__new__
        2. Slashes fixed in Path:__new__
        3. Path:identifier returns a comparable path (lowering all characters for starters)
    """
    suffixDelimeter = "_"

    def __new__(cls, text=None):
        """
        Doesn't remove caps but methods should ignore it.

        Invalid words in windows, probably too expensive to check for them?
        ("CON", "PRN", "AUX", "NUL", "COM0", "LPT0", "COM1", "LPT1", "COM2", "LPT2", "COM3", "LPT3", "COM4"
        , "LPT4", "COM5", "LPT5", "COM6", "LPT6", "COM7", "LPT7", "COM8", "LPT8", "COM9", "LPT9")

        :param str text: Takes a string or Path resembling a filepath or folderpath
        :raises WindowsError: If invlaid character found
        """

        if text is None:
            text = ""

        # Simple invalid characters testing
        for character in tuple(text):
            if character in "<>\"|?*":
                raise WindowsError("Invalid character {} in {}".format(character, text))

        text = text.replace("\\", "/")
        if text.endswith("/"):
            text = text[0:-1]
        if text.startswith("/"):
            text = text[1:]

        return super().__new__(cls, text)

    def __init__(self, _=None):
        super().__init__()

        self.isAbsolute = ":" in self
        self.isRelative = not self.isAbsolute
        self.partsList = self.split("/")

        # Catch some simple mistakes

        if self.count(".") > 1:
            raise WindowsError("More than one dot in {}".format(self))
        for i, part in enumerate(self.partsList):
            if ":" in part:
                if i or (part.index(":") != 1 or part.count(":") > 1):
                    raise WindowsError(": in part #{} ({})".format(i, part), self)
            if i != len(self.partsList) - 1:
                if "." in part:
                    raise WindowsError(". in part that's not last #{} ({})".format(i, part), self)

        self.filenamePure = None
        self.filenameFull = None
        self.suffix = None
        self.filetype = None

        if "." in self.partsList[-1]:
            self._pathWithoutType = self.split(".")[0]

            splitDot = self.partsList[-1].split(".")

            self.filenameFull = self.partsList[-1]
            self.filetype = splitDot[1]
            self.foldersList = self.partsList[0:len(self.partsList) - 1]

            splitSuffix = splitDot[0].split(self.suffixDelimeter)
            self.filenamePure = splitSuffix[0]

            if self.suffixDelimeter in self.filenameFull:
                self.suffix = splitSuffix[1]

        else:
            self.foldersList = self.partsList

        self.isFile = self.filenamePure is not None
        self.isFolder = not self.isFile


    @staticmethod
    def identifier(pathPart):
        """
        :param str pathPart: A full path, partial part or even only a filetype.
        :return: A string that can be compared with other paths' identifiers to see if they point to the same file or folder.
        """
        return pathPart.lower()

    @staticmethod
    def toPath(path, requireFiletype = None):
        """
        Makes sure we're using Path class.
        Has built-in parameters to scrub.

        :param str path: Generic Path
        :param requireFiletype: True, False or filetype ("txt" or "tsv")
        :return: Same Path or a new Path if a string was given
        :raises ValueError: If neither a str or path is given
        :raises AttributeError: if requireFiletype is True and it's not a file and vice versa
        :raises TypeError: if requireFiletype is a specified filetype and doesn't match filetype
        """
        if isinstance(path, Path):  # Because Path[0:5] for example is still a Path, so instantiate again to scrub
            path = Path(path)
        elif isinstance(path, str):
            path = Path(path)
        else:
            raise ValueError("path has neither instance Path nor str, it's {}".format(type(path)))
        
        if requireFiletype is not None:
            if requireFiletype is True:
                if not path.isFile:
                    raise AttributeError("Not a file", path)
            elif requireFiletype is False:
                if path.isFile:
                    raise AttributeError("Is a file", path)
            elif Path.identifier(requireFiletype) != Path.identifier(path.filetype):
                raise TypeError("Mismatch filetype", requireFiletype, path.filetype)
        
        return path

    def addPath(self, path):
        """
        Simply add a path to this one.

        :param str path: Path to be added at the end.
        :return: New conjoined path.
        :raises FileExistsError: If first path is a file.
        :raises AttributeError: If second path is absolute.
        """
        path = self.toPath(path)

        if self.filetype:
            raise FileExistsError("Cannot add {} to {} because first is a file".format(path, self))
        if path.isAbsolute:
            raise AttributeError("Cannot add {} to {} because second is absolute".format(path, self))

        foldersList = self.foldersList.copy()
        foldersList.extend(path.foldersList)
        return path.setFoldersList(foldersList)

    def getPathWithoutFile(self):
        """
        Get a new Path without file.
        :return:
        """
        if not self.isFile:
            return self
        return self.removeFromEnd(self.filenameFull)

    def setPartsList(self, partsList):
        """
        Get a new Path with replaced parts.

        :param list[str] partsList: List containing path parts.
        :return: New path with new parts.
        """
        return Path("/".join(partsList))

    def setFoldersList(self, foldersList):
        """
        Get a new Path with replaced folder list.

        :param list[str] foldersList: List containing folder names.
        :return: New path with new folders.
        """
        if foldersList == self.foldersList:
            return self
        if not foldersList:
            foldersList = False
        return self._getPath(foldersList=foldersList)

    def setFilenamePure(self, filenamePure):
        """
        Get a new Path with replaced pure filename.

        :param str filenamePure: Filename without anything else.
        :return: New path with new pure filename.
        """
        if filenamePure == self.filenamePure:
            return self
        return self._getPath(filenamePure=filenamePure)

    def setSuffix(self, suffix):
        """
        Get a new Path with replaced suffix.

        :param any suffix: Suffix or None
        :return: New Path with or without suffix.
        """
        if suffix == self.suffix:
            return self
        if not suffix:
            suffix = False
        return self._getPath(suffix=suffix)

    def setFiletype(self, filetype):
        """
        Get a new Path with replaed filetype.

        :param filetype:
        :return:
        """
        if filetype == self.filetype:
            return self
        return self._getPath(filetype=filetype)

    def _getPath(self, foldersList = None, filenamePure = None, suffix = None, filetype = None):
        """
        Returns a new Path with optionally changed attributes, if none are changed then it returns self.

        :rtype: Path
        """
        if foldersList is None:
            foldersList = self.foldersList.copy()
        if filenamePure is None:
            filenamePure = self.filenamePure
        if suffix is None:
            suffix = self.suffix
        if filetype is None:
            filetype = self.filetype

        if foldersList == self.foldersList and filenamePure == self.filenamePure and suffix == self.suffix and filetype == self.filetype:
            return self

        if foldersList is False:
            foldersList = []

        if not filenamePure:
            if suffix:
                raise AttributeError("Cannot have suffix without filenamePure")
            if filetype:
                raise AttributeError("Cannot have filetype without filenamePure")
        else:
            if not filetype:
                raise AttributeError("Cannot have filenamePure without filetype")

        if filenamePure:
            suffixParts = [filenamePure]
            if suffix:
                suffixParts.append(suffix)
            filenamePureWithSuffix = self.suffixDelimeter.join(suffixParts)
            foldersList.append("{}.{}".format(filenamePureWithSuffix, filetype))
            return Path("/".join(foldersList))

        else:
            return Path("/".join(foldersList))

    def startsWithPath(self, path):
        """
        See if this Path starts with given path.
        Every part (Folder or File) is tested individually, so it's not tested like a typical string.

        :param str path: Generic path to check with.
        :returns: Whether it starts with that path or not.
        """
        path = Path.toPath(path)
        if len(path.partsList) > len(self.partsList):
            return False

        for i, pathPart in enumerate(path.partsList):
            selfPart = self.partsList[i]
            if Path.identifier(pathPart) != Path.identifier(selfPart):
                return False
        return True

    def endsWithPath(self, path):
        """
        See if this Path ends with given path.
        Every part (Folder or File) is tested individually, so it's not tested like a typical string.

        :param str path: Generic path to check with.
        :returns: Whether it ends with that path or not.
        """
        path = Path.toPath(path)
        if len(path.partsList) > len(self.partsList):
            return False

        for i, pathPart in enumerate(reversed(path.partsList)):
            selfPart = self.partsList[-i - 1]
            if Path.identifier(pathPart) != Path.identifier(selfPart):
                return False
        return True

    def removeFromStart(self, path):
        """
        Get a new Path with atleast one part removed from it's start.

        :param str path: Path that should be removed.
        :returns: New path with removed parts from start.
        """
        path = Path.toPath(path)
        if not self.startsWithPath(path):
            return self
        newPartsList = self.partsList[len(path.partsList):]
        return path.setPartsList(newPartsList)

    def removeFromEnd(self, path):
        """
        Get a new Path with atleast one part removed from it's end.

        :param str path: Path that should be removed.
        :returns: New path with removed parts from end.
        """
        path = Path.toPath(path)
        if not self.endsWithPath(path):
            return self
        newPartsList = self.partsList[:-len(path.partsList)]
        return path.setPartsList(newPartsList)

    def getAbsolute(self, basePath=None):
        """
        SHORTCUT for File.getAbsolutePath(path, basePath).

        Gets absolute path based on basePath unless path already is absolute.
        If basePath is None then current working dir will be used.

        :param str basePath: Optional base Path to a folder. Is converted to absolute using current work dir if it's relative.
        :return: Absolute Path
        """
        return File.getAbsolutePath(self, basePath=basePath)

    def getRelative(self, basePath=None):
        """
        SHORTCUT for File.getAbsolutePath(path, basePath).

        Gets relative path based on basePath.
        If basePath is None then current working dir will be used.

        :param str basePath: Optional base Path to a folder. Is converted to absolute using current work dir if it's relative.
        :return: Relative Path
        :raises AttributeError: If basePath isn't a part of given Path
        """
        return File.getRelativePath(self, basePath=basePath)

    def getParent(self, generations=1, basePath=None):
        """
        Get a Path to any parent folder of a Path.

        If a relative Path is given then a relative Path is returned if possible.
        Relative Paths are converted to Absolute if going past base folder.
        Filepaths' first parent is the folder it's in.

        :param int generations: Which parent to get, default is 1.
        :param str basePath: Used if given Path must be converted to Absolute.
        :return: Path to parent or None if no parent found
        """
        absolutePath = self.getAbsolute(basePath)
        for i in range(generations):
            if len(absolutePath.partsList) == 1:
                return None
            absolutePath = absolutePath.removeFromEnd(absolutePath.partsList[-1])

        if self.isAbsolute:
            return absolutePath
        try:
            return absolutePath.getRelative(basePath)
        except AttributeError:
            return absolutePath



from generalfile.base.classfile import File
