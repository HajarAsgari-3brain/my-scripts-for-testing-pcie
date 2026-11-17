#!/usr/bin/env python3

import subprocess
import time

# ============================================================================
# Configuration
# ============================================================================

BASE_ADDR = 0x80040000

WORD_DATA_REG = 2

WRITE_WORDS_AMOUNT = 1
WRITE_DELAY_S = 0.1

# ============================================================================
# Register Access Helpers
# ============================================================================


def reg_addr(base_addr, reg_index):
    """Return register address from base address and register index."""
    return base_addr + (reg_index * 4)


def write_register(addr, value):
    """Write a 32-bit value to a register using devmem."""
    try:
        subprocess.run(
            ["devmem", hex(addr), "32", hex(value)],
            check=True
        )
    except subprocess.CalledProcessError as err:
        print(f"ERROR: Failed to write 0x{value:08X} to 0x{addr:08X}")
        raise err

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

# ============================================================================
# Data Write Helpers
# ============================================================================


def write_256bit_word_words(data_addr, words):
    """
    Write one 256-bit word as 8 consecutive 32-bit writes.

    Args:
        data_addr: Register address.
        words: List of 8 x 32-bit values.
    """
    if len(words) != 8:
        raise ValueError("Expected exactly 8 words.")

    hex_word = "".join(f"{word:08X}" for word in reversed(words))
    print(f"256-bit Word: {hex_word}")

    for index, word in enumerate(words):
        write_register(data_addr, word)
        print(f"Wrote word {index}: 0x{word:08X}")
        time.sleep(WRITE_DELAY_S)


def write_256bit_word(data_addr, value):
    """
    Write a 256-bit integer as 8 consecutive 32-bit words.

    Args:
        data_addr: Register address.
        value: 256-bit integer.
    """
    words = []

    for i in range(8):
        words.append((value >> (32 * i)) & 0xFFFFFFFF)

    write_256bit_word_words(data_addr, words)


# ============================================================================
# Main
# ============================================================================


def main():
    print("=" * 80)
    print("TX Register Writer")
    print("=" * 80)

    data_addr = reg_addr(BASE_ADDR, WORD_DATA_REG)

    for i in range(WRITE_WORDS_AMOUNT):

        print("\n" + "-" * 80)
        print(f"Writing Word {i + 1}/{WRITE_WORDS_AMOUNT}")
        print("-" * 80)

        words = [
            i * 8 + 0,
            i * 8 + 1,
            i * 8 + 2,
            i * 8 + 3,
            i * 8 + 4,
            i * 8 + 5,
            i * 8 + 6,
            i * 8 + 7,
        ]

        write_256bit_word_words(data_addr, words)


        time.sleep(WRITE_DELAY_S)

    print("\nTransfer complete")


if __name__ == "__main__":
    main()