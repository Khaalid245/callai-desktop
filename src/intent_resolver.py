"""
Intent Resolver Module
Translates various natural language phrases and commands to canonical forms.
Standardizes user input before it reaches the command parser.
"""

from typing import Dict


class IntentResolver:
    """
    Resolves natural language commands to their standardized system counterparts.
    Maps multiple variations (aliases) to a single canonical action.
    """

    def __init__(self) -> None:
        # Establish the mapping of phrases (lowercased) to standard commands.
        # This acts as our lookup dictionary for incoming phrases.
        self._mappings: Dict[str, str] = {
            # Chrome Browser variations
            "open chrome": "open chrome",
            "launch chrome": "open chrome",
            "start chrome": "open chrome",
            "open browser": "open chrome",

            # Calculator variations
            "open calculator": "open calculator",
            "launch calculator": "open calculator",
            "start calculator": "open calculator",

            # Notepad variations
            "open notepad": "open notepad",
            "launch notepad": "open notepad",
            "start notepad": "open notepad",

            # Google navigation variations
            "open google": "open google",
            "go to google": "open google",
            "launch google": "open google",

            # Exit variations
            "exit": "exit",
            "quit": "exit",
            "close": "exit",
            "stop": "exit",
        }

    def resolve(self, phrase: str) -> str:
        """
        Takes raw user input, normalizes it, and matches it to a canonical command.
        Args:
            phrase (str): Raw string command received from the user.
        Returns:
            str: Resolved canonical command if matched, or the normalized input itself.
        """
        # Trim leading/trailing whitespace and make lowercase to ensure matches are uniform.
        normalized = phrase.strip().lower()

        # Check if the normalized string is matched in our intent dictionary mappings.
        if normalized in self._mappings:
            # Return the canonical value associated with the matched alias key.
            return self._mappings[normalized]

        # If no alias match is found, return the normalized string itself.
        # This fallback ensures downstream command processors can handle unknown phrases gracefully.
        return normalized
