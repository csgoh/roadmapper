import unittest
from unittest.mock import MagicMock, patch
from roadmapper.ai import generate_roadmap_code


class TestAI(unittest.TestCase):
    @patch("roadmapper.ai.OpenAI")
    def test_generate_roadmap_code(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content="```python\nprint('Hello World')\n```"))
        ]
        mock_client.chat.completions.create.return_value = mock_completion

        # Execute
        code = generate_roadmap_code("Create a roadmap", "fake-api-key")

        # Verify
        self.assertEqual(code, "print('Hello World')")
        mock_client.chat.completions.create.assert_called_once()

        # Verify prompt structure
        args, kwargs = mock_client.chat.completions.create.call_args
        self.assertEqual(kwargs["model"], "gpt-4o")
        self.assertEqual(len(kwargs["messages"]), 2)
        self.assertEqual(kwargs["messages"][0]["role"], "system")
        self.assertEqual(kwargs["messages"][1]["role"], "user")
        self.assertIn("Roadmapper API Examples", kwargs["messages"][0]["content"])

if __name__ == "__main__":
    unittest.main()
