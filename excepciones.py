"""Excepciones personalizadas del sistema."""

class ErrorSistema(Exception):
    """Clase base para los errores propios del sistema."""
class DatosInvalidosError(ErrorSistema):
    """Se presenta cuando los datos ingresados no son válidos."""
class ServicioNoDisponibleError(ErrorSistema):
    """Se presenta cuando un servicio no está disponible."""
class ReservaInvalidaError(ErrorSistema):
    """Se presenta cuando una reserva no puede procesarse."""
class OperacionNoPermitidaError(ErrorSistema):
    """Se presenta cuando se intenta una operación no permitida."""
