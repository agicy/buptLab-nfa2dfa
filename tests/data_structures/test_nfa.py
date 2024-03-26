import pytest
from src.data_structures.nfa import NFA


def test_is_valid() -> None:
    Q: set[str] = {"q0", "q1", "q2", "q3"}
    T: set[str] = {"a", "b"}
    delta: dict[tuple[str, str], set[str]] = {
        ("q0", "a"): {"q0", "q1"},
        ("q0", "b"): {"q0"},
        ("q1", "a"): {"q2"},
        ("q1", "b"): {"q2"},
        ("q2", "a"): {"q3"},
        ("q2", "b"): {"q3"},
        ("q3", "a"): {"q3"},
        ("q3", "b"): {"q3"},
    }
    q0 = "q0"
    qf: set[str] = {"q3"}

    nfa = NFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)

    assert nfa.is_valid() == True


def test_is_invalid() -> None:
    Q: set[str] = {"q0", "q1", "q2"}
    T: set[str] = {"0", "1"}
    delta: dict[tuple[str, str], set[str]] = {
        ("q0", "0"): {"q0"},
        ("q0", "1"): {"q0", "q3"},
        ("q1", "0"): {"q2"},
    }
    q0 = "q0"
    qf: set[str] = {"q2"}

    with pytest.raises(expected_exception=ValueError):
        NFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)


def test_draw() -> None:
    Q: set[str] = {"q0", "q1", "q2", "q3"}
    T: set[str] = {"a", "b"}
    delta: dict[tuple[str, str], set[str]] = {
        ("q0", "a"): {"q0", "q1"},
        ("q0", "b"): {"q0"},
        ("q1", "a"): {"q2"},
        ("q1", "b"): {"q2"},
        ("q2", "a"): {"q3"},
        ("q2", "b"): {"q3"},
        ("q3", "a"): {"q3"},
        ("q3", "b"): {"q3"},
    }
    q0 = "q0"
    qf: set[str] = {"q3"}

    nfa = NFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)
    nfa.draw(filename="tmp/test_nfa test_draw")
