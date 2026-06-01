"""
Main Entry Point
Initializes the system components, injects dependencies,
and manages the interactive text-based console loop.
"""

import sys
from src.automation import OSAutomator
from src.commands import CommandProcessor
from src.intent_resolver import IntentResolver
from src.speech import VoiceListener
from src.speaker import VoiceSpeaker


def main() -> None:
    """
    Main function to run the CLI loop.
    Coordinates initialization and user interaction.
    """
    # Print welcome banner and instructions
    print("=" * 60)
    print("      AI VOICE-CONTROLLED DESKTOP ASSISTANT - CLI MODE      ")
    print("=" * 60)
    print("Enter a command to control your desktop.")
    print("Available commands:")
    print(" - 'open notepad'")
    print(" - 'open calculator'")
    print(" - 'open chrome'")
    print(" - 'open google'")
    print(" - 'exit'")
    print("-" * 60)

    # Initialize components using dependency injection:
    # 1. Instantiate the OS interaction boundary (OSAutomator).
    automator = OSAutomator()
    # 2. Instantiate the voice output speaker (VoiceSpeaker).
    speaker = VoiceSpeaker()
    # 3. Inject OSAutomator and VoiceSpeaker into the CommandProcessor.
    processor = CommandProcessor(automator, speaker)
    # 4. Instantiate the Intent Resolver to standardize raw phrase inputs.
    intent_resolver = IntentResolver()

    # Choose Input Mode: Text or Voice
    print("\nSelect input mode:")
    print(" 1. Text Mode (Keyboard Input)")
    print(" 2. Voice Mode (Microphone Input)")
    mode_choice = input("Enter choice (1 or 2, default is 1): ").strip()
    
    voice_mode = (mode_choice == "2")
    # 4. Instantiate the Voice Listener only if voice mode is chosen.
    voice_listener = VoiceListener() if voice_mode else None
    
    if voice_mode:
        print("\n>>> Voice Mode Activated <<<")
    else:
        print("\n>>> Text Mode Activated <<<")

    # Announce that the system is ready verbally
    speaker.speak("System online.")

    # Enter the interactive command evaluation loop
    while True:
        try:
            if voice_mode:
                # Capture spoken voice audio and transcribe it
                command_input = voice_listener.listen()
                if command_input is None:
                    # Skip matching if the speech was unrecognized or microphone failed
                    continue
                print(f"Captured Speech: \"{command_input}\"")
            else:
                # Read text input from user with standard prompt
                command_input = input("\n> ")
        except (KeyboardInterrupt, EOFError):
            # Gracefully handle console terminations (like Ctrl+C or Ctrl+D)
            print("\nExiting Desktop Assistant. Goodbye!")
            sys.exit(0)

        # Skip execution if the user pressed Enter without typing anything
        if not command_input.strip():
            continue

        # Resolve natural language variations to a canonical command
        canonical_command = intent_resolver.resolve(command_input)
        # Route the canonical command to the command processor
        result = processor.process_command(canonical_command)

        # Print the resulting outcome message to the console
        if result.success:
            print(f"[SUCCESS] {result.message}")
        else:
            print(f"[ERROR] {result.message}")

        # Check if the execution returned an exit command signal
        if result.is_exit:
            sys.exit(0)


if __name__ == "__main__":
    main()
