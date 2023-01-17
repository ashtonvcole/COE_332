import names

# Exercise 1
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
print('Exercise 1')
longest_words.sort(key = len, reverse = True)
for j in range(len(longest_words)):
    print(longest_words[j])

# Exercise 2
print('Exercise 2')
count = 0
max = 5
while True:
    if count >= max:
        break
    name = names.get_full_name()
    if len(name) == 9:
        print(name)
        count = count + 1

# Exercise 3
