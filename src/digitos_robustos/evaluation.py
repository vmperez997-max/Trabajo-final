from __future__ import annotations

from time import perf_counter
from typing import Any, Callable

import numpy as np


def accuracy(model: Any, images: np.ndarray, labels: np.ndarray) -> float:
    predictions = model.predict(images)
    return float(np.mean(np.asarray(labels) == np.asarray(predictions)))


def measure_latency(
    predictor: Callable[[np.ndarray], Any], images: np.ndarray, repeats: int = 3
) -> float:
    """Devuelve milisegundos por muestra tras varias ejecuciones completas."""
    if repeats < 1 or len(images) == 0:
        raise ValueError("repeats debe ser positivo y debe haber imágenes")
    elapsed = []
    for _ in range(repeats):
        start = perf_counter()
        predictor(images)
        elapsed.append(perf_counter() - start)
    return float(np.median(elapsed) * 1000.0 / len(images))


def robustness_report(
    model: Any, clean_images: np.ndarray, labels: np.ndarray, scenarios: dict[str, np.ndarray]
) -> dict[str, float]:
    """Reporta accuracy limpia y por perturbación, sin mezclar escenarios."""
    clean_score = accuracy(model, clean_images, labels)
    report = {"clean": clean_score}
    report.update({name: accuracy(model, images, labels) for name, images in scenarios.items()})
    return report
