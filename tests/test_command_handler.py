import unittest

from command_handler import (
    build_welcome_payload,
    get_bot_response,
    get_help_text,
    get_quick_actions,
    should_exit,
)


class CommandHandlerTests(unittest.TestCase):
    def test_help_text_lists_supported_commands(self):
        help_text = get_help_text()

        self.assertIn("- Crop status", help_text)
        self.assertIn("- Soil status", help_text)
        self.assertIn("- Exit", help_text)

    def test_quick_actions_match_welcome_payload(self):
        payload = build_welcome_payload()

        self.assertEqual(payload["title"], "AgriFlow Assistant")
        self.assertEqual(payload["quick_actions"], get_quick_actions())
        self.assertEqual(payload["quick_actions"][0], "Help")

    def test_blank_message_prompts_for_input(self):
        response = get_bot_response("", [])

        self.assertEqual(response, "Please type a question so I can help with your farm update.")

    def test_history_uses_current_command_history(self):
        response = get_bot_response("history", ["weather", "soil status"])

        self.assertEqual(response, "Command History:\n1. weather\n2. soil status")

    def test_history_ignores_current_history_request_when_present_in_list(self):
        response = get_bot_response("history", ["weather", "history"])

        self.assertEqual(response, "Command History:\n1. weather")

    def test_detected_topic_returns_matching_response(self):
        response = get_bot_response("weather update", [])

        self.assertTrue(response.startswith("Weather Update:"))

    def test_plural_topic_words_are_supported(self):
        response = get_bot_response("Do you have any farming tips?", [])

        self.assertTrue(response.startswith("Agriculture Tip:"))

    def test_partial_words_do_not_trigger_topic_matches(self):
        response = get_bot_response("watermelon prices", [])

        self.assertEqual(response, "Command not recognized. Try 'help' to see what you can ask.")

    def test_time_substrings_do_not_trigger_topic_matches(self):
        response = get_bot_response("timestamp issue", [])

        self.assertEqual(response, "Command not recognized. Try 'help' to see what you can ask.")

    def test_unknown_prompt_returns_helpful_fallback(self):
        response = get_bot_response("tell me more", [])

        self.assertEqual(response, "Command not recognized. Try 'help' to see what you can ask.")

    def test_welcome_payload_mentions_typing_and_prompts(self):
        payload = build_welcome_payload()

        self.assertIn("type your own question", payload["message"].lower())
        self.assertIn("suggested prompts", payload["message"].lower())

    def test_should_exit_matches_whole_words(self):
        self.assertTrue(should_exit("exit"))
        self.assertTrue(should_exit("please quit now"))
        self.assertFalse(should_exit("exciting farm update"))


if __name__ == "__main__":
    unittest.main()
