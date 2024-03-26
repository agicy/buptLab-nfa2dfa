import pytest
from src.data_structures.epsilon_nfa import EpsilonNFA
from src.data_structures.nfa import NFA
from src.algorithms.enfa2nfa import transfer_epsilon_nfa_to_nfa


def run_example(epsilon_nfa: EpsilonNFA, id: int) -> None:
    nfa: NFA = transfer_epsilon_nfa_to_nfa(epsilon_nfa=epsilon_nfa)
    epsilon_nfa.draw(filename="tmp/test_enfa2nfa pic1_enfa_" + str(object=id))
    nfa.draw(filename="tmp/test_enfa2nfa pic2_nfa_" + str(object=id))
    assert epsilon_nfa.is_valid()
    assert nfa.is_valid()


def test_enfa2nfa() -> None:
    run_example(
        epsilon_nfa=EpsilonNFA(
            Q={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"},
            T={"a"},
            delta={
                ("q0", "a"): {"q1", "q3"},
                ("q0", ""): {"q2"},
                ("q1", ""): {"q4"},
                ("q2", "a"): {"q5"},
                ("q3", ""): {"q6"},
                ("q5", ""): {"q7"},
                ("q6", ""): {"q2"},
            },
            q0="q0",
            qf={"q4", "q7"},
        ),
        id=1,
    )

    run_example(
        epsilon_nfa=EpsilonNFA(
            Q={"q0", "q1", "q2", "q3", "q4"},
            T={"a", "b"},
            delta={
                ("q4", "a"): {"q1"},
                ("q4", "b"): {"q3"},
                ("q1", ""): {"q2"},
                ("q3", "a"): {"q2"},
                ("q0", ""): {"q4"},
            },
            q0="q0",
            qf={"q2"},
        ),
        id=2,
    )

    run_example(
        epsilon_nfa=EpsilonNFA(
            Q={"q0", "q1", "q2", "q3", "q4"},
            T={"a"},
            delta={
                ("q0", ""): {"q1"},
                ("q1", ""): {"q3"},
                ("q2", ""): {"q4"},
                ("q4", ""): {"q3"},
            },
            q0="q0",
            qf={"q0", "q4"},
        ),
        id=3,
    )
