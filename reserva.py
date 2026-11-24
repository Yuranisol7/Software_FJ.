
"""
reserva.py
==========
Módulo encargado de administrar las reservas del sistema Software FJ.

Controla la creación, confirmación, cancelación y finalización
de reservas, incluyendo el cálculo de costos, el historial
de operaciones y el manejo de excepciones.
"""

from datetime import datetime
import math

from excepciones import (
    ReservaInvalidaException,
    OperacionNoPermitidaException,
    ParametroFaltanteException,
    DuracionInvalidaException,
    SistemaFJException
)


class Reserva:
    """Representa una reserva del sistema Software FJ."""

    ESTADOS_VALIDOS = (
        "PENDIENTE",
        "PROCESANDO",
        "CONFIRMADA",
        "COMPLETADA",
        "CANCELADA"
    )

    def __init__(self, cliente, servicio, duracion, **parametros):
        self._validar_inputs(cliente, servicio, duracion)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__parametros = parametros.copy()

        self.__estado = "PENDIENTE"
        self.__fecha_reserva = datetime.now()
        self.__costo = 0
        self.__historial = []

        self._registrar_historial("Reserva creada.")

    @staticmethod
    def _validar_inputs(cliente, servicio, duracion):
        """Valida los datos iniciales de una reserva."""

        from cliente import Cliente
        from servicios import Servicio

        if not isinstance(cliente, Cliente):
            raise ParametroFaltanteException(
                "Debe proporcionar un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ParametroFaltanteException(
                "Debe proporcionar un servicio válido."
            )

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or not math.isfinite(duracion)
            or not 0 < duracion <= 168
        ):
            raise DuracionInvalidaException(
                "La duración debe ser un número mayor que cero "
                "y máximo 168 horas."
            )

    @staticmethod
    def _validar_porcentaje(valor, nombre):
        """Valida los porcentajes de impuestos y descuentos."""

        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or not math.isfinite(valor)
            or not 0 <= valor <= 1
        ):
            raise ParametroFaltanteException(
                f"El porcentaje de {nombre} debe estar entre 0 y 1."
            )

    @property
    def cliente(self):
        """Devuelve el cliente de la reserva."""
        return self.__cliente

    @property
    def servicio(self):
        """Devuelve el servicio reservado."""
        return self.__servicio

    @property
    def duracion(self):
        """Devuelve la duración de la reserva."""
        return self.__duracion

    @property
    def estado(self):
        """Devuelve el estado actual de la reserva."""
        return self.__estado

    @property
    def fecha_reserva(self):
        """Devuelve la fecha de creación de la reserva."""
        return self.__fecha_reserva

    @property
    def costo(self):
        """Devuelve el costo de la reserva."""
        return self.__costo

    @property
    def historial(self):
        """Devuelve una copia del historial de la reserva."""
        return self.__historial.copy()

    def _registrar_historial(self, mensaje):
        """Registra una operación en el historial."""

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.__historial.append(
            f"[{fecha}] {mensaje}"
        )

    def confirmar(self):
        """Confirma la reserva y calcula su costo."""

        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaException(
                "Solo se pueden confirmar reservas pendientes."
            )

        equipos_reservados = False

        try:
            self.__estado = "PROCESANDO"

            self.__servicio.verificar_disponibilidad()

            self.__servicio.validar_parametros(
                **self.__parametros
            )

            costo = self.__servicio.calcular_costo(
                self.__duracion,
                **self.__parametros
            )

            from servicios import AlquilerEquipo

            if isinstance(self.__servicio, AlquilerEquipo):
                cantidad = self.__parametros.get("cantidad", 1)

                self.__servicio.reservar_unidades(cantidad)
                equipos_reservados = True

            self.__cliente.agregar_reserva(self)

            self.__costo = costo
            self.__estado = "CONFIRMADA"

            self._registrar_historial(
                f"Reserva confirmada. Costo: ${self.__costo:,.2f}"
            )

            return self.__costo

        except SistemaFJException as error:

            if equipos_reservados:
                cantidad = self.__parametros.get("cantidad", 1)
                self.__servicio.liberar_unidades(cantidad)

            self.__estado = "PENDIENTE"

            self._registrar_historial(
                f"Error al confirmar la reserva: {error}"
            )

            raise

        except Exception as error:

            if equipos_reservados:
                cantidad = self.__parametros.get("cantidad", 1)
                self.__servicio.liberar_unidades(cantidad)

            self.__estado = "PENDIENTE"

            self._registrar_historial(
                f"Error inesperado al confirmar la reserva: {error}"
            )

            raise ReservaInvalidaException(
                "Ocurrió un error inesperado al confirmar la reserva."
            ) from error

    def cancelar(self, motivo="Sin especificar"):
        """Cancela una reserva pendiente o confirmada."""

        if self.__estado in ("CANCELADA", "COMPLETADA"):
            raise OperacionNoPermitidaException(
                "No se puede cancelar una reserva cancelada o completada."
            )

        if self.__estado == "PROCESANDO":
            raise OperacionNoPermitidaException(
                "No se puede cancelar una reserva en procesamiento."
            )

        if not isinstance(motivo, str) or not motivo.strip():
            raise ParametroFaltanteException(
                "Debe proporcionar un motivo de cancelación válido."
            )

        from servicios import AlquilerEquipo

        if (
            self.__estado == "CONFIRMADA"
            and isinstance(self.__servicio, AlquilerEquipo)
        ):
            cantidad = self.__parametros.get("cantidad", 1)

            self.__servicio.liberar_unidades(cantidad)

        self.__estado = "CANCELADA"

        self._registrar_historial(
            f"Reserva cancelada. Motivo: {motivo.strip()}"
        )

        return True

    def completar(self):
        """Marca una reserva confirmada como completada."""

        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaException(
                "Solo se pueden completar reservas confirmadas."
            )

        from servicios import AlquilerEquipo

        if isinstance(self.__servicio, AlquilerEquipo):
            cantidad = self.__parametros.get("cantidad", 1)

            self.__servicio.liberar_unidades(cantidad)

        self.__estado = "COMPLETADA"

        self._registrar_historial(
            "Reserva completada correctamente."
        )

        return True

    def calcular_costo_con_impuesto(self, impuesto=0.19):
        """Calcula el costo de la reserva con impuesto."""

        self._validar_porcentaje(impuesto, "impuesto")

        return self.__costo * (1 + impuesto)

    def calcular_costo_con_descuento(self, descuento=0.10):
        """Calcula el costo de la reserva con descuento."""

        self._validar_porcentaje(descuento, "descuento")

        return self.__costo * (1 - descuento)

    def calcular_costo_completo(
        self, impuesto=0.19, descuento=0.10
    ):
        """Calcula el costo aplicando descuento e impuesto."""

        self._validar_porcentaje(impuesto, "impuesto")
        self._validar_porcentaje(descuento, "descuento")

        return (
            self.__costo
            * (1 - descuento)
            * (1 + impuesto)
        )

    def __str__(self):
        """Devuelve la información general de la reserva."""

        return (
            f"Reserva | Cliente: {self.__cliente.nombre_completo} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} horas | "
            f"Estado: {self.__estado} | "
            f"Costo: ${self.__costo:,.2f}"
        )
