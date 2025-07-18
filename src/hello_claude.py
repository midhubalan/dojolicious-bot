import marimo

__generated_with = "0.14.11"
app = marimo.App()

with app.setup:
    # Initialization code that runs before all other cells
    from typing import Literal, Iterable

    import marimo as mo

    from anthropic import Anthropic

    AntModel = Literal[
        "claude-opus-4-0",
        "claude-sonnet-4-0",
        "claude-3-7-sonnet-latest",
        "claude-3-5-sonnet-latest",
        "claude-3-5-haiku-latest",
    ]

    MessageKey = Literal["role", "content"]

    Message = dict[MessageKey, str]

    Role = Literal["user", "assistant"]

    client = Anthropic()


@app.class_definition
class MyChat:
    def __init__(
        self,
        *,
        model: AntModel = "claude-3-5-haiku-latest",
        stream: bool = False,
        system: str | None = None,
        stop_sequences: list[str] | None = None
    ) -> None:
        self._messages = []
        self.client = client
        self._model = model 
        self._stream = stream
        self._system = system
        self._stop_sequences = stop_sequences

    def reset_chat(self)->None:
        self._messages = []

    def tail(self, n: int = 2) -> list[Message]:
        if len(self._messages) < n:
            return [msg for msg in self._messages]
        else:
            return [msg for msg in self._messages[-n:]]

    def head(self, n: int = 2) -> list[Message]:
        if len(self._messages) < n:
            return [msg for msg in self._messages]
        else:
            return [msg for msg in self._messages[:n]]

    def all(self) -> Iterable[Message]:
        return (msg for msg in self._messages)

    def _append_message(self, role: Role, content: str) -> None:
        self._messages.append({"role": role, "content": content})

    def add_user_message(self, content: str) -> None:
        self._append_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        self._append_message("assistant", content)

    def send_messages(
        self,
        *,
        system: str | None = None,
        stop_sequences: list[str] | None = None,
    ):
        params = {
            "model": self._model,
            "max_tokens": 1024,
            "messages": self._messages,
        }
        if sys_param := system or self._system :
            params["system"] = sys_param
        if stop_seq := stop_sequences or self._stop_sequences :
            params["stop_sequences"] = stop_seq
        # pyrefly: ignore  # bad-argument-type
        with client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
        message = stream.get_final_message()
        # pyrefly: ignore  # missing-attribute
        self.add_assistant_message( message.content[0].text)


@app.cell
def _():
    quantum_chat = MyChat()
    quantum_chat.add_user_message("Define quantum computing in one sentence")
    quantum_chat.send_messages()
    quantum_chat.add_user_message("Write another sentence")
    quantum_chat.send_messages()
    return (quantum_chat,)


@app.cell
def _(quantum_chat):
    quantum_chat.reset_chat()

    quantum_chat.add_user_message("How do I solve 5x + 2 = 3 for x?")
    quantum_chat.send_messages()

    quantum_chat.reset_chat()

    quantum_chat.add_user_message("How do I solve 5x + 2 = 3 for x?")
    quantum_chat.send_messages(
        system="""
        You are a patient math tutor.
        Do not directly answer a student's questions.
        Guide them to a solution step by step.
        """)
    return


@app.cell
def _():
    code_chat = MyChat( system="""
    You're a helpful coding assistant. 
    When asked for help just provide the code that solves the problem. 
    Do not explain the code, unless you are explicitly asked to do so by the user.
    """)
    code_chat.add_user_message("Write a python function that checks a string for duplicate characters.")
    code_chat.send_messages()
    return (code_chat,)


@app.cell
def _(code_chat):
    code_chat.add_user_message((
        "How can I implement a singleton in python. "
        "Explain the code in a sentence."
    ))
    code_chat.send_messages()
    return


@app.cell
def _():
    struct_chat = MyChat()
    struct_chat.add_user_message("Write a three different gcloud cli commands. Each should be very short")
    struct_chat.add_assistant_message("Here are all three commands with no comments in a single code block:\n```bash")
    struct_chat.send_messages(stop_sequences=["```"])
    return


if __name__ == "__main__":
    app.run()
