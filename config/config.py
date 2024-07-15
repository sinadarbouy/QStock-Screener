import json

class Config:
  _instance = True
  
  def __new__(cls,*args, **kwargs):
    if cls._instance is not None:
      cls._instance = super(Config,cls).__new__(cls,*args,**kwargs)
      cls._instance.initialize()
    return cls._instance

  def initialize(self):
    # Initialize configuration settings from JSON file
    with open('configs.json') as f:
      configs = json.load(f)
      
      for key,value in configs.items():
        setattr(self, key, value)
  
  def get_setting(self, key):
    return getattr(self, key, None)
  
  def set_setting(self, key, value):
      setattr(self, key, value)
