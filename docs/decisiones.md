# Registro inicial de decisiones

## D-001: alcance individual

Se implementa un baseline y una CNN pequeña, con seis pruebas automatizadas y una demostración reproducible. No se incorpora DSS porque el equipo es de una persona y se eligió modalidad A.

## D-002: separación entre limpieza y robustez

Las perturbaciones se generan después de fijar la partición de evaluación. El conjunto limpio se conserva como referencia y cada escenario perturbado se identifica por separado.

## D-003: interpretación de robustez

La robustez se reportará como accuracy por escenario y como caída absoluta respecto a la accuracy limpia. Una mejora en un escenario no autoriza a afirmar robustez general frente a perturbaciones no evaluadas.

## D-004: limitaciones conocidas

MNIST no representa toda la variabilidad de escritura manuscrita real. Ruido gaussiano y rotación son perturbaciones controladas, no una simulación completa de captura documental. La latencia dependerá del hardware.
