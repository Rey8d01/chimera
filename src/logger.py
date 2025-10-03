import logging

from .config import settings

logger = logging.getLogger("AppLogger")
logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
