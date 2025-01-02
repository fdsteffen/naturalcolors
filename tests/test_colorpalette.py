import unittest
import naturalcolors.colorpalette as ncp
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent


class ColorImportTest(unittest.TestCase):

    def testLoad(self):
        default_inputcolors = ncp.load_colors(
            Path(TEST_DIR).joinpath("test_colormap.json")
        )
        self.assertEqual(default_inputcolors["redwhiteblue"][0, 0], 1)
        self.assertEqual(default_inputcolors["redwhiteblue"][0, 1], 0)
        self.assertEqual(default_inputcolors["redwhiteblue"][0, 2], 0)

    def test_undefinedCmap(self):
        default_cmaps = ncp.get_cmap("undefinedCmap")
        self.assertIsNone(default_cmaps)

    def test_getRedColor(self):
        linearSegmentedCmap = ncp.get_cmap(
            "redwhiteblue", Path(TEST_DIR).joinpath("test_colormap.json")
        )
        self.assertEqual(ncp.get_colors(linearSegmentedCmap, n=1)[0, 0], 1)
        self.assertEqual(ncp.get_colors(linearSegmentedCmap, n=1)[0, 1], 0)
        self.assertEqual(ncp.get_colors(linearSegmentedCmap, n=1)[0, 2], 0)


if __name__ == "__main__":
    unittest.main()
