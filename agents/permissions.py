"""Agent permission enforcement."""

from dataclasses import dataclass, field


@dataclass
class PermissionPolicy:
    """Allow-list policy for an agent."""

    agent_id: str
    allowed_tools: set[str] = field(default_factory=set)
    allowed_agents: set[str] = field(default_factory=set)

    def allows_tool(self, tool_name: str) -> bool:
        return tool_name in self.allowed_tools

    def allows_agent(self, agent_id: str) -> bool:
        return agent_id in self.allowed_agents


class PermissionEngine:
    """Central deterministic permission engine."""

    def __init__(self) -> None:
        self._policies: dict[str, PermissionPolicy] = {}

    def register(self, policy: PermissionPolicy) -> None:
        if policy.agent_id in self._policies:
            raise ValueError(
                f"Permission policy already registered: {policy.agent_id}"
            )
        self._policies[policy.agent_id] = policy

    def check_tool(self, agent_id: str, tool_name: str) -> bool:
        policy = self._policies.get(agent_id)
        return bool(policy and policy.allows_tool(tool_name))

    def check_agent(self, agent_id: str, target_agent: str) -> bool:
        policy = self._policies.get(agent_id)
        return bool(policy and policy.allows_agent(target_agent))

    def get_policy(self, agent_id: str) -> PermissionPolicy:
        try:
            return self._policies[agent_id]
        except KeyError as exc:
            raise KeyError(
                f"No permission policy for agent: {agent_id}"
            ) from exc
