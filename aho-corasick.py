""" Algoritmo de Aho-Corasick"""

from collections import deque
AdList = []

def init_trie(keywords):
    create_empty_trie()
    add_keywords(keywords)
    set_fail_transitions()

def create_empty_trie():
    AdList.append({'value': '', 'next_states': [], 'fail_state': 0, 'output': []})

def add_keywords(keywords):
    for keyword in keywords:
        add_keyword(keyword)

def add_keyword(keyword):
    current_state = 0
    j = 0
    keyword = keyword.lower()
    child = find_next_state(current_state, keyword[j])
    while child != None:
        current_state = child
        j = j + 1
        if j < len(keyword):
            child = find_next_state(current_state, keyword[j])
        else:
            break
    
    for i in range(j, len(keyword)):
        node = {'value': keyword[i], 'next_states': [], 'fail_state': 0, 'output': []}
        AdList.append(node)
        AdList[current_state]["next_states"].append(len(AdList) - 1)
        current_state = len(AdList) - 1
    AdList[current_state]["output"].append(keyword)

def find_next_state(current_state, value):
    for node in AdList[current_state]["next_states"]:
        if AdList[node]["value"] == value:
            return node
    return None


def set_fail_transitions():
    q = deque()
    child = 0
    for node in AdList[0]["next_states"]:
        q.append(node)
        AdList[node]["fail_state"] = 0
    while q:
        r = q.popleft()
        for child in AdList[r]["next_states"]:
            q.append(child)
            state = AdList[r]["fail_state"]

            while find_next_state(state, AdList[child]["value"]) == None and state != 0:
                state = AdList[state]["fail_state"]
            
            AdList[child]["fail_state"] = find_next_state(state, AdList[child]["value"])

            if AdList[child]["fail_state"] is None:
                AdList[child]["fail_state"] = 0
            
            AdList[child]["output"] = AdList[child]["output"] + AdList[AdList[child]["fail_state"]]["output"]

def get_keywords_found(line):
    line = line.lower()
    current_state = 0
    keywords_found = []

    for i in range(len(line)):
        while find_next_state(current_state, line[i]) is None and current_state != 0:
            current_state = AdList[current_state]["fail_state"]
        current_state = find_next_state(current_state, line[i])

        if current_state is None:
            current_state = 0
        
        else:
            for j in AdList[current_state]["output"]:
                keywords_found.append({"index": i-len(j) + 1, "words": j})
    
    return keywords_found

# init_trie(['bol', 'fut', 'futebol'])
# print(get_keywords_found("futebolista"))


init_trie(['ta'])
print(get_keywords_found('Importance'))