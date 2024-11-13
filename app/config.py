import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class Envs(Enum):
  Development = 'development'
  Testing = 'testing'
  Stage = 'stage'
  Production = 'production'
  Uknown = 'unknown'

  @classmethod
  def from_string(cl, st: str) -> 'Envs':
    if st == 'development':
      return cl.Development
    elif st == 'testing':
      return cl.Testing
    elif st == 'stage':
      return cl.Stage
    elif st == 'production':
      return cl.Production
    else:
      return cl.Uknown
    
env = Envs.from_string(os.environ['ENV_CONFIG'])


class DevelopmentConfig():
  def __init__(self):
    self.DEBUG = True
    self.TESTING = False


class StageConfig():
  def __init__(self):
    self.DEBUG = False
    self.TESTING = False


class TestingConfig():
  def __init__(self):
    self.DEBUG = True
    self.TESTING = True


config = DevelopmentConfig()
if env == Envs.Development:
  config = DevelopmentConfig()
elif env == Envs.Stage:
  config = StageConfig()
elif env == Envs.Testing:
  config = TestingConfig()
