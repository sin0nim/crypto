# from random import randrange as rr
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl


class RSA:
    def __init__(self, open_key, private_key):
        self.open_key = open_key
        self.private_key = private_key

    @staticmethod
    def gcd(i, j):
        while j > 0:
            i, j = j, i % j
        return i

    @staticmethod
    def euclid(phi_n, m):
        u, v = (phi_n, 0), (m, 1)
        while v[0] != 0:
            q = u[0] // v[0]
            t = (u[0] % v[0], u[1] - q * v[1])
            u, v = v, t
        print(u[1] % phi_n)
        return u[1] % phi_n

    @staticmethod
    def fast_power(m, pw, mod):
        power_list = [(m % mod, pw % 2)]
        pw //= 2
        while pw > 0:
            power_list.append(((m * m) % mod, pw % 2))
            pw //= 2
        result = 1
        for i in range(len(power_list)):
            if power_list[i][1]:
                result *= power_list[i][0]
        return result

    def encrypt(self, block):
        message = int(block)
        encrypted = self.fast_power(message, self.open_key[1], self.open_key[0])
        return encrypted

    def decrypt(self, block):
        message = int(block)
        decrypted = self.fast_power(message, self.private_key, self.open_key[0])
        return decrypted


class PrimeNum:
    def __init__(self, pq_from, pq_to):
        with WolframLanguageSession() as session:
            self.__prime_pair = session.evaluate(wl.RandomPrime({pq_from, pq_to}, 2))
            session.stop()
        print(*self.__prime_pair)
        self.n = self.__prime_pair[0] * self.__prime_pair[1]
        phi_n = (self.__prime_pair[0] - 1) * (self.__prime_pair[1] - 1)
        '''        with WolframLanguageSession() as session:
            sqrt_phi_n = round(session.evaluate(wl.Sqrt(phi_n)))
            session.stop()
        print('sqrt_phi_n =', sqrt_phi_n)
'''
        with WolframLanguageSession() as session:
            rand_key = session.evaluate(wl.RandomPrime({self.__prime_pair[0] + 1, phi_n - 1}))
            session.stop()
        print('rand_key =', rand_key)
        with WolframLanguageSession() as session:
            prime_num = session.evaluate(wl.ExtendedGCD(phi_n, rand_key))
            session.stop()
        print(*prime_num)
        print('prime_num = (', prime_num[0], ', (', *prime_num[1], ')')
        self.open_key = (self.n, rand_key)
        self.private_key = prime_num[1][1] % self.n
        print(f'Open key = ({self.n}, {rand_key})')
        print(f'Private key = {self.private_key}')
        print(f'Test: ({rand_key} * {self.private_key}) % {phi_n} = {(rand_key * self.private_key) % phi_n}')


keys = PrimeNum(100, 1000)


'''aa = RSA(19, 13)
text = '1213141516'
dec_text = ''
while len(text) > 0:
    num_str = text[0]
    text = text[1:]
    while len(text) > 0 and int(num_str + text[0]) < aa.open_key[0]:
        num_str += text[0]
        text = text[1:]
    print('num = ', num_str, '   text = ', text)
    enc_text = str(aa.encrypt(num_str))
    print('encrypted = ', enc_text)
    dec_text += str(aa.decrypt(enc_text))
print('decrypted = ', dec_text)
'''