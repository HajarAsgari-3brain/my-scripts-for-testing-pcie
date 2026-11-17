#!/usr/bin/env python3

import subprocess

# ============================================================================
# Configuration
# ============================================================================

BASE_ADDR = 0x80040000

DATA_GEN_MUX_SEL_ADDR         = 3
FAKE_DATA_GEN_BURST_ACTIVE_ADDR = 4
FAKE_DATA_GEN_BURST_PERIOD_ADDR = 5

DATA_GEN_MUX_SEL_VALUE = 1
BURST_ACTIVE_VALUE     = 128
BURST_PERIOD_VALUE     = 1024

# ============================================================================
# Helpers
# ============================================================================

def reg_addr(reg_index):
    return BASE_ADDR + (reg_index * 4)

def write_register(reg_index, value):
    addr = reg_addr(reg_index)

    subprocess.run(
        ["devmem", hex(addr), "32", hex(value)],
        check=True
    )

    print(
        f"Reg[{reg_index}] "
        f"(0x{addr:08X}) <= 0x{value:08X}"
    )

# ============================================================================
# Main
# ============================================================================

def main():

    print("Configuring Fake Data Generator")

    write_register(DATA_GEN_MUX_SEL_ADDR, DATA_GEN_MUX_SEL_VALUE)
    write_register(FAKE_DATA_GEN_BURST_ACTIVE_ADDR, BURST_ACTIVE_VALUE)
    write_register(FAKE_DATA_GEN_BURST_PERIOD_ADDR, BURST_PERIOD_VALUE)

    print("Configuration complete")

if __name__ == "__main__":
    main()
