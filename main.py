import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from termcolor import colored

from collections import defaultdict

def side_fill(string, size=50, fill="."):
    l = len(string) // 2
    side = fill * max(0, size - l)
    return side + " " + string + " " + side

def extract_named_entities(tree):
    entities = []
    for subtree in tree:
        if isinstance(subtree, Tree):
            entity_label = subtree.label()
            entity_text = " ".join(token for token, pos in subtree.leaves())
            entities.append((entity_text, entity_label))
    return entities

def kwic_search(text, search_term, input_mode="word", output_mode="default", window=5, highlight_color="blue", collocate_color="cyan"):

    print(f"{search_term=}, {input_mode=}, {output_mode=}")
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    ner_tree = ne_chunk(pos_tags)
    entities = extract_named_entities(ner_tree)
    
    results = []

    if input_mode == "word":
        # Convert search_term to list for multi-word matching
        if isinstance(search_term, str):
            search_seq = word_tokenize(search_term.lower())
        else:
            search_seq = [w.lower() for w in search_term]
        seq_len = len(search_seq)

        for i in range(len(tokens) - seq_len + 1):
            if [t.lower() for t in tokens[i:i+seq_len]] == search_seq:
                left = tokens[max(0, i-window):i]
                keyword = " ".join(tokens[i:i+seq_len])
                right = tokens[i+seq_len:i+seq_len+window]
                results.append((left, keyword, right, i, i + seq_len))

    elif input_mode == "pos":
        if isinstance(search_term, str):
            search_seq = [search_term]
        else:
            search_seq = list(search_term)
        seq_len = len(search_seq)

        for i in range(len(pos_tags) - seq_len + 1):
            tag_seq = [tag for _, tag in pos_tags[i:i+seq_len]]
            if tag_seq == search_seq:
                left = tokens[max(0, i-window):i]
                keyword = " ".join(tokens[i:i+seq_len])
                right = tokens[i+seq_len:i+seq_len+window]
                results.append((left, keyword, right, i, i + seq_len))

    elif input_mode == "ner":

        word_list = defaultdict(list)
        word_count = defaultdict(int)

        for i in range(len(tokens)):
            word = tokens[i]
            word_list[word].append(i)

        for entity_text, entity_label in entities:
            if entity_label == search_term:
                try:
                    word = entity_text.split()[0]
                    idx = word_list[word][word_count[word]]
                    word_count[word] += 1
                    left = tokens[max(0, idx-window):idx]
                    right = tokens[idx+1:idx+1+window]
                    results.append((left, entity_text, right, idx, idx + 1))
                except ValueError:
                    continue
    else:
        raise ValueError("input_mode must be 'word', 'pos', or 'ner'")

    frequent_word = defaultdict(list)
    frequent_tag = defaultdict(list)
    frequent_entity = defaultdict(list)

    next_frequent_word = defaultdict(int)
    next_frequent_tag = defaultdict(int)
    next_frequent_entity = defaultdict(int)

    word_to_entity = defaultdict(str)

    # Pre-Process
    for entity_text, entity_label in entities:
        word_to_entity[entity_text] = entity_label

    for i in range(len(results)):
        left, keyword, right, l, r = results[i]
        tag_seq = tuple([tag for _, tag in pos_tags[l:r]])
        
        keyword_entity = word_to_entity[keyword]
        nextword_entity = word_to_entity[right[0]] if len(right) > 0 else ""

        frequent_word[keyword].append(i)
        frequent_tag[tag_seq].append(i)
        frequent_entity[keyword_entity].append(i)
        
        if len(right) > 0:
            next_frequent_word[right[0]] += 1
            next_frequent_tag[pos_tags[r]] += 1
            next_frequent_entity[nextword_entity] += 1
    
    def get_vector(i):
        left, keyword, right, l, r = results[i]
        next_rank = (-next_frequent_word[right[0]], right[0],
                     -next_frequent_tag[pos_tags[r]], pos_tags[r],
                     -next_frequent_entity[next_frequent_entity[right[0]]], frequent_entity[right[0]])
        return next_rank
    
    # Default Setting
    if output_mode == "collocation" or output_mode == "default":
        order = sorted(range(len(results)), key = get_vector)
        for i in range(len(results)):
            left, keyword, right, l, r = results[order[i]]
            right.append("")
            collocate_context = right[0]
            left_context = " ".join(left)
            right_context = " ".join(right[1:])
            print(f"{i}. {left_context} {colored(keyword, highlight_color)} {colored(collocate_context, collocate_color)} {right_context} {pos_tags[r]}")

    # Sequentially
    elif output_mode == "sequentially":
        print(side_fill("Results in sequentially"))
        for i in range(len(results)):
            left, keyword, right, l, r = results[i]
            left_context = " ".join(left)
            right_context = " ".join(right)
            print(f"{i}. {left_context} {colored(keyword, highlight_color)} {right_context}")
     
    # Most frequent token
    elif output_mode == "frequent_word":
        print(side_fill("Results in keyword frequency order"))
        order = sorted(frequent_word.keys(), key = lambda x: -len(frequent_word[x]))
        for key in order:
            print(f"[token = {key}, frequency = {len(frequent_word[key])}]:")
            for i in frequent_word[key]:
                left, keyword, right, l, r = results[i]
                left_context = " ".join(left)
                right_context = " ".join(right)
                print(f"    {left_context} {colored(keyword, highlight_color)} {right_context}")

    # Most frequent token
    elif output_mode == "frequent_pos":
        print(side_fill("Results in POG tag frequency order"))
        order = sorted(frequent_tag.keys(), key = lambda x: -len(frequent_tag[x]))
        for key in order:
            print(f"[token = {list(key)}, frequency = {len(frequent_tag[key])}]:")
            for i in frequent_tag[key]:
                left, keyword, right, l, r = results[i]
                left_context = " ".join(left)
                right_context = " ".join(right)
                print(f"    {left_context} {colored(keyword, highlight_color)} {right_context}")
    else:
        raise ValueError("output_mode must be 'default', 'sequentially', 'frequent_word' or 'frequent_pos'")

    print() # Blank

# Main Text
with open("text.txt", "r") as f:
    text = f.read()

kwic_search(text, ["that"], input_mode="word", window=3)
kwic_search(text, ["NNP", "CC"], input_mode="pos", output_mode="sequentially", window=3, highlight_color="green")
# kwic_search(text, ["NNP", "VBD"], input_mode="pos", window=5)
# kwic_search(text, "PERSON", input_mode="ner")
# kwic_search(text, "LOCATION", input_mode="ner")
