
from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """
    Clase abstracta que representa una entidad general
    del sistema Software FJ.
    """

    _contador_global = 0

    def __init__(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        EntidadBase._contador_global += 1

        self._id = EntidadBase._contador_global
        self._nombre = nombre.strip()
        self._fecha_creacion = datetime.now()
        self._activo = True

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @property
    def activo(self):
        return self._activo

    def activar(self):
        self._activo = True

    def desactivar(self):
        self._activo = False

    @abstractmethod
    def validar(self):
        """Valida los datos específicos de la entidad."""
        pass

    @abstractmethod
    def describir(self):
        """Devuelve una descripción de la entidad."""
        pass

    def __str__(self):
        return f"ID: {self._id} | Nombre: {self._nombre}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id}, nombre='{self._nombre}')"
