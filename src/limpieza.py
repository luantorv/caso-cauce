"""Limpieza de texto para los mensajes de clientes de Cauce.

Completá las dos funciones. Podés usar solo la biblioteca estándar de Python (re, unicodedata).
Verificá tu trabajo con:  python -m pytest -q tests/test_limpieza.py
"""
import re
import unicodedata

_URL_RE = re.compile(r"(?:https?://\S+|www\.\S+)")
_EMAIL_RE = re.compile(r"\S+@\S+\.\S+")
_NUM_CORE = r"\d+(?:[.,]\d+)*"
_MONTO_RE = re.compile(r"(?:\$|\bgs\.?|\busd)\s*" + _NUM_CORE)
_NUM_RE = re.compile(_NUM_CORE)
_NO_PERMITIDO_RE = re.compile(r"[^a-z_\s]")
_ESPACIOS_RE = re.compile(r"\s+")


def quitar_tildes(texto: str) -> str:
    """Devuelve el texto sin tildes ni diéresis: á→a, é→e, ü→u, ñ→n (también en mayúsculas).

    Pista: unicodedata.normalize("NFKD", ...) separa cada letra de su tilde, y
    unicodedata.combining(c) indica si un carácter es una tilde "suelta".
    """
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def limpiar_texto(texto) -> str:
    """Normaliza un mensaje para vectorizarlo. Aplicá estas reglas en este orden:

    1. Si `texto` no es un str (por ejemplo NaN o None), devolver "".
    2. Pasar a minúsculas y quitar tildes.
    3. Reemplazar las URL (empiezan con http://, https:// o www.) por el token _url_.
    4. Reemplazar las direcciones de correo electrónico por _email_.
    5. Reemplazar los montos por _monto_. Un monto es "$", "gs" o "usd" (como palabra
       independiente, con punto opcional: "gs.") seguido, con o sin un espacio, de un número.
    6. Reemplazar los demás números por _num_. Un número puede tener puntos o comas
       internos: 15.000, 8.350,50 y 30.123.456 son un solo número.
    7. Reemplazar por un espacio todo carácter que no sea una letra de la "a" a la "z",
       un guion bajo o un espacio en blanco (así desaparecen signos y emojis).
    8. Dejar un solo espacio entre palabras y quitar los espacios del principio y del final.

    Ejemplos:
        limpiar_texto("¡Me cobraron $ 15.000 y NO los reconozco!")  -> "me cobraron _monto_ y no los reconozco"
        limpiar_texto("mi DNI es 30.123.456 😡")                     -> "mi dni es _num_"
    """
    if not isinstance(texto, str):
        return ""
    texto = quitar_tildes(texto.lower())
    texto = _URL_RE.sub(" _url_ ", texto)
    texto = _EMAIL_RE.sub(" _email_ ", texto)
    texto = _MONTO_RE.sub(" _monto_ ", texto)
    texto = _NUM_RE.sub(" _num_ ", texto)
    texto = _NO_PERMITIDO_RE.sub(" ", texto)
    return _ESPACIOS_RE.sub(" ", texto).strip()
