# Caso 1 — Cauce: clasificación de mensajes con Naive Bayes

Caso práctico del curso de Minería de Datos. Cauce es una fintech/billetera ficticia cuya mesa de entrada deriva automáticamente cada mensaje de un cliente a uno de 5 equipos de atención, pero esa derivación automática falla bastante seguido.

El objetivo es reemplazar (o auditar) esa derivación con un modelo que lea el texto del mensaje y decida a qué equipo mandarlo, usando un **Naive Bayes multinomial programado desde cero** (solo NumPy) como algoritmo principal, y comparando contra **KNN** (`sklearn`, con TF-IDF y distancia coseno).

## Contenido

```
caso1_cauce/
├── caso1_cauce.ipynb         # Notebook guía: un paso de la consigna por celda
├── datos/
│   ├── mensajes_historicos.csv   # ~8.200 mensajes con equipo_final conocido (train/test)
│   └── mensajes_nuevos.csv       # Mensajes nuevos a clasificar, sin equipo_final
├── predicciones_caso1.csv    # Salida esperada: id_mensaje, equipo_predicho, prob_max, prob_fraude, derivacion
├── src/
│   ├── limpieza.py            # Normalización de texto (tildes, montos, números, URLs, emails)
│   ├── naive_bayes.py         # NaiveBayesMultinomial desde cero + utilidades
│   └── derivacion.py          # Regla de derivación automática + indicadores de negocio
├── tests/                     # Pruebas que fijan el comportamiento exacto de src/
└── conftest.py
```

## La consigna de negocio

Cada mensaje de un cliente (chat, WhatsApp, email o formulario web) tiene que terminar en uno de 5 equipos: `transferencias`, `tarjeta`, `cuenta_acceso`, `prestamos_inversiones` o `fraude`. Hoy esa derivación la hace un sistema automático (`equipo_derivado`) que no siempre acierta — el equipo de datos tiene que medir qué tan bien lo hace y proponer un reemplazo basado en el texto del mensaje.

Dos reglas del juego:

- La columna `equipo_derivado` es una **trampa**: es la salida de ese sistema anterior sobre el mismo mensaje, no existe en los mensajes nuevos a clasificar y no puede usarse como variable del modelo (fuga de información). Sí sirve como punto de comparación.
- La regla de derivación final combina dos umbrales de probabilidad: si `P(fraude)` supera un umbral de fraude, el mensaje se deriva a "fraude" aunque no sea la clase más probable (los casos de fraude pesan más); si no, y la probabilidad máxima supera un umbral de confianza, se deriva a la clase más probable; en cualquier otro caso, el mensaje queda para revisión humana.

Naive Bayes se eligió como algoritmo principal porque es barato de evaluar en producción (solo necesita un resumen de tamaño fijo por clase, no guarda los mensajes crudos) y porque sus términos más indicativos por clase sirven para explicar de qué habla cada equipo.

## Cómo trabajar con esto

1. Completar las funciones marcadas en `src/limpieza.py`, `src/naive_bayes.py` y `src/derivacion.py`.
2. Verificar cada módulo con sus pruebas:
   ```sh
   python -m pytest -q
   ```
3. Seguir `caso1_cauce.ipynb` paso a paso: cada celda marcada `# Tu código aquí` usa las funciones de `src/` sobre los datos reales, hasta llegar a `predicciones_caso1.csv` con la clasificación final de los mensajes nuevos.

## Requisitos

Python 3 con `numpy`, `pandas`, `scikit-learn`, `scipy`, `pytest` y Jupyter.
