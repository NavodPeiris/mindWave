def is_repeating(text):

    repeated_words = set()
    repetitions = 0

    words = text.split()
    for i in range(len(words)-1):
        if words[i] == words[i+1]:
            repeated_words.add(words[i])
            repetitions += 1

    print("Repeated Words:", repeated_words)

    return repetitions