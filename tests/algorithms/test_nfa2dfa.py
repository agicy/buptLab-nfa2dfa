import pytest
from src.data_structures.dfa import DFA
from src.data_structures.nfa import NFA
from src.algorithms.nfa2dfa import transfer_nfa_to_dfa


def test_nfa2dfa() -> None:
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

    nfa: NFA = NFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)
    nfa.draw(filename="tmp/test_nfa2dfa pic1_nfa")
    dfa: DFA = transfer_nfa_to_dfa(nfa=nfa)
    dfa.draw(filename="tmp/test_nfa2dfa pic2_dfa")
    assert nfa.is_valid() == True
    assert dfa.is_valid() == True
