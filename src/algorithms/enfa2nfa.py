from data_structures.nfa import NFA
from data_structures.epsilon_nfa import EpsilonNFA
from collections import deque

__all__: list[str] = ["transfer_epsilon_nfa_to_nfa"]


def _epsilon_closure(epsilon_nfa: EpsilonNFA, states: set[str]) -> set[str]:
    epsilon_closure: set[str] = set()
    unprocessed_states: deque[str] = deque()
    for state in states:
        if state not in epsilon_closure:
            epsilon_closure.add(state)
            unprocessed_states.append(state)
    while unprocessed_states:
        current_state: str = unprocessed_states.popleft()
        epsilon_closure.add(current_state)
        if (current_state, "") in epsilon_nfa.delta:
            for state in epsilon_nfa.delta[(current_state, "")]:
                if state not in epsilon_closure:
                    epsilon_closure.add(state)
                    unprocessed_states.append(state)
    return epsilon_closure


def _transfer(epsilon_nfa: EpsilonNFA, states: set[str], symbol: str) -> set[str]:
    result: set[str] = set()
    for current_state in states:
        if (current_state, symbol) in epsilon_nfa.delta:
            result.update(epsilon_nfa.delta[(current_state, symbol)])
    return result


def transfer_epsilon_nfa_to_nfa(epsilon_nfa: EpsilonNFA) -> NFA:
    Q: set[str] = epsilon_nfa.Q
    T: set[str] = epsilon_nfa.T
    delta: dict[tuple[str, str], set[str]] = {}

    for state in Q:
        for symbol in T:
            if symbol != "":
                states: set[str] = _epsilon_closure(
                    epsilon_nfa=epsilon_nfa,
                    states=_transfer(
                        epsilon_nfa=epsilon_nfa,
                        states=_epsilon_closure(
                            epsilon_nfa=epsilon_nfa, states={state}
                        ),
                        symbol=symbol,
                    ),
                )
                if states:
                    delta[(state, symbol)] = states

    q0: str = epsilon_nfa.q0
    qf: set[str] = {
        state
        for state in Q
        if not _epsilon_closure(epsilon_nfa=epsilon_nfa, states={state}).isdisjoint(
            epsilon_nfa.qf
        )
    }

    return NFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)
