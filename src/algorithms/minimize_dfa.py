from data_structures.dfa import DFA

__all__: list[str] = ["minimize_dfa"]


def _hopcroft(dfa: DFA) -> list[set[str]]:
    P: list[set[str]] = [dfa.qf, dfa.Q - dfa.qf]
    W: list[set[str]] = [dfa.qf]
    while W:
        A: set[str] = W.pop()
        for c in dfa.T:
            X = set(q for q in dfa.Q if (q, c) in dfa.delta and dfa.delta[(q, c)] in A)
            for Y in P[:]:
                if X & Y and (Y - X) & Y:
                    P.remove(Y)
                    P.append(X & Y)
                    P.append((Y - X) & Y)
                    if Y in W:
                        W.remove(Y)
                        W.append(X & Y)
                        W.append((Y - X) & Y)
                    else:
                        if len(X & Y) <= len((Y - X) & Y):
                            W.append(X & Y)
                        else:
                            W.append((Y - X) & Y)
    return P


def minimize_dfa(dfa: DFA) -> DFA:
    partition: list[set[str]] = _hopcroft(dfa=dfa)
    partition.reverse()
    dic: dict[str, str] = {
        state: f"q{i}"
        for i, subset in enumerate(iterable=partition)
        for state in subset
    }
    Q: set[str] = set(dic.values())
    T: set[str] = dfa.T
    delta: dict[tuple[str, str], str] = {
        (dic[state], symbol): dic[dfa.delta[(state, symbol)]]
        for state in dfa.Q
        for symbol in dfa.T
    }
    q0: str = dic[dfa.q0]
    qf: set[str] = {dic[state] for state in dfa.qf}
    return DFA(Q=Q, T=T, delta=delta, q0=q0, qf=qf)
