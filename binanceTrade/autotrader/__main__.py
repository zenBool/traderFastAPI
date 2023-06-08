# Запуск autotrader как отдельный пакет (без фронта)
from .trader import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass