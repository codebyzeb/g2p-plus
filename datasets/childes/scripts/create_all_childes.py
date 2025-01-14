import sys
import os
import shutil

from pathlib import Path
sys.path.append('./')
from childes_processor.processor import ChildesProcessor
from childes_processor.downloader import ChildesDownloader

SKIP_DOWNLOAD = True
KEEP_CHILD_UTTERANCES = True
DOWNLOAD_OUT_PATH = Path('downloaded')
PROCESS_OUT_PATH = Path('CHILDES-dataset')
MAX_AGE = None

downloader = ChildesDownloader()

def download_and_process_corpora(collection, corpora, language):
    if not SKIP_DOWNLOAD:   
        for corpus in corpora:
            print(f"\n----------\nDOWNLOADING: Corpus: {corpus} in Collection: {collection} for Language: {language}\n----------\n")
            downloader.download(collection, corpus,
                                DOWNLOAD_OUT_PATH,
                                separate_by_child=False)

        if language != collection:
            if (DOWNLOAD_OUT_PATH / language).exists():
                shutil.rmtree(DOWNLOAD_OUT_PATH / language)
            os.rename(DOWNLOAD_OUT_PATH / collection, DOWNLOAD_OUT_PATH / language)
    
    if language == "Eng-NA":
        phonemize_language = "EnglishNA"
    elif language == "Eng-UK":
        phonemize_language = "EnglishUK"
    else:
        phonemize_language = language
    
    processor = ChildesProcessor(DOWNLOAD_OUT_PATH / language,
                                 keep_child_utterances=KEEP_CHILD_UTTERANCES,
                                 max_age = MAX_AGE)
    
    processor.phonemize_utterances(phonemize_language)
    processor.character_split_utterances()
    processor.print_statistics()

    processor.save_df(PROCESS_OUT_PATH / language)

# Basque
download_and_process_corpora("Other", ["Luque", "Soto"], "Basque")

# Cantonese
download_and_process_corpora("Chinese", ["HKU", "LeeWongLeung", "PaidoCantonese"], "Cantonese")

# Catalan
download_and_process_corpora("Romance", ["EstevePrieto", "GRERLI", "Jordina", "Julia", "MireiaEvaPascual", "SerraSole"], "Catalan")

# Croatian
download_and_process_corpora("Slavic", ["Kovacevic"], "Croatian")

# Danish
download_and_process_corpora("Scandinavian", ["Plunkett"], "Danish")

# Dutch
download_and_process_corpora("DutchAfrikaans", ["Utrecht", "Gillis", "Schaerlaekens", "Groningen", "Schlichting", "VanKampen", "DeHouwer", "Zink"], "Dutch")

# English (US)
download_and_process_corpora("Eng-NA", ["Bates", "Bernstein", "Bliss", "Bloom", "Bohannon", "Braunwald", "Brent", "Brown", "Clark", "ComptonPater", "Davis", "Demetras1", "Demetras2", "Feldman", "Garvey", "Gathercole", "Gelman", "Gleason", "Goad", "HSLLD", "Haggerty", "Hall", "Higginson", "Inkelas", "Kuczaj", "MacWhinney", "McCune", "McMillan", "Menn", "Morisset", "Nelson", "NewEngland", "NewmanRatner", "Nippold", "Peters", "Post", "Providence", "Rollins", "Sachs", "Sawyer", "Snow", "Soderstrom", "Sprott", "StanfordEnglish", "Suppes", "Tardif", "Valian", "VanHouten", "VanKleeck", "Warren", "Weist"], "Eng-NA")

# English (UK)
download_and_process_corpora("Eng-UK", ["Belfast", "Conti1", "Cruttenden", "Edinburgh", "Fletcher", "Forrester", "Gathburn", "Howe", "KellyQuigley", "Korman", "Lara", "MPI-EVA-Manchester", "Manchester", "Nuffield", "Sekali", "Smith", "Thomas", "Tommerdahl", "Wells"], "Eng-UK")

# Estonian
download_and_process_corpora("Other", ["Argus", "Beek", "Kapanen", "Kohler", "Korgesaar", "Kuett", "Kutt", "MAIN", "Vija", "Zupping"], "Estonian")

# Farsi
download_and_process_corpora("Other", ["Family", "Samadi"], "Farsi")

