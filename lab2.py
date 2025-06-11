from lab1 import letter_frequencies
alphabet_with_e = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def clean_text(text):
    text = text.lower().replace('ё', 'е')
    result = ''
    for char in text:
        if char in alphabet:
            result += char
    return result

with open("text.txt", encoding="utf-8") as f:
    text = f.read()
reference_frequencies = letter_frequencies(clean_text(text), alphabet)

#зашифрувати шифром Віженера
def vigenere(text, key, mode='encrypt'):
    text = clean_text(text)
    result = ""
    alphabet_len = len(alphabet)
    key_idx = []
    for char in key:
        key_idx.append(alphabet.index(char))
    key_len = len(key_idx)
    key_pos = 0 
    for char in text:
        text_idx = alphabet.index(char)
        shift = key_idx[key_pos % key_len]
        if mode == 'encrypt':
            new_idx = (text_idx + shift) % alphabet_len
        elif mode == 'decrypt':
            new_idx = (text_idx - shift) % alphabet_len
        else:
            raise ValueError("mode має бути 'encrypt' або 'decrypt'")
        result += alphabet[new_idx]
        key_pos += 1
    return result

#індекс відповідності
def index_of_coincidence(text):
    text = clean_text(text)
    result = 1.0
    ln = len(text)
    if ln < 2:
        return 0 
    result = result / (ln * (ln - 1)) 
    total = 0
    for letter in alphabet:
        count = text.count(letter)
        total += count * (count - 1)
    result = result * total
    return result

#визначити довжину ключа 
def key_len(text, max_key_len=30):
    expected_ic = 0.055
    text = clean_text(text)
    best_key_len = 1
    best_ic_diff = float('inf')
    for k_len in range(1, max_key_len + 1):
        groups = []
        for _ in range(k_len):
            groups.append('')
        for i in range(len(text)):
            group_idx = i % k_len
            groups[group_idx] += text[i]
        total_ic = 0
        for j in range(len(groups)):
            group_ic = index_of_coincidence(groups[j])
            total_ic += group_ic
        avg_ic = total_ic / k_len
        ic_diff = abs(avg_ic - expected_ic)
        if ic_diff < best_ic_diff:
            best_ic_diff = ic_diff
            best_key_len = k_len
    return best_key_len

#визначити символи ключа за допомогою порівняння
def vigenere_key_comparison(text, key_len):
    text = clean_text(text)
    result = ''
    alphabet_len = len(alphabet)
    target_letter = 'о'
    target_index = alphabet.index(target_letter)
    for i in range(key_len):
        group = ''
        for j in range(i, len(text), key_len):
            group += text[j]
        frequencies = letter_frequencies(group, alphabet)
        most_common_index = frequencies.index(max(frequencies))
        key_shift = (most_common_index - target_index) % alphabet_len
        result += alphabet[key_shift]
    return result

#визначити символи ключа за допомогою М
def vigenere_key_m(text, key_len):
    text = clean_text(text)
    result = ''
    alphabet_len = len(alphabet)
    for i in range(key_len):
        group = ''
        for j in range(i, len(text), key_len):
            group += text[j]
        group_frequencies = letter_frequencies(group, alphabet)
        max_score = float('-inf')
        key_shift = 0
        for g in range(alphabet_len): 
            score = 0
            for t in range(alphabet_len):
                shifted_idx = (t + g) % alphabet_len
                p = reference_frequencies[t]  
                count = group_frequencies[shifted_idx]   
                score += p * count
            if score > max_score:
                max_score = score
                key_shift = g
        result += alphabet[key_shift]
    return result

with open("text2.txt", "r", encoding="utf-8") as f:
    text2 = f.read()

key1 = 'ок'  
key2 = 'сон'
key3 = 'туча'
key4 = 'кулон'
key5 = 'одиннадцатиклассница' 

ciphertext1 = vigenere(text2, key1)
ciphertext2 = vigenere(text2, key2)
ciphertext3 = vigenere(text2, key3)
ciphertext4 = vigenere(text2, key4)
ciphertext5 = vigenere(text2, key5)

print()
print(f"Текст зашифрований з ключем '{key1}':\n{ciphertext1}")
print()
print(f"Текст зашифрований з ключем '{key2}':\n{ciphertext2}")
print()
print(f"Текст зашифрований з ключем '{key3}':\n{ciphertext3}")
print()
print(f"Текст зашифрований з ключем '{key4}':\n{ciphertext4}")
print()
print(f"Текст зашифрований з ключем '{key5}':\n{ciphertext5}")

ic = index_of_coincidence(text2)
ic1 = index_of_coincidence(ciphertext1)
ic2 = index_of_coincidence(ciphertext2)
ic3 = index_of_coincidence(ciphertext3)
ic4 = index_of_coincidence(ciphertext4)
ic5 = index_of_coincidence(ciphertext5)

print()
print(f"Індекс відповідності відкритого тексту:\n{ic}")
print()
print(f"Індекс відповідності шифротексту 1:\n{ic1}")
print()
print(f"Індекс відповідності шифротексту 2:\n{ic2}")
print()
print(f"Індекс відповідності шифротексту 3:\n{ic3}")
print()
print(f"Індекс відповідності шифротексту 4:\n{ic4}")
print()
print(f"Індекс відповідності шифротексту 5:\n{ic5}")

with open("text4.txt", "r", encoding="utf-8") as f:
    text4 = f.read()

text4_key_len = key_len(text4)    
text4_key_comparison = vigenere_key_comparison(text4, text4_key_len)
text4_key_m = vigenere_key_m(text4, text4_key_len)

print()
print(f"Значення ключа, одержане шляхом співставлення:\n{text4_key_comparison}")
print()
print(f"Значення ключа, одержане з використанням М:\n{text4_key_m}")

#девелииоборойдей
#делолисоборотней

key = text4_key_m
dectypted_text4 = vigenere(text4, key, 'decrypt')

print()
print(f"Розшифрований текст:\n{dectypted_text4}")