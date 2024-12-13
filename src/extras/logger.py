import logging


def custom_logger(log_file: str = "api_logs.log", level: int = logging.INFO):
    """
    Configura un logger básico que guarda mensajes en un archivo.

    Args:
        log_file (str): Nombre del archivo donde se guardarán los logs.
        level (int): Nivel de loggeo (e.g., logging.INFO, logging.ERROR).
    Returns:
        logger (logging.Logger): Instancia del logger configurado.
    """
    logger = logging.getLogger("basic_logger")
    logger.setLevel(level)

    # Configurar el formato del log
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Configurar el handler para archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Evita duplicar handlers si ya están configurados
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger
