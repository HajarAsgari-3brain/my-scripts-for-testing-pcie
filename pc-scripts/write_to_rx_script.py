#!/usr/bin/env python3

import subprocess

# ============================================================================
# Configuration
# ============================================================================
XDMA_EXE = (
    r"C:\Repos\del_me\3Brain.FW.Nexus.Embedded\nexus_firmware"
    r"\ip\xdma\cpp\windows\build\x64\bin\xdma_rw.exe"
)

# XDMA_EXE = (
#     r"C:\Repos\3Brain.FW.Nexus.Python-framework\usb_lib"
#     r"\xdma\xdma_windows_driver\build\x64\bin\xdma_rw.exe"
# )

XDMA_ADDRESS = "0x00"
PAYLOAD_FILE = "payload.bin"

NUM_WORDS = 2 # 1024 * 1024


WORD_SIZE_BYTES = 32
DWORD_SIZE_BYTES = 4
DWORDS_PER_WORD = WORD_SIZE_BYTES // DWORD_SIZE_BYTES
MAX_WINDOWS_COMMAND_LENGTH = 32767

# ============================================================================
# Payload Generation
# ============================================================================


def create_payload(filename, num_words):
    """
    Create 32-byte words containing incrementing big-endian 32-bit values.
    """

    print("Generating payload:")
    print("-" * 80)

    with open(filename, "wb") as f:
        for word_index in range(num_words):
            first_value = word_index * DWORDS_PER_WORD
            word = b"".join(
                value.to_bytes(DWORD_SIZE_BYTES, byteorder="big")
                for value in reversed(range(first_value, first_value + DWORDS_PER_WORD))
            )
            f.write(word)
            print(f"Word {word_index:02d}: {word.hex().upper()}")

    payload_size = num_words * WORD_SIZE_BYTES 

    print("-" * 80)
    print(f"Created '{filename}' ({payload_size} bytes)")
    print()


# ============================================================================
# XDMA Transfer
# ============================================================================


def transfer_payload(filename, address):
    """
    Transfer payload to FPGA using XDMA.
    """

    with open(filename, "rb") as payload_file:
        payload = payload_file.read()

    if not payload:
        raise ValueError(f"Payload file '{filename}' is empty.")

    cmd = [
        XDMA_EXE,
        "h2c_0",
        "write",
        address,
        *(f"0x{byte:02X}" for byte in payload),
    ]

    if len(subprocess.list2cmdline(cmd)) >= MAX_WINDOWS_COMMAND_LENGTH:
        raise ValueError(
            "Payload is too large for this XDMA executable's inline data interface."
        )

    print("Executing command:")
    print(" ".join(cmd))
    print()

    subprocess.run(cmd, check=True)

    print("Transfer completed successfully.")


# ============================================================================
# Main
# ============================================================================


def main():
    print("=" * 80)
    print("XDMA Host-to-Card Transfer Example")
    print("=" * 80)

    create_payload(PAYLOAD_FILE, NUM_WORDS)
    transfer_payload(PAYLOAD_FILE, XDMA_ADDRESS)


if __name__ == "__main__":
    main()
