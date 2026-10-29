from __future__ import annotations

import numpy as np
from PIL import Image

from .contracts import validate_images


def add_gaussian_noise(images: np.ndarray, std: float, seed: int) -> np.ndarray:
    """Añade ruido gaussiano acotado y conserva el contrato de imágenes."""
    validate_images(images)
    if std < 0:
        raise ValueError("std debe ser no negativo")
    rng = np.random.default_rng(seed)
    noisy = images + rng.normal(0.0, std, size=images.shape)
    return np.clip(noisy, 0.0, 1.0).astype(np.float32)


def rotate_images(images: np.ndarray, degrees: float) -> np.ndarray:
    """Rota imágenes sin cambiar su tamaño ni su rango."""
    validate_images(images)
    rotated = []
    for image in images:
        array = image[..., 0] if image.ndim == 3 and image.shape[-1] == 1 else image
        pil_image = Image.fromarray(np.rint(array * 255).astype(np.uint8))
        transformed = pil_image.rotate(degrees, resample=Image.Resampling.BILINEAR)
        rotated.append(np.asarray(transformed, dtype=np.float32) / 255.0)
    return np.stack(rotated)[..., np.newaxis]
