# ============================================
# Mia Alejandra Fuentes Mérida, 23775 
# Leonardo Dufrey Mejía Mejía, 23648 
# María José Girón Isidro, 23559 
# ============================================

EPSILON = 'ε'
ENDMARKER = '$'


def parse_grammar(grammar_text):
    """
    Formato esperado:
    E  -> T E'
    E' -> + T E' | ε
    T  -> F T'
    T' -> * F T' | ε
    F  -> ( E ) | id
    """
    grammar = {}

    lines = grammar_text.strip().split('\n')
    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue

        if '->' not in line:
            raise ValueError(
                f"Linea {line_number}: falta '->' en la produccion: {line}"
            )

        left, right = line.split('->', 1)
        left = left.strip()
        if not left:
            raise ValueError(
                f"Linea {line_number}: no terminal izquierdo vacio en: {line}"
            )

        productions = right.strip().split('|')

        if left not in grammar:
            grammar[left] = []

        for prod in productions:
            symbols = prod.strip().split()
            if not symbols:
                raise ValueError(
                    f"Linea {line_number}: produccion vacia para {left}. "
                    "Usa ε si corresponde."
                )
            grammar[left].append(symbols)

    if not grammar:
        raise ValueError("La gramatica esta vacia.")

    return grammar


class GrammarAnalyzer:
    def __init__(self, grammar, start_symbol=None):
        self.grammar = grammar
        self.non_terminals = set(grammar.keys())
        self.terminals = self._find_terminals()
        self.first = {nt: set() for nt in self.non_terminals}
        self.follow = {nt: set() for nt in self.non_terminals}

        # Si no se especifica, usa el primer no terminal en el orden de entrada
        self.start_symbol = start_symbol if start_symbol is not None else next(iter(grammar))
        if self.start_symbol not in self.non_terminals:
            raise ValueError(
                f"El simbolo inicial '{self.start_symbol}' no existe en la gramatica."
            )

    def _find_terminals(self):
        terminals = set()

        for left in self.grammar:
            for production in self.grammar[left]:
                for symbol in production:
                    if symbol not in self.grammar and symbol != EPSILON:
                        terminals.add(symbol)

        return terminals

    def first_of_sequence(self, symbols):
        """
        Calcula FIRST de una secuencia de símbolos.
        """
        result = set()

        # Si la secuencia esta vacia va a retornar epsilon
        if not symbols:
            result.add(EPSILON)
            return result

        for symbol in symbols:
            if symbol in self.terminals:
                result.add(symbol)
                return result

            elif symbol == EPSILON:
                result.add(EPSILON)
                return result

            elif symbol in self.non_terminals:
                result.update(self.first[symbol] - {EPSILON})

                if EPSILON in self.first[symbol]:
                    continue
                else:
                    return result

        result.add(EPSILON)
        return result

    def compute_first(self):
        changed = True

        while changed:
            changed = False

            for non_terminal in self.grammar:
                for production in self.grammar[non_terminal]:
                    before = len(self.first[non_terminal])

                    if production == [EPSILON]:
                        self.first[non_terminal].add(EPSILON)
                    else:
                        seq_first = self.first_of_sequence(production)
                        self.first[non_terminal].update(seq_first)

                    after = len(self.first[non_terminal])
                    if after > before:
                        changed = True

    def compute_follow(self):
        # Regla 1: agregar $ al FOLLOW del simbolo inicial
        self.follow[self.start_symbol].add(ENDMARKER)

        changed = True
        while changed:
            changed = False

            for left in self.grammar:
                for production in self.grammar[left]:
                    for i in range(len(production)):
                        symbol = production[i]

                        if symbol in self.non_terminals:
                            beta = production[i + 1:]  # lo que sigue después del simbolo
                            first_beta = self.first_of_sequence(beta)

                            before = len(self.follow[symbol])

                            # Agregar FIRST(beta) sin epsilon
                            self.follow[symbol].update(first_beta - {EPSILON})

                            # Si beta produce epsilon o beta esta vacia,
                            # agregar FOLLOW(left)
                            if not beta or EPSILON in first_beta:
                                self.follow[symbol].update(self.follow[left])

                            after = len(self.follow[symbol])
                            if after > before:
                                changed = True

    def print_sets(self):
        print("No terminales:", sorted(self.non_terminals))
        print("Terminales:", sorted(self.terminals))
        print()

        print("FIRST:")
        for nt in sorted(self.first):
            print(f"FIRST({nt}) = {{ {', '.join(sorted(self.first[nt]))} }}")

        print()

        print("FOLLOW:")
        for nt in sorted(self.follow):
            print(f"FOLLOW({nt}) = {{ {', '.join(sorted(self.follow[nt]))} }}")


# =========================
# Ejemplo 
# =========================
if __name__ == "__main__":
    grammar_text = """
    E  -> T E'
    E' -> + T E' | ε
    T  -> F T'
    T' -> * F T' | ε
    F  -> ( E ) | id
    """

    grammar = parse_grammar(grammar_text)

    analyzer = GrammarAnalyzer(grammar)
    analyzer.compute_first()
    analyzer.compute_follow()
    analyzer.print_sets()