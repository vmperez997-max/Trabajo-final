import unittest

import numpy as np

from digitos_robustos.evaluation import measure_latency, robustness_report


class FixedModel:
    def predict(self, images: np.ndarray) -> np.ndarray:
        return np.zeros(len(images), dtype=np.int64)


class EvaluationTests(unittest.TestCase):
    def test_robustness_report_keeps_named_scenarios(self) -> None:
        images = np.zeros((3, 28, 28), dtype=np.float32)
        labels = np.zeros(3, dtype=np.int64)
        report = robustness_report(FixedModel(), images, labels, {"noise": images})
        self.assertEqual(report, {"clean": 1.0, "noise": 1.0})

    def test_latency_is_positive(self) -> None:
        images = np.zeros((2, 28, 28), dtype=np.float32)
        latency = measure_latency(FixedModel().predict, images)
        self.assertGreaterEqual(latency, 0.0)
