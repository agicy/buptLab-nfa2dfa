import pytest
from src.data_structures.epsilon_nfa import EpsilonNFA


def test_is_valid() -> None:
    Q: set[str] = {"p", "q", "r"}
    T: set[str] = {"a", "b", "c"}
    delta: dict[tuple[str, str], set[str]] = {
        ("p", ""): set(),
        ("p", "a"): {"p"},
        ("p", "b"): {"q"},
        ("p", "c"): {"r"},
        ("q", ""): {"p"},
        ("q", "a"): {"q"},
        ("q", "b"): {"r"},
        ("q", "c"): set(),
        ("r", ""): {"q"},
        ("r", "a"): {"r"},
        ("r", "b"): set(),
        ("r", "c"): {"p"},
    }
    q0 = "p"
    qf: set[str] = {"r"}

    epsilon_nfa = EpsilonNFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)
    assert epsilon_nfa.is_valid() == True


def test_is_invalid() -> None:

    Q: set[str] = {"p", "q", "r"}
    T: set[str] = {"a", "b", "c"}
    delta: dict[tuple[str, str], set[str]] = {
        ("p", ""): set(),
        ("p", "a"): {"p"},
        ("p", "b"): {"q"},
        ("p", "c"): {"r"},
        ("q", ""): {"p"},
        ("q", "a"): {"q"},
        ("q", "b"): {"r"},
        ("q", "c"): set(),
        ("r", ""): {"q"},
        ("r", "a"): {"r"},
        ("r", "b"): set(),
        ("r", "c"): {"p"},
    }
    q0 = "x"
    qf: set[str] = {"r"}

    with pytest.raises(expected_exception=ValueError):
        EpsilonNFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)


def test_draw() -> None:
    Q: set[str] = {"p", "q", "r"}
    T: set[str] = {"a", "b", "c"}
    delta: dict[tuple[str, str], set[str]] = {
        ("p", ""): set(),
        ("p", "a"): {"p"},
        ("p", "b"): {"q"},
        ("p", "c"): {"r"},
        ("q", ""): {"p"},
        ("q", "a"): {"q"},
        ("q", "b"): {"r"},
        ("q", "c"): set(),
        ("r", ""): {"q"},
        ("r", "a"): {"r"},
        ("r", "b"): set(),
        ("r", "c"): {"p"},
    }
    q0 = "p"
    qf: set[str] = {"r"}

    epsilon_nfa = EpsilonNFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)
    epsilon_nfa.draw(filename="tmp/test_epsilon_nfa test_draw")
