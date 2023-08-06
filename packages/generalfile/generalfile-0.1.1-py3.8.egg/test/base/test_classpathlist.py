"""
Tests for generalfile module

Exceptions raised directly by function should be specific Exceptions
Exceptions raised directly by indirect function should be generic Exception
"""
import unittest
from generalfile import PathList, Path, File

class PathListTest(unittest.TestCase):
    def test_pathList(self):
        self.assertRaises(TypeError, PathList, 1)
        self.assertRaises(TypeError, PathList, [1])
        self.assertRaises(TypeError, PathList, "file.txt", 1)
        self.assertRaises(TypeError, PathList, "file.txt", ["folder", True])
        self.assertRaises(TypeError, PathList, "file.txt", ["folder"], ["folder2", None])

        self.assertEqual(PathList("file.txt"), ["file.txt"])
        self.assertEqual(PathList("file.txt", "folder"), ["file.txt", "folder"])
        self.assertEqual(PathList("file.txt", ["folder"]), ["file.txt", "folder"])
        self.assertEqual(PathList("file.txt", ["folder", "folder2/file.txt"]), ["file.txt", "folder", "folder2/file.txt"])
        self.assertEqual(PathList([Path("test.txt").getAbsolute()], "file.txt", ["folder"]), [Path("test.txt").getAbsolute(), "file.txt", "folder"])

    def test_toPath(self):
        self.assertFalse(all([isinstance(path, Path) for path in PathList(["file.txt", "folder"])]))
        self.assertTrue(all([isinstance(path, Path) for path in PathList(["file.txt", "folder"]).toPath()]))
        self.assertTrue(all([isinstance(path, Path) for path in PathList([Path("file.txt"), "folder"]).toPath()]))
        self.assertTrue(all([isinstance(path, Path) for path in PathList([Path("file.txt"), Path("folder")]).toPath()]))

        pathList = PathList(["file.txt", "folder"])
        pathList.toPath()
        self.assertTrue(all([isinstance(path, Path) for path in pathList]))

    def test_getFolders(self):
        self.assertEqual(PathList(["file.txt", "file2.txt"]).getFolders(), [])
        self.assertEqual(PathList(["file.txt", "folder"]).getFolders(), ["folder"])
        self.assertEqual(PathList(["folder1", "folder2/folder3"]).getFolders(), ["folder1", "folder2/folder3"])

    def test_getFiles(self):
        self.assertEqual(PathList(["file.txt", "file2.txt"]).getFiles(), ["file.txt", "file2.txt"])
        self.assertEqual(PathList(["file.txt", "folder"]).getFiles(), ["file.txt"])
        self.assertEqual(PathList(["folder1", "folder2/folder3"]).getFiles(), [])

    def test_getRelative(self):
        self.assertEqual(PathList(Path("file.txt").getAbsolute()).getRelative(), ["file.txt"])
        self.assertEqual(PathList([Path("file.txt").getAbsolute(), "file2.txt"]).getRelative(), ["file.txt", "file2.txt"])

    def test_getAbsolute(self):
        self.assertEqual(PathList(Path("file.txt")).getAbsolute(), [Path("file.txt").getAbsolute()])
        self.assertEqual(PathList([Path("file.txt"), "file2.txt"]).getAbsolute(), [Path("file.txt").getAbsolute(), Path("file2.txt").getAbsolute()])

    def test_exists(self):
        File.write("exists.txt")
        self.assertEqual(PathList("doesntExist.txt", "exists.txt").exists(), (False, True))
        File.delete("exists.txt")



if __name__ == "__main__":
    unittest.main()































