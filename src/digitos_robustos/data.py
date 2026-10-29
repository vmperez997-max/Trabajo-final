from __future__ import annotations

from typing import Any

import numpy as np

from .contracts import validate_images, validate_labels


def _prepare_images(images: Any) -> np.ndarray:
    prepared = np.asarray(images, dtype=np.float32) / 255.0
    if prepared.ndim == 3:
        prepared = prepared[..., np.newaxis]
    validate_images(prepared)
    return prepared


def load_mnist() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Carga MNIST desde Keras y devuelve train/test con forma de canal explícita."""
    try:
        from tensorflow.keras.datasets import mnist
    except ImportError as exc:
        raise RuntimeError(
            "MNIST requiere instalar el extra 'cnn' con una versión compatible de TensorFlow."
        ) from exc
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    train_images = _prepare_images(x_train)
    test_images = _prepare_images(x_test)
    train_labels = np.asarray(y_train, dtype=np.int64)
    test_labels = np.asarray(y_test, dtype=np.int64)
    validate_labels(train_labels, expected_size=len(train_images))
    validate_labels(test_labels, expected_size=len(test_images))
    return train_images, train_labels, test_images, test_labels
