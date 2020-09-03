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
    def levenshtein(a, b):
        if not (len(a) > 0 and len(b) > 0):
            msg = "|a| > |b| > 0"
            raise ValueError(msg)
        D = []
        for i in range(len(a)):
            D.append([])
            for j in range(len(b)):
                D[i].append(0)
        for i in range(len(a)):
            D[i][0] = i
        for j in range(len(b)):
            D[0][j] = j

        for i in range(len(a)):
            for j in range(len(b)):
                cost = [1, 0][a[i] == b[j]]
                D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + cost)
        #print(pprint.pprint(D))

        return D[-1][-1]

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
                if result1 != s and result2 != s and Algos.word_dist(result1, s) < 3 and Algos.word_dist(result2,
                                                                                                         s) < 3:
                    results.add(result1)
                    results.add(result2)

        return results
