# from .spidar.spidar import spidar_registers, spidar_v1
# from .ipackaccess.ipackaccess import ipackaccess_registers, ipackaccess
import getpass
import logging
import socket
import sys

username = getpass.getuser()
hostname = socket.gethostname()

if sys.platform == 'win32':
    log_file = f"C:/Users/{username}/nrgmodbus.log"

else:
    from os.path import expanduser, join
    log_file = join(expanduser("~"), "nrgmodbus.log")

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | [%(module)s:%(lineno)d] | %(message)s'
)

file_handler.setFormatter(formatter)
