# from binance_autotrader_front.main import app

if __name__ == '__main__':
    import os

    # os.system('uvicorn run:app --reload --port 5000')
    os.system('uvicorn binance_autotrader_front.main:app --reload --port 5000')
