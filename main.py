
"""
main.py
=======
Archivo principal del Sistema Integral de Gestión Software FJ.

Ejecuta las pruebas de registro de clientes, creación de servicios,
gestión de reservas y control de excepciones.
"""

from sistema import SistemaFJ

from excepciones import (
    SistemaFJException,
    ClienteInvalidoException,
    ReservaInvalidaException,
    DuracionInvalidaException,
    OperacionNoPermitidaException,
    CapacidadExcedidaException,
    ServicioNoDisponibleException
)


def mostrar_titulo(texto):
    """Muestra un título centrado en la consola."""

    print("\n" + "=" * 65)
    print(texto.center(65))
    print("=" * 65)


def mostrar_resultado(numero, descripcion, exitoso=True):
    """Muestra el resultado de cada operación."""

    estado = "CORRECTO" if exitoso else "ERROR CONTROLADO"

    print(f"\n[{estado}] Operación {numero}: {descripcion}")


def main():
    """Ejecuta las operaciones de prueba del sistema."""

    sistema = SistemaFJ()

    mostrar_titulo("SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")

    cliente1 = None
    cliente2 = None
    sala = None
    equipo = None
    asesoria = None
    reserva1 = None
    reserva2 = None
    reserva3 = None

    operaciones = 0
    exitosas = 0
    fallidas_controladas = 0

    # OPERACION 1: Registrar primer cliente
    try:
        cliente1 = sistema.registrar_cliente(
            "Carlos",
            "Rodriguez",
            "carlos@gmail.com",
            "3101234567",
            "12345678"
        )

        operaciones += 1
        exitosas += 1

        mostrar_resultado(1, "Registro de cliente Carlos")

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(1, str(error), False)

    # OPERACION 2: Registrar segundo cliente
    try:
        cliente2 = sistema.registrar_cliente(
            "Maria",
            "Gonzalez",
            "maria@gmail.com",
            "3119876543",
            "87654321"
        )

        operaciones += 1
        exitosas += 1

        mostrar_resultado(2, "Registro de cliente Maria")

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(2, str(error), False)

    # OPERACION 3: Intentar registrar correo invalido
    try:
        sistema.registrar_cliente(
            "Pedro",
            "Lopez",
            "correo_invalido",
            "3123456789",
            "45678912"
        )

    except ClienteInvalidoException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(
            3,
            f"Validación de correo: {error}",
            False
        )

    # OPERACION 4: Crear servicios
    try:
        sala = sistema.crear_servicio_sala(
            "Sala de conferencias",
            "SALA-01",
            capacidad=20,
            precio_base=50000
        )

        equipo = sistema.crear_servicio_equipo(
            "Alquiler de proyectores",
            "proyector",
            cantidad_total=5,
            precio_base=30000
        )

        asesoria = sistema.crear_servicio_asesoria(
            "Asesoría tecnológica",
            "tecnologia",
            "Laura Martinez",
            precio_base=80000
        )

        operaciones += 1
        exitosas += 1

        mostrar_resultado(4, "Creación de tres servicios")

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(4, str(error), False)

    # OPERACION 5: Crear y confirmar reserva de sala
    try:
        if cliente1 is None or sala is None:
            raise ReservaInvalidaException(
                "No existen los datos necesarios para reservar la sala."
            )

        reserva1 = sistema.crear_reserva(
            cliente1,
            sala,
            3,
            personas=12
        )

        costo = sistema.confirmar_reserva(reserva1)

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            5,
            f"Reserva de sala confirmada. Costo: ${costo:,.0f}"
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(5, str(error), False)

    # OPERACION 6: Consultar costo con impuesto
    try:
        if reserva1 is None:
            raise ReservaInvalidaException(
                "No existe la reserva de sala."
            )

        costo = reserva1.calcular_costo_con_impuesto()

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            6,
            f"Costo con impuesto: ${costo:,.0f}"
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(6, str(error), False)

    # OPERACION 7: Crear y confirmar asesoria
    try:
        if cliente2 is None or asesoria is None:
            raise ReservaInvalidaException(
                "No existen los datos necesarios para la asesoría."
            )

        reserva2 = sistema.crear_reserva(
            cliente2,
            asesoria,
            2,
            urgencia=2
        )

        costo = sistema.confirmar_reserva(reserva2)

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            7,
            f"Asesoría confirmada. Costo: ${costo:,.0f}"
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(7, str(error), False)

    # OPERACION 8: Intentar reservar con duracion negativa
    try:
        if cliente1 is None or sala is None:
            raise ReservaInvalidaException(
                "No existen cliente o sala."
            )

        sistema.crear_reserva(
            cliente1,
            sala,
            -5,
            personas=2
        )

    except DuracionInvalidaException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(
            8,
            f"Duración rechazada: {error}",
            False
        )

    # OPERACION 9: Intentar superar capacidad de sala
    try:
        if cliente1 is None or sala is None:
            raise ReservaInvalidaException(
                "No existen cliente o sala."
            )

        reserva_capacidad = sistema.crear_reserva(
            cliente1,
            sala,
            2,
            personas=30
        )

        sistema.confirmar_reserva(reserva_capacidad)

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            9,
            "La reserva superó una capacidad que debía rechazarse."
        )

    except CapacidadExcedidaException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(
            9,
            f"Capacidad excedida correctamente controlada: {error}",
            False
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(
            9,
            f"Error controlado: {error}",
            False
        )

    # OPERACION 10: Reservar equipos
    try:
        if cliente1 is None or equipo is None:
            raise ReservaInvalidaException(
                "No existen cliente o equipo."
            )

        reserva3 = sistema.crear_reserva(
            cliente1,
            equipo,
            4,
            cantidad=2
        )

        costo = sistema.confirmar_reserva(reserva3)

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            10,
            f"Alquiler de 2 equipos confirmado. Costo: ${costo:,.0f}"
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(
            10,
            f"Error al reservar equipos: {error}",
            False
        )

    # OPERACION 11: Consultar equipos disponibles
    try:
        if equipo is None:
            raise ReservaInvalidaException(
                "No existe el servicio de equipos."
            )

        disponibles = equipo.cantidad_disponible

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            11,
            f"Equipos disponibles: {disponibles}"
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(11, str(error), False)

    # OPERACION 12: Cancelar reserva de equipos
    try:
        if reserva3 is None:
            raise ReservaInvalidaException(
                "No existe la reserva de equipos."
            )

        sistema.cancelar_reserva(
            reserva3,
            "Cancelación solicitada por el cliente"
        )

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            12,
            "Reserva de equipos cancelada"
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(12, str(error), False)

    # OPERACION 13: Intentar cancelar nuevamente
    try:
        if reserva3 is None:
            raise ReservaInvalidaException(
                "No existe la reserva."
            )

        sistema.cancelar_reserva(
            reserva3,
            "Segundo intento de cancelación"
        )

        raise ReservaInvalidaException(
            "La segunda cancelación no fue rechazada."
        )

    except OperacionNoPermitidaException as error:
        operaciones += 1
        fallidas_controladas += 1

        try:
            raise ReservaInvalidaException(
                "Se controló el intento de cancelar dos veces."
            ) from error

        except ReservaInvalidaException as error_encadenado:
            print(f"\nError encadenado: {error_encadenado}")
            print(f"Causa original: {error_encadenado.__cause__}")

            mostrar_resultado(
                13,
                "Manejo de excepciones encadenadas",
                False
            )

    # OPERACION 14: Completar asesoria
    try:
        if reserva2 is None:
            raise ReservaInvalidaException(
                "No existe la reserva de asesoría."
            )

        sistema.completar_reserva(reserva2)

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            14,
            "Asesoría completada"
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(14, str(error), False)

    # OPERACION 15: Intentar utilizar un servicio no disponible
    try:
        if cliente1 is None or sala is None:
            raise ReservaInvalidaException(
                "No existen cliente o sala."
            )

        sala.marcar_no_disponible()

        reserva_prueba = sistema.crear_reserva(
            cliente1,
            sala,
            2,
            personas=5
        )

        sistema.confirmar_reserva(reserva_prueba)

        operaciones += 1
        exitosas += 1

        mostrar_resultado(
            15,
            "El servicio fue utilizado"
        )

    except ServicioNoDisponibleException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(
            15,
            f"Servicio no disponible correctamente controlado: {error}",
            False
        )

    except SistemaFJException as error:
        operaciones += 1
        fallidas_controladas += 1

        mostrar_resultado(15, str(error), False)

    finally:
        if sala is not None:
            sala.marcar_disponible()

        print("\nProceso de pruebas finalizado.")

    # INFORME FINAL
    mostrar_titulo("INFORME FINAL DEL SISTEMA")

    sistema.mostrar_informacion()

    print("\nRESULTADOS DE LAS PRUEBAS")
    print(f"Operaciones ejecutadas: {operaciones}")
    print(f"Operaciones exitosas: {exitosas}")
    print(f"Errores controlados: {fallidas_controladas}")

    # Registrar los resultados mediante el acceso público al Logger
    sistema.logger.info(
        f"Pruebas finalizadas. Operaciones: {operaciones}, "
        f"Exitosas: {exitosas}, "
        f"Errores controlados: {fallidas_controladas}"
    )


if __name__ == "__main__":
    main()
