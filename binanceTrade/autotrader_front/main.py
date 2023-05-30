import os

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount('/assets', StaticFiles(directory='autotrader_front/assets'), name='static')

templates = Jinja2Templates(directory='autotrader_front/templates')

from autotrader_front.routes import home