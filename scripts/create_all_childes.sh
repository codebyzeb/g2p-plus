# Description: Downloads, extracts, and phonemizes all CHILDES corpora


function download_corpora {
    collection=$1
    corpora=$2
    # Iterate through corpora
    for corpus in ${corpora[@]}
    do
        echo "\n----------\nDOWNLOADING: Corpus: $corpus in Collection: $collection\n----------\n"
        python childes_processor.py download $collection -c $corpus -o childes/downloaded
    done
}

function process_corpus {
    collection=$1
    language=$2
    max_age=$3
    echo "\n----------\nEXTRACTING: Collection: $collection\n----------\n"
    python childes_processor.py extract childes/downloaded/$collection -o childes/processed/$collection -m $max_age
    echo "\n----------\nPHONEMIZING: Collection: $collection\n----------\n"
    python childes_processor.py phonemize childes/processed/$collection/adult.txt $language -o childes/phonemized/$collection -s
}


# Eng-NA

collection="Eng-NA"
corpora=("Bates" "Bernstein" "Bliss" "Bloom" "Bohannon" "Brent" "Brown" "Demetras1" "Demetras2" "Feldman" "Garvey" "Gathercole" "Gleason" "Higginson" "Kuczaj" "MacWhinney" "McCune" "McMillan" "Morisset" "Nelson" "NewEngland" "Peters" "Post" "Providence" "Rollins" "Sachs" "Sawyer" "Snow" "Soderstrom" "Suppes" "Tardif" "VanHouten" "Warren" "Weist")
#download_corpora $collection $corpora
#process_corpus $collection "EnglishNA" 24

# Eng-UK

# collection="Eng-UK"
# corpora=("Belfast" "Cruttenden" "Edinburgh" "Fletcher" "Forrester" "Gathburn" "Howe" "KellyQuigley" "Korman" "Lara" "Manchester" "MPI-EVA-Manchester" "Nuffield" "Sekali" "Smith" "Thomas" "Tommerdahl" "Wells")
download_corpora $collection $corpora
process_corpus $collection "EnglishUK" 24

# # French

# collection="French"
# corpora = ("Champaud" "Geneva" "GoadRose" "Hammelrath" "Hunkeler" "Kern-French" "Leveille" "Lyon" "MTLN" "Palais" "Paris" "Pauline" "Stanford-French" "VionColas" "Yamaguchi" "York")
# download_corpora $collection $corpora
# #