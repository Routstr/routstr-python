# Routstr Python SDK

## Prerequisites

Before using the Routstr Python SDK, you need to install and set up `cdk-cli`:

1. Install `cdk-cli`:

   ```bash
   cargo install cdk-cli
   ```

2. Top up your default wallet with some balance (required for now, future updates will improve this):

   ```bash
   cdk-cli receive <token>
   ```

## Usage

```python
import openai

from routstr import patch_openai

client = patch_openai(openai.OpenAI())


def chat() -> None:
    history: list = []
    while True:
        user_msg = {"role": "user", "content": input("\nYou: ")}
        history.append(user_msg)
        ai_msg = {"role": "assistant", "content": ""}

        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-1b-instruct", messages=history
        )
        print(response.choices[0].message.content)
        print(response.usage)

        history.append(ai_msg)


if __name__ == "__main__":
    chat()
```
