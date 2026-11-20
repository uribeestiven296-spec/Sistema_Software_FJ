"""Servicios disponibles en Software FJ."""
from abc import ABC, abstractmethod
from entidades import Entidad
from excepciones import DatosInvalidosError, ServicioNoDisponibleError

class Servicio(Entidad, ABC):
    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatosInvalidosError("La tarifa debe ser un número mayor que cero.")

        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._nombre}' no está disponible."
            )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """
        Variante flexible del cálculo de costos:
        permite calcular con tarifa base y, opcionalmente, impuesto y descuento.
        """
        self.validar_disponibilidad()

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor que cero.")
        if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
            raise DatosInvalidosError("El impuesto debe estar entre 0 y 1.")
        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1.")

        subtotal = self._tarifa_hora * duracion
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    def mostrar_informacion(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"{self._nombre} | ID: {self.identificador} | "
            f"Tarifa/hora: ${self._tarifa_hora:.2f} | Estado: {estado}"
        )

class ReservaSala(Servicio):
    def describir_servicio(self):
        return "Reserva de sala para reuniones, clases o encuentros de trabajo."

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 12:
            raise DatosInvalidosError("La sala se puede reservar entre 1 y 12 horas.")

class AlquilerEquipo(Servicio):
    def describir_servicio(self):
        return "Alquiler de equipos tecnológicos por el tiempo solicitado."

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 24:
            raise DatosInvalidosError("El equipo se puede alquilar entre 1 y 24 horas.")

class AsesoriaEspecializada(Servicio):
    def describir_servicio(self):
        return "Asesoría especializada en tecnología y soluciones informáticas."

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 8:
            raise DatosInvalidosError("La asesoría debe durar entre 1 y 8 horas.")

