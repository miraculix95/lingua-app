"""Minimal record-and-replay double for openai.OpenAI.

Matches the shape used by the codebase::

    client.chat.completions.create(model=..., messages=..., ...)

Each response can be:
- a plain string -> goes into ``choices[0].message.content``
- a dict with key ``"tool_arguments"`` -> goes into
  ``choices[0].message.tool_calls[0].function.arguments`` (modern API)
- a dict with key ``"function_arguments"`` -> goes into
  ``choices[0].message.function_call.arguments`` (legacy, kept for old tests)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class _FunctionPayload:
    arguments: str
    name: str = ""


@dataclass
class _ToolCall:
    function: _FunctionPayload
    id: str = "call_fake"
    type: str = "function"


@dataclass
class _Message:
    content: str | None = None
    function_call: Any = None
    tool_calls: list[_ToolCall] | None = None


@dataclass
class _Choice:
    message: _Message


@dataclass
class _Response:
    choices: list[_Choice]


@dataclass
class _CompletionsAPI:
    parent: FakeOpenAIClient

    def create(self, **kwargs: Any) -> _Response:
        self.parent.calls.append(kwargs)
        idx = self.parent._cursor % len(self.parent.responses)
        self.parent._cursor += 1
        raw = self.parent.responses[idx]
        if isinstance(raw, str):
            return _Response([_Choice(_Message(content=raw))])
        if isinstance(raw, dict) and "tool_arguments" in raw:
            tool = _ToolCall(function=_FunctionPayload(arguments=raw["tool_arguments"]))
            return _Response([_Choice(_Message(tool_calls=[tool]))])
        if isinstance(raw, dict) and "function_arguments" in raw:
            return _Response(
                [_Choice(_Message(function_call=_FunctionPayload(arguments=raw["function_arguments"])))]
            )
        raise TypeError(f"Unsupported response type: {type(raw)}")


@dataclass
class _ChatAPI:
    completions: _CompletionsAPI


@dataclass
class FakeOpenAIClient:
    responses: list[Any]
    calls: list[dict] = field(default_factory=list)
    _cursor: int = 0
    chat: _ChatAPI = field(init=False)

    def __post_init__(self) -> None:
        self.chat = _ChatAPI(completions=_CompletionsAPI(parent=self))
