import unittest
import os
import json
import tempfile

from iiif_tiler_action import updateManifest

class TestUpdateManifest(unittest.TestCase):
    def createDummyImage(self, name, infoJsonFile):
        with open(infoJsonFile, "r") as file:
            # Check image is valid before adding
            infoJson = json.load(file)
            os.mkdir(name)

            with open(f"{name}/info.json", "w") as file:
                json.dump(infoJson, file)

    def setUp(self):
        # Ensure we start in the current project directory 
        os.chdir(os.path.dirname(os.path.dirname(__file__)))            

    def test_manifest(self):
        infoJsonFile = os.path.abspath("tests/fixtures/IMG_5969.json")
        print (infoJsonFile)
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            self.createDummyImage("IMG_5969", infoJsonFile)

            manifest = updateManifest.createManifest("test", "testRepo", "images/manifest.json", tmpdir, skipImageValidation=True)
            self.assertEqual(manifest.id, "https://test.github.io/testRepo/images/manifest.json")
            self.assertEqual(len(manifest.items), 1, "Manifest should have only one canvas")

    def test_v2_manifest(self):
        infoJsonFile = os.path.abspath("tests/fixtures/v2_info.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            self.createDummyImage("IMG_5969", infoJsonFile)

            manifest = updateManifest.createManifest("test", "testRepo", "images/manifest.json", tmpdir, skipImageValidation=True)
            self.assertEqual(manifest.id, "https://test.github.io/testRepo/images/manifest.json")
            self.assertEqual(len(manifest.items), 1, "Manifest should have only one canvas")
  
    def test_canvas_label(self):
        infoJsonFile = os.path.abspath("tests/fixtures/v2_info.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            self.createDummyImage("IMG_5969", infoJsonFile)

            manifest = updateManifest.createManifest("test", "testRepo", "images/manifest.json", tmpdir, skipImageValidation=True)
            self.assertIsNotNone(manifest.items[0].label, "Canvas should have a label")
            self.assertTrue("none" in manifest.items[0].label, "Label should have langauge")
            self.assertTrue(isinstance(manifest.items[0].label["none"], list), "Label should be an array")
            self.assertEqual(manifest.items[0].label["none"][0], "IMG_5969", "Label should match image name")

    def test_malformed_image(self):
        infoJsonFile = os.path.abspath("tests/fixtures/v2_info.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            self.createDummyImage("IMG_5969", infoJsonFile)

            manifest = updateManifest.createManifest("test", "testRepo", "images/manifest.json", tmpdir)
            self.assertEqual(manifest.id, "https://test.github.io/testRepo/images/manifest.json")
            self.assertEqual(len(manifest.items), 0, "Manifest should no canvases as only image is malformed")        

