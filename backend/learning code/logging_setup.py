'''
-> now you can use this logging_setup in 100 different projects.
-> you can change log_file, level accoding to the messages you want to send and then run the function

'''
import logging

def setup_logger(name, log_file='main.log', level=logging.DEBUG):
    # create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler (optional, for debugging)
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(
            '%(name)s - %(levelname)s - %(message)s'
        )
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    return logger