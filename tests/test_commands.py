"""
Command Dispatcher Unit Tests
Verifies text input normalization, command registry lookup,
and dispatch routing using mocks to avoid spawning real system processes.
"""

from unittest.mock import MagicMock
import pytest
from src.commands import CommandProcessor, CommandResult
from src.automation import OSAutomator
from src.speaker import VoiceSpeaker


@pytest.fixture
def mock_automator() -> MagicMock:
    """
    Fixture providing a mocked instance of OSAutomator.
    Prevents unit tests from launching GUI applications on the runner OS.
    """
    return MagicMock(spec=OSAutomator)


@pytest.fixture
def mock_speaker() -> MagicMock:
    """
    Fixture providing a mocked instance of VoiceSpeaker to insulate audio card triggers.
    """
    return MagicMock(spec=VoiceSpeaker)


@pytest.fixture
def processor(mock_automator: MagicMock, mock_speaker: MagicMock) -> CommandProcessor:
    """
    Fixture providing a CommandProcessor injected with mocked automator and speaker.
    """
    return CommandProcessor(automator=mock_automator, speaker=mock_speaker)


def test_process_command_open_notepad_success(processor: CommandProcessor, mock_automator: MagicMock):
    """
    Verifies that 'open notepad' correctly calls OSAutomator.open_notepad and returns success.
    """
    # Setup mock behavior
    mock_automator.open_notepad.return_value = True

    # Call test method
    result: CommandResult = processor.process_command("open notepad")

    # Assertions
    assert result.success is True
    assert "notepad" in result.message.lower()
    assert result.is_exit is False
    mock_automator.open_notepad.assert_called_once()
    # Verify exact spoken feedback was called
    processor._speaker.speak.assert_called_once_with("Opening Notepad.")


def test_process_command_open_notepad_failure(processor: CommandProcessor, mock_automator: MagicMock):
    """
    Verifies graceful error propagation if Notepad fails to launch.
    """
    # Setup mock behavior to fail (e.g., executable missing on OS)
    mock_automator.open_notepad.return_value = False

    # Call test method
    result: CommandResult = processor.process_command("open notepad")

    # Assertions
    assert result.success is False
    assert "not found" in result.message.lower()
    mock_automator.open_notepad.assert_called_once()
    processor._speaker.speak.assert_called_once_with("Opening Notepad.")


def test_process_command_open_calculator(processor: CommandProcessor, mock_automator: MagicMock):
    """
    Verifies that 'open calculator' invokes OSAutomator.open_calculator.
    """
    mock_automator.open_calculator.return_value = True

    result: CommandResult = processor.process_command("open calculator")

    assert result.success is True
    assert "calculator" in result.message.lower()
    mock_automator.open_calculator.assert_called_once()
    processor._speaker.speak.assert_called_once_with("Opening Calculator.")


def test_process_command_open_chrome(processor: CommandProcessor, mock_automator: MagicMock):
    """
    Verifies that 'open chrome' invokes OSAutomator.open_chrome.
    """
    mock_automator.open_chrome.return_value = True

    result: CommandResult = processor.process_command("open chrome")

    assert result.success is True
    assert "chrome" in result.message.lower()
    mock_automator.open_chrome.assert_called_once()
    processor._speaker.speak.assert_called_once_with("Opening Chrome.")


def test_process_command_open_google(processor: CommandProcessor, mock_automator: MagicMock):
    """
    Verifies that 'open google' invokes OSAutomator.open_url with Google's home page URL.
    """
    mock_automator.open_url.return_value = True

    result: CommandResult = processor.process_command("open google")

    assert result.success is True
    assert "google" in result.message.lower()
    mock_automator.open_url.assert_called_once_with("https://www.google.com")
    processor._speaker.speak.assert_called_once_with("Opening Google.")


def test_process_command_exit(processor: CommandProcessor):
    """
    Verifies that 'exit' returns the exit signal flag.
    """
    result: CommandResult = processor.process_command("exit")

    assert result.success is True
    assert result.is_exit is True
    assert "goodbye" in result.message.lower()
    processor._speaker.speak.assert_called_once_with("Goodbye.")


def test_process_command_case_insensitivity_and_whitespace(processor: CommandProcessor, mock_automator: MagicMock):
    """
    Verifies that command matching is case-insensitive and trims whitespaces correctly.
    """
    mock_automator.open_notepad.return_value = True

    # Check mixed case and leading/trailing spacing
    result: CommandResult = processor.process_command("   OpEn nOtEpAd  ")

    assert result.success is True
    assert result.is_exit is False
    mock_automator.open_notepad.assert_called_once()
    processor._speaker.speak.assert_called_once_with("Opening Notepad.")


def test_process_command_unknown(processor: CommandProcessor):
    """
    Verifies that unsupported input returns success=False and does not trigger exceptions.
    """
    result: CommandResult = processor.process_command("open spotify")

    assert result.success is False
    assert "unknown command" in result.message.lower()
    assert result.is_exit is False
    processor._speaker.speak.assert_called_once_with("Sorry, I don't recognize that command.")
