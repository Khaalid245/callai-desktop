"""
Speech Module
Manages microphone hardware interaction and transcribes spoken audio.
Provides a clean abstraction to capture voice commands asynchronously.
"""

from typing import Optional
import speech_recognition as sr


class VoiceListener:
    """
    Handles system microphone interaction and speech-to-text conversion.
    Encapsulates ambient noise calibration and recognition error boundaries.
    """

    def __init__(self) -> None:
        # Initialize the core SpeechRecognition recognizer engine
        self._recognizer = sr.Recognizer()
        
        # Configure thresholds to handle ambient background sounds cleanly
        self._recognizer.dynamic_energy_threshold = True

    def listen(self) -> Optional[str]:
        """
        Calibrates for ambient noise, captures a brief voice input, and transcribes it.
        Returns:
            str: The transcribed clean text in lowercase if successful,
            None: If transcription fails or if there are microphone issues.
        """
        # Step 1: Open the microphone hardware interface
        try:
            microphone = sr.Microphone()
        except (OSError, AttributeError) as err:
            # Handle cases where PyAudio fails to initialize or no microphonic hardware exists
            print(f"\n[ERROR] Microphone hardware unavailable: {err}")
            print("Please ensure a functioning microphone is connected and configured in Windows.")
            return None

        # Step 2: Capture audio stream from the microphone
        try:
            with microphone as source:
                print("\nCalibrating for background noise... (Please be quiet)")
                # Adjust threshold for 1 second to filter out room hums/static
                self._recognizer.adjust_for_ambient_noise(source, duration=1.0)
                
                print("Listening for your command... (Speak now)")
                # Listen with a timeout (how long to wait before starting to speak)
                # and a phrase time limit (maximum length of a spoken command)
                audio_data = self._recognizer.listen(
                    source, 
                    timeout=5.0, 
                    phrase_time_limit=5.0
                )
        except sr.WaitTimeoutError:
            # Triggered if the user did not start speaking within the 5.0 seconds timeout
            print("[INFO] Listening timed out. No speech detected.")
            return None
        except OSError as err:
            # General system audio recording failures
            print(f"\n[ERROR] Audio recording error: {err}")
            return None

        # Step 3: Transcribe captured audio into text
        try:
            print("Processing audio...")
            # Query the Google Web Speech API for fast, zero-configuration online transcription
            transcription = self._recognizer.recognize_google(audio_data)
            
            # Return cleaned, standard lowercase transcription
            return transcription.strip().lower()
            
        except sr.UnknownValueError:
            # Triggered when Google API succeeds but cannot convert the audio wave into words
            print("[WARNING] Could not understand the audio. Please speak clearly.")
            return None
        except sr.RequestError as err:
            # Triggered when network/connection issues prevent reaching the Google Speech API
            print(f"[ERROR] Internet/API connection failed: {err}")
            print("Please check your internet connection and try again.")
            return None
        except Exception as err:
            # General fallback for unexpected transcription engine exceptions
            print(f"[ERROR] An unexpected speech error occurred: {err}")
            return None
