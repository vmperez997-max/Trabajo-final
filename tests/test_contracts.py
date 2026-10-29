import unittest

import numpy as np

from digitos_robustos.contracts import validate_images, validate_labels


class ContractTests(unittest.TestCase):
    def test_valid_image_and_label_contracts(self) -> None:
        validate_images(np.zeros((2, 28, 28), dtype=np.float32))
        validate_labels(np.array([0, 1], dtype=np.int64), expected_size=2)

    def test_rejects_wrong_image_shape(self) -> None:
        with self.assertRaises(ValueError):
            validate_images(np.zeros((2, 32, 32), dtype=np.float32))

