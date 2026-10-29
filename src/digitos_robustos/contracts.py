from __future__ import annotations

import numpy as np


def validate_images(images: np.ndarray) -> None:
    """Valida el contrato de imágenes MNIST normalizadas."""
    if not isinstance(images, np.ndarray):
        raise TypeError("images debe ser un numpy.ndarray")
    if images.ndim not in (3, 4):
        raise ValueError("images debe tener forma (n, 28, 28) o (n, 28, 28, 1)")
    if images.shape[1:3] != (28, 28):
        raise ValueError("cada imagen debe medir 28x28")
    if images.ndim == 4 and images.shape[3] != 1:
        raise ValueError("el canal debe ser único")
    if not np.issubdtype(images.dtype, np.floating):
        raise TypeError("images debe usar un tipo flotante")
    if not np.isfinite(images).all():
        raise ValueError("images no puede contener NaN o infinitos")
    if images.min() < 0.0 or images.max() > 1.0:
        raise ValueError("images debe estar normalizado en [0, 1]")


def validate_labels(labels: np.ndarray, expected_size: int | None = None) -> None:
    """Valida etiquetas enteras de las diez clases MNIST."""
    if not isinstance(labels, np.ndarray):
        raise TypeError("labels debe ser un numpy.ndarray")
    if labels.ndim != 1:
        raise ValueError("labels debe ser un vector")
    if expected_size is not None and len(labels) != expected_size:
        raise ValueError("labels e images deben tener el mismo número de muestras")
    if not np.issubdtype(labels.dtype, np.integer):
        raise TypeError("labels debe ser entero")
    if len(labels) and (labels.min() < 0 or labels.max() > 9):
        raise ValueError("las etiquetas deben estar entre 0 y 9")
