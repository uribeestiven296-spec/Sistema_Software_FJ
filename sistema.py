"""Administración central de clientes, servicios y reservas."""
import logging
from entidades import Cliente
from servicios import Servicio
from reservas import Reserva
from excepciones import DatosInvalidosError, ReservaInvalidaError, ErrorSistema

class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError("El objeto no corresponde a un cliente.")
            if any(c.identificador == cliente.identificador for c in self.clientes):
                raise DatosInvalidosError("Ya existe un cliente con ese identificador.")
            self.clientes.append(cliente)
            logging.info("Cliente %s registrado.", cliente.identificador)
            return True
        except ErrorSistema:
            logging.exception("Error al registrar cliente.")
            raise

    def registrar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El objeto no corresponde a un servicio.")
            if any(s.identificador == servicio.identificador for s in self.servicios):
                raise DatosInvalidosError("Ya existe un servicio con ese identificador.")
            self.servicios.append(servicio)
            logging.info("Servicio %s registrado.", servicio.identificador)
            return True
        except ErrorSistema:
            logging.exception("Error al registrar servicio.")
            raise

    def crear_reserva(self, identificador, cliente_id, servicio_id, duracion):
        try:
            cliente = next(
                (c for c in self.clientes if c.identificador == cliente_id), None
            )
            servicio = next(
                (s for s in self.servicios if s.identificador == servicio_id), None
            )

            if cliente is None:
                raise DatosInvalidosError("El cliente indicado no está registrado.")
            if servicio is None:
                raise DatosInvalidosError("El servicio indicado no está registrado.")

            reserva = Reserva(identificador, cliente, servicio, duracion)
            self.reservas.append(reserva)
            logging.info("Reserva %s creada.", identificador)
            return reserva
        except ErrorSistema:
            logging.exception("No se pudo crear la reserva %s.", identificador)
            raise
        except Exception as error:
            logging.exception("Error inesperado al crear una reserva.")
            raise ErrorSistema("Ocurrió un error inesperado al crear la reserva.") from error

    def buscar_reserva(self, identificador):
        reserva = next(
            (r for r in self.reservas if r.identificador == identificador), None
        )
        if reserva is None:
            raise ReservaInvalidaError("No se encontró la reserva solicitada.")
        return reserva

    def listar_clientes(self):
        return [cliente.mostrar_informacion() for cliente in self.clientes]

    def listar_servicios(self):
        return [
            f"{servicio.mostrar_informacion()} | {servicio.describir_servicio()}"
            for servicio in self.servicios
        ]

    def listar_reservas(self):
        return [reserva.mostrar_informacion() for reserva in self.reservas]
