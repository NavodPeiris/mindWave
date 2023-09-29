def is_repeating(text):

    repeated_words = set()

    words = text.split()
    for i in range(len(words)-1):
        if words[i] == words[i+1]:
            repeated_words.add(words[i])

    print("Repeated Words:", repeated_words)

    if len(repeated_words) > 0:
        return True
    else:
        return False