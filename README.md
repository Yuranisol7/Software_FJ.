# SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ

## 1. Descripción del proyecto

El proyecto **Software FJ** consiste en el desarrollo de un sistema integral para gestionar clientes, servicios y reservas mediante el lenguaje de programación Python.

El sistema permite registrar y validar clientes, administrar diferentes tipos de servicios, realizar reservas, calcular costos y controlar las operaciones mediante excepciones personalizadas. Además, incorpora un mecanismo de registro de eventos y errores para facilitar el seguimiento de las operaciones.

## 2. Objetivo general

Desarrollar una aplicación utilizando Programación Orientada a Objetos que permita gestionar clientes, servicios y reservas de manera organizada, aplicando los principios de abstracción, encapsulamiento, herencia y polimorfismo, junto con el manejo adecuado de excepciones.

## 3. Tecnologías utilizadas

- Python 3.
- Visual Studio Code.
- Programación Orientada a Objetos (POO).
- Git.
- GitHub.

## 4. Estructura del proyecto

El proyecto está organizado en los siguientes módulos:

- `entidad_base.py`: contiene la clase abstracta principal del sistema.
- `excepciones.py`: define las excepciones personalizadas.
- `logger.py`: permite registrar operaciones, eventos y errores.
- `cliente.py`: gestiona y valida la información de los clientes.
- `servicios.py`: administra los diferentes tipos de servicios.
- `reserva.py`: controla la creación, confirmación, cancelación y finalización de reservas.
- `sistema.py`: coordina la administración general del sistema.
- `main.py`: ejecuta el programa y realiza las pruebas de funcionamiento.
- `sistema_fj_logs.txt`: almacena los registros generados durante la ejecución.

## 5. Tipos de servicios

El sistema contempla tres modalidades de servicios:

1. Reserva de salas.
2. Alquiler de equipos tecnológicos.
3. Asesorías especializadas.

Cada servicio cuenta con sus propias validaciones y métodos para calcular los costos correspondientes.

## 6. Principios de Programación Orientada a Objetos

En el desarrollo del proyecto se aplican los siguientes principios:

- **Abstracción:** permite definir una estructura general para las entidades y los servicios.
- **Encapsulamiento:** protege los atributos internos de las clases mediante el uso de atributos privados y propiedades.
- **Herencia:** permite reutilizar características y comportamientos de las clases principales.
- **Polimorfismo:** facilita la implementación de comportamientos específicos en los diferentes tipos de servicios.

También se implementan validaciones, excepciones personalizadas y registro de eventos para mejorar la seguridad y confiabilidad del sistema.

## 7. Manejo de excepciones y registro de eventos

El sistema incorpora excepciones personalizadas para controlar situaciones como datos inválidos, parámetros faltantes, servicios no disponibles, duraciones incorrectas y operaciones no permitidas.

Además, utiliza un módulo de registro (`logger.py`) que almacena información sobre las operaciones y los errores presentados durante la ejecución.

## 8. Ejecución del programa

Para ejecutar el sistema se deben seguir estos pasos:

1. Abrir la carpeta del proyecto en Visual Studio Code.
2. Verificar que Python esté instalado.
3. Abrir la terminal de Visual Studio Code.
4. Ubicarse en la carpeta principal del proyecto.
5. Ejecutar el siguiente comando:

```bash
python main.py
```

## 9. Resultados esperados

Al ejecutar el programa, se realizan diferentes operaciones de prueba para comprobar el funcionamiento del registro de clientes, la creación de servicios, la gestión de reservas, el cálculo de costos y el control de errores.

Las situaciones inválidas son gestionadas mediante excepciones personalizadas, evitando que los errores controlados interrumpan inesperadamente la ejecución del sistema.

## 10. Conclusión

El desarrollo del proyecto Software FJ permite aplicar los conceptos fundamentales de la Programación Orientada a Objetos mediante una solución práctica para la gestión de clientes, servicios y reservas.

Asimismo, la implementación de excepciones personalizadas y el registro de eventos contribuyen a construir una aplicación más organizada, confiable y preparada para manejar diferentes situaciones durante su funcionamiento.
