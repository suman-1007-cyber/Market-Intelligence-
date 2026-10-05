"""Central tool registry for agents."""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolDefinition:
    """Registered callable tool."""

    name: str
    description: str
    handler: Callable[..., Any]
    capabilities: tuple[str, ...] = ()


class ToolRegistry:
    """Deterministic registry of approved tools."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"Tool not registered: {name}") from exc

    def has(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> list[str]:
        return sorted(self._tools)

    def invoke(self, name: str, **kwargs: Any) -> Any:
        return self.get(name).handler(**kwargs)
