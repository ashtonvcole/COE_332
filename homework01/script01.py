# Ashton Cole AVC687
# COE 332: Homework 1

# EXERCISE 1

longest_words = []
with open('words', 'r') as f:
    for line in f:
        word = line.strip('\n')
        length = len(word)
        if len(longest_words) < 5:
            longest_words.append(word)
        else:
            for i in range(5):
                if len(longest_words[i]) < len(word):
                    longest_words[i] = word
                    break
longest_words.sort(key = len, reverse = True)
for j in range(len(longest_words)):
    print(longest_words[j])
