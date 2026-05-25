# ============================================================
#  Basic Encryption & Decryption — Caesar Cipher
#  DecodeLabs Industrial Training Kit — Project 2
# ============================================================


def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted)
        else:
            # spaces and punctuation stay unchanged
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    # decryption = encryption with negative shift
    return caesar_encrypt(text, -shift)


def display_result(original: str, encrypted: str, decrypted: str, shift: int) -> None:
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    RESET  = "\033[0m"

    print("\n" + "=" * 50)
    print(f"  Shift Key  : {CYAN}{shift}{RESET}")
    print("-" * 50)
    print(f"  Original   : {original}")
    print(f"  Encrypted  : {YELLOW}{encrypted}{RESET}")
    print(f"  Decrypted  : {GREEN}{decrypted}{RESET}")
    print("=" * 50 + "\n")


def main():
    print("\n  DecodeLabs — Caesar Cipher")
    print("  Type 'quit' to exit.\n")

    while True:
        text = input("  Enter text   : ")
        if text.lower() == "quit":
            print("  Exiting. Stay secure!\n")
            break
        if not text.strip():
            print("  Please enter some text.\n")
            continue

        try:
            shift = int(input("  Enter shift  : "))
            shift = shift % 26  # normalize
        except ValueError:
            print("  Shift must be a number.\n")
            continue

        encrypted = caesar_encrypt(text, shift)
        decrypted = caesar_decrypt(encrypted, shift)
        display_result(text, encrypted, decrypted, shift)


if __name__ == "__main__":
    main()