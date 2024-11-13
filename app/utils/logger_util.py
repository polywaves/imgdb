import colorlog
import sys

logger = colorlog.getLogger(__name__)
logger.setLevel(colorlog.DEBUG)
formatter = colorlog.ColoredFormatter("%(blue)sLOGGER %(levelname)s: %(message)s")

stream_handler = colorlog.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)