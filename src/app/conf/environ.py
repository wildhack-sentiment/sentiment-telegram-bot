import environ
import os.path

env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

if os.path.exists('app/.env'):
    environ.Env.read_env('app/.env')

__all__ = [
    env,
]
