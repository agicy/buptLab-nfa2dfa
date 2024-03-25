from graphviz import Digraph

__all__: list[str] = ["NFA"]


class NFA:
    def __init__(
        self,
        Q: set[str],
        T: set[str],
        delta: dict[tuple[str, str], set[str]],
        q0: str,
        qf: set[str],
    ) -> None:
        self.Q: set[str] = Q
        self.T: set[str] = T
        self.delta: dict[tuple[str, str], set[str]] = delta
        self.q0: str = q0
        self.qf: set[str] = qf

        print(self.delta)

        if not self.is_valid():
            raise ValueError("Invalid NFA definition")

    def is_valid(self) -> bool:
        for state in self.Q:
            if not state:
                return False

        for symbol in self.T:
            if not symbol:
                return False

        for key, value in self.delta.items():
            if key[0] not in self.Q or key[1] not in self.T:
                return False
            if not value.issubset(self.Q):
                return False

        if self.q0 not in self.Q:
            return False

        if not self.qf.issubset(self.Q):
            return False

        return True

    def draw(self, filename: str) -> None:
        g = Digraph(name="NFA", filename=filename, format="svg")
        g.graph_attr["rankdir"] = "LR"

        for q in self.Q:
            if q in self.qf:
                g.attr(kw="node", shape="doublecircle")
            else:
                g.attr(kw="node", shape="circle")
            g.node(name=q)

        g.attr(kw="node", shape="none")
        g.node(name="")

        g.edge(tail_name="", head_name=self.q0)

        for (q1, t), qs in self.delta.items():
            for q2 in qs:
                g.edge(
                    tail_name=q1,
                    head_name=q2,
                    label=t,
                )

        g.view()
