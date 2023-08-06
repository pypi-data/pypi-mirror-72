import unittest
import rna.plotting


class PlotManager_Test(unittest.TestCase):
    def setUp(self):
        self.inst = rna.plotting.PlotManager(dict(vmin=0, vmax=1,
                                                  cmap='rainbow'))

    def test_axes_and_dims(self):
        self.assertIsNotNone(self.inst.axes)
        self.assertEqual(self.inst.dim, 2)

    def test_color(self):
        color_start = 'r'
        color_start = self.inst.format_colors(color_start,
                                              fmt='rgba', length=1)
        color = color_start
        for fmt in ('norm', 'rgb', 'hex', 'rgba'):
            color = self.inst.format_colors(color, fmt=fmt, length=1)
            self.assertEqual(rna.plotting.colors.color_fmt(color), fmt)
        self.assertEqual(color, color_start)


if __name__ == '__main__':
    unittest.main()
