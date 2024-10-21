import logging
import openai


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    openai_logger = logging.getLogger("openai")
    httpx_logger = logging.getLogger("httpx")
    openai_logger.setLevel(logging.CRITICAL)
    httpx_logger.setLevel(logging.CRITICAL)
