# Description: Downloads, extracts, and phonemizes all CHILDES corpora used in the phonemized CHILDES dataset

SKIP_DOWNLOAD=false

function download_corpora {
    collection=$1
    corpora=$2
    language=$3
    if [ $SKIP_DOWNLOAD = true ];
    then
        return
    fi
    # Iterate through corpora
    for corpus in ${corpora[@]}
    do
        echo "\n----------\nDOWNLOADING: Corpus: $corpus in Collection: $collection for Language: $language\n----------\n"
        python childes_processor.py download $collection -c $corpus -o datasets/childes/downloaded
    done
    if [ $language != $collection ];
    then
        mv datasets/childes/downloaded/$collection datasets/childes/downloaded/$language
    fi
}

function process_corpus {
    language=$1
    if [ $language = "Eng-NA" ];
    then
        python childes_processor.py process datasets/childes/downloaded/$language EnglishNA -o datasets/childes/processed/$language -s
    elif [ $language = "Eng-UK" ];
    then
        python childes_processor.py process datasets/childes/downloaded/$language EnglishUK -o datasets/childes/processed/$language -s
    else
        python childes_processor.py process datasets/childes/downloaded/$language $language -o datasets/childes/processed/$language -s
    fi
}

# # Arabic
# corpora=("KernArabic" "Kuwaiti" "Nazzal" "Salama")
# download_corpora "Other" $corpora "Arabic"
# echo "WARNING: Arabic phonemization is not supported. Skipping phonemization for Arabic."

# Basque
corpora=("Luque" "Soto")
download_corpora "Other" $corpora "Basque"
process_corpus "Basque"

# Cantonese
corpora=("HKU" "LeeWongLeung" "PaidoCantonese")
download_corpora "Chinese" $corpora "Cantonese"
process_corpus "Cantonese"

# Catalan
corpora=("EstevePrieto" "GRERLI" "Jordina" "Julia" "MireiaEvaPascual" "SerraSole")
download_corpora "Romance" $corpora "Catalan"
process_corpus "Catalan"

# Croatian
corpora=("Kovacevic")
download_corpora "Slavic" $corpora "Croatian"
process_corpus "Croatian"

# Danish
corpora=("Plunkett")
download_corpora "Scandinavian" $corpora "Danish"
process_corpus "Danish"

# Dutch
corpora=("Utrecht" "Gillis" "Schaerlaekens" "Groningen" "Schlichting" "VanKampen" "DeHouwer" "Zink")
download_corpora "DutchAfrikaans" $corpora "Dutch"
process_corpus "Dutch"

# Eng-NA
corpora=("Bates" "Bernstein" "Bliss" "Bloom" "Bohannon" "Braunwald" "Brent" "Brown" "Clark" "ComptonPater" "Davis" "Demetras1" "Demetras2" "Feldman" "Garvey" "Gathercole" "Gelman" "Gleason" "Goad" "HSLLD" "Haggerty" "Hall" "Higginson" "Inkelas" "Kuczaj" "MacWhinney" "McCune" "McMillan" "Menn" "Morisset" "Nelson" "NewEngland" "NewmanRatner" "Nippold" "Peters" "Post" "Providence" "Rollins" "Sachs" "Sawyer" "Snow" "Soderstrom" "Sprott" "StanfordEnglish" "Suppes" "Tardif" "Valian" "VanHouten" "VanKleeck" "Warren" "Weist")
download_corpora "Eng-NA" $corpora "Eng-NA"
process_corpus "Eng-NA"

# Eng-UK
corpora=("Belfast" "Conti1" "Cruttenden" "Edinburgh" "Fletcher" "Forrester" "Gathburn" "Howe" "KellyQuigley" "Korman" "Lara" "MPI-EVA-Manchester" "Manchester" "Nuffield" "Sekali" "Smith" "Thomas" "Tommerdahl" "Wells")
download_corpora "Eng-UK" $corpora "Eng-UK"
process_corpus "Eng-UK"

# Estonian
corpora=("Argus" "Beek" "Kapanen" "Kohler" "Korgesaar" "Kuett" "Kutt" "MAIN" "Vija" "Zupping")
download_corpora "Other" $corpora "Estonian"
process_corpus "Estonian"

# Farsi
corpora=("Family" "Samadi")
download_corpora "Other" $corpora "Farsi"
process_corpus "Farsi"

# French
corpora=("Champaud" "Geneva" "GoadRose" "Hammelrath" "Hunkeler" "KernFrench" "Leveillé" "Lyon" "MTLN" "Palasis" "Paris" "Pauline" "StanfordFrench" "VionColas" "Yamaguchi" "York")
download_corpora "French" $corpora "French"
process_corpus "French"

