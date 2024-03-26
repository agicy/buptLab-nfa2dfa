from data_structures.nfa import NFA
from data_structures.dfa import DFA
from collections import deque

__all__: list[str] = ["transfer_nfa_to_dfa"]


def _to_string(fs: frozenset[str]) -> str:
    return "[" + ", ".join(sorted(fs)) + "]"


def transfer_nfa_to_dfa(nfa: NFA) -> DFA:
    tmp_Q: set[frozenset[str]] = set()
    tmp_T: set[str] = nfa.T
    tmp_delta: dict[tuple[frozenset[str], str], frozenset[str]] = {}
    tmp_q0: frozenset[str] = frozenset([nfa.q0])

    tmp_Q.add(tmp_q0)
    unprocessed_states = deque(iterable=[tmp_q0])

    while unprocessed_states:
        current_state: frozenset[str] = unprocessed_states.popleft()
        for symbol in nfa.T:
            tmp_set: set[str] = set()
            for substate in current_state:
                if (substate, symbol) in nfa.delta:
                    tmp_set.update(nfa.delta[(substate, symbol)])
            next_state = frozenset(tmp_set)
            tmp_delta[(current_state, symbol)] = next_state
            if next_state not in tmp_Q:
                tmp_Q.add(next_state)
                unprocessed_states.append(next_state)

    Q: set[str] = {_to_string(fs=state) for state in tmp_Q}
    delta: dict[tuple[str, str], str] = {}
    for key, value in tmp_delta.items():
        delta[(_to_string(fs=key[0]), key[1])] = _to_string(fs=value)
    q0: str = _to_string(fs=tmp_q0)
    qf: set[str] = {
        _to_string(fs=state) for state in tmp_Q if nfa.qf.intersection(state)
    }
    return DFA(Q=Q, T=tmp_T, delta=delta, q0=q0, qf=qf)
