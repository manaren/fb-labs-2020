# "рх","ну","уд","уо","до",

# a = 735, b = 300,


def gcd(x,y):
    if x == 0:
        return y
    return gcd(y%x, x)


def reverse_helper(a, b):
    if a == 0:
        if b != 1:
            return None
        else:
            return (a,b)
    c = reverse_helper(b%a,a)
    if c is None:
        return None
    (x,y) = c
    return (y-(b//a)*x, x)

def reverse(x,m):
    c = reverse_helper(x,m)
    if c is None:
        return None
    (a,b) = c
    return a%m


def solve(a, b, m):
    out = []
    d = gcd(a, m)
    if b%d != 0:
        return  None
    part = m // d
    mb_rev = reverse(a, part)
    if mb_rev == None:
        return None
    rev = (mb_rev*b)%part
    for i in range(d):
        out.append(rev+(i*part))
    return out
    

def ctonum(c):
    c = ord(c)
    shift = 1073
    if c in range(ord('а'), ord('ы')):
        shift -= 1
    return c - shift


def numtoc(num):
    shift = 1073
    if num in range(26):
        shift -= 1
    return chr(num+shift)


def bitonum(bi):
    a = bi[0]
    b = bi[1]
    return ctonum(a)*31+ctonum(b)


def numtobi(n):
    a = n//31
    b = n-(a*31)
    return (numtoc(a%31), numtoc(b%31))


def get_key(x1, y1, x2, y2):
    a = solve(bitonum(x1)- bitonum(x2), bitonum(y1)-bitonum(y2), 31**2)
    if a is None:
        return None
    return list(map(lambda ai: (ai, (bitonum(y1)-ai*bitonum(x1))%(31**2)), a))


def chunks(lst, n, shift=None):
    if shift is None:
        shift = n
    for i in range(0, len(lst), shift):
        out = lst[i:i + n]
        if len(out) != n:
            break
        yield out

def swapii(text):
    return ['ы' if c == 'ь' else  'ь' if c == 'ы' else c for c in text]


def decrypt(bi, a,b):
    rev = reverse(a, 31**2)
    if rev == None:
        return None
    dec = rev*(bitonum(bi)-b)
    return numtobi(dec%(31**2))

def get_text(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.read().replace('\n', '').replace('\r', '')

def decrypt2(no, yes, text):
    for i in no:
        for j in yes:
            for k in no:
                for m in yes:
                    if bitonum(i) != bitonum(k):
                        v = get_key(i,j,k,m)
                        if v is not None:
                            for (a,b) in v:
                                decr = list(map(lambda x: decrypt(x, a,b),text))

                                if decr[0] is not None:
                                    strings = map(lambda x: ''.join(x), decr)
                                    fin_text = ''.join(swapii(''.join(strings)))
                                    if check(fin_text):

                                        print(f'a = {a}, b = {b} \n {fin_text}, ')
                                    

def occurrences(lst):
    out = {}
    for c in lst:
        if c in out:
            out[c] += 1
        else:
            out[c] = 1
    return out


def check(text):
    freqs = list(sorted(occurrences(text).items(), key=lambda x: x[1], reverse=True))
    return freqs[0][0] == 'о' and freqs[1][0] == 'е'
        
txt = list(chunks(swapii(get_text('23.txt')),2))


decrypt2(
    ["ст", "но", "то", "на", "ен"],
    ["рх","ну","уд","уо","до"],
    txt)


