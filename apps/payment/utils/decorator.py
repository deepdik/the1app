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
        except Exception as e:
            logger.info("Stripe API Error:-"
                        + str(e)
                        )
            return {
                'detail': e.error.message,
                'data': {},
                'status_code': 400}

    return wrap
