import pprint


class Algos:

    @staticmethod
    def hamming_distance(a, b):
        if not len(a) == len(b):
            raise Exception("Strings a and b must have the samelength.")
        n = 0
        for i, j in zip(a, b):
            if i != j:
                n += 1
        return n

    @staticmethod
    def hamming_threshold(s, a):
        if Algos.hamming_distance(s, a) < 3:
            return True
        else:
            return False

    @staticmethod
    def word_dist(a, b):
        tmp = a
        tmp1 = b
        if len(a) > len(b):
            pass
        else:
            b = tmp
            a = tmp1
        n = len(list(a)) - len(list(b))
        return n

    @staticmethod
    def insert(s, c, i):
        assert len(s) > 0 and len(c) == 1 \
               and i in range(0, len(s) + 1)
        return s[:1] + c + s[i:]

    @staticmethod
    def replace(s, i, j):
        assert (len(s) > 0 and j in range(0, len(s))
                and i in range(0, len(s)))
        l = list(s)
        tmp = l[i]
        l[i] = l[j]
        l[j] = tmp
        return ''.join(l)

    @staticmethod
    def delete(s, i):
        assert (len(s) > 0 and i in range(0, len(s)))
        return s[:i] + s[i + 1:]

    @staticmethod
    def generate_typo(s):
        results = set()

        for i, char in enumerate(s):
            result0 = Algos.delete(s, i)
            if Algos.word_dist(s, result0) < 3:
                results.add(result0)
            for j, _ in enumerate(s):
                result1 = Algos.insert(s, char, j)
                result2 = Algos.replace(s, i, j)
                if result1 != s and result2 != s and Algos.word_dist(result1, s) < 3 and Algos.word_dist(result2, s) < 3:
                    results.add(result1)
                    results.add(result2)

        return results
