#!/usr/bin/env python3

import subprocess
import time

# ============================================================================
# Configuration
# ============================================================================

BASE_ADDR = 0x80040000

WORD_COUNT_REG = 0
WORD_DATA_REG = 1

READ_WORDS_AMOUNT = 1
READ_DELAY_S = 0.1

# ============================================================================
# Register Access Helpers
# ============================================================================


def reg_addr(base_addr, reg_index):
    """Return register address from base address and register index."""
    return base_addr + (reg_index * 4)


def read_register(addr):
    """Read a 32-bit register using devmem."""
    try:
        value = subprocess.check_output(
            ["devmem", hex(addr), "32"],
            text=True
        ).strip()

        return int(value, 16)

    except subprocess.CalledProcessError as err:
        print(f"ERROR: Failed to read register 0x{addr:08X}")
        raise err


def read_word_count(base_addr):
    """Read the word-count register."""
    addr = reg_addr(base_addr, WORD_COUNT_REG)
    return read_register(addr)


# ============================================================================
# Data Readout
# ============================================================================


def read_256bit_word(data_addr):
    """
    Read one 256-bit word as 8 consecutive 32-bit reads.

    Returns:
        listEight 32-bit words.
    """
    words = []

    for _ in range(8):
        words.append(read_register(data_addr))
        time.sleep(READ_DELAY_S)

    hex_word = "".join(f"{word:08X}" for word in words)

    print(f"256-bit Word: {hex_word}")

    return words


# ============================================================================
# Main
# ============================================================================


def main():
    print("=" * 80)
    print("RX Register Reader")
    print("=" * 80)

    initial_count = read_word_count(BASE_ADDR)
    print(f"Initial Word Count : {initial_count}")

    data_addr = reg_addr(BASE_ADDR, WORD_DATA_REG)

    for i in range(READ_WORDS_AMOUNT):

        print("\n" + "-" * 80)
        print(f"Reading Word {i + 1}/{READ_WORDS_AMOUNT}")
        print("-" * 80)

        read_256bit_word(data_addr)

        remaining_count = read_word_count(BASE_ADDR)
        print(f"Remaining Word Count : {remaining_count}")

        time.sleep(READ_DELAY_S)


if __name__ == "__main__":
    main()