import re


def generate_playfair_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")
    keyword = "".join(dict.fromkeys(keyword))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix_key = keyword + "".join([c for c in alphabet if c not in keyword])
    return [list(matrix_key[i:i + 5]) for i in range(0, 25, 5)]


def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None


def process_text(text):
    text = re.sub(r'[^A-Za-z]', '', text).upper().replace("J", "I")
    processed_text = ""
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                processed_text += a + 'X'
                i += 1
            else:
                processed_text += a + b
                i += 2
        else:
            processed_text += a + 'X'
            i += 1
    return processed_text


def encrypt_decrypt(text, matrix, encrypt=True):
    text = process_text(text)
    result = ""
    step = 1 if encrypt else -1

    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            result += matrix[row_a][(col_a + step) % 5]
            result += matrix[row_b][(col_b + step) % 5]
        elif col_a == col_b:  # Same column
            result += matrix[(row_a + step) % 5][col_a]
            result += matrix[(row_b + step) % 5][col_b]
        else:
            result += matrix[row_a][col_b]
            result += matrix[row_b][col_a]

    return result


def main():
    keyword = input("Enter keyword: ")
    matrix = generate_playfair_matrix(keyword)
    print("Playfair Matrix:")
    for row in matrix:
        print(" ".join(row))

    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").upper()
    text = input("Enter text: ")

    if choice == "E":
        result = encrypt_decrypt(text, matrix, encrypt=True)
    elif choice == "D":
        result = encrypt_decrypt(text, matrix, encrypt=False)
    else:
        print("Invalid choice!")
        return

    print("Result:", result)


if __name__ == "__main__":
    main()