from typing import Literal, Iterable, TypedDict, Union
from typing_extensions import NotRequired, Required

from anthropic.types import (
    MessageParam,
    TextBlockParam,
    DocumentBlockParam,
    ImageBlockParam,
    RedactedThinkingBlockParam,
    ServerToolUseBlockParam,
    ThinkingBlockParam,
    ToolResultBlockParam,
    ToolUseBlockParam,
    WebSearchToolResultBlockParam,
    ContentBlock,
)


Role = Literal["user", "assistant"]

ModelParam = Literal[
    "claude-opus-4-0",
    "claude-sonnet-4-0",
    "claude-3-7-sonnet-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-5-haiku-latest",
]

Content = Union[
    str,
    Iterable[
        Union[
            TextBlockParam,
            ImageBlockParam,
            DocumentBlockParam,
            ThinkingBlockParam,
            RedactedThinkingBlockParam,
            ToolUseBlockParam,
            ToolResultBlockParam,
            ServerToolUseBlockParam,
            WebSearchToolResultBlockParam,
            ContentBlock,
        ]
    ],
]


class MessageCreateParams(TypedDict):
    model: ModelParam
    messages: Iterable[MessageParam]
    max_tokens: int
    stream: NotRequired[Literal[True, False]]
    system: NotRequired[Union[str, Iterable[TextBlockParam]]]
    stop_sequences: NotRequired[list[str]]


class Task(TypedDict):
    task: Required[str]


class EvalRecord(TypedDict):
    output: Content
    test_case: Task
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
