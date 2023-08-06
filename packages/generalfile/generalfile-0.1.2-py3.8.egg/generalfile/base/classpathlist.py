"""
Base component of generalfile
"""

class PathList(list):
    """
    List that contains path with convenient methods.
    Takes None, paths or lists of paths as parameter for initializing.
    """
    def __init__(self, *args):
        paths = []
        for arg in args:
            if isinstance(arg, str):
                paths.append(arg)
            elif isinstance(arg, list) or isinstance(arg, tuple):
                for subArg in arg:
                    if not isinstance(subArg, str):
                        raise TypeError("Iterable doesn't contain a string")
                    paths.append(subArg)
            else:
                raise TypeError("Given arg is neither a string nor list or tuple")

        super().__init__(paths)

    def toPath(self):
        """
        Makes sure all paths inside are using class Path.
        Call this method when a Path's attribute or method is required.

        :return: Itself but all items are Paths class.
        """
        for path in self:
            if not isinstance(path, Path):
                break
        else:
            return self
        pathList = PathList([Path.toPath(path) for path in self])
        self.clear()
        for path in pathList:
            self.append(path)
        return self

    def getFolders(self):
        """
        :return: A new PathList only containing the folder paths.
        """
        return PathList([path for path in self.toPath() if path.isFolder])

    def getFiles(self):
        """
        :return: A new PathList only containing the file paths.
        """
        return PathList([path for path in self.toPath() if path.isFile])

    def getRelative(self, basePath=None):
        """
        :param basePath: Optional base path. Defaults to current work dir.
        :return: A new PathList with all paths converted to relative.
        """
        return PathList([File.getRelativePath(path, basePath) for path in self])

    def getAbsolute(self, basePath=None):
        """
        :param basePath: Optional base path. Defaults to current work dir.
        :return: A new PathList with all paths converted to absolute.
        """
        return PathList([File.getAbsolutePath(path, basePath) for path in self])

    def exists(self):
        """
        See which paths exists. Use all() or any() on result.
        :return: A tuple with Booleans
        :rtype: tuple[bool]
        """
        return tuple(File.exists(path) for path in self)





from generalfile import File, Path
