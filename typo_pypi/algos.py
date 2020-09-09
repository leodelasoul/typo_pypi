import pprint
import random


class Algos:
    THRESHOLD = 1

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

        return D[-1][-1]

    @staticmethod
    def insert(s, c, i):
        all_inserts = set()
        assert len(s) > 0 and len(c) == 1 \
               and i in range(0, len(s) + 1)

        result0 = s[:i] + Algos.fat_finger(c) + s[i:]  # fatfinger
        result1 = s[:i] + c + s[i:]  # simple charrepetition
        if Algos.levenshtein(result0, s) <= Algos.THRESHOLD:
            all_inserts.add(result0)
        if Algos.levenshtein(result1, s) <= Algos.THRESHOLD:  # avoid false positives
            all_inserts.add(result1)

        return all_inserts

    @staticmethod
    def fat_finger(c):
        qwertz = {
            '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7zt5', '7': '8uz6', '8': '9iu7',
            '9': '0oi8', '0': 'po9',
            'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6zgfr5', 'z': '7uhgt6', 'u': '8ijhz7',
            'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
            'a': 'qwsy', 's': 'edxyaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'zhbvft', 'h': 'ujnbgz', 'j': 'ikmnhu',
            'k': 'olmji', 'l': 'kop',
            'y': 'asx', 'x': 'ysdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk',
        }
        qwerty = {  # TODO insert qwerty layout

        }
        if c in qwertz:
            one_char = qwertz[c]
            one_char = list(one_char)
            return one_char[random.randrange(0, len(one_char) - 1)]
        else:
            return ""

    @staticmethod
    def replace(s, i, j,c):
        all_replace = set()
        assert (len(s) > 0 and j in range(0, len(s))
                and i in range(0, len(s)))
        l = list(s)
        result1 = Algos.homoglyph(s, i, j, c)
        tmp = l[i]
        l[i] = l[j]
        l[j] = tmp
        result0 = ''.join(l)

        if Algos.levenshtein(result0, s) <= 2 and result0 != s:  # 2 threshold -> could resolve in more false positives
            all_replace.add(result0)
        if s not in result1:
            all_replace.add(result1)
        return all_replace

    @staticmethod
    def homoglyph(s,i,j,c):
        s = list(s)
        glyph_map = {'1': "１",
                     '2': "２",
                     '3': "３",
                     '4': "４",
                     '5': "５",
                     '6': "６",
                     '7': ["𐒇", "７"],
                     '8': ["Ց", "&", "８"],
                     '9': ["９"],
                     '0': ["Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ"],
                     'a': ["à", "á", "â", "ã", "ä", "å", "а", "ɑ", "α", "а", "ａ"],
                     'A': ["À", "Á", "Â", "Ã", "Ä", "Å", "Ꭺ", "Ａ"],
                     'b': ["d", "lb", "ib", "ʙ", "Ь", "ｂ", "ß"],
                     'B': ["ß", "Β", "β", "В", "Ь", "Ᏼ", "ᛒ", "Ｂ"],
                     'c': ["ϲ", "с", "ⅽ"],
                     'C': ["Ϲ", "С", "с", "Ꮯ", "Ⅽ", "ⅽ", "𐒨", "Ｃ"],
                     'd': ["b", "cl", "dl", "di", "ԁ", "ժ", "ⅾ", "ｄ"],
                     'e': ["é", "ê", "ë", "ē", "ĕ", "ė", "ｅ", "е"],
                     'f': ["Ϝ", "Ｆ", "ｆ"],
                     'g': ["q", "ɢ", "ɡ", "Ԍ", "Ԍ", "ｇ"],
                     'h': ["lh", "ih", "һ", "ｈ"],
                     'i': ["1", "l", "Ꭵ", "ⅰ", "ｉ"],
                     'j': ["ј", "ｊ"],
                     'k': ["ik", "lk", "lc", "κ", "ｋ"],
                     'l': ["1", "i", "ⅼ", "ｌ", "ӏ"],
                     'm': ["n", "nn", "rn", "rr", "ⅿ", "ｍ"],
                     'n': ["m", "r", "ｎ"],
                     'o': ["0", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ"],
                     'p': ["ρ", "р", "ｐ", "р"],
                     'q': ["g", "ｑ"],
                     'r': ["ｒ", "ʀ"],
                     's': ["ｓ", "Ꮪ", "Ｓ"],
                     't': ["ｔ", "τ"],
                     'u': ["ｕ", "υ", "Ս", "Ｕ", "μ"],
                     'v': ["ｖ", "ѵ", "ⅴ"],
                     'w': ["vv", "ѡ", "ｗ"],
                     'x': ["ⅹ", "ｘ"],
                     'y': ["ʏ", "γ", "у", "Ү", "ｙ"],
                     'z': ["ｚ"],
                     }
        if c in glyph_map:
            #for symbol in glyph_map[c]:
            #    l[i] = symbol
            #    homo_glyph = ''.join(l)
            #    homo_glyphs.add(homo_glyph)
            s[j] = glyph_map[c][0]  #otherwise the variation of typos would not be considered useful
            homo_glyph = ''.join(s)
            return homo_glyph
        else:
            return ""



    @staticmethod
    def delete(s, i):
        all_removes = set()
        assert (len(s) > 0 and i in range(0, len(s)))
        result0 = s[:i] + s[i + 1:]  # remove one char from string for each i
        all_removes.add(result0)
        return all_removes

    @staticmethod
    def remove_hyphen(s, i):
        return Algos.delete(s, i)

    @staticmethod
    def generate_typo(s):
        results = set()
        for i, char in enumerate(s):
            results.update(Algos.delete(s, i))
            if char == "-" or char == "/":
                results.update(Algos.remove_hyphen(s, i))  # should resolve in levdistance 1
            for j, _ in enumerate(s):
                results.update(Algos.insert(s, _, j))
                results.update(Algos.replace(s, i, j,_))
        return results
