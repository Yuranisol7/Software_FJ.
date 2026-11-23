
from abc import abstractmethod
from entidad_base import EntidadBase
from excepciones import (
    ServicioNoDisponibleException,
    DuracionInvalidaException,
    CapacidadExcedidaException,
    ParametroFaltanteException
)


class Servicio(EntidadBase):
    """Clase abstracta que representa un servicio."""

    def __init__(self, nombre, precio_base):
        super().__init__(nombre)

        if not isinstance(precio_base, (int, float)) or isinstance(precio_base, bool) or precio_base <= 0:
            raise ParametroFaltanteException(
                "El precio base debe ser mayor que cero."
            )

        self._precio_base = precio_base
        self._disponible = True

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    def marcar_disponible(self):
        self._disponible = True

    def marcar_no_disponible(self):
        self._disponible = False

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleException(
                f"El servicio {self.nombre} no está disponible."
            )
        return True

    def validar(self):
        return self._precio_base > 0

    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass

    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        pass

    def calcular_costo_con_impuesto(self, duracion, impuesto=0.19, **kwargs):
        costo = self.calcular_costo(duracion, **kwargs)
        return costo * (1 + impuesto)

    def calcular_costo_con_descuento(self, duracion, descuento=0.10, **kwargs):
        costo = self.calcular_costo(duracion, **kwargs)
        return costo * (1 - descuento)

    def calcular_costo_completo(self, duracion, impuesto=0.19,
                                descuento=0.10, **kwargs):
        costo = self.calcular_costo(duracion, **kwargs)
        return costo * (1 - descuento) * (1 + impuesto)

    def describir(self):
        return (
            f"Servicio: {self.nombre} | "
            f"Precio base: ${self._precio_base:,.0f}"
        )


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, nombre, numero_sala, capacidad=20,
                 precio_base=50000):
        super().__init__(nombre, precio_base)
        self.__numero_sala = numero_sala
        self.__capacidad = capacidad

    def validar_parametros(self, personas=1, **kwargs):
        if not isinstance(personas, int) or isinstance(personas, bool) or personas <= 0:
            raise ParametroFaltanteException(
                "La cantidad de personas debe ser un entero positivo."
            )

        if personas > self.__capacidad:
            raise CapacidadExcedidaException(
                "La cantidad de personas supera la capacidad de la sala."
            )
        return True

    def calcular_costo(self, duracion, personas=1, **kwargs):
        self.validar_parametros(personas=personas)

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or not 0 < duracion <= 12:
            raise DuracionInvalidaException(
                "La duración de la sala debe ser de 1 a 12 horas."
            )

        costo = self.precio_base * duracion

        if personas > 10:
            costo *= 1.15

        return costo

    def describir(self):
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

    def __init__(self, nombre, tipo_equipo, cantidad_total,
                 precio_base=30000):
        super().__init__(nombre, precio_base)

        if tipo_equipo not in self.TIPOS_VALIDOS:
            raise ParametroFaltanteException(
                "El tipo de equipo no es válido."
            )

        if not isinstance(cantidad_total, int) or isinstance(cantidad_total, bool) or cantidad_total <= 0:
            raise ParametroFaltanteException(
                "La cantidad total debe ser un entero positivo."
            )

        self.__tipo_equipo = tipo_equipo
        self.__cantidad_total = cantidad_total
        self.__cantidad_reservada = 0

    @property
    def cantidad_disponible(self):
        return self.__cantidad_total - self.__cantidad_reservada

    def validar_parametros(self, cantidad=1, **kwargs):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ParametroFaltanteException(
                "La cantidad debe ser un entero positivo."
            )

        if cantidad > self.cantidad_disponible:
            raise CapacidadExcedidaException(
                "No hay suficientes equipos disponibles."
            )
        return True

    def calcular_costo(self, duracion, cantidad=1, **kwargs):
        self.validar_parametros(cantidad=cantidad)

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or not 0 < duracion <= 168:
            raise DuracionInvalidaException(
                "La duración del alquiler debe ser de 1 a 168 horas."
            )

        return self.precio_base * duracion * cantidad

    def reservar_unidades(self, cantidad):
        self.validar_parametros(cantidad=cantidad)
        self.__cantidad_reservada += cantidad

    def liberar_unidades(self, cantidad):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ParametroFaltanteException(
                "La cantidad debe ser un entero positivo."
            )

        if cantidad > self.__cantidad_reservada:
            raise CapacidadExcedidaException(
                "No se pueden liberar más equipos de los reservados."
            )

        self.__cantidad_reservada -= cantidad

    def describir(self):
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

    def __init__(self, nombre, area, asesor, precio_base=80000):
        super().__init__(nombre, precio_base)

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
        if not isinstance(urgencia, int) or isinstance(urgencia, bool) or urgencia not in (1, 2, 3):
            raise ParametroFaltanteException(
                "La urgencia debe ser 1, 2 o 3."
            )
        return True

    def calcular_costo(self, duracion, urgencia=1, **kwargs):
        self.validar_parametros(urgencia=urgencia)

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or not 0 < duracion <= 8:
            raise DuracionInvalidaException(
                "La asesoría debe durar de 1 a 8 horas."
            )

        multiplicador = {1: 1.0, 2: 1.3, 3: 1.6}

        return (
            self.precio_base
            * duracion
            * self.AREAS[self.__area]
            * multiplicador[urgencia]
        )

    def describir(self):
        return (
            f"{super().describir()} | "
            f"Área: {self.__area} | "
            f"Asesor: {self.__asesor}"
        )
