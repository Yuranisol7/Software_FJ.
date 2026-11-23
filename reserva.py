
from datetime import datetime
from excepciones import (
    ReservaInvalidaException,
    OperacionNoPermitidaException,
    ParametroFaltanteException,
    DuracionInvalidaException
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
        self.__parametros = parametros
        self.__estado = "PENDIENTE"
        self.__fecha_reserva = datetime.now()
        self.__costo = 0
        self.__historial = []

        self._registrar_historial("Reserva creada.")

    @staticmethod
    def _validar_inputs(cliente, servicio, duracion):
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
            or not 0 < duracion <= 168
        ):
            raise DuracionInvalidaException(
                "La duración debe ser un número mayor que cero y máximo 168 horas."
            )

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def fecha_reserva(self):
        return self.__fecha_reserva

    @property
    def costo(self):
        return self.__costo

    @property
    def historial(self):
        return self.__historial.copy()

    def _registrar_historial(self, mensaje):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__historial.append(f"[{fecha}] {mensaje}")

    def confirmar(self):
        """Confirma la reserva y calcula su costo."""

        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaException(
                "Solo se pueden confirmar reservas pendientes."
            )

        try:
            self.__estado = "PROCESANDO"
            self.__servicio.verificar_disponibilidad()

            self.__costo = self.__servicio.calcular_costo(
                self.__duracion,
                **self.__parametros
            )

            if self.__servicio.__class__.__name__ == "AlquilerEquipo":
                cantidad = self.__parametros.get("cantidad", 1)
                self.__servicio.reservar_unidades(cantidad)

            self.__cliente.agregar_reserva(self)
            self.__estado = "CONFIRMADA"

            self._registrar_historial(
                f"Reserva confirmada. Costo: ${self.__costo:,.2f}"
            )

            return self.__costo

        except Exception as error:
            self.__estado = "PENDIENTE"
            self._registrar_historial(
                f"Error al confirmar la reserva: {error}"
            )
            raise ReservaInvalidaException(
                "No fue posible confirmar la reserva."
            ) from error

    def cancelar(self, motivo="Sin especificar"):
        """Cancela una reserva pendiente o confirmada."""

        if self.__estado in ("CANCELADA", "COMPLETADA"):
            raise OperacionNoPermitidaException(
                "No se puede cancelar una reserva cancelada o completada."
            )

        if self.__estado == "CONFIRMADA":
            if self.__servicio.__class__.__name__ == "AlquilerEquipo":
                cantidad = self.__parametros.get("cantidad", 1)
                self.__servicio.liberar_unidades(cantidad)

        self.__estado = "CANCELADA"
        self._registrar_historial(
            f"Reserva cancelada. Motivo: {motivo}"
        )

        return True

    def completar(self):
        """Marca la reserva como completada."""

        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaException(
                "Solo se pueden completar reservas confirmadas."
            )

        self.__estado = "COMPLETADA"
        self._registrar_historial("Reserva completada correctamente.")

        return True

    def calcular_costo_con_impuesto(self, impuesto=0.19):
        return self.__costo * (1 + impuesto)

    def calcular_costo_con_descuento(self, descuento=0.10):
        return self.__costo * (1 - descuento)

    def calcular_costo_completo(self, impuesto=0.19, descuento=0.10):
        return self.__costo * (1 - descuento) * (1 + impuesto)

    def __str__(self):
        return (
            f"Reserva | Cliente: {self.__cliente.nombre_completo} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} horas | "
            f"Estado: {self.__estado} | "
            f"Costo: ${self.__costo:,.2f}"
        )
