"""
Speech Module Unit Tests
Validates the transcription pipelines and error handling logic
in speech.py under mocked microphone and API conditions.
"""

from unittest.mock import MagicMock, patch
import pytest
import speech_recognition as sr
from src.speech import VoiceListener


@pytest.fixture
def listener() -> VoiceListener:
    """
    Fixture providing an instance of VoiceListener.
    """
    return VoiceListener()


@patch("speech_recognition.Microphone")
def test_listen_success(mock_microphone: MagicMock, listener: VoiceListener):
    """
    Verifies successful microphone capture and transcription.
    """
    # Setup mocks for Recognizer and Google Web Speech API
    mock_audio = MagicMock()
    listener._recognizer.listen = MagicMock(return_value=mock_audio)
    listener._recognizer.adjust_for_ambient_noise = MagicMock()
    listener._recognizer.recognize_google = MagicMock(return_value="  START NOTEPAD  ")

    # Call listen()
    result = listener.listen()

    # Assertions
    assert result == "start notepad"  # Verifies spaces trimmed and lowercase
    listener._recognizer.adjust_for_ambient_noise.assert_called_once()
    listener._recognizer.listen.assert_called_once()
    listener._recognizer.recognize_google.assert_called_once_with(mock_audio)


@patch("speech_recognition.Microphone")
def test_listen_unknown_value_error(mock_microphone: MagicMock, listener: VoiceListener):
    """
    Verifies graceful error handling when Google cannot understand speech audio.
    """
    mock_audio = MagicMock()
    listener._recognizer.listen = MagicMock(return_value=mock_audio)
    listener._recognizer.adjust_for_ambient_noise = MagicMock()
    # Force recognize_google to throw UnknownValueError
    listener._recognizer.recognize_google = MagicMock(side_effect=sr.UnknownValueError())

    result = listener.listen()

    assert result is None
    listener._recognizer.recognize_google.assert_called_once()


@patch("speech_recognition.Microphone")
def test_listen_request_error(mock_microphone: MagicMock, listener: VoiceListener):
    """
    Verifies graceful handling of internet/API request connection errors.
    """
    mock_audio = MagicMock()
    listener._recognizer.listen = MagicMock(return_value=mock_audio)
    listener._recognizer.adjust_for_ambient_noise = MagicMock()
    # Force recognize_google to throw RequestError
    listener._recognizer.recognize_google = MagicMock(
        side_effect=sr.RequestError("Connection failed")
    )

    result = listener.listen()

    assert result is None


@patch("speech_recognition.Microphone")
def test_listen_timeout_error(mock_microphone: MagicMock, listener: VoiceListener):
    """
    Verifies graceful handling when the listener times out waiting for speech.
    """
    listener._recognizer.adjust_for_ambient_noise = MagicMock()
    # Force listen() to raise WaitTimeoutError
    listener._recognizer.listen = MagicMock(side_effect=sr.WaitTimeoutError())

    result = listener.listen()

    assert result is None


@patch("speech_recognition.Microphone")
def test_listen_microphone_hardware_error(mock_mic_class: MagicMock, listener: VoiceListener):
    """
    Verifies graceful handling when no working microphone hardware exists on the host OS.
    """
    # Force Microscope class instantiation to raise an OSError
    mock_mic_class.side_effect = OSError("No microphone found")

    result = listener.listen()

    assert result is None
