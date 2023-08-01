from laktory._logger import get_logger

logger = get_logger(__name__)


# --------------------------------------------------------------------------- #
# Utilities                                                                   #
# --------------------------------------------------------------------------- #

def is_pipeline():
    try:
        import dlt
    except (ModuleNotFoundError, FileNotFoundError):
        return False
    dbr_version = spark.conf.get("pipelines.dbrVersion", None)
    if dbr_version is None:
        return False
    return True


# --------------------------------------------------------------------------- #
# Readers                                                                     #
# --------------------------------------------------------------------------- #

def read(*args, catalog=None, database=None, **kwargs):
    try:
        import dlt
        return dlt.read(*args, **kwargs)
    except (ModuleNotFoundError, FileNotFoundError):
        table_name = args[0]
        if database is not None:
            table_name = f"{database}.{table_name}"
        if catalog is not None:
            table_name = f"{catalog}.{table_name}"
        return spark.read.table(table_name)


def read_stream(*args, catalog=None, database=None, fmt="delta", **kwargs):
    try:
        import dlt
        return dlt.read_stream(*args, **kwargs)
    except (ModuleNotFoundError, FileNotFoundError):
        table_name = args[0]
        if database is not None:
            table_name = f"{database}.{table_name}"
        if catalog is not None:
            table_name = f"{catalog}.{table_name}"
        return spark.readStream.format(fmt).table(table_name)


# --------------------------------------------------------------------------- #
# Decorators                                                                  #
# --------------------------------------------------------------------------- #

try:
    import dlt

    table = dlt.table
    view = dlt.view
    expect = dlt.expect
    expect_or_drop = dlt.expect_or_drop
    expect_or_fail = dlt.expect_or_fail
    expect_all = dlt.expect_all
    expect_all_or_drop = dlt.expect_all_or_drop
    expect_all_or_fail = dlt.expect_all_or_fail

except (ModuleNotFoundError, FileNotFoundError):

    def table(*table_args, **table_kwargs):

        def decorator(func):
            def wrapper(*args, **kwargs):
                logger.info(f"Running {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def view(*view_args, **view_kwargs):

        def decorator(func):
            def wrapper(*args, **kwargs):
                logger.info(f"Running {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def expect(*table_args, **table_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def expect_or_drop(*table_args, **table_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def expect_or_fail(*table_args, **table_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def expect_all(*table_args, **table_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def expect_all_or_drop(*table_args, **table_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def expect_all_or_fail(*table_args, **table_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
