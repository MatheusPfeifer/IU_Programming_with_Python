import logging
import sys

# Configure logging to record error messages to a file
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def exception_handler(func):
    """
    Decorator to capture exceptions and log error messages.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            print("Error: File not found. Please check the file path.")
        except ValueError as e:
            logging.error(f"Value error: {e}")
            print("Error: An invalid value was encountered.")
        except KeyError as e:
            logging.error(f"Key error: {e}")
            print("Error: Key not found in dictionary or DataFrame.")
        except Exception as e:
            logging.error(f"Unhandled exception: {e}", exc_info=True)
            print(f"An unexpected error occurred: {e}")
    return wrapper
