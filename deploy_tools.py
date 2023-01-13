def make_log_control(message):
    """
    Crea un log de control.

    El log de control registra los procesos que realiza el bot, para así
    gestionar las acciones que ejecuta el mismo.

    Parametros
    ----------
    message : str
        Mensaje que describe el proceso que se ejecuta en ese momento.
    
    Véase También
    -------------
    open : Abre un archivo especifico.
    """
    destFile = r"./logs.txt"
    with open(destFile, "a") as f:
        f.write(f"{message}\r\n")
