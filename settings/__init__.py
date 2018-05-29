from decouple import config

if config('ENV') == 'production':
    from .prod import *
else:
    from .dev import *
