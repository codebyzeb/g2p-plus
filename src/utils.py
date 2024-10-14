""" Utility functions for the project. """

def move_tone_marker_to_after_vowel(syll):
    """ Move the tone marker from the end of a cantonese syllable to directly after the vowel """

    cantonese_vowel_symbols = "eauɔiuːoɐɵyɛœĭŭiʊɪə"
    cantonese_tone_symbols = "˥˧˨˩"
    if not syll[-1] in cantonese_tone_symbols:
        print(syll, syll[-1])
        return syll
    tone_marker = len(syll) - 1
    # Iterate backwards
    for i in range(len(syll)-2, -1, -1):
        if syll[i] in cantonese_tone_symbols:
            tone_marker = i
            continue
        if syll[i] in cantonese_vowel_symbols:
            return syll[:i+1] + syll[tone_marker:] + syll[i+1:tone_marker]
    return syll

def move_tone_marker_to_after_vowel_line(line):
    """ Move the tone marker from the end of a mandarin or cantonese syllable to directly after the vowel """

    vowel_symbols = "eauɔiuːoɐɵyɛœĭŭiʊɪə"
    tone_symbols = ['˥', '˧˥', '˨˩', '˥˩', '˧', '˧˩̰', '˩˧', '˨', '˧˩̰', '˩˧'] 
    last_marker = -1
    line = line.split(' ')
    for i in range(len(line)):
        if line[i] in tone_symbols:
            for j in range(i-1, last_marker, -1):
                if line[j] in vowel_symbols or line[j] in tone_symbols:
                    line[j+1], line[i] = line[i], line[j+1]
                    break
            last_marker = i
    line = ' '.join(line)
    # Combine tone markers with previous vowel
    for tone in tone_symbols:
        line = line.replace(' ' + tone, tone)
    return line
