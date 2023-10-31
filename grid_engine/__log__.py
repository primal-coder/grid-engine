import logging
from functools import wraps

logging.addLevelName(44, 'GRIDENGINE')
logger = logging.getLogger('GRIDENGINE')


def gridengine(message):
    logger.log(44, message)


file_handler = logging.FileHandler('gridengine.log', 'w')
file_handler.setLevel(44)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(module)s - %(message)s'))
logger.addHandler(file_handler)
logger.setLevel(44)
setattr(logger, 'gridengine', gridengine)


def log_method(func):
    import inspect
    frame = inspect.currentframe().f_back
    caller = inspect.getmodule(frame).__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(args[0], object):
            logger.gridengine(f'{func.__name__}({args[0].__class__.__name__})')
            return func(*args, **kwargs)
        logger.gridengine(f'{func.__name__}({args}, {kwargs})')
        return func(*args, **kwargs)

    return wrapper


def log_class(cls):
    import inspect
    frame = inspect.currentframe().f_back
    caller = inspect.getmodule(frame).__name__
    logger.gridengine(f'Caller: {caller}')
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        setattr(cls, name, log_method(method))
    return cls
