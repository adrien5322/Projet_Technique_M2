#!/usr/bin/env python3
"""Generate a secure secret key for JWT authentication."""

import secrets
import sys


def generate_secret_key(length: int = 32) -> str:
    """
    Generate a cryptographically secure secret key.
    
    Args:
        length: Number of bytes (default 32 = 256 bits)
    
    Returns:
        Hex string of the secret key
    """
    return secrets.token_hex(length)


if __name__ == "__main__":
    # Generate a 32-byte (256-bit) key by default
    key_length = 32
    
    if len(sys.argv) > 1:
        try:
            key_length = int(sys.argv[1])
        except ValueError:
            print(f"Invalid length: {sys.argv[1]}. Using default 32 bytes.")
    
    secret_key = generate_secret_key(key_length)
    
    print("=" * 60)
    print("GENERATED SECRET KEY (JWT_SECRET_KEY)")
    print("=" * 60)
    print(f"\n{secret_key}\n")
    print("=" * 60)
    print("INSTRUCTIONS:")
    print("1. Copy this key")
    print("2. Add it to your .env file as JWT_SECRET_KEY=value")
    print("3. NEVER commit the .env file to version control")
    print("4. Use a different key for each environment (dev/staging/prod)")
    print("=" * 60)
