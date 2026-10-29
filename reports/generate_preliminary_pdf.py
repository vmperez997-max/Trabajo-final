from __future__ import annotations

import json
from io import BytesIO
from html import escape
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "resultados_preliminares.pdf"
METRICS = ROOT / "output" / "results" / "metrics.json"
GITHUB = "https://github.com/vmperez997-max/Trabajo-final"
REFERENCE_IMAGE = Path(r"C:\Users\Victor\AppData\Roaming\Code\agentSessionData\e7f9c257-a535-4d79-bf33-4e8aa689e087\attachments\6a36ac75-ff6e-4dd4-ab41-a7f83a0071e2\Pasted Image.png")

NAVY = colors.HexColor("#163A5F")
BLUE = colors.HexColor("#2F6690")
LIGHT_BLUE = colors.HexColor("#EAF2F8")
GRAY = colors.HexColor("#5B6573")


def footer(canvas, document) -> None:
    canvas.saveState()
    if document.page > 1:
        canvas.setStrokeColor(colors.HexColor("#D6DEE5"))
        canvas.line(document.leftMargin, 0.58 * inch, letter[0] - document.rightMargin, 0.58 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GRAY)
        canvas.drawString(document.leftMargin, 0.38 * inch, "INF-8239 | Dígitos manuscritos robustos")
        canvas.drawRightString(letter[0] - document.rightMargin, 0.38 * inch, f"Página {document.page}")
    canvas.restoreState()


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def reference_logo() -> RLImage | Spacer:
    """Recorta el logotipo de la imagen proporcionada como referencia visual."""
    if not REFERENCE_IMAGE.exists():
        return Spacer(1, 0.8 * inch)
    with PILImage.open(REFERENCE_IMAGE) as source:
        logo = source.crop((135, 20, 270, 165))
        buffer = BytesIO()
        logo.save(buffer, format="PNG")
    buffer.seek(0)
    return RLImage(buffer, width=1.22 * inch, height=1.31 * inch)


