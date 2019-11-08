import sys

from loader import extract_words


if __name__ == '__main__':
    list1 = sys.argv[1]
    list2 = sys.argv[2]
    with open(list1) as f:
        l1_words = extract_words(f)
    with open(list2) as f:
        l2_words = extract_words(f)

    print(f'Words in {list1} not in {list2}:')
    print(l1_words - l2_words)
    print(len(l1_words - l2_words))
    print(f'Words in {list2} not in {list1}:')
    print(l2_words - l1_words)
    print(len(l2_words - l1_words))
