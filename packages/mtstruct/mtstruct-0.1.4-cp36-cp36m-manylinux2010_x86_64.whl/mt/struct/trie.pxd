from libcpp.string cimport string

cdef extern from "<iostream>" namespace "std" nogil:
    cdef cppclass istream:
        pass
    cdef cppclass ostream:
        pass


cdef extern from "wordtrie.h":
    cdef cppclass TrieNode_c:
        long long m_count
        int num_descendants()
    cdef cppclass Trie_c:
        Trie_c()
        long long total_count()
        int num_nodes()
        void insert(const string& word, long long count)
        double prob(const string& word)
        double cond_prob(const string& word)

    void load(istream& ist, Trie_c& out_trie)
    void save(ostream& ost, const Trie_c& in_trie)
    void load_from_file(const string& filepath, Trie_c& out_trie)
    void save_to_file(const string& filepath, const Trie_c& in_trie)
