
from cliente import Cliente
from servicios import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)
from reserva import Reserva
from logger import Logger
from excepciones import (
    ClienteInvalidoException,
    ServicioNoDisponibleException,
    OperacionNoPermitidaException
)


class SistemaFJ:
    """Administra las operaciones del sistema Software FJ."""

    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        self.__logger = Logger.obtener_instancia()

        self.__logger.info("Sistema Software FJ iniciado.")

    def registrar_cliente(self, nombre, apellido, email,
                          telefono, documento):
        cliente = Cliente(
            nombre, apellido, email, telefono, documento
        )

        self.__clientes.append(cliente)

        self.__logger.info(
            f"Cliente registrado: {cliente.nombre_completo}"
        )

        return cliente

    def crear_servicio_sala(self, nombre, numero_sala,
                            capacidad=20, precio_base=50000):
        servicio = ReservaSala(
            nombre, numero_sala, capacidad, precio_base
        )

        self.__servicios.append(servicio)
        self.__logger.info(f"Servicio creado: {servicio.nombre}")

        return servicio

    def crear_servicio_equipo(self, nombre, tipo_equipo,
                              cantidad_total, precio_base=30000):
        from excepciones import ParametroFaltanteException

        servicio = AlquilerEquipo(
            nombre, tipo_equipo, cantidad_total, precio_base
        )

        self.__servicios.append(servicio)
        self.__logger.info(f"Servicio creado: {servicio.nombre}")

        return servicio

    def crear_servicio_asesoria(self, nombre, area, asesor,
                                precio_base=80000):
        servicio = AsesoriaEspecializada(
            nombre, area, asesor, precio_base
        )

        self.__servicios.append(servicio)
        self.__logger.info(f"Servicio creado: {servicio.nombre}")

        return servicio

    def crear_reserva(self, cliente, servicio, duracion, **parametros):
        if cliente not in self.__clientes:
            raise ClienteInvalidoException(
                "El cliente no está registrado en el sistema."
            )

        if servicio not in self.__servicios:
            raise ServicioNoDisponibleException(
                "El servicio no está registrado en el sistema."
            )

        reserva = Reserva(
            cliente, servicio, duracion, **parametros
        )

        self.__reservas.append(reserva)

        self.__logger.info(
            f"Reserva creada para {cliente.nombre_completo}."
        )

        return reserva

    def confirmar_reserva(self, reserva):
        if reserva not in self.__reservas:
            raise OperacionNoPermitidaException(
                "La reserva no pertenece al sistema."
            )

        costo = reserva.confirmar()

        self.__logger.info(
            f"Reserva confirmada. Costo: ${costo:,.2f}"
        )

        return costo

    def cancelar_reserva(self, reserva, motivo="Sin especificar"):
        if reserva not in self.__reservas:
            raise OperacionNoPermitidaException(
                "La reserva no pertenece al sistema."
            )

        reserva.cancelar(motivo)

        self.__logger.warning(
            f"Reserva cancelada. Motivo: {motivo}"
        )

        return True

    def completar_reserva(self, reserva):
        if reserva not in self.__reservas:
            raise OperacionNoPermitidaException(
                "La reserva no pertenece al sistema."
            )

        reserva.completar()

        self.__logger.evento("Reserva completada.")

        return True

    def listar_clientes(self):
        return self.__clientes.copy()

    def listar_servicios(self):
        return self.__servicios.copy()

    def listar_reservas(self):
        return self.__reservas.copy()

    def mostrar_resumen(self):
        """Devuelve un resumen general del sistema."""

        confirmadas = sum(
            1 for reserva in self.__reservas
            if reserva.estado == "CONFIRMADA"
        )

        completadas = sum(
            1 for reserva in self.__reservas
            if reserva.estado == "COMPLETADA"
        )

        canceladas = sum(
            1 for reserva in self.__reservas
            if reserva.estado == "CANCELADA"
        )

        total_ingresos = sum(
            reserva.costo
            for reserva in self.__reservas
            if reserva.estado in ("CONFIRMADA", "COMPLETADA")
        )

        return {
            "clientes": len(self.__clientes),
            "servicios": len(self.__servicios),
            "reservas": len(self.__reservas),
            "confirmadas": confirmadas,
            "completadas": completadas,
            "canceladas": canceladas,
            "ingresos": total_ingresos
        }

    def mostrar_informacion(self):
        """Imprime la información general del sistema."""

        print("\n========== SISTEMA SOFTWARE FJ ==========")

        print("\nCLIENTES:")
        for cliente in self.__clientes:
            print(cliente)

        print("\nSERVICIOS:")
        for servicio in self.__servicios:
            print(servicio.describir())

        print("\nRESERVAS:")
        for reserva in self.__reservas:
            print(reserva)

        print("\nRESUMEN:")
        for clave, valor in self.mostrar_resumen().items():
            print(f"{clave.capitalize()}: {valor}")

        print("=========================================")
