# Vocab Test Program
This is a simple quiz program. It was preset with cet-4 and toefl vocab-definition database.  
However you can add a new vocab database by creating (`word_dict_{name}.json`).
Syntax: `{'word': ['definition', 'example'], ...}`

## Run

Run `quiz.py`

## How to use

### Main instruction

When run, the first thing you need to do is to input the index of a word dict.  
After selecting, the vocab dict will be loaded and you will be redirected to  
main instruction.  
Type a command to continue.  
E.g.: type mc to go to multiple choice.  
You can answer a multiple choice question by typing a number (1-4) and press `<Enter>`  
You can always quit by typing `q` and type `<Enter>`.  
Instructions:
+ NT : normal test
+ MC : multiple choice (definition -> word)
+ IMC: inverse multiple choice (word -> definition)
+ CWL: reselect word dict
+ LW : lookup word
+ S  : view statistics (how many correct or incorrect answers you have done in each section)
+ Q  : quit the program

