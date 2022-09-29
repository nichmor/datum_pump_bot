from dotenv import load_dotenv

load_dotenv('.env', override=True)
from bot.app import app

def main() -> None:
    
    print('ready')
    app.run()

if __name__ == '__main__':
    main()