import os


_PREFIX = 'TWCOL_'


def current_env():
    return os.environ.get(_PREFIX + 'ENV', 'dev')


def env(var):
    suffix = {
        'dev': '_DEV',
        'stage': '_STAGE',
        'prod': '_PROD'
    }.get(current_env(), '_DEV')

    varname = _PREFIX + var + suffix

    if varname not in os.environ:
        raise ValueError(f"Variable {varname} not found in environment variables")

    return os.environ[varname]
