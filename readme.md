The Trie class initializes a trie that holds all the sentences together with the maximum number of occurences of each characther to be able to determine the strings with the highest probability in the trie

autoComplete(prompt) is a function that returns a string that represents the auto completed sentence from the prompt using the sentences stored in the Trie class
- If such a sentence exist, the completed sentence with the highest frequency in the Trie is returned
- If there are multiple possible auto-complete sentences with the same highest frequency, then the lexicographically smaller string is returned
- If such a sentence does not exist, None is returned

Example:\
sentences = ["abc", "abazacy", "dbcef", "xzz", "gdbc", "abazacy", "xyz", "abazacy", "dbcef", "xyz", "xxx", "xzz"]\
\# Creating a Trie object\
trie = Trie(sentences)

\# Example 1.1
\# A simple example\
prompt = "ab"
\>>> mycattrie.autoComplete(prompt)
abazacy
\# Example 1.2
\# Another simple example
prompt = "a"
>>> mycattrie.autoComplete(prompt)
abazacy
\# Example 1.3
\# What if the prompt is the same as an existing sentence?
prompt = "dbcef"
>>> mycattrie.autoComplete(prompt)
dbcef
\# Example 1.4
\# What if the length is longer?
prompt = "dbcefz"
>>> mycattrie.autoComplete(prompt)
None
10

\# Example 1.5
\# What if sentences doesn’t exist.
prompt = "ba"
>>> mycattrie.autoComplete(prompt)
None
>>> 
\# Example 1.6
\# A scenario where the tiebreaker is used
prompt = "x"
>>> mycattrie.autoComplete(prompt)
xyz

\# Example 1.7
\# A scenario where the prompt is empty
prompt = ""
>>> mycattrie.autoComplete(prompt)
abazacy


