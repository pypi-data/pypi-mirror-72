from datetime import datetime

import colorama
import logging
from colorama import Fore, Back, Style

logger = logging.getLogger(__name__)


def _msg_user(
    msg,
    title="pyqalx",
    fore=Fore.WHITE,
    back=Back.BLACK,
    log=True,
    level=logging.DEBUG,
):
    """
    Sends a coloured message to the user and also writes the message
    to the logs
    :param msg: The msg that should be logged
    :param title: The title to print to the console
    :param fore: The foreground colour
    :param back: The background color
    :param log: Whether this should be logged to log files
    :param level: The loglevel
    """
    colorama.init()
    bright = Style.BRIGHT
    normal = Style.NORMAL
    if level == logging.ERROR:
        fore = Fore.RED
        # Make sure the errors pop!
        normal = Style.BRIGHT
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = f"[{now}] {title}"
    title = bright, fore, back, f"{title}:", normal
    message = fore, back, msg, Style.RESET_ALL
    print(*title, *message)

    if log:
        logger.log(level=level, msg=msg)
