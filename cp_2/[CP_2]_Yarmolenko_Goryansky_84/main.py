from itertools import *

def shift(offset, char):
    o_char = ord(char)
    out = o_char + (ord(offset) - 1072)
    if o_char < 1072 or o_char > 1103:
        return char
    else:
        if out>1103:
            return chr(out - 31 - 1)
        else:
            return chr(out)


def reverse_shift(offset, char):
    o_char = ord(char)
    out = o_char - (ord(offset) - 1072)
    if o_char < 1072 or o_char > 1103:
        return char
    else:
        if out<1072:
            return chr(1103-(1072-out) + 1)
        else:
            return chr(out)


def encrypt(key, text):
    l = len(key)
    out = []
    for (i, c) in enumerate(text):
        out.append(shift(key[i%l],c))
    return ''.join(out)


def decrypt(key, text):
    l = len(key)
    out = []
    for (i, c) in enumerate(text):
        out.append(reverse_shift(key[i%l],c))
    return out

def occurrences(lst):
    out = {}
    for c in lst:
        if c in out:
            out[c] += 1
        else:
            out[c] = 1
    return out


def I(text):
    occs = occurrences(text)
    n = len(text)
    out = 0
    for t in occs.values():
        out += (t*(t-1))/(n*(n-1))
    return out


def get_text(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.read().replace('\n', '')

def write(path, text):
    f = open(path, "w", encoding="utf-8")
    f.write(text)
    f.close()

def nth(n, text):              
    if n == 0:
        return text
    return text[0::n]


def splitted(r, text):
    out = []
    for i in range(r):
        out.append(nth(r, text[i:]))
    return out


def i_splitted(r, text):
    out = 0
    for sub in splitted(r, text):
        out += I(sub)
    return out/r        


def encrypt_all(words, path):
    text = get_text(path)
    for word in words:
        enc = encrypt(word, text)
        write(f'{path}_{word}', enc)

def indexes_all(words, path):
    text = get_text(f'{path}')
    print(f'    :-:{I(text)}')
    for word in words:
        text = get_text(f'{path}_{word}')
        print(f'{word}:{len(word)}:{I(text)}')
#14


def decrypt_by_len(text, size):
    blocks = splitted(size, text)
    occs_of_blocks = [occurrences(b) for b in blocks]
    
    most_frequent = [list(sorted(occ.items(), key=lambda x: x[1], reverse=True))[0][0] for occ in occs_of_blocks]
    all_rus = ['о', 'е', 'а']
    for rus in product(all_rus, repeat = size):

        key = ''.join(list(map(lambda x: reverse_shift(x[0], x[1]),zip(rus, most_frequent))))
        print(rus, end='|')
        print(key)
#('о', 'е', 'о', 'о', 'о', 'е', 'о', 'о', 'о', 'о', 'о', 'о', 'а', 'о')  экомаятникфуко
                
            
def prepate(path):
    text = get_text(path)
    write(path+'s', ''.join(filter(lambda x: ord(x) >= 1072 and ord(x) <= 1103, text.lower())))

def get_len(path):
    text = get_text(path)
    for i in range(1,60):
        print(f'{i} = {i_splitted(i, text)}')

my_words = ['да', 'они', 'танк', 'мышка', 'синергетический']
def main():
    #decrypt_by_len(get_text('text'),14)
    #indexes_all(['да', 'они', 'танк', 'мышка', 'синергетический'], 'pervomu-igroku-prigotovitsya')
    print(get_len('text.txt'))
    #print("".join(decrypt('экомаятникфуко', get_text('text.txt'))))
if __name__ == "__main__":
    main()