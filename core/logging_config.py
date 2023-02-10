"""
Logging script for Core module
"""
import logging
import os
from datetime import datetime
from logging.handlers import SMTPHandler

from core.config import settings


def setup_logging(log_level: int = logging.INFO) -> None:
    """
    Setup logging
    :param log_level: Level of logging
    :type log_level: int
    :return: None
    :rtype: NoneType
    """
    current_date: str = datetime.today().strftime('%d-%b-%Y-%H-%M-%S')
    current_file_directory: str = os.path.dirname(os.path.abspath(__file__))
    project_root: str = current_file_directory
    while os.path.basename(project_root) != "car-sales-etl":
        project_root = os.path.dirname(project_root)
    log_filename: str = f'log-{current_date}.log'
    filename_path: str = f'{project_root}/logs/{log_filename}'

    logger: logging.Logger = logging.getLogger()
    logger.setLevel(log_level)

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    formatter = logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s][%(lineno)d]:'
        ' %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler: logging.FileHandler = logging.FileHandler(filename_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if log_level == logging.CRITICAL:
        mail_handler = SMTPHandler(
            mailhost=settings.MAIL_SERVER,
            fromaddr=settings.MAIL_FROM,
            toaddrs=settings.MAIL_TO,
            subject=settings.MAIL_SUBJECT,
            credentials=tuple(settings.MAIL_CREDENTIALS),
            timeout=settings.MAIL_TIMEOUT
        )
        mail_handler.setLevel(log_level)
        logger.addHandler(mail_handler)
