from collections import Counter
import string


def frequency_analysis(ciphertext):
    ciphertext = ''.join(filter(str.isalpha, ciphertext)).lower()
    freq = Counter(ciphertext)
    total_chars = sum(freq.values())

    freq_percentage = {char: (count / total_chars) * 100 for char, count in freq.items()}
    return dict(sorted(freq_percentage.items(), key=lambda item: item[1], reverse=True))


def decrypt_monoalphabetic(ciphertext):
    english_freq_order = "etaoinshrdlcumwfgypbvkjxqz"
    cipher_freq_order = list(frequency_analysis(ciphertext).keys())

    decryption_map = {cipher_freq_order[i]: english_freq_order[i] for i in range(len(cipher_freq_order))}

    decrypted_text = ''.join(decryption_map.get(char, char) for char in ciphertext.lower())
    return decrypted_text


def generate_playfair_matrix(keyword):
    keyword = ''.join(dict.fromkeys(keyword.replace("j", "i")))
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    matrix = []
    used_chars = set()

    for char in keyword + alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]


def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col


def prepare_playfair_text(plaintext):
    plaintext = plaintext.replace("j", "i").lower()
    plaintext = ''.join(filter(str.isalpha, plaintext))
    pairs = []
    i = 0

    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext) and plaintext[i] != plaintext[i + 1]:
            b = plaintext[i + 1]
            i += 2
        else:
            b = 'x'
            i += 1

        pairs.append((a, b))
    return pairs


def playfair_encrypt(plaintext, matrix):
    pairs = prepare_playfair_text(plaintext)
    encrypted_text = ""

    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += matrix[row1][col2] + matrix[row2][col1]

    return encrypted_text


def playfair_decrypt(ciphertext, matrix):
    decrypted_text = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            decrypted_text += matrix[row1][col2] + matrix[row2][col1]

    return decrypted_text.replace("x", "")


if __name__ == "__main__":
    choice = input(
        "Choose an option:\n1. Monoalphabetic Cipher Decryption\n2. Playfair Cipher Encryption/Decryption\nEnter choice: ")

    if choice == "1":
        encrypted_text = input("Enter the encrypted text: ")
        decrypted_text = decrypt_monoalphabetic(encrypted_text)
        print("Most likely decrypted text:", decrypted_text)

    elif choice == "2":
        keyword = input("Enter the keyword: ").lower()
        matrix = generate_playfair_matrix(keyword)
        print("Playfair Matrix:")
        for row in matrix:
            print(" ".join(row))

        action = input("Choose action:\n1. Encrypt\n2. Decrypt\nEnter choice: ")
        text = input("Enter the text: ").lower()

        if action == "1":
            encrypted_text = playfair_encrypt(text, matrix)
            print("Encrypted Text:", encrypted_text)
        elif action == "2":
            decrypted_text = playfair_decrypt(text, matrix)
            print("Decrypted Text:", decrypted_text)
