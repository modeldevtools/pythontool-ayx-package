import os
import sqlite3
from unittest import TestCase
from ayx.CachedData import CachedData
from ayx.tests.testdata.datafiles import getTestFileName
from pathlib import Path

class TestCachedDataRead(TestCase):

    def setUp(self):
        self.data = CachedData()

    def testDefaultConfig(self):
        expected = ['#1','#2','1']
        actual = self.data.getIncomingConnectionNames()
        self.assertCountEqual(expected, actual)


class TestCachedDataSpecificConfig(TestCase):

    def setUp(self):
        config_filepath = getTestFileName('config_valid_2')
        self.data = CachedData(config_filepath)

    def testSpecificConfig(self):
        expected = ['VALID2_#1','VALID2_#2','VALID2_1']
        actual = self.data.getIncomingConnectionNames()
        self.assertCountEqual(expected, actual)

class TestNoInputs(TestCase):
    def setUp(self):
        file = getTestFileName('no_input_data_config')
        self.data = CachedData(file)

    def testNoInput(self):
        expected = []
        actual = self.data.getIncomingConnectionNames()
        self.assertEqual(expected, actual)


class TestWorkflowConstants(TestCase):
    def setUp(self):
        self.data  = CachedData()

    def testWorkflowConstants(self):
        guiInteractionActual = self.data.getWorkflowConstant("Engine.GuiInteraction")
        self.assertEqual("1", guiInteractionActual)

        with self.assertRaises(ReferenceError) as e:
            itrNumActual = self.data.getWorkflowConstant("IterationNumber")

        self.assertTrue("The Constant \"IterationNumber\" does not exist -- make sure you typed it exactly the same in the Alteryx GUI and your python code." in str(e.exception))


        itrNumActual = self.data.getWorkflowConstant("Engine.IterationNumber")
        self.assertEqual(0, itrNumActual)

        win_dir = self.data.getWorkflowConstant("Engine.ModuleDirectory")
        self.assertEqual("s:\\Alteryx\\bin_x64\\Debug\\", win_dir)

        python_path = self.data.getWorkflowConstant("Engine.ModuleDirectory", return_as_path=True)
        expected_path = Path('s:/')
        expected_path = expected_path / "Alteryx" / "bin_x64" / "Debug"
        self.assertEqual(expected_path, python_path)