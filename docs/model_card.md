# Model Card - CNN pequeña para MNIST

## Uso previsto

Clasificación experimental de dígitos manuscritos de 28x28 píxeles en escala de grises. El modelo sirve para comparar robustez ante ruido gaussiano y rotación dentro del alcance de INF-8239.

## No usos

No debe utilizarse como OCR documental general, en imágenes médicas, para decisiones individuales ni como evidencia de desempeño sobre escrituras o dispositivos no representados por MNIST.

## Datos y entrenamiento

- Dataset: MNIST, 60,000 imágenes de entrenamiento y 10,000 de prueba.
- Semilla: 8239.
- Arquitectura: dos convoluciones pequeñas, pooling, capa densa y salida softmax de 10 clases.
- Entrenamiento: 2 épocas, batch de 128, optimizador Adam.
- Hardware observado: CPU de Windows 11.

## Resultados

| Escenario | Accuracy |
|---|---:|
| Limpio | 98.17% |
| Ruido gaussiano | 96.97% |
| Rotación | 95.95% |
| Ruido + rotación | 94.84% |

Latencia observada: 0.352 ms por muestra en el entorno de ejecución. El baseline de centroides alcanzó 82.03% limpio y 71.55% con ruido + rotación.

## Limitaciones

MNIST no cubre la diversidad de escritura, iluminación, compresión, perspectiva y resolución de documentos reales. Las perturbaciones evaluadas son controladas. La latencia no debe generalizarse a otro hardware.

## Monitoreo recomendado

Antes de cualquier uso fuera del curso, medir accuracy por clase, revisar errores visualmente, evaluar un conjunto externo y abstenerse cuando la entrada no cumpla el contrato 28x28, escala de grises y rango [0, 1].
