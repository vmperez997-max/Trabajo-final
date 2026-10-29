from __future__ import annotations

from typing import Any

import numpy as np


class Baseline:
    """Baseline de centroides por clase sobre los píxeles aplanados."""

    def __init__(self, seed: int = 8239) -> None:
        self._seed = seed
        self._centroids: dict[int, np.ndarray] = {}

    def fit(self, images: np.ndarray, labels: np.ndarray) -> "Baseline":
        flattened = images.reshape(len(images), -1)
        self._centroids = {
            int(label): flattened[labels == label].mean(axis=0)
            for label in np.unique(labels)
        }
        return self

    def predict(self, images: np.ndarray) -> np.ndarray:
        if not self._centroids:
            raise RuntimeError("el baseline debe entrenarse antes de predecir")
        flattened = images.reshape(len(images), -1)
        classes = np.array(sorted(self._centroids), dtype=np.int64)
        centroids = np.stack([self._centroids[int(label)] for label in classes])
        distances = ((flattened[:, None, :] - centroids[None, :, :]) ** 2).mean(axis=2)
        return classes[np.argmin(distances, axis=1)]


def build_small_cnn(seed: int = 8239) -> Any:
    """Construye la CNN candidata; TensorFlow se importa solo al solicitarla."""
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise RuntimeError(
            "La CNN requiere el extra opcional 'cnn' y una versión compatible de TensorFlow."
        ) from exc
    tf.keras.utils.set_random_seed(seed)
    return tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(28, 28, 1)),
            tf.keras.layers.Conv2D(16, 3, activation="relu"),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, activation="relu"),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax"),
        ],
        name="cnn_pequena",
    )
