import os
import sys
import struct
import codecs


ULL_BYTES = struct.calcsize('!Q')
SHORT_BYTES = struct.calcsize('!h')
INDEX_HEADER = 'IDX'


class T(object):
    def __init__(self, nodes, leafs):
        self.nodes = nodes
        self.leafs = leafs
        self._index_bytes = None
        self._size_bytes = None

    def node_bytes(self):
        """Returns a number of bytes required to write node index."""
        return sum(ULL_BYTES + len(letter.encode('utf-8')) + SHORT_BYTES for (letter, subtrie) in self.nodes.items())

    def leafs_bytes(self):
        return sum(len(leaf.encode('utf-8')) + SHORT_BYTES for leaf in self.leafs)

    def index_bytes(self):
        if self._index_bytes is None:
            self._index_bytes = len(INDEX_HEADER) + 2 * ULL_BYTES + self.node_bytes() + self.leafs_bytes()
        return self._index_bytes

    def size_bytes(self):
        if self._size_bytes is None:
            self._size_bytes = self.index_bytes() + sum(t.size_bytes() for t in self.nodes.values())
        return self._size_bytes

    def index(self, offset=0):
        result = ['IDX', struct.pack('!Q', self.index_bytes()), struct.pack('!Q', len(self.nodes))]

        offset += self.index_bytes()
        for letter in sorted(self.nodes):
            t = self.nodes[letter]
            utf8_letter = letter.encode('utf-8')
            result.append(struct.pack('!h%dsQ' % len(utf8_letter), len(utf8_letter), utf8_letter, offset))
            offset += t.size_bytes()

        for leaf in self.leafs:
            utf8_leaf = leaf.encode('utf-8')
            result.append(struct.pack('!h%ds' % len(utf8_leaf), len(utf8_leaf), utf8_leaf))

        return ''.join(result)

    def write_to_file(self, f, offset=0):
        f.write(self.index(offset))
        offset += self.index_bytes()
        for letter in sorted(self.nodes):
            t = self.nodes[letter]
            t.write_to_file(f, offset)
            offset += t.size_bytes()


def makedb(directory, f):
    """Creates a database file of all texts in the directory."""
    words = read_directory_words(directory)
    trie = maketrie(words)
    trie.write_to_file(f)


def maketrie(wordpaths):
    """Creates and returns a trie containing all wordpaths."""
    nodes = {}
    leafs = []

    grouped = {}
    for word, path in wordpaths:
        if len(word) == 0:
            leafs.append(path)
        else:
            grouped.setdefault(word[0], []).append((word[1:], path))

    for letter, wordpath_list in grouped.items():
        nodes[letter] = maketrie(wordpath_list)

    return T(nodes, set(leafs))


def read_directory_words(directory):
    """Yields words in all files in directory."""
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            for word, path in read_words(path):
                yield word, path


# Change this function if you want different tokenization mechanism
def read_words(path):
    """Yields words in file at path."""
    data = codecs.open(path, encoding='utf-8', errors='replace').read()
    for word in data.split():
        yield word.lower(), path


if __name__ == '__main__':
    f = file(sys.argv[2], 'wb')
    makedb(sys.argv[1], f)
