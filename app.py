import datetime
import os
import db_manager

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def registrar_producto():
    """Registra un nuevo producto en la base de datos."""
    limpiar_pantalla()
    nombre = input("📦 Nombre del producto: ")
    precio = float(input("💰 Precio del producto: "))
    stock = int(input("📊 Cantidad en stock: "))

    db_manager.ejecutar_query("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))
    print(f"✅ Producto '{nombre}' registrado con éxito.")

def registrar_orden():
    """Crea una nueva orden."""
    limpiar_pantalla()
    productos = db_manager.obtener_resultados("SELECT * FROM productos")

    if not productos:
        print("⚠️ No hay productos registrados.")
        return

    print("📋 Productos disponibles:")
    for p in productos:
        print(f"{p[0]}: {p[1]} - ${p[2]} - Stock: {p[3]}")

    producto_id = int(input("🔢 ID del producto a ordenar: "))
    cantidad = int(input("📦 Cantidad: "))

    producto = next((p for p in productos if p[0] == producto_id), None)
    if not producto or producto[3] < cantidad:
        print("❌ Stock insuficiente o producto no encontrado.")
        return

    db_manager.ejecutar_query("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
    db_manager.ejecutar_query("INSERT INTO ordenes (producto_id, cantidad, fecha) VALUES (?, ?, ?)", 
                               (producto_id, cantidad, datetime.datetime.now()))

    print(f"✅ Orden registrada con éxito.")

def gestionar_envio():
    """Registra el envío de una orden."""
    limpiar_pantalla()
    ordenes = db_manager.obtener_resultados("SELECT * FROM ordenes")

    if not ordenes:
        print("⚠️ No hay órdenes pendientes.")
        return

    print("📦 Órdenes pendientes:")
    for o in ordenes:
        print(f"{o[0]}: Producto {o[1]} - Cantidad: {o[2]} - Fecha: {o[3]}")

    orden_id = int(input("🔢 ID de la orden a enviar: "))
    orden = next((o for o in ordenes if o[0] == orden_id), None)

    if not orden:
        print("❌ Orden no encontrada.")
        return

    db_manager.ejecutar_query("INSERT INTO envios (orden_id, fecha_envio) VALUES (?, ?)", 
                               (orden_id, datetime.datetime.now()))

    db_manager.ejecutar_query("DELETE FROM ordenes WHERE id = ?", (orden_id,))
    print(f"🚚 Envío registrado con éxito.")

def mostrar_reportes():
    """Muestra los reportes del sistema."""
    limpiar_pantalla()
    print("\n📊 Reporte de Productos 📊")
    for p in db_manager.obtener_resultados("SELECT * FROM productos"):
        print(f"{p[0]}: {p[1]} - Stock: {p[3]} - Precio: ${p[2]}")

    print("\n📊 Reporte de Órdenes 📊")
    for o in db_manager.obtener_resultados("SELECT * FROM ordenes"):
        print(f"{o[0]}: Producto {o[1]} - Cantidad: {o[2]} - Fecha: {o[3]}")

    print("\n📊 Reporte de Envíos 📊")
    for e in db_manager.obtener_resultados("SELECT * FROM envios"):
        print(f"{e[0]}: Orden {e[1]} - Fecha de Envío: {e[2]}")

    input("\nPresione Enter para continuar...")

def menu():
    """Muestra el menú principal."""
    while True:
        limpiar_pantalla()
        print("\n📦 Sistema de Control Logístico 📦")
        print("1️⃣ Registrar Producto")
        print("2️⃣ Registrar Orden")
        print("3️⃣ Gestionar Envío")
        print("4️⃣ Ver Reportes")
        print("5️⃣ Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            registrar_orden()
        elif opcion == "3":
            gestionar_envio()
        elif opcion == "4":
            mostrar_reportes()
        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
