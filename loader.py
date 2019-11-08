import os


LEXICON_PATH = os.getenv('LEXICON_PATH',
                         '/Users/cesar/coding/aerolith-infra/lexica')

# Years:
# 1979 OSPD1
# 1991 OSPD2
# 1992 ? some update to OSPD2?
# 1996 OWL?
# 1998 OSPD3?
# 2006 OWL2
# 2015 OWL3
# 2016 OWL3.1 -- long words
# 2019 NWL18

years = [1979, 1991, 1992, 1996, 1998, 2006, 2015, 2016, 2019]


def extract_words(f):
    words = f.read()
    out = set()
    for w in words.split('\n'):
        sp = w.split(' ', 1)
        if len(sp) > 0:
            word = sp[0].strip().upper()
            if word != '':
                out.add(word)
    return out


def tryint(s):
    if s != '':
        return int(s)
    return ''


def extract_joey(f):
    words = f.read()
    out = {}
    for w in words.split('\n'):
        if '---' in w:
            continue
        sp = w.split(None, 1)
        if len(sp) < 2:
            continue

        # The word is definitely the first element
        word = sp[0]
        if word[-1] == '*':
            word = word[:-1]  # Remove asterisk; history below will fix it.
        addl_info = sp[1].split(',')
        if word not in out:
            out[word] = set()

        if len(addl_info) > 1:
            # This word was deleted and then readded later. Just count one
            # comma for now for simplicity.
            assert len(addl_info) == 2
            first_appearance, first_deletion = [
                tryint(y) for y in addl_info[0].split('-')]
            second_appearance, second_deletion = [
                tryint(y) for y in addl_info[1].split('-')]
            for year in years:
                if year >= first_appearance and year < first_deletion:
                    out[word].add(year)
                if year >= second_appearance and (second_deletion == '' or
                                                  year < second_deletion):
                    out[word].add(year)
        else:
            # Just one addition and one possible deletion
            first_appearance, first_deletion = [
                tryint(y) for y in addl_info[0].split('-')]
            for year in years:
                if year >= first_appearance and (first_deletion == '' or
                                                 year < first_deletion):
                    out[word].add(year)

    return out


def loader():
    with open(os.path.join(LEXICON_PATH, 'NWL18.txt')) as f:
        nwl18 = extract_words(f)

    with open(os.path.join(LEXICON_PATH, 'joey-newwords.txt')) as f:
        word_history = extract_joey(f)
    # Assume every word in NWL18 was good in 1979 unless told otherwise
    # I'm pretty sure this is not true for long words, but that's ok; we
    # know there was a separate long word dictionary back then and I
    # have to draw the line somewhere.

    for year in years:
        f = open(os.path.join(LEXICON_PATH, f'pseudo_twl{year}.txt'), 'w')
        this_dict = set()
        for word, wh_years in word_history.items():
            if year in wh_years:
                # This word is good in this year
                this_dict.add(word)

        for word in nwl18:
            if word in word_history and year not in word_history[word]:
                # Although this word is good in nwl18 it was not good in the given
                # year
                continue
            this_dict.add(word)
        this_dict = sorted(list(this_dict))
        for w in this_dict:
            f.write(w + '\n')
        f.close()


if __name__ == '__main__':
    loader()