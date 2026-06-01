"""
Automation Module
Interacts with the host Windows Operating System using standard libraries.
Defines functions to launch local applications and navigate to web URLs.
"""

import os
import subprocess
import webbrowser
from typing import Optional


class OSAutomator:
    """
    Handles OS-level application launching and automation tasks.
    Encapsulates subprocess invocation and web browser protocols.
    """

    def open_notepad(self) -> bool:
        """
        Launches the Windows Notepad application.
        Returns:
            bool: True if launched successfully, False otherwise.
        """
        try:
            # subprocess.Popen runs notepad.exe asynchronously as a background process.
            # Using Popen ensures the python script does not block waiting for Notepad to close.
            subprocess.Popen(["notepad.exe"])
            return True
        except FileNotFoundError:
            # Fallback if notepad.exe is not in the system PATH.
            return False

    def open_calculator(self) -> bool:
        """
        Launches the Windows Calculator application.
        Returns:
            bool: True if launched successfully, False otherwise.
        """
        try:
            # calc.exe is the standard executable name for the Windows calculator.
            # Launches asynchronously to prevent blocking.
            subprocess.Popen(["calc.exe"])
            return True
        except FileNotFoundError:
            return False

    def open_chrome(self) -> bool:
        """
        Launches the Google Chrome application.
        First tries launching via PATH/Registry using os.startfile,
        then falls back to common absolute Windows paths.
        Returns:
            bool: True if launched successfully, False otherwise.
        """
        # First attempt: Try os.startfile. This leverages Windows shell execution
        # which automatically looks up registered app locations in the registry.
        try:
            os.startfile("chrome.exe")
            return True
        except FileNotFoundError:
            pass

        # Second attempt: Check standard installation directories on Windows
        standard_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for path in standard_paths:
            if os.path.exists(path):
                try:
                    subprocess.Popen([path])
                    return True
                except Exception:
                    pass

        # If not found anywhere, notify failure
        return False

    def open_url(self, url: str) -> bool:
        """
        Opens a URL in the system's default web browser.
        Args:
            url (str): The web address to open (must start with http:// or https://).
        Returns:
            bool: True if browser was successfully invoked, False otherwise.
        """
        try:
            # webbrowser.open triggers the OS default browser to navigate to the specified URL.
            # This is cross-platform and honors user settings.
            webbrowser.open(url)
            return True
        except Exception:
            return False
