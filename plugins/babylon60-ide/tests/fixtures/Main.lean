set_option warningAsError true
def wrap (x : UInt32) : UInt32 := x + 1
theorem zero_succ : wrap 0 = 1 := by rfl
