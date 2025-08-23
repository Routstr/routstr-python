import openai

from routstr import patch_openai

client = patch_openai(
    openai.OpenAI(
        base_url="http://localhost:8000/v1",
    )
)


def chat() -> None:
    history: list = []
    while True:
        user_msg = {"role": "user", "content": input("\nYou: ")}
        history.append(user_msg)
        ai_msg = {"role": "assistant", "content": ""}

        for chunk in client.chat.completions.create(
            model="meta-llama/llama-3.2-1b-instruct",
            messages=history,
            stream=True,
        ):
            if len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content is not None:
                    ai_msg["content"] += content
                    print(content, end="", flush=True)
        print()
        history.append(ai_msg)


if __name__ == "__main__":
    chat()
