_MAX_NUMBER_OF_SUGGESTIONS = 10

class _Node:
    def __init__(self, data):
        self.data = data
        self.end_of_word = False
        self.child = {}

class Trie:
    def __init__(self):
        self.root = _Node(None)

    def insert(self, word):
        word = word.strip()
        curr = self.root
        while word:
            if word[0] not in curr.child:
                curr.child[word[0]] = _Node(word[0])
            curr = curr.child[word[0]]
            word = word[1:]
            if len(word) is 0:
                curr.end_of_word = True

    def batch_insert(self, words):
        for word in words:
            self.insert(word)

    def search(self, word):
        result = []
        curr = self.root
        og_word = word

        while word:
            if word[0] not in curr.child:
                return result
            curr = curr.child[word[0]]
            word = word[1:]

        if curr.end_of_word:
            result.append(og_word)

        def _search_helper(self, word, node):
            if len(result) >= _MAX_NUMBER_OF_SUGGESTIONS:
                return result
            for child_node in node.child.values():
                if child_node.end_of_word and len(result) < _MAX_NUMBER_OF_SUGGESTIONS:
                    result.append(word + child_node.data)
                _search_helper(self, word + child_node.data, child_node)
            return result
        return _search_helper(self, og_word, curr)
