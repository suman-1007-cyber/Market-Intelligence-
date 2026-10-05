"""Agent contracts and capability declarations."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentContract:
    """Machine-readable contract describing an agent."""

    agent_id: str
    name: str
    version: str
    description: str
    capabilities: tuple[str, ...] = ()
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    required_context: tuple[str, ...] = ()

    def validate_input(self, data: Any) -> bool:
        """Basic deterministic contract validation."""
        schema_type = self.input_schema.get("type")

        if schema_type == "object":
            return isinstance(data, dict)

        if schema_type == "list":
            return isinstance(data, list)

        if schema_type == "string":
            return isinstance(data, str)

        if schema_type == "number":
            return isinstance(data, (int, float)) and not isinstance(data, bool)

        return True

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities
