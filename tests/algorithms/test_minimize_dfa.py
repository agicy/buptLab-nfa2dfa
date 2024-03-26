from src.data_structures.dfa import DFA
from src.algorithms.minimize_dfa import minimize_dfa


def test_miniminze_dfa() -> None:
    Q: set[str] = {"q0", "q1", "q2", "q3", "q4"}
    T: set[str] = {"a", "b"}
    delta: dict[tuple[str, str], str] = {
        ("q0", "a"): "q1",
        ("q0", "b"): "q1",
        ("q1", "a"): "q2",
        ("q1", "b"): "q3",
        ("q2", "a"): "q4",
        ("q2", "b"): "q4",
        ("q3", "a"): "q4",
        ("q3", "b"): "q4",
        ("q4", "a"): "q4",
        ("q4", "b"): "q4",
    }
    q0 = "q0"

    qf: set[str] = {"q4"}

    dfa = DFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)
    miniminzed_dfa: DFA = minimize_dfa(dfa=dfa)
    dfa.draw(filename="tmp/test_minimize_dfa org")
    miniminzed_dfa.draw(filename="tmp/test_minimize_dfa min")
