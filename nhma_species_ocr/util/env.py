import os
from decouple import Config, RepositoryEnv


env_config = Config(RepositoryEnv(os.path.join(os.path.dirname(__file__), '../../.env')))