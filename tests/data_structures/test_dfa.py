import pytest
from src.data_structures.dfa import DFA


def test_is_valid() -> None:
    Q: set[str] = {"q0", "q1", "q2", "q3", "q4"}
    T: set[str] = {"a", "b"}
    delta: dict[tuple[str, str], str] = {
        ("q0", "a"): "q1",
        ("q0", "b"): "q0",
        ("q1", "a"): "q2",
        ("q1", "b"): "q3",
        ("q2", "a"): "q4",
        ("q2", "b"): "q3",
        ("q3", "a"): "q4",
        ("q3", "b"): "q0",
        ("q4", "a"): "q4",
        ("q4", "b"): "q4",
    }
    q0 = "q0"
    qf: set[str] = {"q4"}

    dfa = DFA(Q, T, delta, q0, qf)

    assert dfa.is_valid()


def test_is_not_valid() -> None:
    Q: set[str] = {"q0", "q1", "q2"}
    T: set[str] = {"0", "1"}
    delta: dict[tuple[str, str], str] = {
        ("q0", "0"): "q0",
        ("q0", "1"): "q1",
        ("q1", "0"): "q3",
        ("q1", "1"): "q1",
        ("q2", "0"): "q2",
        ("q2", "1"): "q2",
    }
    q0 = "q0"
    qf: set[str] = {"q2"}

    with pytest.raises(expected_exception=ValueError):
        DFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)


def test_draw() -> None:
    Q: set[str] = {"q0", "q1", "q2", "q3", "q4"}
    T: set[str] = {"a", "b"}
    delta: dict[tuple[str, str], str] = {
        ("q0", "a"): "q1",
        ("q0", "b"): "q0",
        ("q1", "a"): "q2",
        ("q1", "b"): "q3",
        ("q2", "a"): "q4",
        ("q2", "b"): "q3",
        ("q3", "a"): "q4",
        ("q3", "b"): "q0",
        ("q4", "a"): "q4",
        ("q4", "b"): "q4",
    }
    q0 = "q0"
    qf: set[str] = {"q4"}

    dfa = DFA(Q, T, delta, q0, qf)
    dfa.draw(filename="tmp/test_dfa test_draw")
