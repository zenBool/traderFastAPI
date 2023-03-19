import os

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount('/assets', StaticFiles(directory='binance_autotrader_front/assets'), name='static')

templates = Jinja2Templates(directory='binance_autotrader_front/templates')

from binance_autotrader_front.routes import home