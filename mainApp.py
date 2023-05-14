from ModuloCells import HashedEnvelopedCellCombo

m = HashedEnvelopedCellCombo()
m.generate_hashed_cell_output(1, 1)
print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
m.generate_hashed_cell_output(1, 0)
print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
m.generate_hashed_cell_output(0, 1)
print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
m.generate_hashed_cell_output(0, 0)
print(f"g:: {m.gi_or_bi1_ifk0}  a:: {m.ai_ifk1}  h:: {m.hi_or_ai_ifk0}  p:: {m.pi_or_bi1_ifk1}")
