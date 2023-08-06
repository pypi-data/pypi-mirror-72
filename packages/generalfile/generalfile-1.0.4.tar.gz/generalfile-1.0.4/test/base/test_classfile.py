"""
Tests for generalfile module

Exceptions raised directly by function should be specific Exceptions
Exceptions raised directly by indirect function should be generic Exception
"""
import unittest
import multiprocessing as mp
import time


from generalfile.base.classpath import Path
from generalfile.base.classfile import File
from test.base.setUpWorkDir import SetUpWorkDir

class FileTest(unittest.TestCase):
    def setUp(self):
        """Set working dir and clear folder"""
        SetUpWorkDir.activate()

    def test_toPath(self):
        File.write("exists.txt")
        File.createFolder("folderExists")

        self.assertRaises(AttributeError,       File.toPath, path=File.getAbsolutePath("folderDoesntExist"),  requireFiletype=True)
        self.assertRaises(AttributeError,       File.toPath, path=File.getAbsolutePath("folderDoesntExist"),  requireFiletype=True,     requireExists=True)
        self.assertRaises(AttributeError,       File.toPath, path=File.getAbsolutePath("doesntExist.txt"),    requireFiletype=False)
        self.assertRaises(AttributeError,       File.toPath, path=File.getAbsolutePath("doesntExist.txt"),    requireFiletype=False,    requireExists=True)

        self.assertRaises(AttributeError,       File.toPath, path="folderExists",       requireFiletype=True)
        self.assertRaises(AttributeError,       File.toPath, path="folderDoesntExist",  requireFiletype=True)
        self.assertRaises(AttributeError,       File.toPath, path="folderExists",       requireFiletype=True,   requireExists=True)
        self.assertRaises(AttributeError,       File.toPath, path="folderDoesntExist",  requireFiletype=True,   requireExists=True)
        self.assertRaises(AttributeError,       File.toPath, path="exists.txt",         requireFiletype=False)
        self.assertRaises(AttributeError,       File.toPath, path="doesntExist.txt",    requireFiletype=False)
        self.assertRaises(AttributeError,       File.toPath, path="exists.txt",         requireFiletype=False,   requireExists=True)
        self.assertRaises(AttributeError,       File.toPath, path="doesntExist.txt",    requireFiletype=False,   requireExists=True)

        self.assertRaises(TypeError,            File.toPath, path="exists.txt",         requireFiletype="tsv")
        self.assertRaises(TypeError,            File.toPath, path="doesntExist.txt",    requireFiletype="tsv")
        self.assertRaises(TypeError,            File.toPath, path="exists.txt",         requireFiletype="tsv",  requireExists=True)
        self.assertRaises(TypeError,            File.toPath, path="doesntExist.txt",    requireFiletype="tsv",  requireExists=True)

        self.assertRaises(FileNotFoundError,    File.toPath, path="folderDoesntExist",                          requireExists=True)
        self.assertRaises(FileNotFoundError,    File.toPath, path="doesntExist.txt",                            requireExists=True)
        self.assertRaises(FileNotFoundError,    File.toPath, path="folderDoesntExist",  requireFiletype=False,  requireExists=True)
        self.assertRaises(FileNotFoundError,    File.toPath, path="doesntExist.txt",    requireFiletype=True,   requireExists=True)
        self.assertRaises(FileNotFoundError,    File.toPath, path="doesntExist.txt",    requireFiletype="txt",  requireExists=True)

        self.assertRaises(FileExistsError,      File.toPath, path="folderExists",                               requireExists=False)
        self.assertRaises(FileExistsError,      File.toPath, path="exists.txt",                                 requireExists=False)
        self.assertRaises(FileExistsError,      File.toPath, path="Exists.txt",                                 requireExists=False)
        self.assertRaises(FileExistsError,      File.toPath, path="folderExists",       requireFiletype=False,  requireExists=False)
        self.assertRaises(FileExistsError,      File.toPath, path="exists.txt",         requireFiletype=True,   requireExists=False)
        self.assertRaises(FileExistsError,      File.toPath, path="exists.txt",         requireFiletype="txt",  requireExists=False)

        path = Path("test")
        self.assertIsNot(File.toPath(path), path)
        self.assertIsNot(File.toPath("test"), File.toPath("test"))
        self.assertEqual(File.toPath("test"), File.toPath("test"))

        self.assertEqual(File.toPath("test.txt", requireFiletype=True), "test.txt")
        self.assertEqual(File.toPath("test.txt", requireFiletype="txt"), "test.txt")
        File.write("test.txt")
        self.assertEqual(File.toPath("test.txt", requireExists=True), "test.txt")
        self.assertEqual(File.toPath("tEst.txt", requireExists=True), "tEst.txt")

    def test_exists(self):
        self.assertFalse(File.exists(File.getAbsolutePath("doesntExist")))

        self.assertFalse(File.exists(Path("doesntExist")))
        self.assertFalse(File.exists("doesntExist"))
        self.assertFalse(File.exists("doesntExist.txt"))

        File.write("test.txt")
        self.assertTrue(File.exists("test.txt"))
        self.assertTrue(File.exists("tEst.txt"))
        File.delete("test.txt")
        self.assertFalse(File.exists("test.txt"))
        self.assertFalse(File.exists("Test.txt"))

        File.createFolder("test")
        self.assertTrue(File.exists("test"))
        self.assertTrue(File.exists("teSt"))
        File.delete("test")
        self.assertFalse(File.exists("test"))

    def test_getWorkingDir(self):
        workingDir = File.getWorkingDir()
        File.setWorkingDir("folder")
        self.assertEqual(File.getWorkingDir().removeFromStart(workingDir), "folder")
        File.setWorkingDir(workingDir)

    def test_setWorkingDir(self):
        workingDir = File.getWorkingDir()
        self.assertRaises(Exception, File.setWorkingDir, "file.txt")
        self.assertEqual(File.setWorkingDir("folder"), File.getAbsolutePath(Path("")))
        File.setWorkingDir(workingDir)

    def test_getAbsolutePath(self):
        path = Path("folder")
        self.assertEqual(File.getAbsolutePath(path), File.getWorkingDir().addPath("folder"))
        path = Path("folder/file.txt")
        self.assertEqual(File.getAbsolutePath(path, "folder"), File.getWorkingDir().addPath("folder/folder/file.txt"))
        self.assertTrue(File.sameDestination(File.getAbsolutePath(path, "foldEr"), File.getWorkingDir().addPath("folder/folder/file.txt")))
        self.assertEqual(File.getAbsolutePath(File.getAbsolutePath(Path("test.txt")), "folder"), File.getAbsolutePath("test.txt"))

    def test_getRelativePath(self):
        self.assertRaises(Exception, File.getRelativePath, "test", "basePathWithFile.txt")
        self.assertRaises(AttributeError, File.getRelativePath, "folder/file.txt", "anotherFolder")

        path = File.getAbsolutePath(Path("folder/folder2/file.txt"))
        self.assertEqual(File.getRelativePath(path), "folder/folder2/file.txt")
        self.assertEqual(File.getRelativePath(path, "folder"), "folder2/file.txt")
        self.assertEqual(File.getRelativePath(path, "folder/folder2"), "file.txt")
        self.assertEqual(File.getRelativePath(path, "folder/foldEr2"), "file.txt")

    def test_sameDestination(self):
        self.assertTrue(File.sameDestination("folder", "folder"))
        self.assertTrue(File.sameDestination("Folder", "folder"))
        self.assertTrue(File.sameDestination("Folder", "foldeR"))
        self.assertTrue(File.sameDestination("file.txt", "file.txt"))
        self.assertTrue(File.sameDestination("File.txt", "file.txt"))
        self.assertTrue(File.sameDestination("file.txt", "File.txt"))
        self.assertTrue(File.sameDestination(File.getAbsolutePath("file.txt"), File.getAbsolutePath("file.txt")))
        self.assertTrue(File.sameDestination("file.txt", File.getAbsolutePath("file.txt")))
        self.assertTrue(File.sameDestination(File.getAbsolutePath("file.txt"), "file.txt"))
        self.assertTrue(File.sameDestination(File.getAbsolutePath("folder"), File.getAbsolutePath("folder")))
        self.assertTrue(File.sameDestination("folder", File.getAbsolutePath("folder")))
        self.assertTrue(File.sameDestination(File.getAbsolutePath("folder"), "folder"))

        self.assertFalse(File.sameDestination(File.getAbsolutePath("folder"), "folder.txt"))
        self.assertFalse(File.sameDestination("folder/file.txt", "folder"))
        self.assertFalse(File.sameDestination(File.getAbsolutePath("folder", "folder"), "folder"))
        self.assertFalse(File.sameDestination(File.getAbsolutePath("foldEr", "folder"), "fOlder"))

    def test__read_txt(self):
        File.write("test.txt")
        with open("test.txt", "r") as textIO:
            self.assertIsNone(File._read_txt(textIO))
        
        File.write("test2.txt", ["hello", "there", 2])
        with open("test2.txt", "r") as textIO:
            self.assertEqual(File._read_txt(textIO), ["hello", "there", 2])

    def test__write_txt(self):
        with open("test.txt", "w") as textIO:
            self.assertIsNone(File._write_txt(textIO, None))

        with open("test.txt", "w") as textIO:
            self.assertEqual(File._write_txt(textIO, ["hello", "there", 2]), '["hello", "there", 2]')

    def test_read(self):
        self.assertRaises(Exception, File.read, "folder")
        self.assertRaises(Exception, File.read, File.getAbsolutePath("folder"))
        self.assertRaises(EnvironmentError, File.read, "missingMethod.nonExistantFiletype")
        self.assertRaises(EnvironmentError, File.read, File.getAbsolutePath("missingMethod.nonExistantFiletype"))

        self.assertEqual(File.read(File.getAbsolutePath("doesntExist.txt")), None)
        self.assertEqual(File.read("doesntExist.txt"), None)
        self.assertEqual(File.read(File.getAbsolutePath("doesntExist.txt"), "default"), "default")
        self.assertEqual(File.read("doesntExist.txt", "default"), "default")

        File.write("test.txt", "hello")
        self.assertEqual(File.read("test.txt"), "hello")

        File.write("test2.txt", ["hello", "there", 2])
        self.assertEqual(File.read("test2.txt"), ["hello", "there", 2])

        File.write(File.getAbsolutePath("test3.txt"), ["hello", "there", 2])
        self.assertEqual(File.read("test3.txt"), ["hello", "there", 2])

        File.write(File.getAbsolutePath("test3.txt"), ["hello", "there", 2], overwrite=True)
        self.assertEqual(File.read("tEst3.txt"), ["hello", "there", 2])

    def test_write(self):
        self.assertRaises(Exception, File.write, "folder")
        self.assertRaises(Exception, File.write, File.getAbsolutePath("folder"))
        self.assertRaises(EnvironmentError, File.write, "missingMethod.nonExistantFiletype")
        self.assertIsNone(File.write("test.txt"))
        self.assertRaises(FileExistsError, File.write, "test.txt")
        self.assertRaises(FileExistsError, File.write, "tEst.txt")
        self.assertRaises(FileExistsError, File.write, File.getAbsolutePath("test.txt"))

        self.assertEqual(File.write("folder/folder/folder/test.txt", "hello"), '"hello"')
        self.assertEqual(File.write("folder/folder/folder/test.txt", "helloa", overwrite=True), '"helloa"')
        self.assertEqual(File.write(File.getAbsolutePath("folder/folder/folder/test.txt"), "hellos", overwrite=True), '"hellos"')

    def test_rename(self):
        File.write("folder/test.txt")
        self.assertRaises(NameError, File.rename, "folder/test.txt", "aux")
        self.assertRaises(NameError, File.rename, "folder", "aux")

        File.rename("folder/test.txt", "hello")
        self.assertTrue(File.exists("folder/hello.txt"))
        self.assertFalse(File.exists("folder/test.txt"))
        File.rename("folder", "folder2")
        self.assertTrue(File.exists("folder2"))
        self.assertFalse(File.exists("folder"))


    def test_copy(self):
        File.write("exists.txt", 1)
        File.write("exists2.txt", 2)
        File.write("folder/exists.txt", 3)
        self.assertRaises(Exception, File.copy, "doesntExist.txt", "")
        self.assertRaises(Exception, File.copy, "doesntExist", "")
        self.assertRaises(Exception, File.copy, File.getAbsolutePath("doesntExist"), "")
        self.assertRaises(RecursionError, File.copy, "exists.txt", "exists.txt")
        self.assertRaises(RecursionError, File.copy, File.getAbsolutePath("exists.txt"), "exists.txt")
        self.assertRaises(AttributeError, File.copy, "exists.txt", "file.tsv")
        self.assertRaises(FileExistsError, File.copy, "exists.txt", "exists2.txt")
        self.assertRaises(FileExistsError, File.copy, "exists.txt", File.getAbsolutePath("exists2.txt"))
        self.assertRaises(NotADirectoryError, File.copy, "folder", "exists.txt")
        self.assertRaises(FileExistsError, File.copy, "exists.txt", "folder")
        self.assertRaises(FileExistsError, File.copy, "folder", "")

        self.assertRaises(NameError, File.copy, "exists.txt", "aux.txt")
        self.assertRaises(NameError, File.copy, "exists.txt", "aux")
        self.assertRaises(NameError, File.copy, "folder", "aux")

        File.copy(File.getAbsolutePath("Exists.txt"), "exists7.txt")
        self.assertEqual(File.read("exisTs7.txt"), 1)

        File.copy(File.getAbsolutePath("exists.txt"), "exists6.txt")
        self.assertEqual(File.read("exists6.txt"), 1)

        File.copy("exists.txt", "exists3.txt")
        self.assertEqual(File.read("exists3.txt"), 1)

        File.copy("exists2.txt", "folder")
        self.assertEqual(File.read("folder/exists2.txt"), 2)

        File.copy("exists2.txt", File.getAbsolutePath("folder2"))
        self.assertEqual(File.read("folder2/exists2.txt"), 2)

        File.copy("exists2.txt", "newFolder")
        self.assertEqual(File.read("newFolder/exists2.txt"), 2)

        File.copy(File.getAbsolutePath("exists2.txt"), File.getAbsolutePath("newFolder2"))
        self.assertEqual(File.read("newFolder2/exists2.txt"), 2)

        File.copy("folder", "folder4")
        self.assertEqual(File.read("folder4/exists.txt"), 3)
        self.assertEqual(File.read("folder4/exists2.txt"), 2)

        File.write("folder3/exists4.txt", 4)
        File.write("folder3/exists5.txt", 5)
        File.copy("folder3", "")
        self.assertEqual(File.read("exists4.txt"), 4)

        File.copy("exists.txt", "exists2.txt", overwrite=True)
        self.assertEqual(File.read("exists2.txt"), 1)

        File.copy("exists.txt", "folder", overwrite=True)
        self.assertEqual(File.read("folder/exists.txt"), 1)

        File.copy("exists.txt", "folDer9")
        self.assertEqual(File.read("folder9/exists.txt"), 1)

        File.copy(File.getAbsolutePath("exists.txt"), File.getAbsolutePath("folder3"), overwrite=True)
        self.assertEqual(File.read("folder3/exists.txt"), 1)

        File.copy("folder3", "", overwrite=True)
        self.assertEqual(File.read("exists4.txt"), 4)
        self.assertEqual(File.read("exists5.txt"), 5)

    def test_createFolder(self):
        self.assertFalse(File.createFolder(""))
        self.assertTrue(File.createFolder("folder"))
        self.assertFalse(File.createFolder("folder"))
        self.assertFalse(File.createFolder("Folder"))
        self.assertTrue(File.createFolder("folder/folder/folder/file.txt"))
        self.assertTrue(File.createFolder(File.getAbsolutePath("folder/folder/folder2")))
        self.assertTrue(File.createFolder(File.getAbsolutePath("folder/folder/Folder3")))

    def test_clearFolder(self):
        File.write("folder/test.txt", 5)
        self.assertTrue(File.clearFolder("folder"))
        self.assertEqual(len(File.getPaths("folder")), 0)

        File.write("folder/test.txt", 5)
        self.assertTrue(File.clearFolder("Folder"))
        self.assertEqual(len(File.getPaths("folDer")), 0)

        File.write("folder/test.txt", 5)
        File.write("folder/folder2/tes2.txt", 3)
        self.assertTrue(File.clearFolder("folder/test.txt"))
        self.assertEqual(len(File.getPaths("folder")), 0)

        File.write("folder/test.txt", 5)
        File.write("folder/folder2/tes2.txt", 3)
        self.assertTrue(File.clearFolder(File.getAbsolutePath("folder/test.txt")))
        self.assertEqual(len(File.getPaths("folder")), 0)

    def test_trash(self):
        self.assertFalse(File.trash("doesntExist.txt"))
        self.assertFalse(File.trash("doesntExist"))
        self.assertFalse(File.trash(File.getAbsolutePath("doesntExist")))

        File.write("exists.txt")
        self.assertTrue(File.trash("exists.txt"))

        File.write("folder/exists.txt")
        self.assertTrue(File.trash("folder"))

        File.write("folder/exists.txt")
        self.assertTrue(File.trash(File.getAbsolutePath("folder")))

        File.write("folder/exists.txt")
        self.assertTrue(File.trash(File.getAbsolutePath("Folder")))
        self.assertEqual(len(File.getPaths("folder")), 0)

    def test_delete(self):
        self.assertFalse(File.delete("doesntExist.txt"))
        self.assertFalse(File.delete("doesntExist"))
        self.assertFalse(File.delete(File.getAbsolutePath("doesntExist")))

        File.write("exists.txt")
        self.assertTrue(File.delete("exists.txt"))

        File.write("folder/exists.txt")
        self.assertTrue(File.delete("folder"))

        File.write("folder/exists.txt")
        self.assertTrue(File.delete(File.getAbsolutePath("folder")))

        File.write("folder/exists.txt")
        self.assertTrue(File.delete(File.getAbsolutePath("Folder")))
        self.assertEqual(len(File.getPaths("folder")), 0)

    def test_getPaths(self):
        File.write("test.txt")
        File.write("folder/test2.txt")
        File.write("folder/test3.txt")

        self.assertEqual(len(File.getPaths("doesntExist")), 0)
        self.assertEqual(len(File.getPaths("doesntExist/doesntExist.txt")), 0)

        self.assertEqual(len(File.getPaths()), 4)
        self.assertEqual(len(File.getPaths("")), 4)
        self.assertEqual(len(File.getPaths("doesntExist.txt")), 4)
        self.assertEqual(len(File.getPaths(File.getAbsolutePath(""))), 4)

        self.assertEqual(len(File.getPaths("folder/test2.txt")), 2)
        self.assertEqual(len(File.getPaths(File.getAbsolutePath("folder/test2.txt"))), 2)
        self.assertEqual(len(File.getPaths("folder")), 2)
        self.assertEqual(len(File.getPaths(File.getAbsolutePath("folder"))), 2)
        self.assertEqual(len(File.getPaths(File.getAbsolutePath("folDer"))), 2)

    def test_getTimeModified(self):
        File.write("folder/test.txt")
        # Sometimes it got a really small negative number because it's so fast, such as "-2.384185791015625e-07"
        self.assertTrue(-0.1 <= time.time() - File.getTimeModified("folder/test.txt") < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeModified(File.getAbsolutePath("folder/test.txt")) < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeModified("folder") < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeModified(File.getAbsolutePath("folder")) < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeModified("Folder") < 0.1)

    def test_getTimeCreated(self):
        File.write("folder/test.txt")
        self.assertTrue(-0.1 <= time.time() - File.getTimeCreated("folder/test.txt") < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeCreated(File.getAbsolutePath("folder/test.txt")) < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeCreated("folder") < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeCreated(File.getAbsolutePath("folder")) < 0.1)
        self.assertTrue(-0.1 <= time.time() - File.getTimeCreated("Folder") < 0.1)

    def test_threads(self):
        threads = []
        queue = mp.Queue()
        for i in range(count := 10):
            threads.append(mp.Process(target=threadTest, args=(queue, i)))
        for thread in threads:
            thread.start()

        results = []
        for i in range(count):
            self.assertNotIn(get := queue.get(), results)
            results.append(get)

        self.assertEqual(len(results), count)

