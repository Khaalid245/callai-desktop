"""
Speaker Module Unit Tests
Verifies voice property configurations, speech synthesis queue triggers,
and crash-isolation boundaries under mocked pyttsx3 engines.
"""

from unittest.mock import MagicMock, patch
import pytest
from src.speaker import VoiceSpeaker


@patch("pyttsx3.init")
def test_speaker_initialization_success(mock_init: MagicMock):
    """
    Verifies that the speaker initializes pyttsx3 engine and sets speed/volume.
    """
    mock_engine = MagicMock()
    mock_init.return_value = mock_engine

    # Instantiate speaker
    speaker = VoiceSpeaker()

    # Assertions
    assert speaker._engine == mock_engine
    mock_init.assert_called_once()
    mock_engine.setProperty.assert_any_call("rate", 160)
    mock_engine.setProperty.assert_any_call("volume", 1.0)


@patch("pyttsx3.init")
def test_speaker_initialization_failure(mock_init: MagicMock):
    """
    Verifies that speaker handles initialization failure (e.g. driver missing) without crashing.
    """
    # Force pyttsx3.init to raise an Exception
    mock_init.side_effect = Exception("SAPI5 initialization failed")

    # Instantiate speaker - should not raise exception
    speaker = VoiceSpeaker()

    # Assertions
    assert speaker._engine is None
    mock_init.assert_called_once()


@patch("pyttsx3.init")
def test_speak_calls_engine(mock_init: MagicMock):
    """
    Verifies that speak() calls say() and runAndWait() on the pyttsx3 engine.
    """
    mock_engine = MagicMock()
    mock_init.return_value = mock_engine
    speaker = VoiceSpeaker()

    # Trigger speak
    speaker.speak("Hello World")

    # Assertions
    mock_engine.say.assert_called_once_with("Hello World")
    mock_engine.runAndWait.assert_called_once()


@patch("pyttsx3.init")
def test_speak_handles_runtime_exceptions(mock_init: MagicMock):
    """
    Verifies that speak() handles engine say/run runtime exceptions gracefully without crashing.
    """
    mock_engine = MagicMock()
    mock_init.return_value = mock_engine
    # Force engine.say to raise a runtime Exception
    mock_engine.say.side_effect = Exception("Audio channel blocked")

    speaker = VoiceSpeaker()

    # Call speak - should catch the exception and complete cleanly
    speaker.speak("Test voice crash safety")

    # Assertions
    mock_engine.say.assert_called_once()
    # runAndWait should not be called if say fails
    mock_engine.runAndWait.assert_not_called()


@patch("pyttsx3.init")
def test_speak_fallback_when_engine_none(mock_init: MagicMock):
    """
    Verifies that if the engine is None (failed initialization), speak() safely skips audio calls.
    """
    mock_init.side_effect = Exception("Driver missing")
    speaker = VoiceSpeaker()

    assert speaker._engine is None

    # Call speak - should complete without crash or raising errors
    speaker.speak("Visual only speech text")
