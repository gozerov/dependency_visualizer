import unittest
import tarfile
from io import BytesIO
from main import ShellEmulator  # Import your emulator class

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a virtual tar file in memory for testing
        cls.vfs_tar = BytesIO()
        with tarfile.open(fileobj=cls.vfs_tar, mode="w") as tar:
            # Create folders and files in memory
            folder1 = tarfile.TarInfo("vfs/folder1/")
            folder2 = tarfile.TarInfo("vfs/folder2/")
            file1 = tarfile.TarInfo("vfs/folder1/file1.txt")
            file2 = tarfile.TarInfo("vfs/folder2/file2.txt")
            
            file1.size = len(b"Hello World\n")
            file2.size = len(b"Second File\n")

            tar.addfile(folder1)
            tar.addfile(folder2)
            tar.addfile(file1, BytesIO(b"Hello World\n"))
            tar.addfile(file2, BytesIO(b"Second File\n"))

        # Set up shell emulator
        cls.vfs_tar.seek(0)
        cls.emulator = ShellEmulator("testuser", "localhost", cls.vfs_tar)

    # Test for `ls` command
    def test_ls_root(self):
        output = self.emulator.ls()
        self.assertIn("file1.txt", output)

    def test_ls_folder1(self):
        self.emulator.cd("folder1")
        output = self.emulator.ls()
        self.assertIn("file1.txt", output)

    # Test for `cd` command
    def test_cd_root(self):
        self.emulator.cd("/")
        self.assertEqual(self.emulator.current_dir, "vfs/")

    def test_cd_folder1(self):
        self.emulator.cd("folder1")
        self.assertEqual(self.emulator.current_dir, "vfs/folder1/")

    def test_cd_invalid(self):
        output = self.emulator.cd("invalid_folder")
        self.assertEqual(output, "No such directory: invalid_folder")

    # Test for `head` command
    def test_head_file1(self):
        self.emulator.cd("folder1")
        output = self.emulator.head("file1.txt")
        self.assertIn("Hello World", output)

    def test_head_invalid_file(self):
        output = self.emulator.head("nonexistent.txt")
        self.assertEqual(output, "No such file: nonexistent.txt")

    # Test for `wc` command
    def test_wc_file2(self):
        output = self.emulator.wc("file1.txt")
        self.assertIn("1 2 12 file1.txt", output)

    def test_wc_invalid_file(self):
        output = self.emulator.wc("nonexistent.txt")
        self.assertEqual(output, "No such file: nonexistent.txt")

    # Test for `exit` command
    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.emulator.exit_emulator()

if __name__ == "__main__":
    unittest.main()