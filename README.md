# Dígitos manuscritos robustos

Proyecto final individual de INF-8239 Ciencia de Datos II, modalidad A.

## Pregunta

¿Hasta qué punto una CNN pequeña mejora a un baseline para clasificar dígitos manuscritos cuando las imágenes contienen ruido gaussiano, rotación o ambas perturbaciones, manteniendo una latencia adecuada para una demostración local?

## Alcance

- Dataset inicial: MNIST, sujeto a verificación de versión, licencia, cobertura y limitaciones.
- Modelos: un baseline reproducible y una CNN pequeña.
- Evaluación: accuracy en datos limpios, robustez ante perturbaciones y latencia de inferencia.
- Pruebas: seis pruebas automatizadas de contrato, reproducibilidad y comportamiento.
- Producto: código ejecutable, resultados trazables, informe técnico y demostración.

Los PDF ubicados en la carpeta raíz son únicamente material de referencia metodológica. No forman parte de los datos, código, resultados ni fuentes del experimento.

## Estructura

```text
digitos_manuscritos_robustos/
├── README.md
├── pyproject.toml
├── configs/default.toml
├── docs/decisiones.md
├── src/digitos_robustos/
├── tests/
└── scripts/
```

## Preparación

```powershell
python -m pip install -e .
```

La CNN requiere instalar el extra compatible con el entorno disponible:

```powershell
python -m pip install -e ".[cnn]"
```

## Validación

```powershell
python -m unittest discover -s tests -v
```

## Reproducibilidad

Toda ejecución debe registrar semilla, versión de Python, versiones de dependencias, configuración, partición de datos, métricas y latencia. No se deben mezclar imágenes perturbadas entre entrenamiento y prueba sin documentarlo explícitamente.
