
from datetime import datetime


class Logger:
    """Registra las operaciones y errores del sistema Software FJ."""

    _instancia = None

    def __init__(self):
        self.archivo = "sistema_fj_logs.txt"

    @classmethod
    def obtener_instancia(cls):
        """Devuelve una única instancia del Logger."""
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def registrar(self, nivel, mensaje):
        """Guarda un mensaje en el archivo de registros."""
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{fecha}] [{nivel}] {mensaje}\n"

        try:
            with open(self.archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as error:
            print(f"No se pudo escribir el registro: {error}")

    def info(self, mensaje):
        self.registrar("INFO", mensaje)

    def error(self, mensaje):
        self.registrar("ERROR", mensaje)

    def warning(self, mensaje):
        self.registrar("WARNING", mensaje)

    def evento(self, mensaje):
        self.registrar("EVENTO", mensaje)
