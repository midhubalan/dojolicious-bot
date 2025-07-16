import marimo

__generated_with = "0.14.11"
app = marimo.App()


@app.cell
def _():
    from functools import partial
    from typing import Literal

    from anthropic import (
        Anthropic,
        # AsyncAnthropic,
    )
    return Anthropic, Literal, partial


@app.cell
def _(Anthropic):
    client = Anthropic()
    model = "claude-sonnet-4-0"
    return client, model


@app.cell
def _(Literal, partial):
    Role = Literal['user', 'assistant']

    def append_message(messages, *, role: Role,  content: str):
      messages.append({"role": role, "content": content})
      return messages

    add_user_message = partial(append_message, role='user')
    add_assistant_message = partial(append_message, role='assistant')
    return add_assistant_message, add_user_message


@app.cell
def _(client, model):
    def chat(messages, system=None):
      params = {
        "model":model,
        "max_tokens":1024,
        "messages": messages,
        # stream=True,
      }
      if system:
        params["system"] = system
      message = client.messages.create( **params
        )
      return message.content[0].text
    return (chat,)


@app.cell
def _(client, model):
    def chat_stream(messages, system:str|None=None, stop_sequences:list[str]|None=None):
      params = {
        "model":model,
        "max_tokens":1024,
        "messages": messages,
      }
      if system:
        params["system"] = system
      if stop_sequences:
        params["stop_sequences"] = stop_sequences
      with client.messages.stream(**params) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

        message = stream.get_final_message()
        return message.content[0].text
    return (chat_stream,)


@app.cell
def _(add_assistant_message, add_user_message, chat):
    messages = []
    add_user_message(messages, content="Define quantum computing in one sentence")

    resp = chat(messages)
    print(resp)

    add_assistant_message(messages, content=resp)

    add_user_message(messages, content="Write another sentence")

    add_assistant_message(messages, content=chat(messages))

    for message in messages:
      print(message)
    return


@app.cell
def _(add_assistant_message, add_user_message, chat):
    system = "\nYou are a patient math tutor.\nDo not directly answer a student's questions.\nGuide them to a solution step by step.\n"
    messages_1 = []
    add_user_message(messages_1, content='How do I solve 5x + 2 = 3 for x?')
    add_assistant_message(messages_1, content=chat(messages_1))

    for message_1 in messages_1:
        print(message_1)
    print('****' * 5)
    messages_1 = []
    add_user_message(messages_1, content='How do I solve 5x + 2 = 3 for x?')
    add_assistant_message(messages_1, content=chat(messages_1, system))
    for message_1 in messages_1:
        print(message_1)
    return


@app.cell
def _(add_assistant_message, add_user_message, chat_stream):
    messages_2 = []
    user_message = '\nWrite a python function that checks a string for duplicate characters.\n'
    add_user_message(messages_2, content=user_message)
    system_1 = "\n  You're a helpful coding assistant. When asked for help just provide the code that solves the problem. Do not explain the code, unless you are explicitly asked to do so by the user.\n"
    add_assistant_message(messages_2, content=chat_stream(messages_2, system_1))
    for message_2 in messages_2:
        print(message_2)
    print()
    return system_1, user_message


@app.cell
def _(add_assistant_message, add_user_message, chat_stream, system_1):
    messages_2 = []
    user_message = user_message + 'Explain the code in two sentences.'
    add_user_message(messages_2, content=user_message)
    add_assistant_message(messages_2, content=chat_stream(messages_2, system_1))
    for message_2 in messages_2:
        print(message_2)
    return (user_message,)


@app.cell
def _(chat_stream):
    messages=[
            {
                "role": "user",
                "content": "Write a three different gcloud cli commands. Each should be very short"
            },
                    {
                "role": "assistant",
                "content": "Here are all three commands with no comments in a single code block:\n```bash"
            },
        ]

    chat_stream(messages,stop_sequences=["```"])
    return


@app.cell
def _():
    import marimo as mo
    return


if __name__ == "__main__":
    app.run()
