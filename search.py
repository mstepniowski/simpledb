import sys
import struct


ULL_BYTES = struct.calcsize('!Q')
SHORT_BYTES = struct.calcsize('!h')
INDEX_HEADER = 'IDX'


def search(dbfile, prefix):
    """Returns all words having a given prefix using a dbfile."""
    idx = Index.from_file(dbfile)
    for letter in prefix:
        if letter not in idx.nodes:
            print 'No completions'
            return
        else:
            print letter, idx.nodes[letter]
            idx = Index.from_file(dbfile, idx.nodes[letter])
    if idx.nodes:
        print 'Completions:'
        for completion in idx.nodes:
            print ' - ' + completion

    if idx.leafs:
        print 'Pattern found in files:'
        for path in idx.leafs:
            print ' - ' + path

class Index(object):
    def __init__(self, data):
        self.data = data
        self.nodes = {}
        self.leafs = []
        self.parse()

    @classmethod
    def from_file(self, f, offset=0):
        f.seek(offset)
        size_data = f.read(len(INDEX_HEADER) + ULL_BYTES)
        header, index_size = struct.unpack('!%dsQ' % len(INDEX_HEADER), size_data)
        if header != INDEX_HEADER:
            import ipdb; ipdb.set_trace()
        data = f.read(index_size - ULL_BYTES - len(INDEX_HEADER))
        return Index(data)

    def parse(self):
        node_count, = struct.unpack_from('!Q', self.data)
        offset = ULL_BYTES

        # Read nodes
        for n in range(node_count):
            letter_bytes, = struct.unpack_from('!h', self.data, offset)
            offset += SHORT_BYTES
            letter, index_offset = struct.unpack_from('!%dsQ' % letter_bytes, self.data, offset)
            offset += letter_bytes + ULL_BYTES
            self.nodes[letter] = index_offset

        # Read leafs
        while offset < len(self.data):
            path_bytes, = struct.unpack_from('!h', self.data, offset)
            offset += SHORT_BYTES
            path, = struct.unpack_from('!%ds' % path_bytes, self.data, offset)
            offset += path_bytes
            self.leafs.append(path)


if __name__ == '__main__':
    f = file(sys.argv[1], 'rb')
    search(f, sys.argv[2])
