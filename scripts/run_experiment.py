from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import numpy as np

from digitos_robustos.data import load_mnist
from digitos_robustos.evaluation import measure_latency
from digitos_robustos.models import Baseline, build_small_cnn
from digitos_robustos.perturbations import add_gaussian_noise, rotate_images


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "output" / "results"


def keras_accuracy(model: object, images: np.ndarray, labels: np.ndarray) -> float:
    probabilities = model.predict(images, verbose=0)
    return float(np.mean(np.argmax(probabilities, axis=1) == labels))


def evaluate_scenarios(model: object, scenarios: dict[str, np.ndarray], labels: np.ndarray) -> dict[str, float]:
    return {name: keras_accuracy(model, images, labels) for name, images in scenarios.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena y evalúa baseline y CNN sobre MNIST.")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--train-limit", type=int, default=0)
    parser.add_argument("--test-limit", type=int, default=0)
    parser.add_argument("--seed", type=int, default=8239)
    args = parser.parse_args()
    if args.epochs < 1:
        raise ValueError("--epochs debe ser positivo")

    np.random.seed(args.seed)
    x_train, y_train, x_test, y_test = load_mnist()
    if args.train_limit:
        x_train, y_train = x_train[: args.train_limit], y_train[: args.train_limit]
    if args.test_limit:
        x_test, y_test = x_test[: args.test_limit], y_test[: args.test_limit]

    scenarios = {
        "clean": x_test,
        "gaussian_noise": add_gaussian_noise(x_test, std=0.20, seed=args.seed),
        "rotation": rotate_images(x_test, degrees=15.0),
    }
    scenarios["noise_and_rotation"] = rotate_images(scenarios["gaussian_noise"], degrees=15.0)

    baseline = Baseline(seed=args.seed).fit(x_train, y_train)
    baseline_start = perf_counter()
    baseline_predictions = baseline.predict(x_test)
    baseline_latency = (perf_counter() - baseline_start) * 1000.0 / len(x_test)
    baseline_metrics = {
        name: float(np.mean(baseline_predictions == y_test))
        if name == "clean"
        else float(np.mean(baseline.predict(images) == y_test))
        for name, images in scenarios.items()
    }
    baseline_metrics["latency_ms_per_sample"] = float(baseline_latency)

    cnn = build_small_cnn(seed=args.seed)
    cnn.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    history = cnn.fit(
        x_train,
        y_train,
        epochs=args.epochs,
        batch_size=128,
        validation_split=0.1,
        verbose=2,
    )
    cnn_metrics = evaluate_scenarios(cnn, scenarios, y_test)
    cnn_metrics["latency_ms_per_sample"] = measure_latency(
        lambda batch: cnn.predict(batch, verbose=0), x_test[: min(128, len(x_test))]
    )

    RESULTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "python": sys.version,
            "platform": platform.platform(),
            "seed": args.seed,
            "epochs": args.epochs,
            "train_samples": len(x_train),
            "test_samples": len(x_test),
            "tensorflow": __import__("tensorflow").__version__,
        },
        "models": {"baseline_centroid": baseline_metrics, "cnn_small": cnn_metrics},
        "cnn_history": {key: [float(value) for value in values] for key, values in history.history.items()},
        "robustness_drop_from_clean": {
            "baseline_centroid": {
                name: baseline_metrics["clean"] - baseline_metrics[name]
                for name in scenarios
                if name != "clean"
            },
            "cnn_small": {
                name: cnn_metrics["clean"] - cnn_metrics[name]
                for name in scenarios
                if name != "clean"
            },
        },
        "demo_sample": {
            "index": 0,
            "true_label": int(y_test[0]),
            "cnn_prediction": int(np.argmax(cnn.predict(x_test[:1], verbose=0)[0])),
        },
    }
    output = RESULTS / "metrics.json"
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
