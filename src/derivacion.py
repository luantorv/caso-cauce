"""Regla de derivación de mensajes y sus indicadores de negocio.

Completá las dos funciones. Solo NumPy. Verificá tu trabajo con:  python -m pytest -q tests/test_derivacion.py
"""
import numpy as np

REVISION = "revision_humana"


def derivar(proba, clases, umbral_fraude, umbral_confianza):
    """Decide el destino de cada mensaje a partir de las probabilidades del modelo.

    proba : array (n_mensajes, n_clases) con P(clase | mensaje); columnas en el orden de `clases`.
    clases : lista o array con los nombres de las clases (incluye "fraude").

    Regla, en este orden de prioridad:
    1. Si P(fraude) >= umbral_fraude, el destino es "fraude" (aunque no sea la clase más probable).
    2. Si no, y la probabilidad máxima >= umbral_confianza, el destino es la clase más probable.
    3. En cualquier otro caso, el destino es REVISION ("revision_humana").

    Devuelve un array de n_mensajes strings.
    """
    proba = np.asarray(proba)
    clases_lista = list(clases)
    clases_arr = np.asarray(clases_lista)
    idx_fraude = clases_lista.index("fraude")

    idx_max = np.argmax(proba, axis=1)
    prob_max = proba[np.arange(len(proba)), idx_max]
    prob_fraude = proba[:, idx_fraude]

    destino = np.full(len(proba), REVISION, dtype=object)
    confiable = prob_max >= umbral_confianza
    destino[confiable] = clases_arr[idx_max[confiable]]
    destino[prob_fraude >= umbral_fraude] = "fraude"
    return destino


def evaluar_derivacion(y_real, destino):
    """Calcula los indicadores del negocio. Devuelve un dict con tres claves:

    - "cobertura": proporción de mensajes derivados automáticamente (destino distinto de REVISION).
    - "exactitud_automatica": entre los derivados automáticamente, proporción con destino == y_real.
    - "fraude_perdido": entre los mensajes cuyo y_real es "fraude", proporción derivada automáticamente
      a un equipo que no es "fraude". Los enviados a revisión humana no cuentan como perdidos.

    Los tres valores son proporciones entre 0 y 1 (float).
    """
    y_real = np.asarray(y_real)
    destino = np.asarray(destino)

    automatico = destino != REVISION
    cobertura = automatico.mean()
    exactitud_automatica = (destino[automatico] == y_real[automatico]).mean()

    es_fraude_real = y_real == "fraude"
    perdido = automatico & (destino != "fraude")
    fraude_perdido = perdido[es_fraude_real].mean()

    return {
        "cobertura": float(cobertura),
        "exactitud_automatica": float(exactitud_automatica),
        "fraude_perdido": float(fraude_perdido),
    }
