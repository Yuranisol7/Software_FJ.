
"""
logger.py
=========
Módulo encargado del registro de eventos del sistema Software FJ.

Implementa el patrón Singleton para garantizar una única instancia
del Logger y almacenar información sobre operaciones, advertencias
y errores del sistema.
"""

from datetime import datetime


class Logger:
    """Registra las operaciones y errores del sistema Software FJ."""

    _instancia = None

    def __init__(self):
        """Inicializa el archivo de registros."""

        self.archivo = "sistema_fj_logs.txt"

    @classmethod
    def obtener_instancia(cls):
        """Devuelve una única instancia del Logger."""

        if cls._instancia is None:
            cls._instancia = cls()

        return cls._instancia

    def registrar(self, nivel, mensaje):
        """Guarda un mensaje con fecha y nivel en el archivo."""

        if not isinstance(nivel, str) or not nivel.strip():
            print("No se pudo registrar: el nivel no es válido.")
            return False

        if not isinstance(mensaje, str) or not mensaje.strip():
            print("No se pudo registrar: el mensaje está vacío.")
            return False

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        linea = (
            f"[{fecha}] [{nivel.strip().upper()}] "
            f"{mensaje.strip()}\n"
        )

        try:
            with open(
                self.archivo,
                "a",
                encoding="utf-8"
            ) as archivo:
                archivo.write(linea)

            return True

        except OSError as error:
            print(
                f"No se pudo escribir el registro: {error}"
            )
            return False

    def info(self, mensaje):
        """Registra información general."""

        return self.registrar("INFO", mensaje)

    def error(self, mensaje):
        """Registra errores del sistema."""

        return self.registrar("ERROR", mensaje)

    def warning(self, mensaje):
        """Registra advertencias."""

        return self.registrar("WARNING", mensaje)

    def evento(self, mensaje):
        """Registra eventos importantes."""

        return self.registrar("EVENTO", mensaje)
