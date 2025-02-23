import unittest
import os
import logging

import pyfakefs
from pyfakefs.fake_filesystem_unittest import TestCase

from greenberry.utils.search_for_namespace import search_for_namespace



logging.basicConfig()

class testSearch(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_find_file(self):
        file_path = "/test/file.txt"
        directory = "src"
        self.fs.create_dir("test/")
        self.fs.create_file("src" + file_path)
        self.fs.create_file("src" + file_path + ".js")
        self.assertEqual(search_for_namespace("file.txt", directory), ["file.txt"])


if __name__ == "__main__":
    unittest.main()
