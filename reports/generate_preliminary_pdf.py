from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "resultados_preliminares.pdf"


def build_pdf() -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=9, leading=12))
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch
    )
    story = [
        Paragraph("Dígitos manuscritos robustos", styles["TitleCenter"]),
        Paragraph("Resultados preliminares - INF-8239 Ciencia de Datos II", styles["Heading2"]),
        Spacer(1, 12),
        Paragraph(
            "Este documento registra el estado verificable de la base reproducible del proyecto individual en modalidad A. No contiene métricas de entrenamiento de MNIST ni de la CNN, porque esas ejecuciones aún no se han realizado.",
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
            ["Diagnóstico del editor", "Sin errores reportados"],
            ["Contrato de imágenes", "28x28, flotantes, rango [0, 1]"],
            ["Perturbaciones", "Ruido reproducible y rotación con forma preservada"],
            ["Repositorio Git", "Pendiente de inicialización/publicación"],
            ["CNN y MNIST", "Pendientes de ejecución por compatibilidad de TensorFlow"],
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
                "La evidencia actual demuestra que el contrato de entrada, las transformaciones controladas, la medición de latencia y la suite de seis pruebas funcionan en el entorno seleccionado. No permite concluir todavía qué modelo clasifica mejor ni qué tan robusto es frente a ruido o rotación.",
                styles["BodyText"],
            ),
            Spacer(1, 10),
            Paragraph("4. Próximos resultados requeridos", styles["Heading2"]),
            Paragraph(
                "Cargar MNIST, entrenar el baseline y la CNN con semilla registrada, evaluar el conjunto limpio y tres escenarios perturbados, medir latencia, analizar errores y actualizar este informe con tablas y conclusiones delimitadas.",
                styles["BodyText"],
            ),
            Spacer(1, 18),
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
