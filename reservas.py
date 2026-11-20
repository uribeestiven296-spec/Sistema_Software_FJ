"""Gestión de reservas."""
from datetime import datetime
import logging
from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import DatosInvalidosError, ReservaInvalidaError, OperacionNoPermitidaError, ErrorSistema

class Reserva(Entidad):
    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada")

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("La reserva requiere un servicio válido.")

        servicio.validar_disponibilidad()
        servicio.validar_parametros(duracion)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__fecha = datetime.now()

    @property
    def estado(self):
        return self.__estado

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    def confirmar(self):
        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )
        self.__servicio.validar_disponibilidad()
        self.__estado = "Confirmada"
        logging.info("Reserva %s confirmada.", self.identificador)

    def cancelar(self):
        if self.__estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        self.__estado = "Cancelada"
        logging.info("Reserva %s cancelada.", self.identificador)

    def procesar(self, impuesto=0.0, descuento=0.0):
        try:
            if self.__estado != "Confirmada":
                raise ReservaInvalidaError(
                    "La reserva debe estar confirmada para procesar el cobro."
                )
            total = self.__servicio.calcular_costo(
                self.__duracion, impuesto, descuento
            )
        except ErrorSistema as error:
            logging.exception("No fue posible procesar la reserva %s.", self.identificador)
            raise ReservaInvalidaError(
                f"Error al procesar la reserva: {error}"
            ) from error
        else:
            logging.info(
                "Reserva %s procesada. Total: $%.2f",
                self.identificador, total
            )
            return total
        finally:
            logging.info("Finalizó el intento de procesamiento de reserva %s.",
                         self.identificador)

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.identificador} | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion} h | "
            f"Estado: {self.__estado} | Fecha: "
            f"{self.__fecha.strftime('%Y-%m-%d %H:%M:%S')}"
        )
