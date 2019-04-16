from datasketch import MinHash

def get_variable(name):
    loc = locals()
    key = ''
    for key in loc:
        if loc[key] == name:
            return key


def parse_segged_word(doc):
    if doc is None or doc is "":
        return []
    return [word.split(':')[0] for sentence in doc.split(';') for word in sentence.split(',')]


def compute_min_hash(word_list):
    m = MinHash()
    for word in word_list:
        m.update(word.encode())
    return m


def update_min_hash(m, word_list):
    for word in word_list:
        m.update(word.encode())
    return m