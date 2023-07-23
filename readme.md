The Trie class initializes a trie that holds all the sentences together with the maximum number of occurences of each characther to be able to determine the strings with the highest probability in the trie

autoComplete(prompt) is a function that returns a string that represents the auto completed sentence from the prompt using the sentences stored in the Trie class
- If such a sentence exist, the completed sentence with the highest frequency in the Trie is returned
- If there are multiple possible auto-complete sentences with the same highest frequency, then the lexicographically smaller string is returned
- If such a sentence does not exist, None is returned
