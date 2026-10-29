from __future__ import annotations

import os
from pathlib import Path
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
    cache_dir = Path(__file__).resolve().parents[2] / "data" / "keras"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("KERAS_HOME", str(cache_dir))
    local_archive = cache_dir / "datasets" / "mnist.npz"
    if local_archive.exists():
        with np.load(local_archive) as archive:
            x_train, y_train = archive["x_train"], archive["y_train"]
            x_test, y_test = archive["x_test"], archive["y_test"]
        return (
            _prepare_images(x_train),
            np.asarray(y_train, dtype=np.int64),
            _prepare_images(x_test),
            np.asarray(y_test, dtype=np.int64),
        )
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
