"""
Tests for generalfile module

Exceptions raised directly by function should be specific Exceptions
Exceptions raised directly by indirect function should be generic Exception
"""
import unittest
from generalfile import Path, File

class PathTest(unittest.TestCase):
    def test_path(self):
        self.assertRaises(WindowsError, Path, "tes*t.txt")
        self.assertRaises(WindowsError, Path, "te<st")
        self.assertRaises(WindowsError, Path, "te>st")
        self.assertRaises(WindowsError, Path, "te\"st")
        self.assertRaises(WindowsError, Path, "te|st")
        self.assertRaises(WindowsError, Path, "te?st")
        self.assertRaises(WindowsError, Path, "te:st")
        self.assertRaises(WindowsError, Path, "test.txt/test.txt")
        self.assertRaises(WindowsError, Path, "C:/folder/te:st.txt")
        self.assertRaises(WindowsError, Path, "C:/folder/te.st.txt")
        self.assertRaises(WindowsError, Path, "AB:/folder/test.txt")
        self.assertRaises(WindowsError, Path, ":A/folder/test.txt")

        self.assertEqual(Path("folder\\file.txt"), "folder/file.txt")
        self.assertEqual(Path("Folder/file.txt"), "Folder/file.txt")
        self.assertEqual(Path(""), "")
        self.assertEqual(Path("folder"), "folder")
        self.assertEqual(Path("folder/"), "folder")
        self.assertEqual(Path("folder\\"), "folder")
        self.assertEqual(Path("/folder"), "folder")
        self.assertEqual(Path("\\folder"), "folder")
        self.assertEqual(Path("file.txt"), "file.txt")

    def test_toPath(self):
        self.assertRaises(ValueError, Path.toPath, True)
        self.assertRaises(ValueError, Path.toPath, None)
        self.assertRaises(ValueError, Path.toPath, ["list"])

        self.assertRaises(AttributeError, Path.toPath, "file.txt", requireFiletype=False)
        self.assertRaises(AttributeError, Path.toPath, "folder", requireFiletype=True)

        self.assertRaises(TypeError, Path.toPath, "file.tsv", requireFiletype="txt")
        self.assertRaises(TypeError, Path.toPath, "folder/file.txt", requireFiletype="tsv")

        self.assertTrue(isinstance(Path.toPath("test"), Path))
        self.assertTrue(isinstance(Path.toPath("test/file.txt"), Path))
        self.assertTrue(isinstance(Path.toPath(""), Path))

    def test_addPath(self):
        self.assertRaises(FileExistsError, Path("file.txt").addPath, Path("folder"))
        self.assertRaises(FileExistsError, Path("file.txt").addPath, Path("file.txt"))

        self.assertRaises(AttributeError, Path("folder").addPath, Path("file.txt").getAbsolute())
        self.assertRaises(AttributeError, Path("folder").addPath, Path("file.txt").getAbsolute())

        self.assertEqual(Path("folder").addPath("file.txt"), "folder/file.txt")
        self.assertEqual(Path("folder").getAbsolute().addPath("file.txt").getRelative(), "folder/file.txt")
        self.assertEqual(Path("folder").addPath("folder2"), "folder/folder2")
        self.assertEqual(Path("folder/folder2").addPath("folder3/file.txt"), "folder/folder2/folder3/file.txt")

    def test_getPathWithoutFile(self):
        self.assertEqual(Path("test.txt").getPathWithoutFile(), "")
        self.assertEqual(Path("folder/test.txt").getPathWithoutFile(), "folder")
        self.assertEqual(Path("C:/folder/test.txt").getPathWithoutFile(), "C:/folder")
        self.assertEqual(Path("C:/folder/test_SUFFIX.tsv").getPathWithoutFile(), "C:/folder")

    def test_setPartsList(self):
        self.assertRaises(Exception, Path().setPartsList, ["test", "test.fail.txt"])
        self.assertRaises(Exception, Path().setPartsList, ["C:", "test.fail.txt"])
        self.assertRaises(Exception, Path().setPartsList, ["C:", "te:st.txt"])
        self.assertRaises(Exception, Path().setPartsList, ["file.txt", "test.txt"])

        self.assertEqual(Path("C:/test/file.txt").setPartsList(["folder"]), "folder")
        self.assertEqual(Path("").setPartsList(["folder", "test.txt"]), "folder/test.txt")
        self.assertEqual(Path("").setPartsList(["test.txt"]), "test.txt")

    def test_setFoldersList(self):
        self.assertRaises(Exception, Path().setFoldersList, ["test", "test.fail.txt"])
        self.assertRaises(Exception, Path().setFoldersList, ["C:", "test.fail.txt"])
        self.assertRaises(Exception, Path().setFoldersList, ["C:", "te:st.txt"])
        self.assertRaises(Exception, Path().setFoldersList, ["file.txt", "test.txt"])
        self.assertRaises(Exception, Path("folder/test.txt").setFoldersList, ["test.txt"])

        self.assertEqual(Path("").setFoldersList(["folder"]), "folder")
        self.assertEqual(Path("").setFoldersList(["folder", "test.txt"]), "folder/test.txt")
        self.assertEqual(Path("test.txt").setFoldersList(["folder"]), "folder/test.txt")
        self.assertEqual(Path("").setFoldersList(["test.txt"]), "test.txt")
        self.assertEqual(Path("folder/file.txt").setFoldersList(["C:"]), "C:/file.txt")

    def test_setFilenamePure(self):
        self.assertRaises(Exception, Path().setFilenamePure, "test.txt")
        self.assertRaises(Exception, Path("hello.txt").setFilenamePure, "test.txt")

        self.assertEqual(Path("hello.txt").setFilenamePure("file"), "file.txt")
        self.assertEqual(Path("folder/hello.txt").setFilenamePure("file"), "folder/file.txt")
        self.assertEqual(Path("folder/hello_SUFFIX.txt").setFilenamePure("file"), "folder/file_SUFFIX.txt")

    def test_setSuffix(self):
        self.assertRaises(Exception, Path().setSuffix, "suffix")
        self.assertRaises(Exception, Path("hello").setSuffix, "suffix")
        self.assertRaises(Exception, Path("hello.txt").setSuffix, "suffix.txt")

        self.assertEqual(Path("file.txt").setSuffix("suffix"), "file_suffix.txt")
        self.assertEqual(Path("folder/file.txt").setSuffix("suffix"), "folder/file_suffix.txt")
        self.assertEqual(Path("folder/hello_SUFFIX.txt").setSuffix("test"), "folder/hello_test.txt")
        self.assertEqual(Path("C:/folder/hello_SUFFIX.txt").setSuffix("test"), "C:/folder/hello_test.txt")

    def test_setFiletype(self):
        self.assertRaises(Exception, Path("folder").setFiletype, "txt")
        self.assertRaises(Exception, Path().setFiletype, "txt")
        self.assertRaises(Exception, Path().getAbsolute().setFiletype, "txt")
        self.assertRaises(Exception, Path("test.txt").setFiletype, "")

        self.assertEqual(Path("test.tsv").setFiletype("txt"), "test.txt")
        self.assertEqual(Path("folder/test.tsv").setFiletype("txt"), "folder/test.txt")
        self.assertEqual(Path("folder/test_SUFFIX.tsv").setFiletype("txt"), "folder/test_SUFFIX.txt")
        self.assertEqual(Path("folder/test_SUFFIX.tsv").getAbsolute().setFiletype("txt").getRelative(), "folder/test_SUFFIX.txt")

    def test_startsWithPath(self):
        self.assertFalse(Path("file.txt").startsWithPath("folder"))
        self.assertFalse(Path("file.txt").startsWithPath("file"))
        self.assertFalse(Path("folder/file.txt").startsWithPath("file.txt"))
        self.assertFalse(Path("folder/file.txt").getAbsolute().startsWithPath("folder"))
        self.assertFalse(Path("file.txt").startsWithPath(File.getWorkingDir()))

        self.assertTrue(Path("folder/file.txt").startsWithPath("folder"))
        self.assertTrue(Path("file.txt").startsWithPath("file.txt"))
        self.assertTrue(Path("file_SUFFIX.txt").startsWithPath("file_SUFFIX.txt"))
        self.assertTrue(Path("filE.txt").startsWithPath("file.txt"))
        self.assertTrue(Path("file.txt").getAbsolute().startsWithPath(File.getWorkingDir()))

    def test_endsWithPath(self):
        self.assertFalse(Path("file.txt").endsWithPath("folder"))
        self.assertFalse(Path("file.txt").endsWithPath("file"))
        self.assertFalse(Path("folder/file.txt").endsWithPath("folder"))
        self.assertFalse(Path("folder/file.txt").getAbsolute().endsWithPath("file"))

        self.assertTrue(Path("folder/file.txt").endsWithPath("file.txt"))
        self.assertTrue(Path("file.txt").endsWithPath("file.txt"))
        self.assertTrue(Path("file_SUFFIX.txt").endsWithPath("file_SUFFIX.txt"))
        self.assertTrue(Path("filE.txt").endsWithPath("file.txt"))
        self.assertTrue(Path("filE.txt").getAbsolute().endsWithPath("file.txt"))

    def test_removeFromStart(self):
        self.assertEqual(Path("test.txt").removeFromStart("test.txt"), "")
        self.assertEqual(Path("folder/test.txt").removeFromStart("Folder"), "test.txt")
        self.assertEqual(Path("folder/test.txt").removeFromStart("test"), "folder/test.txt")
        self.assertEqual(Path("folder/test.txt").getAbsolute().removeFromStart(File.getWorkingDir()), "folder/test.txt")

    def test_removeFromEnd(self):
        self.assertEqual(Path("test.txt").removeFromEnd("test.txt"), "")
        self.assertEqual(Path("test.txt").removeFromEnd("txt"), "test.txt")
        self.assertEqual(Path("folder/test.txt").removeFromEnd("test.txt"), "folder")
        self.assertEqual(Path("folder/test.txt").removeFromEnd("test"), "folder/test.txt")
        self.assertEqual(Path("folder/test.txt").getAbsolute().removeFromEnd("folder/test.txt"), File.getWorkingDir())

    def test_getAbsolute(self):
        self.assertEqual(Path("").getAbsolute(), File.getWorkingDir())
        self.assertEqual(Path("test.txt").getAbsolute(), File.getWorkingDir().addPath("test.txt"))
        self.assertEqual(Path("test.txt").getAbsolute("folder"), Path("folder/test.txt").getAbsolute())

    def test_getRelative(self):
        self.assertRaises(Exception, Path("file.txt").getRelative, "doesntExist")
        self.assertEqual(Path("folder/test.txt").getRelative("folder"), "test.txt")
        self.assertEqual(Path("folder/test.txt").getAbsolute().getRelative("folder"), "test.txt")
        self.assertEqual(Path().getAbsolute().getRelative(), "")

    def test_getParent(self):
        self.assertEqual(Path("folder/file.txt").getParent(), "folder")
        self.assertEqual(Path("folder/file.txt").getParent(2), "")
        self.assertEqual(Path("folder/file.txt").getParent(2), File.getWorkingDir().getRelative())
        self.assertEqual(Path("folder/file.txt").getParent(0), "folder/file.txt")
        self.assertEqual(Path("folder/file.txt").getParent(3), File.getWorkingDir().getParent(1))

if __name__ == "__main__":
    unittest.main()































