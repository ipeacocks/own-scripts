# word-search

A word search, word find, word seek, word sleuth or mystery word puzzle is a word game that consists of the letters of words placed in a grid, which usually has a rectangular or square shape. (c) Wikipedia

I've only slightly modificated this solution https://github.com/robbiebarrat/word-search    
This variant can automatically generate random rectangle board, board size could be sent via parameter from terminal:

```
$ python3 wordsearch.py -s 16
```
```
** This is GAMEBOARD **
FDIDXDSCOLBBOCDU
MEROFPUNNGYZGYOR
WXEEZCRZHMZDGQIX
VMWJOSHTSDSWKWDO
ZKTQPDTMUZOBWHPL
...
MIFFGCOSDSENVSQC
LJFASQOGPILRZZLI
FKAEBXECBLMSTPGX
UGCTYKAUNHEBVMCG
**********************
AY starting at row 9 and column 3 ⇓
BY starting at row 9 and column 4 ⇓
...
TO starting at row 7 and column 14 ⇗
UH starting at row 12 and column 4 ⇗
WE starting at row 4 and column 3 ⇗
```

Vocabulary (words for looking them in board) is loaded from `words.txt`.
All libs used in script seems are standard.