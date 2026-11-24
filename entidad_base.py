
"""
entidad_base.py
===============
Define la clase abstracta EntidadBase, que sirve como
estructura general para las entidades del sistema Software FJ.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """Clase abstracta base para las entidades del sistema."""

    _contador_global = 0

    def __init__(self, nombre):
        """Inicializa los atributos comunes de una entidad."""

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                "El nombre debe ser un texto válido y no puede estar vacío."
            )

        EntidadBase._contador_global += 1

        self._id = EntidadBase._contador_global
        self._nombre = nombre.strip()
        self._fecha_creacion = datetime.now()
        self._activo = True

    @property
    def id(self):
        """Retorna el identificador único de la entidad."""
        return self._id

    @property
    def nombre(self):
        """Retorna el nombre de la entidad."""
        return self._nombre

    @property
    def fecha_creacion(self):
        """Retorna la fecha de creación."""
        return self._fecha_creacion

    @property
    def activo(self):
        """Indica si la entidad está activa."""
        return self._activo

    def activar(self):
        """Activa la entidad."""
        self._activo = True

    def desactivar(self):
        """Desactiva la entidad."""
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
        """Representación legible de la entidad."""
        return f"ID: {self._id} | Nombre: {self._nombre}"

    def __repr__(self):
        """Representación técnica de la entidad."""
        return (
            f"{self.__class__.__name__}"
            f"(id={self._id}, nombre='{self._nombre}')"
        )
