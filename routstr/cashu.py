import os


def get_token(value: str = "8") -> str:
    return os.popen(f'printf "0\n{value}\n" | cdk-cli send | tail -n 1').read().strip()


def set_token(token: str) -> None:
    os.popen(f'cdk-cli receive "{token}"').read()
