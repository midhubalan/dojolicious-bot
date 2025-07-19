# Initialization code that runs before all other cells
from typing import Iterable, Union

from ._types import Role, MessageCreateParams, ModelParam, Content

from anthropic import Anthropic

from anthropic.types import (
    MessageParam,
    # MessageCreateParams,
    TextBlockParam,
)

client = Anthropic()


class AntChat:
    def __init__(
        self,
        *,
        model: ModelParam = "claude-3-5-haiku-latest",
        stream: bool = True,
        system: Union[str, Iterable[TextBlockParam]] | None = None,
        stop_sequences: list[str] | None = None,
    ) -> None:
        self._messages: list[MessageParam] = []
        self._client = client
        self._model = model
        self._stream = stream
        self._system = system
        self._stop_sequences = stop_sequences

    def reset(self) -> None:
        self._messages = []

    def tail(self, n: int = 2) -> list[MessageParam]:
        if len(self._messages) < n:
            return [msg for msg in self._messages]
        else:
            return [msg for msg in self._messages[-n:]]

    def head(self, n: int = 2) -> list[MessageParam]:
        if len(self._messages) < n:
            return [msg for msg in self._messages]
        else:
            return [msg for msg in self._messages[:n]]

    def _get_last_message_content(self, role: Role) -> Content:
        if len(self._messages) == 0:
            raise LookupError("no messages in chat")
        for msg in self._messages[::-1]:
            if msg["role"] == role:
                return msg["content"]
        raise LookupError("no prompt or response found in chat")

    def get_last_prompt(self) -> Content:
        return self._get_last_message_content("user")

    def get_last_response(self) -> Content:
        return self._get_last_message_content("assistant")

    def all(self) -> Iterable[MessageParam]:
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
        params: MessageCreateParams = {
            "model": self._model,
            "max_tokens": 1024,
            "messages": self._messages,
        }
        if sys_param := system or self._system:
            params["system"] = sys_param
        if stop_seq := stop_sequences or self._stop_sequences:
            params["stop_sequences"] = stop_seq
        # pyrefly: ignore  # bad-argument-type
        with self._client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
        message = stream.get_final_message()
        # pyrefly: ignore  # missing-attribute
        self.add_assistant_message(message.content[0].text)


def main():
    struct_chat = AntChat()
    struct_chat.add_user_message(
        (
            "Write a three different gcloud cli commands. "
            "Each should be very short"
        )
    )
    struct_chat.add_assistant_message(
        (
            "Here are all three commands with no comments "
            "in a single code block:\n```bash"
        )
    )
    struct_chat.send_messages(stop_sequences=["```"])

    print(struct_chat.get_last_response())
    print(struct_chat.get_last_prompt())


if __name__ == "__main__":
    main()
