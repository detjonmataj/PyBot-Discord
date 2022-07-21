from utils.PyBot import PyBot
from dotenv import load_dotenv
from os import environ as env


def main() -> None:
    load_dotenv()
    token: str = env["TOKEN"]
    prefix: str = env["PREFIX"]
    PyBot(token, prefix)


if __name__ == '__main__':
    main()
