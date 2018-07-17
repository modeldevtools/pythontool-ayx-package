import os
import sqlite3
import pandas
from unittest import TestCase
from ayx.Alteryx import read, write
from ayx.CachedData import SqliteDb, deleteFile, fileExists

def outputFilename(connection_num):
    return 'output_{}.sqlite'.format(connection_num)


class TestAlteryxWrite(TestCase):

    def setUp(self):
        self.output_connections = [1,2,3,4,5]
        # delete pre-existing output data
        for connection_num in self.output_connections:
            deleteFile(outputFilename(connection_num))
        # create a pandas dataframe to write out
        self.data = read("#1")

    def testAyxWriteData(self):
        # loop through all valid connections
        for connection_num in self.output_connections:
            # get filepath
            filepath = os.path.abspath(outputFilename(connection_num))
            # it shouldn't exist (after setup executed)
            if fileExists(filepath):
                raise FileExistsError('File already exists: {}'.format(filepath))
            # write data
            write(self.data, connection_num)
            result = fileExists(filepath)
            self.assertTrue(result)

    def tearDown(self):
        for connection_num in self.output_connections:
            deleteFile(outputFilename(connection_num))

class TestAlteryxWriteContents(TestCase):

    def setUp(self):
        self.connection = 5
        self.filename = outputFilename(self.connection)
        self.data = read("#2")
        deleteFile(self.filename)
        self.test = True

    def testAyxWriteDataResultType(self):
        result = type(write(self.data, self.connection))
        expected = pandas.core.frame.DataFrame
        self.assertEqual(result, expected)

    def testAyxWriteDataContents(self):
        write(self.data, self.connection)
        expected = self.data
        with SqliteDb(self.filename, create_new=False) as result_db:
            actual = result_db.getData()
        print(expected.head())
        print(actual.head())
        pandas.testing.assert_frame_equal(expected, actual)

    def tearDown(self):
        deleteFile(self.filename)
