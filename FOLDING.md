# Folding

Folding maps are simple lookup tables that can be used to solve a range of transcription errors. These can include 1-to-1 mappings for correcting the symbol used for a particular phoneme, or more complicated mappings to solve contextual errors, such as merging two phoneme symbols that the backend has incorrectly split. You can read more about these error types in [our paper](https://arxiv.org/abs/2504.03036).

G2P+ does not need a folding map to run, but it is recommended to use a backend and language code with a folding map if you want to link analysis to Phoible or ensure that the phonemic inventory has been validated. To disable folding maps, use the `--uncorrected` option.

## Implementing a folding map

Folding maps are `.csv` files stored in [`g2p_plus/folding`](https://github.com/codebyzeb/g2p-plus/tree/main/g2p_plus/folding). For instance, the folding map used when the `en-gb` language code is selected with the `phonemizer` backend is stored under [`g2p_plus/folding/phonemizer/en-gb.csv`](https://github.com/codebyzeb/g2p-plus/blob/main/g2p_plus/folding/phonemizer/en-gb.csv). For each backend, there is also a general folding map that is applied first, solving language-independent errors. For instance, the [`phonemizer` folding map](https://github.com/codebyzeb/g2p-plus/blob/main/g2p_plus/folding/phonemizer/phonemizer.csv) contains mappings to correct the `dʒ` and `tʃ` phonemes to match phoible, as well as several mappings that ensure that the phoneme `ɹ` is not joined with a preceding vowel. 

To create a new folding map, simply copy one of the CSV in the folder of the chosen backend and replace the entries with your own. Space characters are included to allow for start-of-phoneme and end-of-phoneme characters to be matched separately (e.g. the [Polish folding map](https://github.com/codebyzeb/g2p-plus/blob/main/g2p_plus/folding/phonemizer/pl.csv?plain=1) for `phonemizer` adds a space before `s` and after `t` to avoid replacing the characters of the phoneme `ts`). 

In order to decide entries:
1. Choose the [Phoible](https://phoible.org/) inventory you want to match
2. Convert a corpus into phonemes using G2P+
3. Examine the output set of phonemes and compare it to the Phoible inventory
4. Add mappings to solve any errors found

This process is described in more detail in [our paper](https://arxiv.org/abs/2504.03036).

## Supported folding maps

The folding maps currently implemented are described below. Most of these were created in order to facilitate the development of the [IPA CHILDES corpus](https://huggingface.co/datasets/phonemetransformers/IPA-CHILDES). We encourage contributors to create additional folding maps to improve the coverage of G2P+. Note that there are no language-specific folding maps for the `pinyin-to-ipa` and `pingyam` backends since these only support one language each (Mandarin and Cantonese), so the general folding map for those backends accomplishes everything required.

| Backend     | Language Code | Phoible Inventory
|------------------|--------|-----|
| phonemizer | `ca` (Catalan) | [2555](https://phoible.org/inventories/view/2555)
| phonemizer | `cy` (Welsh) | [2406](https://phoible.org/inventories/view/2406)
| phonemizer | `da` (Danish) | [2406](https://phoible.org/inventories/view/2406)
| phonemizer | `de` (German) | [2398](https://phoible.org/inventories/view/2398)
| phonemizer | `en-gb` (British English) | [2252](https://phoible.org/inventories/view/2252)
| phonemizer | `en-us` (North American English) | [2175](https://phoible.org/inventories/view/2175)
| phonemizer | `et` (Estonian) | [2181](https://phoible.org/inventories/view/2181)
| phonemizer | `eu` (Basque) | [2161](https://phoible.org/inventories/view/2161)
| phonemizer | `fa-latn` (Farsi, Latin Script) | [516](https://phoible.org/inventories/view/516)
| phonemizer | `fr-fr` (French) | [2269](https://phoible.org/inventories/view/2269)
| phonemizer | `ga` (Irish) | [2521](https://phoible.org/inventories/view/2521)
| phonemizer | `id` (Indonesian) | [1690](https://phoible.org/inventories/view/1690)
| phonemizer | `is` (Icelandic) | [2568](https://phoible.org/inventories/view/2568)
| phonemizer | `it` (Italian) | [1145](https://phoible.org/inventories/view/1145)
| phonemizer | `ja` (Japanese) | [2196](https://phoible.org/inventories/view/2196)
| phonemizer | `ko` (Korean) | [423](https://phoible.org/inventories/view/423)
| phonemizer | `nb` (Norwegian) | [499](https://phoible.org/inventories/view/499)
| phonemizer | `nl` (Dutch) | [2405](https://phoible.org/inventories/view/2405)
| phonemizer | `pl` (Polish) | [1046](https://phoible.org/inventories/view/1046)
| phonemizer | `pt` (Portuguese) | [2206](https://phoible.org/inventories/view/2206)
| phonemizer | `pt-br` (Brazilian Portuguese) | [2207](https://phoible.org/inventories/view/2207)
| phonemizer | `qu` (Quechua) | [104](https://phoible.org/inventories/view/104)
| phonemizer | `ro` (Romanian) | [2443](https://phoible.org/inventories/view/2443)
| phonemizer | `sv` (Swedish) | [1150](https://phoible.org/inventories/view/1150)
| phonemizer | `tr` (Turkish) | [2217](https://phoible.org/inventories/view/2217)
| epitran | `cmn-Hans` (Simplified Mandarin) | [2457](https://phoible.org/inventories/view/2457)
| epitran | `cmn-Latn` (Mandarin Pinyin) | [2457](https://phoible.org/inventories/view/2457)
| epitran | `deu-Latn` (German) | [2398](https://phoible.org/inventories/view/2398)
| epitran | `hrv-Latn` (Croatian) | [1139](https://phoible.org/inventories/view/1139)
| epitran | `hun-Latn` (Hungarian) | [2191](https://phoible.org/inventories/view/2191)
| epitran | `ind-Latn` (Indonesian) | [1690](https://phoible.org/inventories/view/1690)
| epitran | `spa-Latn` (Spanish) | [164](https://phoible.org/inventories/view/164)
| epitran | `srp-Latn` (Serbian) | [2499](https://phoible.org/inventories/view/2499)
| epitran | `yue-Latn` (Cantonese) | [2309](https://phoible.org/inventories/view/2309)

## Recommended backends

See [RECOMMENDED.md](https://github.com/codebyzeb/g2p-plus/blob/main/RECOMMENDED.md) for recommended backends for each language, based on the development of the [IPA CHILDES corpus](https://huggingface.co/datasets/phonemetransformers/IPA-CHILDES) and discussed in [our paper](https://arxiv.org/abs/2504.03036).