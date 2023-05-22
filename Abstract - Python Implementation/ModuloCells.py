import BinaryArithmeticUtils as Binary


class HashedEnvelopedCombo:
    # hashed cell output
    gi_or_bi1_ifk0 = None
    ai_ifk1 = None
    hi_or_ai_ifk0 = None
    pi_or_bi1_ifk1 = None
    # enveloped cell output
    gi_prim = None
    hi_prim = None
    pi_prim = None

    def generate_hashed_cell_output(self, a: int, b: int):
        self.gi_or_bi1_ifk0 = a & b  # and
        self.hi_or_ai_ifk0 = a ^ b  # xor
        self.pi_or_bi1_ifk1 = a | b  # or
        self.ai_ifk1 = self.gi_or_bi1_ifk0 | (Binary.negate(a) & Binary.negate(b))  # xnor
        return [self.gi_or_bi1_ifk0, self.ai_ifk1, self.hi_or_ai_ifk0, self.pi_or_bi1_ifk1]

    def generate_enveloped_cell_output(self, bi_prev: int, ai: int):
        self.gi_prim = ai & bi_prev
        self.hi_prim = ai ^ bi_prev
        self.pi_prim = ai | bi_prev
        return [self.gi_prim, self.hi_prim, self.pi_prim]
