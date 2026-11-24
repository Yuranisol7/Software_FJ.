
"""
cliente.py
==========
Módulo que representa y administra los clientes del sistema Software FJ.

Implementa herencia, encapsulamiento, propiedades y validaciones
mediante excepciones personalizadas.
"""

import re

from entidad_base import EntidadBase
from excepciones import ClienteInvalidoException


class Cliente(EntidadBase):
    """Representa un cliente del sistema Software FJ."""

    def __init__(self, nombre, apellido, email, telefono, documento):
        super().__init__(nombre)

        self.__apellido = apellido.strip() if isinstance(apellido, str) else apellido
        self.__email = email.strip().lower() if isinstance(email, str) else email
        self.__telefono = telefono.strip() if isinstance(telefono, str) else telefono
        self.__documento = documento.strip() if isinstance(documento, str) else documento
        self.__reservas = []

        self.validar()

    @property
    def apellido(self):
        """Devuelve el apellido del cliente."""
        return self.__apellido

    @property
    def email(self):
        """Devuelve el correo electrónico."""
        return self.__email

    @property
    def telefono(self):
        """Devuelve el teléfono del cliente."""
        return self.__telefono

    @property
    def documento(self):
        """Devuelve el documento del cliente."""
        return self.__documento

    @property
    def nombre_completo(self):
        """Devuelve el nombre completo del cliente."""
        return f"{self.nombre} {self.__apellido}"

    @property
    def reservas(self):
        """Devuelve una copia de las reservas del cliente."""
        return self.__reservas.copy()

    def validar(self):
        """Comprueba que los datos del cliente sean correctos."""

        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ClienteInvalidoException(
                "El nombre es obligatorio."
            )

        if not isinstance(self.__apellido, str) or not self.__apellido:
            raise ClienteInvalidoException(
                "El apellido es obligatorio."
            )

        if not isinstance(self.__email, str):
            raise ClienteInvalidoException(
                "El correo electrónico debe ser texto."
            )

        patron_email = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.fullmatch(patron_email, self.__email):
            raise ClienteInvalidoException(
                "El correo electrónico no es válido."
            )

        if not isinstance(self.__telefono, str):
            raise ClienteInvalidoException(
                "El teléfono debe ser texto."
            )

        telefono_limpio = re.sub(
            r"[\s+\-]", "", self.__telefono
        )

        if (
            not telefono_limpio.isdigit()
            or not 7 <= len(telefono_limpio) <= 15
        ):
            raise ClienteInvalidoException(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        if not isinstance(self.__documento, str):
            raise ClienteInvalidoException(
                "El documento debe ser texto."
            )

        if (
            len(self.__documento) < 6
            or not re.fullmatch(r"[A-Za-z0-9-]+", self.__documento)
        ):
            raise ClienteInvalidoException(
                "El documento debe tener al menos 6 caracteres "
                "y contener únicamente letras, números o guiones."
            )

        return True

    def agregar_reserva(self, reserva):
        """Agrega una reserva a la lista del cliente."""

        if reserva is None:
            raise ClienteInvalidoException(
                "No se puede agregar una reserva vacía."
            )

        if reserva in self.__reservas:
            raise ClienteInvalidoException(
                "La reserva ya está registrada para este cliente."
            )

        self.__reservas.append(reserva)

    def describir(self):
        """Devuelve una descripción detallada del cliente."""

        return (
            f"Cliente: {self.nombre_completo} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__email}"
        )

    def __str__(self):
        """Devuelve la información básica del cliente."""

        return (
            f"{self.nombre_completo} | "
            f"Correo: {self.__email} | "
            f"Teléfono: {self.__telefono}"
        )
