import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def exception_handler(func):
    """
    decorator to handle exceptions
    we can also apply circuit braker
    """

    def wrap(*args, **kwargs):
        # storing time before function execution
        try:
            res = func(*args, **kwargs)
            return {
                'detail': 'success',
                'data': res,
                'status_code': 200}

        except TypeError as e:
            return {
                'detail': str(e),
                'data': None,
                'status_code': 500}

        except Exception as e:
            return {
                'detail': str(e.error.message),
                'data': None,
                'status_code': 500}


    return wrap
