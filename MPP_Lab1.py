import numpy as np
import scipy.stats as stats
import string


def beta_interval_partition(data, alphabet):
    alphabet_size = len(alphabet)
    # Сортуємо числовий ряд
    sorted_data = np.sort(data)

    # Визначаємо параметри бета-розподілу на основі даних
    alpha, beta, loc, scale = stats.beta.fit(sorted_data)

    # Обчислюємо кумулятивну ймовірність для кожного значення
    cumulative_probabilities = stats.beta.cdf(sorted_data, alpha, beta, loc=loc, scale=scale)

    # Розбиваємо інтервали відповідно до кумулятивної ймовірності та обраного алфавіту
    interval_indices = np.digitize(cumulative_probabilities, np.linspace(0, 1, alphabet_size + 1))

    # Створюємо словник, де ключі - це номери інтервалів, а значення - це відповідні значення
    interval_dict = {}
    for idx, value in zip(interval_indices, sorted_data):
        if idx not in interval_dict:
            interval_dict[idx] = []
        interval_dict[idx].append(value)
        # Призначення знаків з алфавіту

    # alphabet = list(string.ascii_uppercase)[:alphabet_size]
    assigned_symbols = {key: alphabet[key - 1] for key in interval_dict.keys()}

    # Вивід результату - заміна номерів інтервалів на букви алфавіту
    result = {}
    for key, values in interval_dict.items():
        symbol = assigned_symbols[key]
        result[symbol] = values

    return result



# Використання функції
data = np.random.beta(2, 5, 10000)  # Згенеруємо випадкові дані
alphabet_size = 26  # Задаємо розмір алфавіту
alphabet = list(string.ascii_uppercase)[:alphabet_size]  # Алфавіт буде складатися лише з великих літер - можна змінити


intervals = beta_interval_partition(data, alphabet)
for key, values in intervals.items():
    print(f"Інтервал {key}: {values}")

# вивід буквенного ряду
letter_data = ''
for number in data:
    for interval in intervals.items():
        letter = interval[0]
        numbers = interval[1]
        if number in numbers:
            letter_data += letter
            break
print("Початкові дані:")
print(data)
print(letter_data)

# Побудова та вивід матриці
ling_matrix = [[0] * alphabet_size for i in range(alphabet_size)]
for i in range(len(ling_matrix)):
    for j in range(len(ling_matrix[0])):
        row_letter = alphabet[i]
        col_letter = alphabet[j]
        seeking_letters = str(row_letter+col_letter)
        appear = 0
        for l in range(len(letter_data)-1):
            if letter_data[l:l+2] == seeking_letters:
                appear += 1
        ling_matrix[i][j] = appear

print(np.matrix(ling_matrix))
