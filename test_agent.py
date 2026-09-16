import unittest
from types import SimpleNamespace
from unittest.mock import patch

import agent


class Build2MCPTests(unittest.TestCase):
    def test_mcp_tools_have_one_owner(self):
        schemas = [
            {"name": name, "description": "MCP test schema", "input_schema": {}}
            for name in ("next_available_day", "fare_rules")
        ]
        with patch.object(agent.mcp_client, "tools", return_value=schemas) as discover:
            tools = agent.tool_list()
        discover.assert_called_once_with()
        names = [tool["name"] for tool in tools]
        self.assertEqual(len(names), 11)
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(tools, agent.build_tools() + schemas)
        self.assertFalse({"next_available_day", "fare_rules"} & agent.LOCAL_TOOLS.keys())
        self.assertFalse({"next_available_day", "fare_rules"} &
                         {tool["name"] for tool in agent.EXTRA_TOOLS})

    def test_remote_dispatch_preserves_tool_id(self):
        response = SimpleNamespace(content=[
            SimpleNamespace(type="tool_use", name="next_available_day",
                            id="test-call", input={"origin": "DEN", "dest": "AUS",
                                                   "date": "2025-05-08"})
        ])
        with patch.object(agent.mcp_client, "tool_names", {"next_available_day"}), \
                patch.object(agent.mcp_client, "call_remote", return_value="2025-05-09") as call, \
                patch.object(agent, "call_local") as local:
            result = agent.tool_results(response)
        call.assert_called_once_with("next_available_day", response.content[0].input)
        local.assert_not_called()
        self.assertEqual(result, [{"type": "tool_result", "tool_use_id": "test-call",
                                   "content": "2025-05-09"}])


if __name__ == "__main__":
    unittest.main()
