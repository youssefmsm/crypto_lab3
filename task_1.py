import itertools
import string


def decrypt(ciphertext, key):
    alphabet = string.ascii_lowercase
    decrypted_text = ''
    translation_table = str.maketrans(key, alphabet)
    decrypted_text = ciphertext.translate(translation_table)
    return decrypted_text


def brute_force_monoalphabetic(ciphertext):
    alphabet = string.ascii_lowercase
    all_permutations = itertools.permutations(alphabet)

    for perm in all_permutations:
        key = ''.join(perm)
        decrypted_text = decrypt(ciphertext, key)
        print(f"Key: {key} => {decrypted_text}")


if __name__ == "__main__":
    encrypted_message = input("Enter the encrypted message: ").lower()
    brute_force_monoalphabetic(encrypted_message)
