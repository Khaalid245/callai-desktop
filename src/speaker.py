"""
Speaker Module
Manages offline Text-to-Speech (TTS) voice synthesis.
Uses the pyttsx3 library (Windows SAPI5) to provide verbal notifications.
"""

import sys
import pyttsx3


class VoiceSpeaker:
    """
    Handles speech synthesis for assistant verbal feedback.
    Encapsulates speed controls and wraps audio calls to prevent crashes on sound failure.
    """

    def __init__(self) -> None:
        self._engine = None
        try:
            # Initialize offline SAPI5 speech engine
            self._engine = pyttsx3.init()
            
            # Configure a friendly, natural-sounding voice speed
            # Standard rate is 200 (which is fast), we slow it down to 160.
            self._engine.setProperty("rate", 160)
            
            # Set volume to maximum
            self._engine.setProperty("volume", 1.0)
        except Exception as err:
            # Handle audio driver failures gracefully so the assistant doesn't crash on sound errors
            print(f"\n[WARNING] Voice output engine failed to initialize: {err}")
            print("The application will proceed in visual-only mode.")

    def speak(self, text: str) -> None:
        """
        Queues and verbally synthesizes the provided text.
        Prints the text to the terminal and speaks it.
        Args:
            text (str): The message text to speak.
        """
        # Always output visually to stdout first
        print(f"[ASSISTANT VOICE] {text}")

        # Skip speaking if the audio engine failed to load (visual fallback)
        if not self._engine:
            return

        try:
            # Queue the spoken text
            self._engine.say(text)
            # Process the queued say() instructions synchronously
            self._engine.runAndWait()
        except Exception as err:
            # Catch unexpected sound synthesis driver exceptions
            print(f"\n[WARNING] Failed to play audio feedback: {err}")
