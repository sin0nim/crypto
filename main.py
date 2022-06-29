from RSA import RSA, PrimeNum


print('Боб:')
degree = int(input('Задайте порядок чисел p, q : '))
key = PrimeNum(10 ** (degree - 1), 10 ** degree)
rsa = RSA(key.open_key, key.private_key)
print(f'Алисе - открытый ключ = ({key.open_key[0]}, {key.open_key[1]})')

print('Алиса:')
text = input('Введите сообщение: ')

encrypted = ''
test_text = ''
while len(text) > 0:
    num_str = text[0]
    text = text[1:]
    while len(text) > 0 and int(num_str + text[0]) < rsa.open_key[0]:
        num_str += text[0]
        text = text[1:]
    print('original =', num_str, end=' | ')
    enc_text = rsa.encrypt(num_str)
    encrypted += (' ' + enc_text)
    print('encrypted =', enc_text)
    # test_text = rsa.decrypt(enc_text)
    # print('test: ', test_text)


print('Бобу - зашифрованное сообщение:')
print(encrypted)

print('Боб:')
dec_list = [str_num for str_num in encrypted.split()]
# print(dec_list)
dec_text = ''
for i in range(len(dec_list)):
    dec_text += rsa.decrypt(dec_list[i])
print('Расшифрованное сообщение:')
print(dec_text)
