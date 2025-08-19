import os
import shutil
import sys


def _check_cdk_cli() -> None:
    if not shutil.which("cdk-cli"):
        print("cdk-cli is not installed. Please install it with:")
        print("cargo install cdk-cli")
        print("Then topup the default wallet.")
        sys.exit(1)

    # check balance
    balance = os.popen("cdk-cli balance").read().strip()
    if not balance or "0 sat" in balance:
        print(
            "Default wallet is empty. "
            "Please topup the wallet using `cdk-cli receive <token>`."
        )
        sys.exit(1)


_check_cdk_cli()


def get_token(value: str = "8") -> str:
    return os.popen(f'printf "0\n{value}\n" | cdk-cli send | tail -n 1').read().strip()


def set_token(token: str) -> None:
    os.popen(f'cdk-cli receive "{token}"').read()
