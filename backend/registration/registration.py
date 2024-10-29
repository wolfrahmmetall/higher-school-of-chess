from fastapi import FastAPI
from pkgs.config import Settings

app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)

@app.get('/')
def hello_api():
    return {'msg':'hello_api'}