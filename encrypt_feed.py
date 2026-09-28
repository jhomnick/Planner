#!/usr/bin/env python3
"""Encrypt feed.json -> feed.enc.json for the Homnick Planner.

Usage:  PLANNER_PASS='family passphrase' python3 encrypt_feed.py [feed.json] [feed.enc.json]

AES-256-GCM, key from PBKDF2-SHA256 (250,000 rounds) with the salt baked into index.html.
The page decrypts it in the browser with the same passphrase.
"""
import base64, json, os, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_B64 = "3CkFdEBni/lU2OeJL3d7Hw=="   # must match SALT_B64 in index.html
ITER = 250_000

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "feed.json"
    dst = sys.argv[2] if len(sys.argv) > 2 else "feed.enc.json"
    pw = os.environ.get("PLANNER_PASS")
    if not pw:
        sys.exit("Set PLANNER_PASS to the family passphrase")
    data = json.load(open(src))          # validates the JSON before publishing
    key = PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(SALT_B64), ITER).derive(pw.strip().encode())
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, json.dumps(data, separators=(",", ":")).encode(), None)
    json.dump({"v": 1, "iv": base64.b64encode(iv).decode(), "ct": base64.b64encode(ct).decode()}, open(dst, "w"))
    print(f"wrote {dst} ({len(ct)} bytes) — generated {data.get('generated')}")

if __name__ == "__main__":
    main()
