import math

alphabet_with_space = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
alphabet_no_space = alphabet_with_space[:-1]

#частоти букв
def letter_frequencies(text, alphabet):
    result = []
    for char in alphabet:
        count = text.count(char)
        result.append(count)
    return result

#частоти біграм
def bigram_frequencies(text, alphabet, step=1):
    alphabet_len = len(alphabet)
    result = []
    for i in range(alphabet_len):
        row = []
        for j in range(alphabet_len):
            row.append(0)
        result.append(row)
    filtered_text = ""
    for char in text:
        if char in alphabet:
            filtered_text += char 
    text = filtered_text           
    i = 0
    while i < len(text) - 1:
        first = text[i]
        second = text[i + 1]
        row_idx = alphabet.index(first)
        col_idx = alphabet.index(second)
        result[row_idx][col_idx] += 1
        i += step
    return result

#h1 h2
def calculate_entropy(frequencies, h=1):
    if h == 1:
        total = sum(frequencies)
        result = 0
        for frequency in frequencies:
            if frequency != 0:
                p = frequency / total
                result += p * math.log2(p)
        result = - result
        return result

    elif h == 2:
        total = 0
        for row in frequencies:
            for frequency in row:
                total += frequency
        result = 0
        for row in frequencies:
            for frequency in row:
                if frequency != 0:
                    p = frequency / total
                    result += p * math.log2(p)
        result = - result / 2 
        return result

    else:
        raise ValueError("h має бути 1 або 2")

#частоти символів відсортовані за спаданням 
def print_sorted_frequencies(frequencies, alphabet):
    pairs = []
    for i in range(len(alphabet)):
        symbol = alphabet[i]
        frequency = frequencies[i]
        pair = (symbol, frequency)
        pairs.append(pair)
    pairs.sort(key=lambda x: x[1], reverse=True)
    print()
    for pair in pairs:
        symbol = pair[0]
        frequency = pair[1]
        print("частота символа ", symbol + " : ", frequency)

def fill_matrix(matrix, alphabet):
    width = 6
    result = " " * width + "".join(f"{ch:>{width}}" for ch in alphabet) + "\n"
    for i, j in enumerate(matrix):
        result += f"{alphabet[i]:<{width}}" + "".join(f"{count:>{width}}" for count in j) + "\n"
    return result        

with open("text.txt", encoding="utf-8") as f:
    text = f.read().lower()

letter_frequencies_with_space = letter_frequencies(text, alphabet_with_space)
print_sorted_frequencies(letter_frequencies_with_space, alphabet_with_space) 

overlapping_bigram_matrix_with_space = bigram_frequencies(text, alphabet_with_space, 1)
nonoverlapping_bigram_matrix_with_space  = bigram_frequencies(text, alphabet_with_space, 2)

print()

H1_with_space = calculate_entropy(letter_frequencies_with_space, 1)
print(f"H1 (з пробілами): {H1_with_space}")

H2_with_space_over = calculate_entropy(overlapping_bigram_matrix_with_space, 2)
print(f"H2 перекривні (з пробілами): {H2_with_space_over}")

H2_with_space_non = calculate_entropy(nonoverlapping_bigram_matrix_with_space, 2)
print(f"H2 неперекривні (з пробілами): {H2_with_space_non}")

letter_frequencies_no_space = letter_frequencies(text, alphabet_no_space)
nonoverlapping_bigram_matrix_no_space = bigram_frequencies(text, alphabet_no_space, 2)
overlapping_bigram_matrix_no_space = bigram_frequencies(text, alphabet_no_space, 1)

H1_no_space = calculate_entropy(letter_frequencies_no_space, 1)
print(f"H1 (без пробілів): {H1_no_space}")

H2_no_space_over = calculate_entropy(overlapping_bigram_matrix_no_space, 2)
print(f"H2 неперекривні (без пробілів): {H2_no_space_over}")

H2_no_space_non = calculate_entropy(nonoverlapping_bigram_matrix_no_space, 2)
print(f"H2 неперекривні (без пробілів): {H2_no_space_non}")

with open("text1.txt", "w", encoding="utf-8") as out:
    out.write("Біграми (перекривні):\n")
    out.write(fill_matrix(overlapping_bigram_matrix_with_space, alphabet_with_space))
    out.write("\n")

    out.write("Біграми (неперекривні):\n")
    out.write(fill_matrix(nonoverlapping_bigram_matrix_with_space, alphabet_with_space))
    out.write("\n")