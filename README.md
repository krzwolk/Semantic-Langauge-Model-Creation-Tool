# Semantic-Language-Model-Tool

The tool will generate semantic corpora using either WordNet method or Latent Semantic Analysis (LSA).

Method 1: WordNet

–Mathematical model–

Using WordNet to get a probability estimator is shown in [2]. In particular, we want to get P(w_i|w), where w_i and w are assumed to have a relationship in WordNet.

The formular is below: P(w_i|w) = \frac{c(w_i,w|W,L)}{\sum_{w_j} c(w_j,w|W,L)}.

Where, W is a window size, c(w_i,w|W,L) is the count that w_i and w appearing together within W-window. It can be got just by counting in certain corpus.

To smooth the model, we can apply interpolated absolute discount or Kneser-Ney smoothing strategies.

What relationships can be considered:

synonym
hypernym
hyponym
hierarchical distance between words

Method 2: LSA (Latent Semantic Analysis)

LSA is shown to be helpful in speech recognition [3] and has been successfully used in many applications. Thus, I believe that it is promising for CMUSphinx project and should be tried.

–Mathematical model–

*The high level idea of LSA is to convert words into concept representations and it assumes that if the occurrence pattern of words in documents is similar then the words are similar.

a) To build the LAS model, a co-occurrence matrix W will be built first, where w_{ij} is a weighted count of word w_j and document d_j. w_{ij} = G_i L_{ij} C_{ij} where, C_{ij} is the count of w_i in document d_j; L_{ij} is local weight; G_i is global weight. Usually, L_{ij} and G_i can use TF/IDF.

b) Then, SVD Analysis will be applied to W, then W = U S V^T where, W is a MN matrix, (M is the Vocabulary size, N is document size); U is MR, S is RR and V is a RN matrix. R is usually a predefined dimension number between 100 and 500.

c) After that, each word w_i can be denoted as a new vector U_i = u_i*S

d) Based on this new vector, a distance between two words is defined: K(U_i, U_j) = \frac{u_iS^2u_m^T}{|u_iS||u_m*S|}

e) Therefore, we can perform a clustering to words into K clusters, C_1, C_2, …., C_K.

f) Let H_{q-1} be the history for word W_q, then we can get the probability of W_q given H_{q-1} by formula below: P(W_q|H_{q-1}) = P(W_q|W_{q-1},W_{q-2},…W_{q-n+1}, d_{q_1}) = P(W_q|W_{q-1},W_{q-2},…W_{q-n+1})*P(W_q|d_{q_1}|) where, P(W_q|W_{q-1},W_{q-2},…W_{q-n+1}) is ngram model; P(d_{q_1}|W_q) is the LSA model.

And, P(W_q|d_{q_1}) = P(U_q|V_q) = K(U_q, V_{q_1})/Z(U,V) K(U_q, V_{q_1}) = \frac{U_qSV_{q-1}^T}{|U_qS^{1/2}||V_{q-1}*S^{1/2}|}

Z(U,V) is normalized factor.

g) We can apply word smoothing to the model based K-Clustering as follows: P(W_q|d_{q_1}) = \sum_{k=1}^{K} P(W_q|C_k)P(C_k|d_{q_1})

where, P(W_q|C_k), P(C_k|d_{q_1}) can be computer use the distance measurement given above by a normalized factor.

h) In this way, N-gram and LSA model are combined into one language model.

Firstly, install morfeusz2 components (you may try to run 'install_morfeusz2_components.sh' with 'sudo') and other python packets ( 'install_python_packets.sh').
If you can`t run the scripts, open them as text files and execute them line-by-line.


LSA
Copy 'stopwords_pl.txt' to the folder with scripts (read 'links_for_downloading.txt')

usage lsa_train.py:
python lsa_train.py # default corpus filename is 'pl.txt'
python lsa_train.py your_corpus_filename.txt # corpus filename may be specified

Files 'dict.txt' and 'svdMat.svd' will be generated


usage lsa_test.py:
python lsa_test.py # default corpus filename is 'pl.txt'
python lsa_test.py your_corpus_filename.txt # corpus filename may be specified

The file 'generated_with_lsa.txt' will be generated




WordNet
Copy 'plwordnet-3.0-visdisc.xml' to the folder with scripts (see 'links_for_downloading.txt')

usage wn_test.py:
python wn_test.py # default corpus filename is 'pl.txt'
python wn_test.py your_corpus_filename.txt # corpus filename may be specified

The file 'generated_with_wn.txt' will be generated
