import win32print

def listar_impresoras():
    """
    Lista todas las impresoras disponibles en el sistema.
    """
    impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    if not impresoras:
        print("No se encontraron impresoras disponibles.")
        return None
    return impresoras

def seleccionar_impresora(impresoras):
    """
    Permite al usuario seleccionar una impresora de la lista.
    """
    print("Impresoras disponibles:")
    for i, impresora in enumerate(impresoras):
        print(f"{i + 1}. {impresora[2]}")  # impresora[2] contiene el nombre de la impresora

    while True:
        try:
            seleccion = int(input("Seleccione el número de la impresora: ")) - 1
            if 0 <= seleccion < len(impresoras):
                return impresoras[seleccion][2]  # Devuelve el nombre de la impresora seleccionada
            else:
                print("Número fuera de rango. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")

def imprimir_texto(nombre_impresora, texto):
    try:
        # Abre la impresora seleccionada
        hprinter = win32print.OpenPrinter(nombre_impresora)
        try:
            # Inicia un trabajo de impresión
            job = win32print.StartDocPrinter(hprinter, 1, ("Impresión de Texto", None, "RAW"))
            win32print.StartPagePrinter(hprinter)

            # Envía el texto a la impresora
            win32print.WritePrinter(hprinter, (texto + "\n"*6).encode("utf-8"))

            # Envía el comando de corte de papel
            comando_corte = b'\x1D\x56\x01'  # Comando de corte completo
            win32print.WritePrinter(hprinter, comando_corte)

            # Finaliza el trabajo de impresión
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
        finally:
            # Cierra la impresora
            win32print.ClosePrinter(hprinter)
        print(f"Texto enviado a la impresora: {nombre_impresora}")
    except Exception as e:
        print(f"Error al imprimir: {e}")

def main():
    # Listar impresoras disponibles
    impresoras = listar_impresoras()
    if not impresoras:
        return

    # Seleccionar una impresora
    impresora_seleccionada = seleccionar_impresora(impresoras)
    if not impresora_seleccionada:
        return

    # Pedir al usuario que ingrese el texto a imprimir

if __name__ == "__main__":
    main()


