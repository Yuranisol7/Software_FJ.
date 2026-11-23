
import re
from entidad_base import EntidadBase
from excepciones import ClienteInvalidoException


class Cliente(EntidadBase):
    """Representa un cliente del sistema Software FJ."""

    def __init__(self, nombre, apellido, email, telefono, documento):
        super().__init__(nombre)

        self.__apellido = apellido
        self.__email = email
        self.__telefono = telefono
        self.__documento = documento
        self.__reservas = []

        self.validar()

    @property
    def apellido(self):
        return self.__apellido

    @property
    def email(self):
        return self.__email

    @property
    def telefono(self):
        return self.__telefono

    @property
    def documento(self):
        return self.__documento

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.__apellido}"

    @property
    def reservas(self):
        return self.__reservas.copy()

    def validar(self):
        """Comprueba que los datos del cliente sean correctos."""

        if not isinstance(self.__apellido, str) or not self.__apellido.strip():
            raise ClienteInvalidoException(
                "El apellido es obligatorio."
            )

        if not isinstance(self.__email, str):
            raise ClienteInvalidoException(
                "El correo electrónico debe ser texto."
            )

        patron_email = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.match(patron_email, self.__email.strip()):
            raise ClienteInvalidoException(
                "El correo electrónico no es válido."
            )

        if not isinstance(self.__telefono, str):
            raise ClienteInvalidoException(
                "El teléfono debe ser texto."
            )

        telefono_limpio = re.sub(r"[\s+\-]", "", self.__telefono)

        if not telefono_limpio.isdigit() or not 7 <= len(telefono_limpio) <= 15:
            raise ClienteInvalidoException(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        if not isinstance(self.__documento, str):
            raise ClienteInvalidoException(
                "El documento debe ser texto."
            )

        documento_limpio = self.__documento.strip()

        if len(documento_limpio) < 6:
            raise ClienteInvalidoException(
                "El documento debe tener al menos 6 caracteres."
            )

        return True

    def agregar_reserva(self, reserva):
        """Agrega una reserva a la lista del cliente."""

        if reserva is None:
            raise ClienteInvalidoException(
                "No se puede agregar una reserva vacía."
            )

        self.__reservas.append(reserva)

    def describir(self):
        return (
            f"Cliente: {self.nombre_completo} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__email}"
        )

    def __str__(self):
        return (
            f"{self.nombre_completo} | "
            f"Correo: {self.__email} | "
            f"Teléfono: {self.__telefono}"
        )
