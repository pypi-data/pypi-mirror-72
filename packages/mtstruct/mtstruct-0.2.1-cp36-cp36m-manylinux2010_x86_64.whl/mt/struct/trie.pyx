# distutils: language = c++
# cython: language_level = 3

from trie cimport Trie_c, load_from_file, save_to_file
import mt.base.path as _bp
import mt.base.threading as _bt


__all__ = ['Trie']


cdef class Trie:
    '''A simple word trie implemented in C++.'''

    cdef Trie_c c_trie
    cdef object lock

    def __cinit__(self):
        self.c_trie = Trie_c()
        self.lock = _bt.ReadWriteLock()

    def total_count(self):
        '''Returns the total number of word counts.'''
        with _bt.ReadRWLock(self.lock):
            return self.c_trie.total_count()

    def num_nodes(self):
        '''Returns the total number of nodes of the trie.'''
        with _bt.ReadRWLock(self.lock):
            return self.c_trie.num_nodes()

    def insert(self, str word, int count=1):
        '''Inserts a word with frequency/count.

        Parameters
        ----------
        word : str
            The word to be inserted.
        count : int
            The number of times the word occurs.
        '''
        with _bt.WriteRWLock(self.lock):
            self.c_trie.insert(word.encode(), count)

    def prob(self, str word):
        '''Returns the probability that the word occurs.

        Parameters
        ----------
        word : str
            The query word.

        Returns
        -------
        double
            The probability that the word occurs.
        '''
        with _bt.ReadRWLock(self.lock):
            return self.c_trie.prob(word.encode())

    def cond_prob(self, str word):
        '''Returns the probability that the word occurs, given that everything except the last character has been given.

        Parameters
        ----------
        word : str
            The query word.

        Returns
        -------
        double
            The probability that the word occurs.
        '''
        with _bt.ReadRWLock(self.lock):
            return self.c_trie.cond_prob(word.encode())

    # ----- serialization -----

    @staticmethod
    def from_file(str filepath):
        '''Loads the Trie from a file.

        Parameters
        ----------
        filepath : str
            path to file to read from

        Returns
        -------
        Trie
            a loaded Trie
        '''
        if not _bp.exists(filepath):
            raise OSError("File not found: '{}'".format(filepath))

        trie = Trie()
        load_from_file(filepath.encode(), trie.c_trie)
        return trie

    def to_file(self, str filepath):
        '''Saves the Trie to a file.

        Parameters
        ----------
        filepath : str
            path to file to save to
        '''
        with _bt.ReadRWLock(self.lock):
            save_to_file(filepath.encode(), self.c_trie)
