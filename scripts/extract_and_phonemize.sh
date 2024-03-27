
echo Extracting and phonemizing for language: $1
python childes_processor.py extract childes/downloaded/$1 -o childes/processed/$1
python childes_processor.py phonemize childes/processed/$1/adult.txt $1 -o childes/phonemized/$1 -s
