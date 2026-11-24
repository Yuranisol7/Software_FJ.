
"""
servicios.py
============
Módulo de gestión de servicios del sistema Software FJ.

Implementa clases abstractas, herencia y polimorfismo para
administrar reservas de salas, alquiler de equipos y asesorías.
"""

from abc import ABC, abstractmethod
import math

from entidad_base import EntidadBase

from excepciones import (
    ServicioNoDisponibleException,
    DuracionInvalidaException,
    CapacidadExcedidaException,
    ParametroFaltanteException
)


class Servicio(EntidadBase, ABC):
    """Clase abstracta que representa un servicio."""

    def __init__(self, nombre, precio_base):
        super().__init__(nombre)

        if (
            not isinstance(precio_base, (int, float))
            or isinstance(precio_base, bool)
            or not math.isfinite(precio_base)
            or precio_base <= 0
        ):
            raise ParametroFaltanteException(
                "El precio base debe ser un número mayor que cero."
            )

        self._precio_base = precio_base
        self._disponible = True

    @property
    def precio_base(self):
        """Devuelve el precio base del servicio."""
        return self._precio_base

    @property
    def disponible(self):
        """Indica si el servicio está disponible."""
        return self._disponible

    def marcar_disponible(self):
        """Activa la disponibilidad del servicio."""
        self._disponible = True

    def marcar_no_disponible(self):
        """Desactiva la disponibilidad del servicio."""
        self._disponible = False

    def verificar_disponibilidad(self):
        """Comprueba que el servicio esté disponible."""

        if not self._disponible:
            raise ServicioNoDisponibleException(
                f"El servicio {self.nombre} no está disponible."
            )

        return True

    def validar(self):
        """Comprueba que el precio base sea válido."""
        return self._precio_base > 0

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Valida los parámetros específicos de cada servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        """Calcula el costo según el tipo de servicio."""
        pass

    def calcular_costo_con_impuesto(
        self, duracion, impuesto=0.19, **kwargs
    ):
        """Calcula el costo incluyendo el impuesto."""

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 1
        ):
            raise ParametroFaltanteException(
                "El impuesto debe estar entre 0 y 1."
            )

        costo = self.calcular_costo(duracion, **kwargs)

        return costo * (1 + impuesto)

    def calcular_costo_con_descuento(
        self, duracion, descuento=0.10, **kwargs
    ):
        """Calcula el costo aplicando un descuento."""

        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 1
        ):
            raise ParametroFaltanteException(
                "El descuento debe estar entre 0 y 1."
            )

        costo = self.calcular_costo(duracion, **kwargs)

        return costo * (1 - descuento)

    def calcular_costo_completo(
        self, duracion, impuesto=0.19,
        descuento=0.10, **kwargs
    ):
        """Calcula el costo aplicando descuento e impuesto."""

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 1
        ):
            raise ParametroFaltanteException(
                "El impuesto debe estar entre 0 y 1."
            )

        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 1
        ):
            raise ParametroFaltanteException(
                "El descuento debe estar entre 0 y 1."
            )

        costo = self.calcular_costo(duracion, **kwargs)

        return costo * (1 - descuento) * (1 + impuesto)

    def describir(self):
        """Devuelve la descripción general del servicio."""

        return (
            f"Servicio: {self.nombre} | "
            f"Precio base: ${self._precio_base:,.0f}"
        )


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(
        self, nombre, numero_sala, capacidad=20,
        precio_base=50000
    ):
        super().__init__(nombre, precio_base)

        if (
            not isinstance(numero_sala, str)
            or not numero_sala.strip()
        ):
            raise ParametroFaltanteException(
                "El número de sala es obligatorio."
            )

        if (
            not isinstance(capacidad, int)
            or isinstance(capacidad, bool)
            or capacidad <= 0
        ):
            raise ParametroFaltanteException(
                "La capacidad debe ser un entero positivo."
            )

        self.__numero_sala = numero_sala.strip()
        self.__capacidad = capacidad

    def validar_parametros(self, personas=1, **kwargs):
        """Valida la cantidad de personas de la reserva."""

        if (
            not isinstance(personas, int)
            or isinstance(personas, bool)
            or personas <= 0
        ):
            raise ParametroFaltanteException(
                "La cantidad de personas debe ser un entero positivo."
            )

        if personas > self.__capacidad:
            raise CapacidadExcedidaException(
                "La cantidad de personas supera la capacidad de la sala."
            )

        return True

    def calcular_costo(self, duracion, personas=1, **kwargs):
        """Calcula el costo de reservar una sala."""

        self.validar_parametros(personas=personas)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or not math.isfinite(duracion)
            or not 0 < duracion <= 12
        ):
            raise DuracionInvalidaException(
                "La duración de la sala debe ser de 1 a 12 horas."
            )

        costo = self.precio_base * duracion

        if personas > 10:
            costo *= 1.15

        return costo

    def describir(self):
        """Devuelve la descripción de la sala."""

        return (
            f"{super().describir()} | "
            f"Sala: {self.__numero_sala} | "
            f"Capacidad: {self.__capacidad} personas"
        )


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""

    TIPOS_VALIDOS = [
        "proyector",
        "laptop",
        "impresora",
        "camara",
        "microfono",
        "tablet"
    ]

    def __init__(
        self, nombre, tipo_equipo, cantidad_total,
        precio_base=30000
    ):
        super().__init__(nombre, precio_base)

        if not isinstance(tipo_equipo, str):
            raise ParametroFaltanteException(
                "El tipo de equipo debe ser texto."
            )

        tipo_equipo = tipo_equipo.strip().lower()

        if tipo_equipo not in self.TIPOS_VALIDOS:
            raise ParametroFaltanteException(
                "El tipo de equipo no es válido."
            )

        if (
            not isinstance(cantidad_total, int)
            or isinstance(cantidad_total, bool)
            or cantidad_total <= 0
        ):
            raise ParametroFaltanteException(
                "La cantidad total debe ser un entero positivo."
            )

        self.__tipo_equipo = tipo_equipo
        self.__cantidad_total = cantidad_total
        self.__cantidad_reservada = 0

    @property
    def cantidad_disponible(self):
        """Devuelve la cantidad de equipos disponibles."""

        return self.__cantidad_total - self.__cantidad_reservada

    def validar_parametros(self, cantidad=1, **kwargs):
        """Valida la cantidad de equipos solicitados."""

        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ParametroFaltanteException(
                "La cantidad debe ser un entero positivo."
            )

        if cantidad > self.cantidad_disponible:
            raise CapacidadExcedidaException(
                "No hay suficientes equipos disponibles."
            )

        return True

    def calcular_costo(self, duracion, cantidad=1, **kwargs):
        """Calcula el costo del alquiler de equipos."""

        self.validar_parametros(cantidad=cantidad)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or not math.isfinite(duracion)
            or not 0 < duracion <= 168
        ):
            raise DuracionInvalidaException(
                "La duración del alquiler debe ser de 1 a 168 horas."
            )

        return self.precio_base * duracion * cantidad

    def reservar_unidades(self, cantidad):
        """Registra las unidades de equipos reservadas."""

        self.validar_parametros(cantidad=cantidad)

        self.__cantidad_reservada += cantidad

    def liberar_unidades(self, cantidad):
        """Libera las unidades de equipos reservadas."""

        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ParametroFaltanteException(
                "La cantidad debe ser un entero positivo."
            )

        if cantidad > self.__cantidad_reservada:
            raise CapacidadExcedidaException(
                "No se pueden liberar más equipos de los reservados."
            )

        self.__cantidad_reservada -= cantidad

    def describir(self):
        """Devuelve la descripción del alquiler de equipos."""

        return (
            f"{super().describir()} | "
            f"Tipo: {self.__tipo_equipo} | "
            f"Disponibles: {self.cantidad_disponible}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada."""

    AREAS = {
        "tecnologia": 1.0,
        "finanzas": 1.2,
        "legal": 1.5,
        "marketing": 1.1,
        "rrhh": 1.0
    }

    def __init__(
        self, nombre, area, asesor, precio_base=80000
    ):
        super().__init__(nombre, precio_base)

        if not isinstance(area, str):
            raise ParametroFaltanteException(
                "El área de asesoría debe ser texto."
            )

        area = area.strip().lower()

        if area not in self.AREAS:
            raise ParametroFaltanteException(
                "El área de asesoría no es válida."
            )

        if not isinstance(asesor, str) or not asesor.strip():
            raise ParametroFaltanteException(
                "Debe indicar el nombre del asesor."
            )

        self.__area = area
        self.__asesor = asesor.strip()

    def validar_parametros(self, urgencia=1, **kwargs):
        """Valida el nivel de urgencia de la asesoría."""

        if (
            not isinstance(urgencia, int)
            or isinstance(urgencia, bool)
            or urgencia not in (1, 2, 3)
        ):
            raise ParametroFaltanteException(
                "La urgencia debe ser 1, 2 o 3."
            )

        return True

    def calcular_costo(self, duracion, urgencia=1, **kwargs):
        """Calcula el costo de una asesoría especializada."""

        self.validar_parametros(urgencia=urgencia)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or not math.isfinite(duracion)
            or not 0 < duracion <= 8
        ):
            raise DuracionInvalidaException(
                "La asesoría debe durar de 1 a 8 horas."
            )

        multiplicador = {
            1: 1.0,
            2: 1.3,
            3: 1.6
        }

        return (
            self.precio_base
            * duracion
            * self.AREAS[self.__area]
            * multiplicador[urgencia]
        )

    def describir(self):
        """Devuelve la descripción de la asesoría."""

        return (
            f"{super().describir()} | "
            f"Área: {self.__area} | "
            f"Asesor: {self.__asesor}"
        )