# German
corpora=("Caroline" "Grimm" "Leo" "Manuela" "Miller" "Rigol" "Stuttgart" "Szagun" "Wagner" "Weissenborn")
download_corpora "German" $corpora "German"
process_corpus "German"

# # Greek
# corpora=("Doukas" "PaidoGreek" "Stephany")
# download_corpora "Other" $corpora "Greek"
# echo "WARNING: Greek phonemization is not supported. Skipping phonemization for Greek."

# # Hebrew
# corpora=("BatEl" "BermanLong" "BSF" "Levy" "Naama" "Ravid")
# download_corpora "Other" $corpora "Hebrew"
# echo "WARNING: Hebrew phonemization is not supported. Skipping phonemization for Hebrew."

# Hungarian
corpora=("Bodor" "MacWhinney" "Reger")
download_corpora "Other" $corpora "Hungarian"
process_corpus "Hungarian"

# Icelandic
corpora=("Einarsdottir" "Kari")
download_corpora "Scandinavian" $corpora "Icelandic"
process_corpus "Icelandic"

# Indonesian
corpora=("Jakarta")
download_corpora "EastAsian" $corpora "Indonesian"
process_corpus "Indonesian"

# Irish
corpora=("Gaeltacht" "Guilfoyle")
download_corpora "Celtic" $corpora "Irish"
process_corpus "Irish"

# Italian
corpora=("Antelmi" "Calambrone" "D_Odorico" "Roma" "Tonelli")
download_corpora "Romance" $corpora "Italian"
process_corpus "Italian"

# Japanese
corpora=("Hamasaki" "Ishii" "MiiPro" "Miyata" "NINJAL-Okubo" "Noji" "Ogawa" "Okayama" "Ota" "PaidoJapanese" "StanfordJapanese" "Yokoyama")
download_corpora "Japanese" $corpora "Japanese"
process_corpus "Japanese"

# Korean
corpora=("Jiwon" "Ko" "Ryu")
download_corpora "EastAsian" $corpora "Korean"
process_corpus "Korean"

# Mandarin
corpora=("Chang1" "Chang2" "ChangPN" "ChangPlay" "Erbaugh" "LiReading" "LiZhou" "TCCM-reading" "TCCM" "Tong" "Xinjiang" "Zhou1" "Zhou2" "Zhou3" "ZhouAssessment" "ZhouDinner")
download_corpora "Chinese" $corpora "Mandarin"
process_corpus "Mandarin"

# Norwegian
corpora=("Garmann" "Ringstad")
download_corpora "Scandinavian" $corpora "Norwegian"
process_corpus "Norwegian"

# PortugueseBr
corpora=("AlegreLong" "AlegreX")
download_corpora "Romance" $corpora "PortugueseBr"
process_corpus "PortugueseBr"

# PortuguesePt
corpora=("Batoreo" "CCF" "Florianopolis" "Santos")
download_corpora "Romance" $corpora "PortuguesePt"
process_corpus "PortuguesePt"

# Quechua
corpora=("Gelman" "Gildersleeve")
download_corpora "Other" $corpora "Quechua"
process_corpus "Quechua"

# Romanian
corpora=("Avram" "Goga" "KernRomanian")
download_corpora "Romance" $corpora "Romanian"
process_corpus "Romanian"

# Spanish
corpora=("Aguirre" "BeCaCeSno" "ColMex" "DiezItza" "FernAguado" "Koine" "Linaza" "LlinasOjea" "Marrero" "Montes" "Nieva" "OreaPine" "Ornat" "Remedi" "Romero" "SerraSole" "Shiro" "Vila")
download_corpora "Spanish" $corpora "Spanish"
process_corpus "Spanish"

# Swedish
corpora=("Andren" "Lacerda" "Lund" "StanfordSwedish")
download_corpora "Scandinavian" $corpora "Swedish"
process_corpus "Swedish"

# # Thai
# corpora=("CRSLP")
# download_corpora "EastAsian" $corpora "Thai"
# echo "WARNING: Thai phonemization is not supported. Skipping phonemization for Thai."

# # Tamil
# corpora=("Narasimhan")
# download_corpora "Other" $corpora "Tamil"
# echo "WARNING: Too few utterances for Tamil. Skipping phonemization for Tamil."

# Turkish
corpora=("Aksu" "Altinkamis")
download_corpora "Other" $corpora "Turkish"
process_corpus "Turkish"

# Welsh
corpora=("CIG1" "CIG2")
download_corpora "Celtic" $corpora "Welsh"
process_corpus "Welsh"

