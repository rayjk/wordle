# Wordle
Automatic Wordle solver for Linux including guess submission and result interpretation.

## Usage:
* `wordle.py`: Solves daily Wordle found at https://www.nytimes.com/games/wordle/index.html 
* `wordle_all.py`: Solves all Wordles in archive at https://www.devangthakkar.com/wordle_archive/?1
* Navigate to the corresponding webpage
* Upon launch of a script, it will ask you to mouse over the top left and bottom right part of the Wordle grid. This is used for analyzing submission results.
* The program will attempt to solve the Wordle. In the case of `wordle_all.py`, it will automatically advance through the archive and solve all puzzles.

Install the wordle Anaconda environment:<br>
`conda env create --file envname.yml`

Results on wordle archive (https://www.devangthakkar.com/wordle_archive/?1):

![Archive Results](data/wordleArchivePerformance.png)
