import unittest

import numpy as np

from digitos_robustos.perturbations import add_gaussian_noise, rotate_images


class PerturbationTests(unittest.TestCase):
    def test_noise_is_reproducible_and_bounded(self) -> None:
        images = np.full((2, 28, 28, 1), 0.5, dtype=np.float32)
        first = add_gaussian_noise(images, std=0.2, seed=8239)
        second = add_gaussian_noise(images, std=0.2, seed=8239)
        self.assertTrue(np.array_equal(first, second))
        self.assertTrue(0.0 <= first.min() <= first.max() <= 1.0)

    def test_rotation_preserves_contract(self) -> None:
        images = np.zeros((2, 28, 28, 1), dtype=np.float32)
        rotated = rotate_images(images, degrees=15)
        self.assertEqual(rotated.shape, images.shape)
        self.assertEqual(rotated.dtype, np.float32)
