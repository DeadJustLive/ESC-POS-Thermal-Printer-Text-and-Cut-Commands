import win32print

def list_printers():
    """
    Lists all available printers on the system.
    """
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    if not printers:
        print("No available printers found.")
        return None
    return printers

def select_printer(printers):
    """
    Allows the user to select a printer from the list.
    """
    print("Available printers:")
    for i, printer in enumerate(printers):
        print(f"{i + 1}. {printer[2]}")  # printer[2] contains the printer name

    while True:
        try:
            selection = int(input("Select the printer number: ")) - 1
            if 0 <= selection < len(printers):
                return printers[selection][2]  # Returns the name of the selected printer
            else:
                print("Number out of range. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")

def print_text(printer_name, text):
    try:
        # Open the selected printer
        hprinter = win32print.OpenPrinter(printer_name)
        try:
            # Start a print job
            job = win32print.StartDocPrinter(hprinter, 1, ("Text Print", None, "RAW"))
            win32print.StartPagePrinter(hprinter)

            # Send the text to the printer
            win32print.WritePrinter(hprinter, (text + "\n"*6).encode("utf-8"))

            # Send the paper cut command
            cut_command = b'\x1D\x56\x01'  # Full cut command
            win32print.WritePrinter(hprinter, cut_command)

            # End the print job
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
        finally:
            # Close the printer
            win32print.ClosePrinter(hprinter)
        print(f"Text sent to printer: {printer_name}")
    except Exception as e:
        print(f"Error printing: {e}")

def main():
    # List available printers
    printers = list_printers()
    if not printers:
        return

    # Select a printer
    selected_printer = select_printer(printers)
    if not selected_printer:
        return

    # Prompt the user to enter the text to print
    text_to_print = input("Enter the text to print: ")
    print_text(selected_printer, text_to_print)

if __name__ == "__main__":
    main()