def build_pdf() -> Path:
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    baseline = metrics["models"]["baseline_centroid"]
    cnn = metrics["models"]["cnn_small"]
    meta = metrics["metadata"]

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=31, textColor=colors.white, alignment=TA_CENTER, spaceAfter=18))
    styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=13, leading=18, textColor=colors.white, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="CoverBlack", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=15, textColor=colors.black, alignment=TA_CENTER, spaceAfter=2))
    styles.add(ParagraphStyle(name="CoverSmallBlack", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=10, textColor=colors.black, alignment=TA_CENTER, spaceAfter=1))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=8, spaceAfter=9))
    styles.add(ParagraphStyle(name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=BLUE, spaceBefore=7, spaceAfter=5))
    styles.add(ParagraphStyle(name="BodyJust", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, alignment=TA_JUSTIFY, spaceAfter=7))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11, textColor=GRAY))
    styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=10, leading=14, textColor=NAVY, backColor=LIGHT_BLUE, borderColor=colors.HexColor("#B7D1E5"), borderWidth=0.5, borderPadding=9, spaceBefore=5, spaceAfter=10))

    document = SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=0.72 * inch, leftMargin=0.72 * inch, topMargin=0.72 * inch, bottomMargin=0.78 * inch)
    story = []

    # Portada centrada inspirada en la presentación visual de la referencia.
    story.extend([
        Spacer(1, 0.18 * inch),
        reference_logo(),
        Spacer(1, 0.08 * inch),
        p("Universidad Autónoma de Santo Domingo", styles["CoverBlack"]),
        p("UASD", styles["CoverBlack"]),
        p("Facultad de Ciencias - Escuela de Informática", styles["CoverSmallBlack"]),
        p("División de Postgrado y Educación Permanente", styles["CoverSmallBlack"]),
        Spacer(1, 0.18 * inch),
        p("INF-8239 Ciencia de Datos II", styles["CoverBlack"]),
        p("Trabajo final - Modalidad A", styles["CoverBlack"]),
        Spacer(1, 0.18 * inch),
        p("Dígitos manuscritos robustos", styles["CoverBlack"]),
        p("Visión por computadora", styles["CoverSmallBlack"]),
        Spacer(1, 0.2 * inch),
        p("Presentado por:", styles["CoverSmallBlack"]),
        p("Victor Manuel Perez Padilla", styles["CoverSmallBlack"]),
        p("Matrícula: 100801946", styles["CoverSmallBlack"]),
        Spacer(1, 0.15 * inch),
        p("Tema: TF.19", styles["CoverSmallBlack"]),
        p("Santo Domingo, República Dominicana", styles["CoverSmallBlack"]),
        p("Octubre de 2026", styles["CoverSmallBlack"]),
        PageBreak(),
    ])

    story.extend([
        p("Resumen", styles["Section"]),
        p("Este proyecto compara un baseline de centroides con una CNN pequeña para clasificar dígitos manuscritos de MNIST y estudiar el efecto de ruido gaussiano, rotación y su combinación. La CNN obtuvo 98.17% de accuracy en imágenes limpias y 94.84% bajo la combinación de perturbaciones, frente a 82.03% y 71.55% del baseline, respectivamente. La conclusión accionable es usar la CNN dentro del dominio evaluado, manteniendo la advertencia de que MNIST no representa por sí solo documentos manuscritos reales.", styles["BodyJust"]),
        p("Contenido del informe", styles["Section"]),
        Table([["1. Introducción y problema", "3"], ["2. Objetivos", "3"], ["3. Datos y preparación", "4"], ["4. Metodología e implementación", "4"], ["5. Resultados", "5"], ["6. Limitaciones y uso responsable", "6"], ["7. Conclusiones", "6"]], colWidths=[5.8 * inch, 0.6 * inch], style=TableStyle([("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D2DC")), ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE), ("ALIGN", (1, 0), (1, -1), "RIGHT"), ("FONTNAME", (0, 0), (-1, -1), "Helvetica"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")])])),
        Spacer(1, 12),
        p("Palabras clave: visión por computadora, MNIST, CNN, robustez, ruido, rotación, reproducibilidad.", styles["Small"]),
        PageBreak(),
    ])

    story.extend([
        p("1. Introducción y problema", styles["Section"]),
        p("La clasificación de dígitos manuscritos es un problema controlado de visión por computadora que permite estudiar la relación entre representación visual, capacidad predictiva y robustez. El riesgo metodológico central de este trabajo es confundir un buen resultado en imágenes limpias con un modelo resistente a cambios de captura.", styles["BodyJust"]),
        p("La pregunta de investigación es: ¿hasta qué punto una CNN pequeña mejora a un baseline al clasificar dígitos manuscritos con ruido gaussiano, rotación o ambas perturbaciones, manteniendo una latencia adecuada para una demostración local?", styles["Callout"]),
        p("2. Objetivos", styles["Section"]),
        p("Objetivo general", styles["Subsection"]),
        p("Comparar un baseline reproducible con una CNN pequeña para determinar cuál ofrece mejor equilibrio entre accuracy, robustez y latencia en MNIST.", styles["BodyJust"]),
        p("Objetivos específicos", styles["Subsection"]),
        p("1. Definir un contrato de entrada para imágenes 28x28 en escala de grises. 2. Entrenar y evaluar ambos modelos con una semilla registrada. 3. Medir el desempeño en imágenes limpias, con ruido, con rotación y con ambas perturbaciones. 4. Documentar limitaciones, pruebas y una conclusión accionable.", styles["BodyJust"]),
        p("3. Datos y preparación", styles["Section"]),
        p("Se utilizó MNIST, descargado mediante el mecanismo de Keras y conservado localmente en una caché excluida del repositorio. La partición oficial contiene 60,000 imágenes de entrenamiento y 10,000 de prueba. Las imágenes se convierten a flotantes, se normalizan al rango [0, 1] y se representan con un canal explícito.", styles["BodyJust"]),
        p("Las perturbaciones se aplican únicamente al conjunto de prueba ya separado: ruido gaussiano con desviación estándar 0.20, rotación de 15 grados y la composición de ambos escenarios. Esto evita mezclar artificialmente escenarios de evaluación con el entrenamiento.", styles["BodyJust"]),
        PageBreak(),
    ])

    story.extend([
        p("4. Metodología e implementación", styles["Section"]),
        p("El baseline calcula un centroide por clase a partir de los píxeles aplanados y asigna cada imagen a la clase con menor distancia media cuadrática. La CNN utiliza dos capas convolucionales pequeñas, pooling, una capa densa y una salida softmax de diez clases. Se entrenó con Adam, batch de 128 y dos épocas.", styles["BodyJust"]),
        p("La semilla experimental fue 8239. El flujo se ejecuta desde scripts/run_experiment.py, registra la versión de Python, plataforma, TensorFlow, tamaño de las particiones, métricas y latencia en output/results/metrics.json. El repositorio reproducible se encuentra en GitHub.", styles["BodyJust"]),
        p("5. Resultados", styles["Section"]),
        p(f"La ejecución se realizó con Python {escape(meta['python'].split()[0])}, TensorFlow {escape(meta['tensorflow'])}, {meta['train_samples']:,} muestras de entrenamiento y {meta['test_samples']:,} muestras de prueba.", styles["BodyJust"]),
    ])
    result_rows = [["Modelo", "Limpio", "Ruido", "Rotación", "Ruido + rotación", "ms/muestra"], ["Baseline centroides", f"{baseline['clean']:.2%}", f"{baseline['gaussian_noise']:.2%}", f"{baseline['rotation']:.2%}", f"{baseline['noise_and_rotation']:.2%}", f"{baseline['latency_ms_per_sample']:.3f}"], ["CNN pequeña", f"{cnn['clean']:.2%}", f"{cnn['gaussian_noise']:.2%}", f"{cnn['rotation']:.2%}", f"{cnn['noise_and_rotation']:.2%}", f"{cnn['latency_ms_per_sample']:.3f}"]]
    story.extend([
        Table(result_rows, colWidths=[1.35 * inch, 0.72 * inch, 0.72 * inch, 0.72 * inch, 1.05 * inch, 0.85 * inch], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B9C7D3")), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]), ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8)])),
        Spacer(1, 10),
        p("La CNN mejora 15.14 puntos porcentuales sobre el baseline en limpio y 23.29 puntos en la combinación de ruido y rotación. Su caída desde limpio es de 3.33 puntos, mientras que la del baseline es de 10.48 puntos. Esto aporta evidencia a favor de la CNN dentro de los escenarios evaluados, sin justificar generalización fuera de ellos.", styles["Callout"]),
        p("6. Pruebas y reproducibilidad", styles["Section"]),
        p("La suite automatizada contiene seis pruebas aprobadas: contrato de imágenes y etiquetas, rechazo de formas incorrectas, reproducibilidad y rango del ruido, preservación de forma en rotación, reporte de escenarios y medición de latencia. El enlace del repositorio es:", styles["BodyJust"]),
        p(escape(GITHUB), styles["Small"]),
        PageBreak(),
    ])

    story.extend([
        p("7. Análisis de errores y robustez", styles["Section"]),
        p("El escenario más exigente fue la combinación de ruido y rotación. La CNN alcanzó 94.84%, mientras que el baseline cayó a 71.55%. La diferencia indica que la CNN aprende representaciones espaciales más estables para las perturbaciones controladas. Sin embargo, accuracy agregada no muestra qué clases específicas concentran los errores; por eso se recomienda incorporar una matriz de confusión y revisión visual por clase en una iteración posterior.", styles["BodyJust"]),
        p("8. Limitaciones y uso responsable", styles["Section"]),
        p("MNIST no representa toda la variabilidad de escritura manuscrita, perspectiva, iluminación, compresión, tinta, papel o resolución de documentos reales. El ruido gaussiano y la rotación son aproximaciones controladas. La latencia observada depende del CPU y no debe interpretarse como garantía para otro equipo.", styles["BodyJust"]),
        p("El modelo debe abstenerse de conclusiones fuera del contrato de entrada y no debe utilizarse como OCR documental general sin validación externa. La Model Card y la declaración de uso de IA acompañan el repositorio.", styles["BodyJust"]),
        p("9. Green AI y trazabilidad", styles["Section"]),
        p("Se utilizó una CNN pequeña, dos épocas y ejecución en CPU, limitando el costo computacional del experimento. La configuración, semilla, dependencias, métricas y código quedan registrados para facilitar repetición y auditoría.", styles["BodyJust"]),
        p("10. Conclusiones", styles["Section"]),
        p("Para el alcance individual de este proyecto, la CNN pequeña es el modelo recomendado: obtuvo mayor accuracy en limpio, menor degradación relativa bajo las perturbaciones evaluadas y una latencia local inferior a 1 ms por muestra. La recomendación se detiene o debe escalarse cuando la imagen no cumpla el contrato, cuando se use un dominio distinto de MNIST o cuando se necesite evidencia de desempeño por clase en datos externos.", styles["Callout"]),
        p("Referencias", styles["Section"]),
        p("Yann LeCun, Corinna Cortes y Christopher Burges. MNIST handwritten digit database. http://yann.lecun.com/exdb/mnist/", styles["Small"]),
        p("TensorFlow Keras. MNIST dataset API. https://www.tensorflow.org/api_docs/python/tf/keras/datasets/mnist", styles["Small"]),
        p("Repositorio del proyecto. " + escape(GITHUB), styles["Small"]),
    ])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    return OUTPUT


if __name__ == "__main__":
    print(build_pdf())
