#!/usr/bin/env python3
# PyCrypt v2.1 - Internal Decoder Tool
# DO NOT MODIFY

import sys, base64, hashlib, time

# === NOISE / DECOYS ===
def _init_noise():
    return [i ^ 0xAA for i in range(50)]

def _fake_validate(data):
    h = hashlib.md5(data.encode()).hexdigest()
    return h.startswith("0000")

# === REAL DATA (FRAGMENTED) ===
_FRAG_A = b'Q1RGU01LOHtweX'
_FRAG_B = b'dGhuX3Izdl9t'
_FRAG_C = b'YXN0ZXJ9'

# === CORE LOGIC ===
def _decode_chain(fragments):
    raw = b''.join(fragments)
    # Base64 decode first
    decoded = base64.b64decode(raw)
    # XOR with dynamic key derived from length
    key = len(decoded) & 0xFF
    return bytes([b ^ key for b in decoded]).decode('utf-8')

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pycrypt.py <auth_code>")
        sys.exit(1)

    code = sys.argv[1]
    if len(code) != 4 or not code.isdigit():
        print("[-] Invalid auth code format")
        sys.exit(1)

    # Decoy check (always fails for random input)
    if not _fake_validate(code):
        print("[-] Authentication failed. System locked.")
        sys.exit(1)

    # Real execution path (only reached if auth passes)
    flag = _decode_chain([_FRAG_A, _FRAG_B, _FRAG_C])
    print(f"[+] Decoded payload: {flag}")

if __name__ == "__main__":
    main()