# French
download_and_process_corpora("French", ["Champaud", "Geneva", "GoadRose", "Hammelrath", "Hunkeler", "KernFrench", "Leveillé", "Lyon", "MTLN", "Palasis", "Paris", "Pauline", "StanfordFrench", "VionColas", "Yamaguchi", "York"], "French")

# German
download_and_process_corpora("German", ["Caroline", "Grimm", "Leo", "Manuela", "Miller", "Rigol", "Stuttgart", "Szagun", "Wagner", "Weissenborn"], "German")

# Greek
# download_and_process_corpora("Other", ["Doukas", "PaidoGreek", "Stephany"], "Greek")
# print("WARNING: Greek phonemization is not supported. Skipping phonemization for Greek.")

# Hebrew
# download_and_process_corpora("Other", ["BatEl", "BermanLong", "BSF", "Levy", "Naama", "Ravid"], "Hebrew")
# print("WARNING: Hebrew phonemization is not supported. Skipping phonemization for Hebrew.")

# Hungarian
download_and_process_corpora("Other", ["Bodor", "MacWhinney", "Reger"], "Hungarian")

# Icelandic
download_and_process_corpora("Scandinavian", ["Einarsdottir", "Kari"], "Icelandic")

# Indonesian
download_and_process_corpora("EastAsian", ["Jakarta"], "Indonesian")

# Irish
download_and_process_corpora("Celtic", ["Gaeltacht", "Guilfoyle"], "Irish")

# Italian
download_and_process_corpora("Romance", ["Antelmi", "Calambrone", "D_Odorico", "Roma", "Tonelli"], "Italian")

# Japanese
download_and_process_corpora("Japanese", ["Hamasaki", "Ishii", "MiiPro", "Miyata", "NINJAL-Okubo", "Noji", "Ogawa", "Okayama", "Ota", "PaidoJapanese", "StanfordJapanese", "Yokoyama"], "Japanese")

# Korean
download_and_process_corpora("EastAsian", ["Jiwon", "Ko", "Ryu"], "Korean")

# Mandarin
download_and_process_corpora("Chinese", ["Chang1", "Chang2", "ChangPN", "ChangPlay", "Erbaugh", "LiReading", "LiZhou", "TCCM-reading", "TCCM", "Tong", "Xinjiang", "Zhou1", "Zhou2", "Zhou3", "ZhouAssessment", "ZhouDinner"], "Mandarin")

# Norwegian
download_and_process_corpora("Scandinavian", ["Garmann", "Ringstad"], "Norwegian")

# Polish
download_and_process_corpora("Slavic", ["Szuman", "WeistJarosz"], "Polish")

# Portuguese (Brazil)
download_and_process_corpora("Romance", ["AlegreLong", "AlegreX"], "PortugueseBr")

# Portuguese (Portugal)
download_and_process_corpora("Romance", ["Batoreo", "CCF", "Florianopolis", "Santos"], "PortuguesePt")

# Quechua
download_and_process_corpora("Other", ["Gelman", "Gildersleeve"], "Quechua")

# Romanian
download_and_process_corpora("Romance", ["Avram", "Goga", "KernRomanian"], "Romanian")

# Spanish
download_and_process_corpora("Spanish", ["Aguirre", "BeCaCeSno", "ColMex", "DiezItza", "FernAguado", "Koine", "Linaza", "LlinasOjea", "Marrero", "Montes", "Nieva", "OreaPine", "Ornat", "Remedi", "Romero", "SerraSole", "Shiro", "Vila"], "Spanish")

# Serbian
download_and_process_corpora("Slavic", ["SCECL"], "Serbian")

# Swedish
download_and_process_corpora("Scandinavian", ["Andren", "Lacerda", "Lund", "StanfordSwedish"], "Swedish")

# Thai
# download_and_process_corpora("EastAsian", ["CRSLP"], "Thai")
# print("WARNING: Thai phonemization is not supported. Skipping phonemization for Thai.")

# Tamil
# download_and_process_corpora("Other", ["Narasimhan"], "Tamil")
# print("WARNING: Too few utterances for Tamil. Skipping phonemization for Tamil.")

# Turkish
download_and_process_corpora("Other", ["Aksu", "Altinkamis"], "Turkish")

# Welsh
download_and_process_corpora("Celtic", ["CIG1", "CIG2"], "Welsh")
