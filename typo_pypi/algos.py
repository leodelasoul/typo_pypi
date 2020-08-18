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
    def levenshtein(a, b):
        pass

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
            results.add(Algos.delete(s, i))
            for j, _ in enumerate(s):
                # if len(s) == j:
                if len(s) == j:
                    results.add(Algos.insert(s, char, j))
                    results.add(Algos.replace(s, i, j))

        return results
