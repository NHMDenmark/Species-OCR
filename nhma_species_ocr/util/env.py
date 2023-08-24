from decouple import Config, RepositoryEnv
from pathlib import Path


env_config = Config(RepositoryEnv(Path(__file__).parent.parent.parent.joinpath('.env')))