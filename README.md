# AI Voice-Controlled Desktop Assistant

A professional, modular desktop assistant designed to accept voice commands, interpret user actions, launch applications/websites, and control desktop activities. The codebase is built with clean architecture principles to allow seamless integration of AI modules and hardware sensors in later phases.

## Project Objectives
1. **Voice Commands**: Capture and process audio voice commands (to be implemented in future phases).
2. **Action Interpreter**: Understand commands and map them to desktop and web tasks.
3. **Application Control**: Open and control local desktop applications.
4. **Web Automation**: Browse and open user-requested websites.
5. **Desktop Control**: Command core desktop actions (e.g. system status, volume, etc.).
6. **Extensible Integration**: Designed from the ground up to support advanced AI models and sensor hardware.

## Project Structure
```text
voice-assistant/
│
├── docs/             # Documentation, designs, architecture docs
├── src/              # Application source code
├── tests/            # Unit and integration tests
├── .gitignore        # Git ignore rules for Python/IDEs
├── README.md         # Project documentation (this file)
└── requirements.txt  # Python package dependencies
```

## Environment Setup

### Prerequisites
- Python 3.12.x
- pip 24.x or higher
- Git

### Installation
1. Clone the repository and navigate to the project directory:
   ```powershell
   git clone <repository_url>
   cd callai-desktop
   ```

2. Create and activate a Python virtual environment:
   ```powershell
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment (Windows PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

3. Install development and project dependencies:
   ```powershell
   python -m pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

## Running Tests
To run the automated suite:
```powershell
.\.venv\Scripts\pytest
```