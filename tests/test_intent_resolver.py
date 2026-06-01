"""
Intent Resolver Unit Tests
Validates all variations, aliases, spaces, casing,
and fallback logic inside the IntentResolver module.
"""

import pytest
from src.intent_resolver import IntentResolver


@pytest.fixture
def resolver() -> IntentResolver:
    """
    Fixture providing an instance of IntentResolver.
    """
    return IntentResolver()


def test_resolve_exact_canonicals(resolver: IntentResolver):
    """
    Verifies that standard canonical inputs pass through unchanged.
    """
    assert resolver.resolve("open notepad") == "open notepad"
    assert resolver.resolve("open calculator") == "open calculator"
    assert resolver.resolve("open chrome") == "open chrome"
    assert resolver.resolve("open google") == "open google"
    assert resolver.resolve("exit") == "exit"


def test_resolve_chrome_aliases(resolver: IntentResolver):
    """
    Verifies Chrome aliases correctly resolve to 'open chrome'.
    """
    assert resolver.resolve("launch chrome") == "open chrome"
    assert resolver.resolve("start chrome") == "open chrome"
    assert resolver.resolve("open browser") == "open chrome"


def test_resolve_calculator_aliases(resolver: IntentResolver):
    """
    Verifies Calculator aliases correctly resolve to 'open calculator'.
    """
    assert resolver.resolve("launch calculator") == "open calculator"
    assert resolver.resolve("start calculator") == "open calculator"


def test_resolve_notepad_aliases(resolver: IntentResolver):
    """
    Verifies Notepad aliases correctly resolve to 'open notepad'.
    """
    assert resolver.resolve("launch notepad") == "open notepad"
    assert resolver.resolve("start notepad") == "open notepad"


def test_resolve_google_aliases(resolver: IntentResolver):
    """
    Verifies Google website aliases correctly resolve to 'open google'.
    """
    assert resolver.resolve("go to google") == "open google"
    assert resolver.resolve("launch google") == "open google"


def test_resolve_exit_aliases(resolver: IntentResolver):
    """
    Verifies exit aliases correctly resolve to 'exit'.
    """
    assert resolver.resolve("quit") == "exit"
    assert resolver.resolve("close") == "exit"
    assert resolver.resolve("stop") == "exit"


def test_resolve_normalization(resolver: IntentResolver):
    """
    Verifies case insensitivity and whitespace trimming.
    """
    assert resolver.resolve("   LaUnCh ChRoMe   ") == "open chrome"
    assert resolver.resolve("  GO to GOOGLE  ") == "open google"
    assert resolver.resolve("\tSTART calculator\n") == "open calculator"


def test_resolve_unknown_phrases(resolver: IntentResolver):
    """
    Verifies that unmatched inputs return the normalized input itself.
    """
    assert resolver.resolve("open microsoft word") == "open microsoft word"
    assert resolver.resolve("hello computer") == "hello computer"
    assert resolver.resolve("   invalid command   ") == "invalid command"
