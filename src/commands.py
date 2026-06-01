"""
Commands Module
Implements the Command Processing logic using a registry pattern.
Decouples command recognition from actual execution.
"""

from typing import Callable, Dict, Tuple
from src.automation import OSAutomator
from src.speaker import VoiceSpeaker


class CommandResult:
    """
    Standardized wrapper for command execution outcomes.
    Carries success status, user-facing message, and exit signal flags.
    """
    def __init__(self, success: bool, message: str, is_exit: bool = False):
        # success: Indicates whether the action ran without OS/system failure.
        self.success = success
        # message: User-facing text describing the result.
        self.message = message
        # is_exit: Signal flag telling the CLI main loop to terminate.
        self.is_exit = is_exit


class CommandProcessor:
    """
    Parses and dispatches incoming user commands via an internal registry map.
    Eliminates long if-elif-else branches by associating commands directly with methods.
    """

    def __init__(self, automator: OSAutomator, speaker: VoiceSpeaker):
        # Inject the OSAutomator dependency to decouple command logic from system calls.
        self._automator = automator
        # Inject the VoiceSpeaker dependency to support verbal voice feedback.
        self._speaker = speaker
        
        # Define the Registry mapping commands (normalized strings) to action callables.
        # This keeps the command dispatcher extensible and easy to modify.
        self._registry: Dict[str, Callable[[], Tuple[bool, str]]] = {
            "open chrome": self._handle_open_chrome,
            "open calculator": self._handle_open_calculator,
            "open notepad": self._handle_open_notepad,
            "open google": self._handle_open_google,
            "exit": self._handle_exit,
        }

    def process_command(self, command_text: str) -> CommandResult:
        """
        Cleans the input text, finds matches in the registry, and runs them.
        Args:
            command_text (str): Raw string received from user input.
        Returns:
            CommandResult: Structured execution output.
        """
        # Normalize: trim surrounding whitespace and convert to lowercase for uniform comparison.
        normalized = command_text.strip().lower()

        # Check if normalized command exists in registry mapping.
        if normalized in self._registry:
            # Retrieve the callable handler and execute it.
            handler = self._registry[normalized]
            success, msg, *extra = handler()
            is_exit = extra[0] if extra else False
            return CommandResult(success=success, message=msg, is_exit=is_exit)
        else:
            # Speak the error message verbally
            self._speaker.speak("Sorry, I don't recognize that command.")
            # Handle unknown commands gracefully without crashing the system.
            return CommandResult(
                success=False,
                message=f"Unknown command: '{command_text}'. Please try 'open notepad', 'open chrome', 'open calculator', 'open google', or 'exit'."
            )

    # Individual handler wrappers.
    # Each returns: (success_status: bool, user_message: str, [optional] is_exit: bool)

    def _handle_open_chrome(self) -> Tuple[bool, str]:
        # Verbally announce action before execution
        self._speaker.speak("Opening Chrome.")
        if self._automator.open_chrome():
            return True, "Successfully launched Google Chrome browser."
        return False, "Failed to launch Google Chrome browser (application not found)."

    def _handle_open_calculator(self) -> Tuple[bool, str]:
        self._speaker.speak("Opening Calculator.")
        if self._automator.open_calculator():
            return True, "Successfully launched Calculator."
        return False, "Failed to launch Calculator (application not found)."

    def _handle_open_notepad(self) -> Tuple[bool, str]:
        self._speaker.speak("Opening Notepad.")
        if self._automator.open_notepad():
            return True, "Successfully launched Notepad."
        return False, "Failed to launch Notepad (application not found)."

    def _handle_open_google(self) -> Tuple[bool, str]:
        self._speaker.speak("Opening Google.")
        if self._automator.open_url("https://www.google.com"):
            return True, "Successfully opened Google (https://www.google.com) in default browser."
        return False, "Failed to open default web browser."

    def _handle_exit(self) -> Tuple[bool, str, bool]:
        self._speaker.speak("Goodbye.")
        # Returns True status, farewell message, and True for the is_exit flag.
        return True, "Exiting Desktop Assistant. Goodbye!", True
