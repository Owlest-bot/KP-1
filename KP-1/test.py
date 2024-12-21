import unittest
import os
import shutil

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = "config.yaml"
        cls.emulator = ShellEmulator(cls.config_path)

    def test_ls(self):
        result = self.emulator.ls()
        self.assertIn("file1.txt", result)
        self.assertIn("file2.txt", result)

    def test_cd(self):
        self.assertEqual(self.emulator.cd("dir1"), "Changed directory to /dir1/")
        self.assertEqual(self.emulator.cd("nonexistent"), "No such directory")

    def test_rm(self):
        self.assertEqual(self.emulator.rm("file1.txt"), "Removed file1.txt")
        self.assertEqual(self.emulator.rm("nonexistent.txt"), "File not found")

    def test_find(self):
        self.assertIn("file2.txt", self.emulator.find("file2.txt"))
        self.assertEqual(self.emulator.find("nonexistent.txt"), "File not found")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.emulator.vfs_temp_path)

if __name__ == '__main__':
    unittest.main()