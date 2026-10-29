from pathlib import Path
import json

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "resultados_preliminares.pdf"
METRICS = ROOT / "output" / "results" / "metrics.json"


def build_pdf() -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    metrics = json.loads(METRICS.read_text(encoding="utf-8")) if METRICS.exists() else None
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=9, leading=12))
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch
    )
    story = [
        Paragraph("Dígitos manuscritos robustos", styles["TitleCenter"]),
        Paragraph("Resultados experimentales - INF-8239 Ciencia de Datos II", styles["Heading2"]),
        Spacer(1, 12),
        Paragraph(
            "Este documento registra los resultados reproducibles del proyecto individual en modalidad A, ejecutado sobre MNIST con 60,000 imágenes de entrenamiento, 10,000 de prueba, semilla 8239 y dos épocas de entrenamiento para la CNN.",
            styles["BodyText"],
        ),
        Spacer(1, 10),
        Paragraph("1. Alcance aprobado", styles["Heading2"]),
        Paragraph(
            "Se implementará un baseline, una CNN pequeña, perturbaciones de ruido gaussiano y rotación, y evaluación mediante accuracy, robustez y latencia. El dataset previsto es MNIST, sujeto a verificación de versión, licencia, cobertura y limitaciones.",
            styles["BodyText"],
        ),
        Spacer(1, 10),
        Paragraph("2. Evidencia de validación actual", styles["Heading2"]),
    ]
    table = Table(
        [
            ["Componente", "Resultado"],
            ["Pruebas automatizadas", "6 de 6 aprobadas"],
            ["Baseline limpio", f"{metrics['models']['baseline_centroid']['clean']:.2%}" if metrics else "Pendiente"],
            ["CNN limpia", f"{metrics['models']['cnn_small']['clean']:.2%}" if metrics else "Pendiente"],
            ["Baseline: ruido + rotación", f"{metrics['models']['baseline_centroid']['noise_and_rotation']:.2%}" if metrics else "Pendiente"],
            ["CNN: ruido + rotación", f"{metrics['models']['cnn_small']['noise_and_rotation']:.2%}" if metrics else "Pendiente"],
            ["Latencia baseline / CNN", f"{metrics['models']['baseline_centroid']['latency_ms_per_sample']:.3f} / {metrics['models']['cnn_small']['latency_ms_per_sample']:.3f} ms/muestra" if metrics else "Pendiente"],
            ["Repositorio Git", "Publicado en GitHub"],
        ],
        colWidths=[2.2 * inch, 4.4 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#183B56")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4CE")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF4F7")]),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend([table, Spacer(1, 12)])
    story.extend(
        [
            Paragraph("3. Interpretación", styles["Heading2"]),
            Paragraph(
                "La CNN supera al baseline en datos limpios (98.17% frente a 82.03%) y conserva mejor desempeño bajo la combinación de perturbaciones (94.84% frente a 71.55%). La caída de la CNN en ese escenario es de 3.33 puntos porcentuales; por tanto, dentro de las perturbaciones evaluadas, la CNN es la opción recomendada. Esta conclusión no se extiende a otros tipos de ruido, resoluciones o dominios documentales.",
                styles["BodyText"],
            ),
            Spacer(1, 10),
            Paragraph("4. Limitaciones y siguiente mejora", styles["Heading2"]),
            Paragraph(
                "MNIST no representa toda la variabilidad de escritura manuscrita real. Las perturbaciones son controladas y la latencia depende del hardware. La siguiente mejora debe incorporar análisis de errores por clase y una validación con imágenes externas antes de usar el modelo fuera de este experimento.",
                styles["BodyText"],
            ),
            Spacer(1, 18),
            Paragraph(
                "Repositorio GitHub: https://github.com/vmperez997-max/Trabajo-final",
                styles["Small"],
            ),
            Spacer(1, 8),
            Paragraph(
                "Generado automáticamente desde la base reproducible del proyecto.",
                styles["Small"],
            ),
        ]
    )
    document.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(build_pdf())
