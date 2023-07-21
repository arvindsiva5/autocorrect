class TrieNode:
    def __init__(self, key: int = None, occ: int = 0) -> None:
        """
        Function description: Intializes a node with key that represents the charachter and occ which
                              is the number of occurences of the key

        :Input:
            key: An integer representing the ASCII code of the characther minus 96
            occ: An integer representing the number of occurences of the key at this position
                 in a list of sentences to be stored in CatsTrie
        :Output:
            No output
            A node for CatsTrie is initialized with key, occ and link

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        self.key = key  # the characther to store
        self.occ = occ  # the number of occurences of this characthere
        self.link = [None for _ in range(27)]  # links to children nodes

class Trie:
    def __init__(self, sentences: list[str]) -> None:
        """
        Function description: Initializes a trie that holds all the sentences together with the maximum number
                              of occurences of each characther to be able to determine the strings with the
                              highest probability in the trie

        Approach description:
        The words in sentences are stored in a trie data structure. To build the trie a node class TrieNode
        was created. The TrieNode stores the charcahter in the word as key. The TrieNode has link a
        list of size 27 that stores pointer to its child characther nodes. The 0-th index of link is used
        to store link to a terminal node to represent the end of the word. The index 1 to 26 in link store
        pointers to child nodes in order from character 'a' to 'z'. For example, if a node must have a childnode
        with key 'a', at link[1] the pointer to child node is stored while other index of link will be None.
        For every word in sentences, the word inserted into the trie by making nodes for each characther and
        using a terminal node with key '$' to end the word. To be able to autocomplete a prompt from sentences
        the nodes in the trie need to store the number of occurences. Moreover, a trie can only store unique words
        so by storing the number of occurences this will represent the frequency of each word helping in auto
        completing a prompt. When inserting a word, for every characther, if the characther does not have a node
        a new node is inserted with occ = 1 whereas if a node exists its occ is increased by 1 (same for
        terminal node to end the word). Then we backtrack from the terminal node to update the occ value of the
        nodes for the inserted word. When we backtrack from terminal node, for every node predescesing the
        terminal node, the maximum occ value of all its child nodes are found and this value is updated to be the
        new occ value of the node. This way of updating the occ for nodes for every word helps ensure the
        autocomplte can calculate the frequency of every word correctly and return the correct word based
        on autocomplete conditions.

        To insert a word of length M in a trie M+1 nodes must be inserted or have their occ updated. And to update
        the values, we traverse back from M+1 node (terminal node) to the root node. The operation to find the 
        max occ value of the child nodes is constant time O(1) because every node has constant link size of 27 so
        at most they have 27 child nodes. Hence, since inserting traverse down M times and up M times, the time 
        complexity to insert a node is O(M) and we have N word in sentences so we insert N times. Now lets say
        the longest word has length M in sentences. Taking this into account for worst case time complexity
        inserting every word in sentences will cost O(N*M).

        For every word of length M inserted in a trie there is at most M+1 nodes created. In this case we can say
        to insert a word we need Aux space complexity of O(M). Then we insert N words in sentences. Lets say the
        longest word in sentences is length M. Taking into account the worst acse aux space complexity, the aux
        space complexity of creating trie from sentences is O(N*M).

        :Input:
            sentences: A list of strings with N sentences, where N is a positive integer. The longest
            sentence would have M characters, as mapped from the cat vocabulary where, M is a positive integer.

        :Output:
            No output
            A trie with all the strings in sentences with the number of occurences of each characther
            at each position is created

        :Time complexity: O(N*M), where N is the number of strings in sentences
                                , where M is the length of the longest string in sentences
        :Aux space complexity: O(N*M), where N is the number of strings in sentences
                                     , where M is the length of the longest string in sentences
        """
        self.head = TrieNode()  # initialize root node in trie

        # insert all sentences to the trie
        for s in sentences:
            # insert only non empty strings
            if len(s) > 0:
                self.insert_node(self.head, s, 0)

    def insert_node(self, current: TrieNode, word: str, i: int) -> None:
        """
        Function description: Inserts a TrieNode for every charcather in word and updates their
                              occ based on the maximum number of occurneces of their child charcather.
                              The last node will have '$' as the key to terminate the word

        :Input:
            current: The current TrieNode being traveresed to insert a new TrieNode as its child
            word: The string to be inserted into Trie
            i: An integer representing the index of a characther in word
        :Output:
            No output
            A TrieNode with key of word[i] is added to the Trie or nothing TrieNode with key '$' is
            inserted if i >= len(s)

        :Time complexity: O(M), where M is the length of word
        :Aux space complexity: O(M), where M is the length of word
        """
        # executed if all characthers in word is inserted as nodes
        if i >= len(word):
            # if the word is already in trie, the terminal node occ is increased
            if current.link[0]:
                current.link[0].occ += 1
            # if the word is not in in trie, terminal node is inserted
            else:
                current.link[0] = TrieNode("$", 1)
            return  # end the insert process

        # executed to insert node for each charachter in word
        else:
            # get the index of link to store the node of word[i]
            index = ord(word[i]) - 96

            # if the node does not exists a new one is inserted
            if current.link[index] == None:
                current.link[index] = TrieNode(word[i], 1)

            # if the node exists, the occ is increased by 1
            else:
                current.link[index].occ += 1

            # recursive call to insert next char in word
            self.insert_node(current.link[index], word, i + 1)

            # updates the occ the node for word[i] with the maximum occurence value of
            # its children nodes
            current.link[index].occ = self.get_max_occ_value(current.link[index])

    def get_max_occ_value(self, current: TrieNode) -> int:
        """
        Function description: Finds the maximum number of occurences of the children charcather TrieNode
                              of a TrieNode if there is children. If the TrieNode has no children
                              (terminal node, key = '$') the number of occurences of the node is returned

        :Input:
            current: The current TrieNode being traveresed when inserting a string
        :Output:
            An integer representing the maximum value of occ of children in link
            or the value of current.occ if current has no child

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        # executed if current is a terminal node (no child)
        if current.key == "$":
            return current.occ  # number of occ of terminal node
        # executed if current ahs child
        else:
            # get index of child node with maximum occ value
            max_index = self.get_max_occ_node_index(current)
            # return value of maximum occ of the child node
            return current.link[max_index].occ

    def get_max_occ_node_index(self, current: TrieNode) -> tuple[int, bool]:
        """
        Function description: Finds the index of the children charcather TrieNode with the
                              maximum number of occurences if there is children. If two or more
                              children have same occ value as the maximum occurence the index of
                              the lexicographically smaller one is returned. If the TrieNode
                              has no children (terminal node, key = '$') the number of occurences
                              of the node is returned

        :Input:
            current: The current TrieNode being traveresed when lookup for a string
        :Output:
            An integer representing index of child in link with maximum occ value

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        # set to index of terminal node ($) if the node is the last charachther of a word
        index = 0
        # store maximum occurence of child node (lexicographically smallest one)
        max_occ = 0

        for i in range(len(current.link)):  # loop all child nodes
            if current.link[i] != None:  # if a node exists
                # update max_occ if current.link[i].occ more than max_occ
                # and update the indes to i
                if current.link[i].occ > max_occ:
                    max_occ = current.link[i].occ
                    index = i

        # return the index of child node with maximum occurence (highest frequency)
        return index

    def autoComplete(self, prompt: str) -> str:
        """
        Function description: Returns a string that represents the auto completed sentence from the prompt.
                              - If such a sentence exist, the completed sentence with the highest
                              frequency in the Trie is returned
                              - If there are multiple possible auto-complete sentences with the same
                              highest frequency, then the lexicographically smaller string is returned
                              - If such a sentence does not exist, None is returned

        Approach description:
        Earlier when creating the trie each node has key, occ and link. To auto complete the prompt the value
        of occ is used to determine the word with highest frequency from sentences. To autocomplete, it starts
        by traversing the trie based on characthers in prompt. If the length of prompt is longer than
        an existing word in the trie, None is returned. Next, when traversing the trie, if the last characther
        in prompt was found in trie, the occ value of the children nodes are checked. From here onwards,
        we traverse the nodes with highest occ values. When reaching the last char of prompt in trie, if the
        child node with highest occ is the terminal node, prompt is returned. If some other child node than
        terminal node had highest occ value we traverse down that node and continue traversing the child nodes
        with highest occ value till a terminal node is reached, in this case the string prompt added with the
        chars from traversal after prompt characthers are returned as the autocomplete string. Also when
        selecting the child node with max occ, if two or more of the nodes had same value which is the highest
        the lexicographically smaller one is selected. If the prompt is an empty string we traverse down
        the child nodes from the root node with max occ values to get the word with highest frequency in the
        trie for autocomplete. By doing all these the function will be able to autocomplete the prompt as
        specified in the specs.

        To autocmplete the prompt, in the trie we need to traverse the chars in prompt, if prompt has length
        of X, we need to visit X nodes and from the node of prompt last char, in the worst case there is a
        longer word with higher frequency that should be the autocomplete result. If so we need to traverse some
        extra nodes. This extra nodes represent a word with highest frequency starting from prompt or could be the
        terminal node where prompt has highest frequency. (If it is the terminal node we just need X operation
        and time complexity of O(X), same goes with prompt not found in trie). In the worst case this extra
        operations after traverse prompt can be the longest word in trie of length Y. A such we perform X + Y
        operations in the worst case resulting in a time complexity of O(X+Y). The finding of child nodes with 
        maximum occ is constant time which does not impact the O(X+Y) time complexity.

        For every node we traverse to autocmplete, we add the key to construct the auto completed word from prompt.
        When doing so, the time complexity is O(X+Y) and each node we add 1 char (constant sapce) to build the 
        auto completed word, so it consume X+Y extra space which gives aux space complexity of O(X+Y).

        :Input:
            prompt: A string that represents the incomplete sentence that is to be completed by the trie
        :Output:
            A string that represents the auto completed sentence from the prompt
            - If such a sentence exist, the completed sentence with the highest frequency in the
              cat sentences list is returned
            - If there are multiple possible auto-complete sentences with the same highest frequency,
              then the lexicographically smaller string is returned
            - If such a sentence does not exist, None is returned

        :Time complexity: O(X+Y), where X is the length of prompt
                                , where Y is the length of the string with highest occurence in Trie
        :Aux space complexity: O(X+Y), where X is the length of prompt
                                     , where Y is the length of the string with highest occurence in
                                     Trie
        """
        # traverse the trie to autocomplete the prompt
        return self.traverse(self.head, prompt, 0)

    def traverse(self, current: TrieNode, prompt: str, i: int) -> str:
        """
        Function description: Returns a string that represents the auto completed sentence from the prompt.
                              - If such a sentence exist, the completed sentence with the highest
                              frequency in the Trie is returned
                              - If there are multiple possible auto-complete sentences with the same
                              highest frequency, then the lexicographically smaller string is returned
                              - If such a sentence does not exist, None is returned

        :Input:
            current: The current TrieNode being traveresed when lookup for a string
            prompt: A string that represents the incomplete sentence that is to be completed by the trie
            i: The index of characther in prompt currently being traversed
        :Output:
            A string that represents the auto completed sentence from the prompt
            - If such a sentence exist, the completed sentence with the highest frequency in the
              cat sentences list is returned
            - If there are multiple possible auto-complete sentences with the same highest frequency,
              then the lexicographically smaller string is returned
            - If such a sentence does not exist, None is returned

        :Time complexity: O(X+Y), where X is the length of prompt
                                , where Y is the length of the string with highest occurence in Trie
        :Aux space complexity: O(X+Y), where X is the length of prompt
                                     , where Y is the length of the string with highest occurence in
                                     Trie
        """
        n = len(prompt)  # length of prompt

        # executed until all char in prompt is traversed
        if i < n:
            # get the index of prompt[i] node in link
            index = ord(prompt[i]) - 96

            # executed if prompt[i] exists
            if current.link[index] != None:
                # recursive call to traverse next char in prompt
                ret = self.traverse(current.link[index], prompt, i + 1)

                # return None if next char not in trie
                # else return the autocompleted word
                return (current.link[index].key + ret) if ret != None else ret

            # executed if prompt[i] does not exist
            # prompt longer than a word in trie
            else:
                return None

        # executed if all char in prompt is traversed
        else:
            # traverse to find the next characthers with highest occurence
            # to get autocomplete word with highest frequency
            # deals with the prompt is the same as an existing sentence
            # but it can be completed with higher frequency
            return self.traverse_max(current)

    def traverse_max(self, current: TrieNode) -> str:
        """
        Function description: Finds the string with the highest frequenecy in TrieNode
                              thats starts with current.key

        :Input:
            current: The current TrieNode being traveresed when lookup for a string
        :Output:
            A string starting with current.key and with a characther among the children of current
            with the highest occurence in the trie by traversing down the children of current

        :Time complexity: O(Y), where Y is the length of the word with highest frequency starting
                                from current
        :Aux space complexity: O(Y), where Y is the length of the word with highest frequency starting
                               from current
        """
        # checks if current is a terminal node
        is_leaf = current.key == "$"

        # return empty string to stop traverse if terminal node is reached
        if is_leaf:
            return ""

        # get index of next node to traverse
        i = self.get_max_occ_node_index(current)

        # if the next node is a terminal node return empty string
        # to terminate traverse and form final word
        if i == 0:
            return ""

        # recursive call to add next key with highest occurence to form highest frequency word
        return current.link[i].key + self.traverse_max(current.link[i])
