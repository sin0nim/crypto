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
            m_last = power_list[-1][0]
            power_list.append(((m_last * m_last) % mod, pw % 2))
            pw //= 2
        result = 1
        for i in range(len(power_list)):
            if power_list[i][1]:
                result *= power_list[i][0]
                result %= mod
        return result

    def encrypt(self, block):
        message = int(block)
        encrypted = self.fast_power(message, self.open_key[1], self.open_key[0])
        # encrypted = (message ** self.open_key[1]) % self.open_key[0]
        return str(encrypted)

    def decrypt(self, block):
        message = int(block)
        decrypted = self.fast_power(message, self.private_key, self.open_key[0])
        # decrypted = (message ** self.private_key) % self.open_key[0]
        return str(decrypted)


class PrimeNum:
    def __init__(self, pq_from, pq_to):
        test_value = -1
        while test_value != 1:
            with WolframLanguageSession() as session:
                self.__prime_pair = session.evaluate(wl.RandomPrime({pq_from, pq_to}, 2))
                print('p, q = ', *self.__prime_pair, end=' | ')
                self.n = self.__prime_pair[0] * self.__prime_pair[1]
                phi_n = (self.__prime_pair[0] - 1) * (self.__prime_pair[1] - 1)
                coprime = False
                while not coprime:
                    rand_key = session.evaluate(wl.RandomPrime({self.__prime_pair[0] + 1, phi_n - 1}))
                    coprime = session.evaluate(wl.CoprimeQ(rand_key, phi_n))
                    print('rand_key =', rand_key, ' coprime =', coprime)
                # print('rand_key =', rand_key)
                prime_num = session.evaluate(wl.ExtendedGCD(phi_n, rand_key))
            # print('prime_num = (', prime_num[0], ', (', *prime_num[1], ')')
            self.open_key = (self.n, rand_key)
            self.private_key = prime_num[1][1] % self.n
            print(f'Open key = ({self.n}, {rand_key})')
            print(f'Private key = {self.private_key}')
            test_value = (rand_key * self.private_key) % phi_n
            print(f'Test: ({rand_key} * {self.private_key}) % {phi_n} = {test_value}', end=' | ')
            if test_value == 1:
                print('OK')
            else:
                print('failed')
        print('*' * 10)