from bot.app import app
from dotenv import load_dotenv

def main() -> None:
    load_dotenv()
    print('ready')
    app.run()

if __name__ == '__main__':
    main()