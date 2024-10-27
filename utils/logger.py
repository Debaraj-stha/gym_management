import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%s",
    format="%(asctime)s %(levelname)s  %(message)s  ",
)
