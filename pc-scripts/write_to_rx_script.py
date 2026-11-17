#!/usr/bin/env python3

import subprocess

# ============================================================================
# Configuration
# ============================================================================
# XDMA_EXE = (
#     r"C:\Repos\del_me\3Brain.FW.Nexus.Embedded\nexus_firmware"
#     r"\ip\xdma\cpp\windows\build\x64\bin\xdma_rw.exe"
# )

XDMA_EXE = (
    r"C:\Repos\3Brain.FW.Nexus.Python-framework\usb_lib"
    r"\xdma\xdma_windows_driver\build\x64\bin\xdma_rw.exe"
)

XDMA_ADDRESS = "0x00"
PAYLOAD_FILE = "payload.bin"

NUM_WORDS = 5 # 1024 * 1024


WORD_SIZE_BYTES = 32 

# ============================================================================
# Payload Generation
# ============================================================================


def create_payload(filename, num_words):
    """
    Create a binary payload containing incrementing 32-bit words.
    """

    print("Generating payload:")
    print("-" * 80)

    with open(filename, "wb") as f:
        for word in range(num_words):
            f.write(word.to_bytes(WORD_SIZE_BYTES, byteorder="little"))
            print(f"Word {word:02d}: 0x{word:08X}")

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

    cmd = [
        XDMA_EXE,
        "h2c_0",
        "write",
        address,
        "-f",
        filename,
    ]

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
