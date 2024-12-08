import logging
import sys
import json


class JsonFormatter(logging.Formatter):
  """Formatter to dump error message into JSON"""

  def format(self, record: logging.LogRecord) -> str:
    record_dict = {
      "level": record.levelname,
      "date": self.formatTime(record),
      "message": record.getMessage(),
      "module": record.module,
      "lineno": record.lineno,
    }

    return json.dumps(record_dict, indent=2)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
formatter = JsonFormatter()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)