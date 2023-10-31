import logging
from functools import wraps

logging.addLevelName(77, 'GRID_OBJECT')
logger = logging.getLogger('GRID_OBJECT')
file_handler = logging.FileHandler('grid_engine/_grid_object/_grid_object.log', 'w')
file_handler.setLevel(77)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.setLevel(77)

def log_method(func):
    import inspect
    frame = inspect.currentframe().f_back
    caller = inspect.getmodule(frame).__name__
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f'{caller}.{func.__name__}({args}, {kwargs})')
        return func(*args, **kwargs)

    return wrapper

def log_class(cls):
    import inspect
    frame = inspect.currentframe().f_back
    caller = inspect.getmodule(frame).__name__
    logger.debug(f'Caller: {caller}')
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        setattr(cls, name, log_method(method))
    return cls
