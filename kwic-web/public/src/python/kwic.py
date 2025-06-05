from pyodide.ffi import to_js
from collections import defaultdict

def word_tokenize(text):
    """
    Simple word tokenizer that splits on whitespace and punctuation
    """
    import re
    # Split on whitespace and punctuation
    tokens = re.findall(r'\w+|[^\w\s]', text)
    return tokens

def pos_tag(tokens):
    """
    Simple POS tagger with basic grammatical rules
    """
    import re
    
    # Basic POS tagging rules
    pos_tagged = []
    
    for i, token in enumerate(tokens):
        token_lower = token.lower()
        
        # Numbers
        if re.match(r'^\d+$', token):
            pos = 'CD'  # Cardinal number
        elif re.match(r'^\d+(st|nd|rd|th)$', token_lower):
            pos = 'JJ'  # Ordinal number
        
        # Punctuation
        elif token in '.!?':
            pos = '.'   # Sentence terminator
        elif token in ',;:':
            pos = ','   # Comma
        elif token in '()[]{}':
            pos = '-LRB-' if token in '([{' else '-RRB-'
        elif token in '"\'':
            pos = '``' if i == 0 or tokens[i-1] in ' \t\n' else '\'\''
        
        # Common function words
        elif token_lower in ['the', 'a', 'an']:
            pos = 'DT'  # Determiner
        elif token_lower in ['is', 'are', 'was', 'were', 'be', 'being', 'been']:
            pos = 'VBZ' if token_lower in ['is'] else 'VBP' if token_lower in ['are'] else 'VBD' if token_lower in ['was', 'were'] else 'VB'
        elif token_lower in ['have', 'has', 'had']:
            pos = 'VBZ' if token_lower == 'has' else 'VBD' if token_lower == 'had' else 'VBP'
        elif token_lower in ['do', 'does', 'did']:
            pos = 'VBZ' if token_lower == 'does' else 'VBD' if token_lower == 'did' else 'VBP'
        elif token_lower in ['will', 'would', 'can', 'could', 'may', 'might', 'shall', 'should', 'must']:
            pos = 'MD'  # Modal
        elif token_lower in ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']:
            pos = 'PRP'  # Personal pronoun
        elif token_lower in ['my', 'your', 'his', 'her', 'its', 'our', 'their']:
            pos = 'PRP$'  # Possessive pronoun
        elif token_lower in ['this', 'that', 'these', 'those']:
            pos = 'DT'  # Demonstrative
        elif token_lower in ['and', 'or', 'but', 'yet', 'so', 'for', 'nor']:
            pos = 'CC'  # Coordinating conjunction
        elif token_lower in ['in', 'on', 'at', 'by', 'for', 'with', 'to', 'from', 'of', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once']:
            pos = 'IN'  # Preposition
        elif token_lower in ['not', 'never', 'no', 'none', 'nobody', 'nothing', 'nowhere', 'neither', 'nor']:
            pos = 'RB'  # Adverb (negation)
        elif token_lower in ['very', 'quite', 'rather', 'really', 'too', 'so', 'more', 'most', 'less', 'least']:
            pos = 'RB'  # Adverb (degree)
        
        # Morphological patterns
        elif token_lower.endswith('ly'):
            pos = 'RB'  # Adverb
        elif token_lower.endswith('ing'):
            pos = 'VBG'  # Present participle/gerund
        elif token_lower.endswith('ed'):
            pos = 'VBD'  # Past tense verb
        elif token_lower.endswith('er') and len(token) > 3:
            pos = 'JJR'  # Comparative adjective
        elif token_lower.endswith('est') and len(token) > 4:
            pos = 'JJS'  # Superlative adjective
        elif token_lower.endswith('s') and len(token) > 2 and not token_lower.endswith('ss'):
            # Check if likely plural noun or 3rd person singular verb
            if i > 0 and tokens[i-1].lower() in ['the', 'these', 'those', 'many', 'few', 'several']:
                pos = 'NNS'  # Plural noun
            else:
                pos = 'VBZ'  # 3rd person singular verb
        elif token_lower.endswith('tion') or token_lower.endswith('sion') or token_lower.endswith('ment') or token_lower.endswith('ness'):
            pos = 'NN'  # Noun
        
        # Capitalization patterns
        elif token[0].isupper() and i > 0 and tokens[i-1] not in '.!?':
            pos = 'NNP'  # Proper noun
        
        # Default cases
        elif token.isalpha():
            # Check context for better guessing
            if i > 0 and tokens[i-1].lower() in ['the', 'a', 'an', 'this', 'that', 'my', 'your', 'his', 'her', 'its', 'our', 'their']:
                pos = 'NN'  # Noun after determiner
            elif i < len(tokens) - 1 and tokens[i+1].lower() in ['is', 'are', 'was', 'were', 'will', 'would']:
                pos = 'NN'  # Noun before verb
            else:
                pos = 'NN'  # Default to noun for unknown words
        else:
            pos = 'SYM'  # Symbol
        
        pos_tagged.append((token, pos))
    
    return pos_tagged

def ne_chunk(tagged_tokens):
    """
    Simple NE chunker that returns the original tagged tokens
    """
    return tagged_tokens

class Tree:
    def __init__(self, label, leaves):
        self.label = label
        self.leaves = leaves
    
    def label(self):
        return self.label

def extract_named_entities(tree):
    entities = []
    for subtree in tree:
        if isinstance(subtree, Tree):
            entity_label = subtree.label()
            entity_text = " ".join(token for token, pos in subtree.leaves())
            entities.append((entity_text, entity_label))
    return entities

async def kwic_search(text, search_term, input_mode="word", output_mode="default", window=5):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    ner_tree = ne_chunk(pos_tags)
    entities = extract_named_entities(ner_tree)
    
    results = []

    if input_mode == "word":
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
                results.append({
                    "left": left,
                    "keyword": keyword,
                    "right": right,
                    "start": i,
                    "end": i + seq_len,
                    "pos_tags": [tag for _, tag in pos_tags[i:i+seq_len]],
                    "next_word": right[0] if len(right) > 0 else "",
                    "next_pos": pos_tags[i+seq_len][1] if i+seq_len < len(pos_tags) else ""
                })

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
                results.append({
                    "left": left,
                    "keyword": keyword,
                    "right": right,
                    "start": i,
                    "end": i + seq_len,
                    "pos_tags": tag_seq,
                    "next_word": right[0] if len(right) > 0 else "",
                    "next_pos": pos_tags[i+seq_len][1] if i+seq_len < len(pos_tags) else ""
                })

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
                    results.append({
                        "left": left,
                        "keyword": entity_text,
                        "right": right,
                        "start": idx,
                        "end": idx + 1,
                        "pos_tags": [pos_tags[idx][1]],
                        "next_word": right[0] if len(right) > 0 else "",
                        "next_pos": pos_tags[idx+1][1] if idx+1 < len(pos_tags) else "",
                        "entity_label": entity_label
                    })
                except (ValueError, IndexError):
                    continue

    else:
        raise ValueError("input_mode must be 'word', 'pos', or 'ner'")    # Sort results based on output mode (standard KWIC output formats)
    if output_mode == "kwic" or output_mode == "default":
        # Standard KWIC format: sort alphabetically by keyword
        def get_kwic_score(result):
            keyword = result["keyword"].lower()
            return keyword
        
        sorted_results = sorted(results, key=get_kwic_score)
        
    elif output_mode == "frequency":
        # Sort by collocation frequency (most frequent collocations first)
        frequent_next_word = defaultdict(int)
        for result in results:
            if result["next_word"]:
                frequent_next_word[result["next_word"]] += 1
        
        def get_frequency_score(result):
            next_word = result["next_word"]
            return -frequent_next_word.get(next_word, 0) if next_word else float('inf')
        
        sorted_results = sorted(results, key=get_frequency_score)
        
    elif output_mode == "right_sort":
        # Sort alphabetically by right context (next word)
        def get_right_sort_score(result):
            next_word = result["next_word"].lower() if result["next_word"] else ""
            return next_word
        
        sorted_results = sorted(results, key=get_right_sort_score)
        
    elif output_mode == "left_sort":
        # Sort alphabetically by left context (previous word)
        def get_left_sort_score(result):
            left_words = result["left"]
            prev_word = left_words[-1].lower() if left_words else ""
            return prev_word
        
        sorted_results = sorted(results, key=get_left_sort_score)
        
    elif output_mode == "position":
        # Sort by position in original text (chronological order)
        sorted_results = sorted(results, key=lambda x: x["start"])
        
    else:
        # Default: standard KWIC alphabetical sort by keyword
        def get_default_score(result):
            keyword = result["keyword"].lower()
            return keyword
        
        sorted_results = sorted(results, key=get_default_score)

    return to_js(sorted_results)
