"""Clase abstracta Entidad y clase Cliente."""
from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError

class Entidad(ABC):
    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError("El identificador es obligatorio.")
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass

class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise DatosInvalidosError("El nombre debe tener al menos 2 caracteres.")
        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        if not isinstance(telefono, str) or not telefono.strip().isdigit():
            raise DatosInvalidosError("El teléfono debe contener únicamente números.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        return (
            f"Cliente: {self.__nombre} | ID: {self.identificador} | "
            f"Correo: {self.__correo} | Teléfono: {self.__telefono}"
        )
