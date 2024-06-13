import sys
from loguru import logger
logger.remove()

logger.add("05 Log.txt", level="TRACE")
logger.add(sys.stderr, level="TRACE")

logger.trace("This is a trace message")
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.success("This is a success message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

