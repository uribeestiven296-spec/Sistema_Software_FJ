"""Punto de entrada y pruebas de demostración de Software FJ."""
import logging
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ
from excepciones import ErrorSistema

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

def ejecutar_demostracion():
    sistema = SistemaSoftwareFJ()

    print("=" * 65)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 65)

    # Operación 1: registro de cliente válido.
    try:
        cliente1 = Cliente("C001", "Laura Gómez", "laura@gmail.com", "3001234567")
        sistema.registrar_cliente(cliente1)
        print("[OK] Operación 1: cliente Laura registrado.")
    except ErrorSistema as error:
        print("[ERROR] Operación 1:", error)

    # Operación 2: registro de un segundo cliente válido.
    try:
        cliente2 = Cliente("C002", "Carlos Pérez", "carlos@gmail.com", "3107654321")
        sistema.registrar_cliente(cliente2)
        print("[OK] Operación 2: cliente Carlos registrado.")
    except ErrorSistema as error:
        print("[ERROR] Operación 2:", error)

    # Operación 3: intento de registro con correo inválido.
    try:
        cliente_invalido = Cliente("C003", "Ana Ruiz", "correo-no-valido", "3001112222")
        sistema.registrar_cliente(cliente_invalido)
    except ErrorSistema as error:
        print("[CONTROLADO] Operación 3: registro inválido:", error)
        logging.warning("Se rechazó un cliente con correo inválido.")

    # Operación 4: creación de servicio de sala.
    try:
        sala = ReservaSala("S001", "Sala de reuniones", 50000)
        sistema.registrar_servicio(sala)
        print("[OK] Operación 4: servicio de sala registrado.")
    except ErrorSistema as error:
        print("[ERROR] Operación 4:", error)

    # Operación 5: creación de servicio de alquiler de equipo.
    try:
        equipo = AlquilerEquipo("S002", "Portátil empresarial", 25000)
        sistema.registrar_servicio(equipo)
        print("[OK] Operación 5: servicio de equipo registrado.")
    except ErrorSistema as error:
        print("[ERROR] Operación 5:", error)

    # Operación 6: creación de servicio de asesoría.
    try:
        asesoria = AsesoriaEspecializada("S003", "Asesoría informática", 80000)
        sistema.registrar_servicio(asesoria)
        print("[OK] Operación 6: servicio de asesoría registrado.")
    except ErrorSistema as error:
        print("[ERROR] Operación 6:", error)

    # Operación 7: intento de registrar un servicio duplicado.
    try:
        sistema.registrar_servicio(
            ReservaSala("S001", "Otra sala", 60000)
        )
    except ErrorSistema as error:
        print("[CONTROLADO] Operación 7: servicio duplicado:", error)

    # Operación 8: creación de una reserva válida.
    try:
        reserva1 = sistema.crear_reserva("R001", "C001", "S001", 2)
        print("[OK] Operación 8: reserva R001 creada.")
    except ErrorSistema as error:
        print("[ERROR] Operación 8:", error)

    # Operación 9: confirmación de reserva.
    try:
        reserva1.confirmar()
        print("[OK] Operación 9: reserva R001 confirmada.")
    except ErrorSistema as error:
        print("[ERROR] Operación 9:", error)

    # Operación 10: procesamiento con impuesto del 19 % y descuento del 10 %.
    try:
        total = reserva1.procesar(impuesto=0.19, descuento=0.10)
        print(f"[OK] Operación 10: total de la reserva R001: ${total:,.2f}")
    except ErrorSistema as error:
        print("[ERROR] Operación 10:", error)

    # Operación 11: intento de reserva con duración fuera del límite.
    try:
        sistema.crear_reserva("R002", "C002", "S002", 30)
    except ErrorSistema as error:
        print("[CONTROLADO] Operación 11: duración inválida:", error)

    # Operación 12: intento de reserva con cliente inexistente.
    try:
        sistema.crear_reserva("R003", "C999", "S003", 2)
    except ErrorSistema as error:
        print("[CONTROLADO] Operación 12: cliente inexistente:", error)

    # Operación 13: reserva correcta y cancelación.
    try:
        reserva2 = sistema.crear_reserva("R004", "C002", "S003", 1)
        reserva2.cancelar()
        print("[OK] Operación 13: reserva R004 creada y cancelada.")
    except ErrorSistema as error:
        print("[ERROR] Operación 13:", error)

    # Operación 14: intento de procesar una reserva pendiente.
    try:
        reserva3 = sistema.crear_reserva("R005", "C001", "S002", 3)
        reserva3.procesar()
    except ErrorSistema as error:
        print("[CONTROLADO] Operación 14: procesamiento no permitido:", error)

    # try/except/else/finally: ejemplo explícito de ejecución controlada.
    try:
        print("\nVerificación final: cantidad de clientes:", len(sistema.clientes))
    except Exception as error:
        logging.exception("Error en la verificación final.")
        print("Se presentó un error:", error)
    else:
        print("La verificación final se ejecutó correctamente.")
    finally:
        print("La demostración terminó. Consulte software_fj.log para ver los registros.")

    print("\n--- CLIENTES REGISTRADOS ---")
    for dato in sistema.listar_clientes():
        print(dato)

    print("\n--- SERVICIOS REGISTRADOS ---")
    for dato in sistema.listar_servicios():
        print(dato)

    print("\n--- RESERVAS REGISTRADAS ---")
    for dato in sistema.listar_reservas():
        print(dato)


if __name__ == "__main__":
    ejecutar_demostracion()
