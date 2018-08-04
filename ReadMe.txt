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
