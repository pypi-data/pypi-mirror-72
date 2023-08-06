"""
Base component of generalfile
"""
from send2trash import send2trash
import os
import shutil
import json
import pathlib

from generallibrary.time import Timer, sleep
from generalfile.extensions.classfiletsv import FileTSV

class File(FileTSV):
    """
    File class exists so that FileTSV for example can inherit it.
    Method parameter 'path' takes a Path or a Str, Str is converted to Path.
    """
    timeoutSeconds = 5
    deadLockSeconds = 3
    def __init__(self):
        raise UserWarning("No need to instantiate File, all methods are static or classmethods")

    @staticmethod
    def toPath(path, requireFiletype=None, requireExists=None):
        """
        Makes sure we're using Path class.
        Has built-in parameters to scrub.
        Uses Path.toPath() but it also has extra functionality to check whether path exists.

        :param str path: Resemble a filepath or folderpath
        :param requireFiletype: True, False or filetype ("txt" or "tsv")
        :param bool requireExists: Require file or folder to exist or not
        :return: Same Path or a new Path if a string was given
        :raises AttributeError: if requireFiletype is True and it's not a file and vice versa
        :raises TypeError: if requireFiletype is a specified filetype and doesn't match filetype
        :raises FileNotFoundError: if requireExists is True and file doesn't exist
        :raises FileExistsError: if requireExists is False and file exists
        """
        path = Path.toPath(path, requireFiletype)

        if requireExists is not None:
            exists = File.exists(path)
            if exists and not requireExists:
                raise FileExistsError("Path exists", path)
            if requireExists and not exists:
                raise FileNotFoundError("Path doesn't exist", path)
        return path

    @staticmethod
    def exists(path):
        """
        Works for both file and folder.

        :param str path: Resemble a filepath or folderpath
        :return: Whether file or folder exists or not
        :rtype: bool
        """
        path = Path.toPath(path)
        path = File.getAbsolutePath(path)
        return os.path.exists(path)

    @staticmethod
    def getWorkingDir():
        """
        :returns: Current working directory as absolute Path
        """
        return Path(os.getcwd())

    @staticmethod
    def setWorkingDir(path):
        """
        Sets new working directory, if a relative path is given then current working directory will be taken into account.

        :param str path: Path to folder
        :return: Absolute Path to new working directory
        """
        path = File.toPath(path, requireFiletype=False)
        path = File.getAbsolutePath(path)
        File.createFolder(path)
        os.chdir(path)
        return path

    @staticmethod
    def getAbsolutePath(path, basePath=None):
        """
        Gets absolute path based on absolute basePath unless path already is absolute.

        :param str path: Generic Path to be converted.
        :param str basePath: Optional base Path to a folder. Is converted to absolute using current work dir if it's relative.
        :return: Absolute Path
        """
        path = File.toPath(path)
        if path.isAbsolute:
            return path

        if basePath is None:
            basePath = File.getWorkingDir()
        else:
            basePath = File.toPath(basePath, requireFiletype=False)
            basePath = File.getAbsolutePath(basePath)
        return basePath.addPath(path)

    @staticmethod
    def getRelativePath(path, basePath=None):
        """
        Gets relative path based on basePath.
        If basePath is None then current working dir will be used.

        :param str path: Generic Path to be converted
        :param str basePath: Optional base Path to a folder. Is converted to absolute using current work dir if it's relative.
        :return: Relative Path
        :raises AttributeError: If basePath isn't a part of given Path
        """
        path = File.toPath(path)
        path = File.getAbsolutePath(path)

        if basePath is None:
            basePath = File.getWorkingDir()
        else:
            basePath = File.toPath(basePath, requireFiletype=False)
            basePath = File.getAbsolutePath(basePath)
        if (relativePath := path.removeFromStart(basePath)).isAbsolute:
            raise AttributeError("Working directory ('{}') is not part of path ('{}') so we cannot get the relative path".format(File.getWorkingDir(), path))
        return relativePath

    @staticmethod
    def sameDestination(path1, path2):
        """
        Detects if two paths point to same folder or file based on current working directory by converting to absolute paths.
        Compares identifiers instead of strings directly, to ignore case.

        :param str path1: Generic Path
        :param str path2: Generic Path
        :return: Whether paths point to same destination or not.
        """
        path1 = File.toPath(path1)
        path2 = File.toPath(path2)

        path1 = File.getAbsolutePath(path1)
        path2 = File.getAbsolutePath(path2)

        return Path.identifier(path1) == Path.identifier(path2)

    @staticmethod
    def _read_txt(textIO):
        """
        Reads txt file from IO stream as JSON.
        This method is included in default File because they're needed for backup.

        :param io.TextIO textIO: From "with open(Path) as textIO"
        :return: serializable object or None
        """
        try:
            read = textIO.read()
        except:
            return None
        else:
            if read == "":
                return None
            return json.loads(read)

    @staticmethod
    def _write_txt(textIO, serializable):
        """
        Writes to txt file IO stream with JSON.
        This method is part of default File because they're needed for backup.

        :param io.TextIO textIO: From "with open(Path) as textIO"
        :param serializable: Any serializable object that json can use
        :return: json string (json.dumps)
        """
        jsonDumps = json.dumps(serializable)
        try:
            textIO.write(jsonDumps)
        except:
            return None
        else:
            if jsonDumps == "" or serializable is None:
                return None
            return jsonDumps

    @classmethod
    def read(cls, path, default=None):
        """
        Dynamic function that can read any document if methods exist for that filetype

        Generic read method:
            Only used dynamically by this method.

            Suffix has to match a filetype.

            Method has to take path as parameter and return a useful object for that filetype.

        :param str path: Path or Str
        :param default: What is returned as backup if reading fails or file doesn't exist
        :return: Useful object for that filetype (Dynamic)
        :raises EnvironmentError: if read method is missing for that filetype
        """
        path = File.toPath(path, requireFiletype=True)
        exists = File.exists(path)
        if (readMethod := getattr(cls, "_read_{}".format(path.filetype), None)) is None:
            raise EnvironmentError("Missing read method for filetype {}".format(path.filetype))
        if not exists:
            return default

        with open(path, "r") as textIO:
            read = readMethod(textIO)
        return default if read is None else read

    @classmethod
    def write(cls, path, writeObj=None, overwrite=False):
        """
        Dynamic function that can write to any document if methods exist for that filetype.

        Can only lock and backup if file exists.

        Generic write method:
            Only used dynamically by this method.
            Suffix has to match a filetype.
            Method has to take path and useful object as parameter, return object is optional

        :param bool overwrite: Set to False if overwriting shouldn't be allowed
        :param str path: Path or Str
        :param writeObj: A useful object that the dynamic write method can use
        :return: Whatever the write method returns
        :raises EnvironmentError: if write method is missing for that filetype
        :raises FileExistsError: if overwriting when overwrite is set to False
        """
        path = File.toPath(path, requireFiletype=True)
        exists = File.exists(path)
        if (writeMethod := getattr(cls, "_write_{}".format(path.filetype), None)) is None:
            raise EnvironmentError("Missing write method for filetype {}".format(path.filetype))
        if exists and not overwrite:
            raise FileExistsError("Tried to overwrite {} when overwrite was False".format(path))

        if not exists:
            File.createFolder(path)

        pathNew = path.setSuffix("NEW")
        pathLock = path.setSuffix("LOCK")
        timer = Timer()

        while True:
            try:
                with open(pathLock, "x") as lockIO:
                    with open(pathNew, "w") as textIO:
                        writeReturn = writeMethod(textIO, writeObj)
                    File.delete(path)
                    File.rename(pathNew, path.filenamePure)
                    lockIO.close()
                    File.delete(pathLock)
            except FileExistsError as e:
                # PermissionError would have triggered if we couldn't delete lock
                File.delete(pathLock)
            except PermissionError as e:
                pass
            else:
                break
            if timer.seconds() > File.timeoutSeconds:
                raise TimeoutError(f"Couldn't open {pathLock} for writing")
        return writeReturn

    @staticmethod
    def rename(path, name):
        """
        Rename a file or folder. Cannot change filetype.

        :param str path: Generic path to folder or file that exists.
        :param name: New name of folder or file.
        :return: None
        :raises EnvironmentError: If new path exists
        :raises NameError: If used invalid name
        """
        path = File.toPath(path, requireExists=True)
        if path.isFile:
            newPath = path.setFilenamePure(name).setSuffix(None)
        else:
            newPath = path.getParent().addPath(name)
        if File.exists(newPath):
            raise EnvironmentError(f"New path {newPath} exists already")
        try:
            os.rename(path, newPath)
        except FileExistsError:
            raise NameError(f"{newPath} probably contains an invalid name such as CON, PRN, NUL or AUX")

    @staticmethod
    def copy(path, destPath, overwrite=False):
        """
        Copy and paste a file to file, file to folder or folder to folder.
        Creates new folders if needed.
        When copying folder it excludes the parent folder, simply add the folder name to the end of target Path if that's desired.

        :param str path: Path or Str
        :param str destPath: Path to folder or file
        :param bool overwrite: Allow overwriting or not
        :return: None
        :raises RecursionError: If paths are identical
        :raises FileExistsError: If trying to overwrite when not allowed
        :raises AttributeError: If filetypes don't match
        :raises NotADirectoryError: If trying to copy folder to file
        :raises NameError: If used invalid name
        """
        path = File.toPath(path, requireExists=True)
        path = File.getAbsolutePath(path)
        destPath = File.toPath(destPath)
        destPath = File.getAbsolutePath(destPath)

        if File.sameDestination(path, destPath):
            raise RecursionError("Identical paths")

        if path.isFile:
            if destPath.isFile:
                if path.filetype != destPath.filetype:
                    raise AttributeError("Filetypes don't match")
            elif destPath.isFolder:
                destPath = destPath.addPath(path.filenameFull)
            if File.exists(destPath):
                if not overwrite:
                    raise FileExistsError("Not allowed to overwrite")

            File.createFolder(destPath)
            try:
                shutil.copy(path, destPath, follow_symlinks=False)
            except FileNotFoundError:
                raise NameError(f"{destPath} probably contains an invalid name such as CON, PRN, NUL or AUX")

        elif path.isFolder and destPath.isFolder:
            if not overwrite:
                filePathList = File.getPaths(path).getFiles()
                relativePaths = filePathList.getRelative(path)
                absoluteDestPaths = relativePaths.getAbsolute(destPath)
                if any(absoluteDestPaths.exists()):
                    raise FileExistsError("Atleast one file exists and not allowed to overwrite")

            try:
                shutil.copytree(path, destPath, dirs_exist_ok=True)
            except NotADirectoryError:
                raise NameError(f"{destPath} probably contains an invalid name such as CON, PRN, NUL or AUX")
        else:
            raise NotADirectoryError("Cannot copy folder to file")

    @staticmethod
    def createFolder(path):
        """
        Create folder(s) for path.
        If a filepath is given then the filename is ignored.

        :param str path: Path or Str
        :return: Whether any folders were created or not
        :raises NameError: If used invalid name
        """
        path = File.toPath(path)
        path = File.getAbsolutePath(path)
        path = path.getPathWithoutFile()

        if File.exists(path):
            return False

        try:
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        except NotADirectoryError:
            raise NameError(f"{path} probably contains an invalid name such as CON, PRN, NUL or AUX")

        return True

    @staticmethod
    def clearFolder(path, delete=False):
        """
        Make a target folder empty of everything.

        :param str path: Path or Str
        :param bool delete: Whether to delete files or put them in trash
        :return: Whether folder existed or not
        """
        path = File.toPath(path)
        path = File.getAbsolutePath(path)
        path = path.getPathWithoutFile()

        if not File.exists(path):
            return False
        if delete:
            File.delete(path)
        else:
            File.trash(path)
        File.createFolder(path)
        return True

    @staticmethod
    def trash(path):
        """
        Puts a file or folder in trashcan.

        :param str path: Path inside working directory
        :return: Whether path exists or not
        """
        path = File.toPath(path)
        path = File.getRelativePath(path)
        workingDir = File.getWorkingDir()

        if not File.exists(path):
            return False
        send2trash(path)
        # Reset working dir because send2trash can change it if it removed part of it
        if File.getWorkingDir() != workingDir:
            File.setWorkingDir(workingDir)
        return True

    @staticmethod
    def delete(path):
        """
        Deletes a file or folder, skipping trashcan

        :param str path: Path or Str
        :return: Whether path exists or not
        """
        path = File.toPath(path)
        if not File.exists(path):
            return False

        timer = Timer()
        if path.isFile:
            while True:
                try:
                    os.remove(path)
                except FileNotFoundError:
                    return False
                # Try again since it might just be being used by another process
                except PermissionError:
                    pass
                else:
                    break
                if timer.seconds() > File.timeoutSeconds:
                    raise TimeoutError(f"Couldn't delete {path}")
        elif path.isFolder:
            shutil.rmtree(path, ignore_errors=True)
        # If path is working dir then shutil.rmtree() only clears folder.
        if not File.sameDestination(path, File.getWorkingDir()):
            while File.exists(path):
                sleep(0.001)
        return True

    @staticmethod
    def getPaths(path = None, maxDepth=0):
        """
        Get a PathList obj from a path containing absolute Paths to both files and folders inside path.
        PathList extends list class with some convenient Path functionality.

        :param path: Path to folder. File is ignored. Default is Path("") which reads current work dir.
        :param maxDepth: Maximum folder depth, 0 means no limit.
        :return: PathList containing every absolute Paths in folder.
        """
        if path is None:
            path = Path("")
        path = File.toPath(path)
        path = path.getPathWithoutFile()
        if not File.exists(path):
            return PathList()

        path = File.getAbsolutePath(path)
        pathFoldersLen = len(path.foldersList)

        folderPathsToSearch = PathList(path)
        pathList = PathList()

        while folderPathsToSearch:
            folderPath = folderPathsToSearch[0]
            for subPath in os.listdir(folderPath):
                absoluteSubPath = folderPath.addPath(subPath)
                pathList.append(absoluteSubPath)
                if absoluteSubPath.isFile:
                    continue
                if maxDepth and len(absoluteSubPath.foldersList) - pathFoldersLen >= maxDepth:
                    continue
                folderPathsToSearch.append(absoluteSubPath)

            del folderPathsToSearch[0]
        return pathList

    @staticmethod
    def getTimeModified(path):
        """
        Gets time of when file (or folder?) was last modified

        :param str path: Path or Str
        :return: Time or None if file wasn't found
        """
        path = File.toPath(path)
        try:
            return os.path.getmtime(path)
        except FileNotFoundError:
            return None
        # except PermissionError: HERE **

    @staticmethod
    def getTimeCreated(path):
        """
        Gets datetime of when file (or folder?) was created.
        Can be innacurate it seems when re-creating files.

        :param str path: Path or Str
        :return: Datetime or None
        """
        path = File.toPath(path)
        try:
            return os.path.getctime(path)
        except FileNotFoundError:
            return None

    @staticmethod
    def openFolder(path):
        """
        Open file explorer on given path, files are ignored

        :param str path: Generic path that exists
        """
        path = File.toPath(path, requireExists=True).getPathWithoutFile()
        os.startfile(path)



from generalfile.base.classpath import Path
from generalfile.base.classpathlist import PathList

