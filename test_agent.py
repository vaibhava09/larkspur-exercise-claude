import unittest
from types import SimpleNamespace
from unittest.mock import patch

import agent


class Build2LocalTests(unittest.TestCase):
    def test_local_tool_schema_and_registration(self):
        tools = agent.tool_list()
        names = [tool["name"] for tool in tools]
        self.assertEqual(len(names), 10)
        self.assertEqual(len(names), len(set(names)))
        self.assertIs(agent.LOCAL_TOOLS["next_available_day"], agent.next_available_day)
        schema = next(tool for tool in tools if tool["name"] == "next_available_day")
        self.assertGreaterEqual(len(schema["description"]), 40)
        self.assertEqual(schema["input_schema"]["required"], ["origin", "dest", "date"])

    def test_local_dispatch_preserves_tool_id(self):
        response = SimpleNamespace(content=[
            SimpleNamespace(type="tool_use", name="next_available_day",
                            id="test-call", input={"origin": "DEN", "dest": "AUS",
                                                   "date": "2025-05-08"})
        ])
        with patch.object(agent.mcp_client, "tool_names", set()), \
                patch.object(agent, "call_local", return_value="2025-05-09") as call:
            result = agent.tool_results(response)
        call.assert_called_once_with(agent.next_available_day, "next_available_day",
                                     response.content[0].input)
        self.assertEqual(result, [{"type": "tool_result", "tool_use_id": "test-call",
                                   "content": "2025-05-09"}])


if __name__ == "__main__":
    unittest.main()
