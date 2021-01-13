import sys
from random import randint, getrandbits
out = open('out.txt', 'w')

def file_print(message):
    message = str(message)
    print(message)
    out.write(message + '\n')


def gcd(a, b):
    """
    a: int
    b: int
    :return: int
    """
    if(b == 0): 
        return a 
    else: 
        return gcd(b, a % b)

def extended_euclid_algorithm_gcd(a, b):
    """
    Extended euclidian algorithm
    a: int
    b: int
    :return: Tuple[int int int]
    """

    if a == 0:
        return b, 0, 1

    d, x1, y1 = extended_euclid_algorithm_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


def inverse_number(a, n):
    """inverse number a^-1 mod n"""
    a = a % n

    # Получаем х потому что алгоритм эвклида возвращает обратные для двух чисел
    # для которых применялся алгоритм, но только приусловии что они взаимопростые
    d, x, y = extended_euclid_algorithm_gcd(a, n)  
    if d == 1:
        return x


def miller_rabin_iteration(prime, x):
    """
    
    """
    if gcd(prime, x) != 1:
        return False

    # Знаходження розв'язку рівняння з методички
    # p-1 = d*2^s
    # Знаходимо d
    d = prime - 1
    while d % 2 == 0:
        d //= 2
    
    #далі всі кроки описані в методичці
    m = pow(x, d, prime)

    if m == 1 or m == prime - 1:
        return True

    while d < prime - 1:
        result_of_iteration = pow(x, d, prime)
        if result_of_iteration == prime - 1:
            return True
        if result_of_iteration == 1:
            return False
        d *= 2
    return False


def prime_test(p, k=50):
    """
    Тест Миллера-Рабина, который включает в себя кучу итераций, в данном случае 50(по умолчаюнию)
    Если хотя бы на одном из шагов число провалит тест на простоту, то число не простое

    :p: int - число, простоту которого мы хотим проверить
    :return: bool (True - число простое / False - число непростое)
    """
    for i in range(0, k):
        x = randint(2, p - 2)
        if miller_rabin_iteration(p, x):
            pass
        else:
            return False 
    else:
        return True

def gen_prime(number_of_bits):
    """
    Generates prime number with certain number of bits
    """

    rand_num = getrandbits(number_of_bits)

    if rand_num % 2 == 0:
        rand_num += 1

    for num in range(rand_num, rand_num*2, 2):
        if prime_test(num):
            prime = num
            file_print("[*] Prime number {}".format(hex(prime)))
            break
        else:
            file_print('[*] Number {} is not prime'.format(hex(num)))
            

    return num

def generate_pair_of_keys(bit_len):
    """
    Генерує експоненту(0x10001),
    """
    file_print("Генерація простого числа 'p' ...")
    p = gen_prime(bit_len)
    file_print("Просте число сгенеровано 'p'")

    file_print("Генерація простого числа 'q' ...")
    q = gen_prime(bit_len)
    file_print("Просте число сгенеровано'q'")

    e = 0x10001
    f = (p - 1) * (q - 1)
    n = p * q
    d = inverse_number(e, f) % f

    file_print(' p={}\n q={}\n n={}\n f={}\n e={}\n d={}'.format(hex(p), hex(q), hex(n), hex(f), hex(e), hex(d)))

    return e, d, n


def encrypt(m, e, n):
    """
    Зашифрувати публічним ключем
    m: повідомлення
    e: публіна ступінь 
    n: публіний модуль

    m^e mod n
    """
    result = pow(m, e, n)
    return result


def decrypt(c, d, n):
    """
    Розшифрувати приватним ключем
    c: шифротекст
    d: секретна ступінь
    n: публічний модуль
    
    с^d mod n
    """
    result = pow(c, d, n)
    return result


def sign(m, d, n):
    """
    Зашифурвати приватним ключем(підписати)
    """
    result = pow(m, d, n)
    return result


def verify(m, s, e, n):
    """
    Розшифрувати публічним ключем та перевірити чи повідомлення однакові
    s^e mod n - розшифрування повідомлення
    """
    return m == pow(s, e, n)
    

def send_key(k, d, n, e1, n1):
    """
    Шифрує одне і те саме повідомлення різними способами і повертає
    нам два зашифрованих повідомлення
    """
    # Зашифрувати певне повідомлення(k) своїм приватним 
    # ключем (d, n), та отримати(s).
    s = pow(k, d, n)


    # Зашифрувати повідомлення(k1) публічним 
    # ключем отримувача(e1, n1)
    k1 = pow(k, e1, n1)

    # Зашифрувати зашифроване повідомлення(s) публічним 
    # ключем отримувача(e1, n1)
    s1 = pow(s, e1, n1)

    return k1, s1

def receive_key(k1, S1, d1, n1, e, n):
    # Розшифровується повідомлення ключем отримувача
    k = pow(k1, d1, n1)

    # Розшифровується повідомлення, що зашифроване двома ключами.
    # Розшифровується тільки нашем ключем
    S = pow(S1, d1, n1)

    # Верифікація
    if verify(k, S, e, n):
        return k
    return 0



def test_encryption_with_server_key(modulus, exponent):
    """
    Зашифрувати повідомлення серверним ключем, за допомогою нашого алгоритму
    щоб перевірити на сайті правильність шифрування
    """
    k = 0x102410240124
    print(hex(encrypt(k, exponent, modulus)))


def test_server_verification(message, signed_message, modulus, exponent):
    if verify(message, signed_message, exponent, modulus):
        print('Верифіковано')
    else:
        print('Не верифіковано')


def test_sending_key_to_server(message, modulus, exponent):  
    e, d, n = generate_pair_of_keys(64) 
    k, s = send_key(message, d, n, exponent, modulus)
    print(' ' + hex(k) + '\n ' + hex(s))
    

def main():
    #Preparation
    BITS_LEN = 256
    e1, d1, n1 = generate_pair_of_keys(BITS_LEN)
    e2, d2, n2 = generate_pair_of_keys(BITS_LEN)
    while n2 < n1:
        file_print("- Генерація іншої пари ключів")
        e1, d1, n1 = generate_pair_of_keys(BITS_LEN)
        e2, d2, n2 = generate_pair_of_keys(BITS_LEN)

    # Test encryption/decryption
    clear_text = 123554323
    cipher_text = encrypt(clear_text, e1, n1)
    decrypted_text = decrypt(cipher_text, d1, n1)
    file_print("    Testing RSA\n        Відкритий текст:      {}\n    [-] Шифрований текст: {}\n    [-] Розшифрований текст: {}".format(clear_text, cipher_text, decrypted_text))

    # Value to be exchanged
    k = 322223

    file_print("Підготовка даних до відправки ...")
    k1, S1 = send_key(k, d1, n1, e2, n2)
    file_print("[*] Відправка ...") 
    file_print("[*] Отримання ...")

    if receive_key(k1, S1, d2, n2, e1, n1):
        file_print("!!!!! Верифіковано! !!!!!")
    else:
        file_print("ХХХХХ Не Верифіковано! ХХХХХ")



if __name__ == '__main__':  
    server_modulus = 0xBEB955648DEF70195AA70C0CF237F7125C756D9B73EB734DA3207CDDA2F3E269
    server_exponent = 0x10001
    signed_message = 0x0BCDA2FB48D952659F452DE39D6D39D211B5394B7D5C1B286B8AB2A49A59F368

    # test_encryption_with_server_key(server_modulus, server_exponent)
    # test_server_verification(0xffffff, signed_message, server_modulus, server_exponent)
    #test_sending_key_to_server(0xffffff, server_modulus, server_exponent)

    main()
