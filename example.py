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

        history.append(ai_msg)


if __name__ == "__main__":
    chat()
