import matplotlib
import logging

logger = logging.getLogger(__name__)

def configure_matplotlib():
    """
    Configures matplotlib to use a non-interactive backend ('Agg'),
    which is essential for running in a web server environment.
    """

    try:
        matplotlib.use('Agg')
        logger.info("Matplotlib backend set to 'Agg'.")
    except Exception as e:
        logger.error(f"Failed to set matplotlib backend: {e}")