def threadTest(queue, i):
    """
    Simple target function for multiprocess testing

    :param mp.Queue queue:
    :param int i:
    """
    queue.put(int(File.write("test.txt", i, overwrite=True)))

if __name__ == "__main__":
    x = unittest.main()







    # @staticmethod
    # def readValue(path, key):
    #     """
    #
    #     :param path:
    #     :param key:
    #     :return:
    #     """
    #     path = File.toPath(path)
    #     values = File.read(path, default={})
    #     if key not in values:
    #         return None
    #     return values[key]
    #
    # @staticmethod
    # def setValue(path, key, value):
    #     path = File.toPath(path)
    #     """
    #     """
    #     values = File.read(path, default={})
    #     values[key] = value
    #     File.write(path, values)
    #     return value
    #
    # @staticmethod
    # def index(path, key=None, value=None):
    #     path = File.toPath(path)
    #     """
    #     """
    #     if value is not None:
    #         return File().setValue(path, key, value)
    #     else:
    #         if key is None:
    #             return File().read(path, default={})
    #         else:
    #             return File().readValue(path, key)




# class FileTSV(File):
#     def scrubDictOfDicts(self, dictOfDicts, indexName):
#         """
#         dictOfDicts can be singular dict also
#         """
#         if isinstance(dictOfDicts, dict):
#             if isinstance(lib.dictFirstValue(dictOfDicts), dict):
#                 return dictOfDicts
#             else:
#                 return {dictOfDicts[indexName]: dictOfDicts}
#
#         print(dictOfDicts)
#         lib.error("dictOfDicts failed scrubbing, printed above")
#
#     def tsvWrite(self, filepath, dictOfDicts, indexName):
#         dictOfDicts = self.scrubDictOfDicts(dictOfDicts, indexName)
#         filepath = self.yesTsv(filepath)
#         self.createFolderPath(filepath)
#
#         with open(filepath, 'w') as tsvfile:
#             writer = csv.writer(tsvfile, delimiter = "\t", lineterminator = "\n")
#             writer.writerow(list(lib.dictFirstValue(dictOfDicts, iterate = True).columns))
#             for index, subDict in dictOfDicts.items():
#                 writer.writerow(list(subDict.values()))
#         return dictOfDicts
#
#     def tsvAppend(self, filepath, dictOfDicts, indexName):
#         """
#         Write instead if file doesn't exist
#         """
#         filepath = self.yesTsv(filepath)
#
#         if not self.exists(filepath):
#             return self.tsvWrite(filepath, dictOfDicts, indexName)
#
#         dictOfDicts = self.scrubDictOfDicts(dictOfDicts, indexName)
#
#         with open(filepath, 'a') as tsvfile:
#             writer = csv.writer(tsvfile, delimiter = "\t", lineterminator = "\n")
#             for index, subDict in dictOfDicts.items():
#                 writer.writerow(list(subDict.values()))
#
#         return dictOfDicts
#
#     def tsvRowToDict(self, row):
#         return {k: lib.strToDynamicType(v) for k, v in row.items()}
#
#     def tsvRead(self, filepath, indexName):
#         """
#         Manually add index to each created dict
#         Check for indexName duplicates, if there are any just use the last one
#         row in reader is an iterator I think, it contains all values as strings, first row will be the labels
#         """
#         filepath = self.yesTsv(filepath)
#         if not self.exists(filepath):
#             return {}
#
#         with open(filepath, 'r') as tsvfile:
#             reader = csv.DictReader(tsvfile, delimiter = "\t")
#             returnDict = {subDict[indexName]: subDict for subDict in map(self.tsvRowToDict, reader)}
#             # returnDict = {subDict[indexName]: subDict for subDict in map(dict, reader)}  # Without casting, 3 times faster
#
#         return returnDict
#
#     def tsvUpdate(self, filepath, values, indexName):
#         """
#         See if row exists, insert new if it doesn't, update if it does
#         Use pandas dataframe?
#         """
#         df = pd.read_csv(filepath)
#         print(df.head(5))
#
#     def yesTsv(self, filepath):
#         # return "{}.tsv".format(self.noFiletypeEnding(filepath))
#         return ""
