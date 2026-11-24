
"""
excepciones.py
==============
Módulo de excepciones personalizadas del sistema Software FJ.

Define una excepción general y diferentes excepciones específicas
para controlar errores en clientes, servicios y reservas.
"""


class SistemaFJException(Exception):
    """Excepción general del sistema Software FJ."""

    def __init__(self, mensaje, codigo=None):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(mensaje)

    def __str__(self):
        """Devuelve el mensaje del error y su código si existe."""

        if self.codigo:
            return f"[{self.codigo}] {self.mensaje}"

        return self.mensaje


class ClienteInvalidoException(SistemaFJException):
    """Error relacionado con los datos de un cliente."""
    pass


class ParametroFaltanteException(SistemaFJException):
    """Error cuando falta un parámetro obligatorio."""
    pass


class ServicioNoDisponibleException(SistemaFJException):
    """Error cuando un servicio no está disponible."""
    pass


class ReservaInvalidaException(SistemaFJException):
    """Error relacionado con una reserva inválida."""
    pass


class OperacionNoPermitidaException(SistemaFJException):
    """Error cuando una operación no está permitida."""
    pass


class DuracionInvalidaException(SistemaFJException):
    """Error cuando la duración de un servicio no es válida."""
    pass


class CapacidadExcedidaException(SistemaFJException):
    """Error cuando se supera la capacidad permitida."""
    pass
