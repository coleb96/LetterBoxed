prompt = [
    ['g','i','o'],
    ['t','l','b'],
    ['y','u','p'],
    ['s','a','h']
] # 10/18/2023



all_letters = 'abcdefghijklmnopqrstuvwxyz-()/\\.0123456789'
exclude_letters = all_letters
for i in prompt:
    for j in i:
        exclude_letters = exclude_letters.replace(j, '')

with open('words.txt', 'r') as word_file:
    words = word_file.readlines()
words = [word.strip() for word in words]


print(f'Starting with list of {len(words)}.')

print('removing words that are too short...')
words = [word for word in words if len(word) > 2]
print(f'{len(words)} words remaining for consideration')

print('removing words that contain non-prompt letters...')
words = [word for word in words if not any(letter in word for letter in exclude_letters)]
print(f'{len(words)} words remaining for consideration')

print('removing words with adjacent same-side letters...')
for p in prompt:
    for i, L in enumerate(p):
        words = [word for word in words if not (L+p[0] in word)]
        words = [word for word in words if not (L+p[1] in word)]
        words = [word for word in words if not (L+p[2] in word)]
print(f'{len(words)} words remaining for consideration')

def contains_all_letters(word_list, prompt):
    all_words = []
    for word in word_list:
        all_words += word

    all_letters = []
    for p in prompt:
        for L in p:
            all_letters += L

    for letter in all_letters:
        if letter not in all_words:
            return False
    return True

def contains_a_solution(list_word_list, prompt):
    for word_list in list_word_list:
        if contains_all_letters(word_list, prompt):
            return True
    return False

def return_solutions(list_word_list, prompt):
    solutions = []
    for word_list in list_word_list:
        if contains_all_letters(word_list, prompt):
            solutions.append(word_list)
    return solutions

print('Searching for solutions...')
best_solutions = [['a','b','c','d', 'e']] # Start with a dummy solution to be overwritten
for word in words: # Evaluate possible solutions for each starting word
    list_word_list = [[word]] # initialize the potential solution list
    while (not contains_a_solution(list_word_list, prompt)) & (len(list_word_list[0]) < len(best_solutions[0])): # Stop adding words when the potential soltion list contains a solution or is already longer than previous solutions
        next_word_list = [] # Initialize next iteration of potential solutions list
        for word_list in list_word_list: # for each potential solution
            next_words = [word for word in words if word[0] == word_list[-1][-1]] # Next word should start with the same letter as the last of the previous word
            for next_word in next_words:
                next_word_list.append(
                    word_list + [next_word]
                ) # This will create a new potential solution list by adding all possible additional words to all the entries of the previous potential solutions list
        list_word_list = next_word_list # overwrite with new iteration of potential solutions
        
    if contains_a_solution(list_word_list, prompt):
        if len(list_word_list[0]) < len(best_solutions[0]):
            best_solutions = return_solutions(list_word_list, prompt) # These are the new best solutions
        else:
            best_solutions += return_solutions(list_word_list, prompt) # These will be added to the list of best solutions
    

print(f'Found {len(best_solutions)} solutions with {len(best_solutions[0])} words each. Here they are:')
for solution in best_solutions:
    print('   ' + ','.join(solution))
