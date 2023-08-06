import unittest
from .base import crop, resize, intrinsics
from .base import _width, _height, _cx, _cy

class TestBase(unittest.TestCase):

    def test_crop(self):
        intr = intrinsics(128, 96, 128.0, 128.0, 0.5 * 128 -
                          0.5, 0.5 * 96 - 0.5, half_pixel_centers=False)
        intr = crop(intr, 80, 50, 10, 20)

        self.assertEqual(_width(intr), 80)
        self.assertEqual(_height(intr), 50)
        self.assertEqual(_cx(intr), 0.5 * 128 - 0.5 - 10)
        self.assertEqual(_cy(intr), 0.5 * 96 - 0.5 - 20)

    def test_resize(self):
        intr = intrinsics(128, 96, 128.0, 128.0, 0.5 * 128 -
                          0.5, 0.5 * 96 - 0.5, half_pixel_centers=False)

        w = 80
        h = 170

        intr = resize(intr, w, h)

        self.assertEqual(_width(intr), w)
        self.assertEqual(_height(intr), h)
        self.assertEqual(_cx(intr), 0.5 * w - 0.5)
        self.assertEqual(_cy(intr), 0.5 * h - 0.5)


if __name__ == '__main__':
    unittest.main()
