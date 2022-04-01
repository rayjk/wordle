import pyautogui as pgui
from screeninfo import get_monitors
import pickle
import time
import copy


def getScreen():
    screen = pgui.screenshot()
    dim = screen.size
    cropDim = (w*.1307, h*.2509, w*.3719, h*.7685)
    screen = screen.crop(cropDim)
    screen = screen.resize((200, 200))
    return screen


def nextGuess(guesses, solDat, wordScores):
    invalidScores = []
    submit = -1
    for score in sorted(wordScores.keys(), reverse=True):
        toRemove = []
        for word in wordScores[score]:
            skip = False
            if word in guesses:
                if word not in toRemove:
                    toRemove.append(word)
                continue
            for pos in solDat['inPos']:
                if solDat['inPos'][pos] != word[pos]:
                    if word not in toRemove:
                        toRemove.append(word)
                    skip = True
                    break
            if skip is True:
                continue
            for letter in solDat['out']:
                if word.count(letter) \
                        > tuple(solDat['inPos'].values()).count(letter) \
                        + tuple(solDat['inWrong'].keys()).count(letter):
                    if word not in toRemove:
                        toRemove.append(word)
                    skip = True
                    break
            if skip is True:
                continue
            for letter in solDat['inWrong'].keys():
                if letter not in word:
                    if word not in toRemove:
                        toRemove.append(word)
                    break
                for wrongPos in solDat['inWrong'][letter]:
                    if letter == word[wrongPos]:
                        if word not in toRemove:
                            toRemove.append(word)
                        skip = True
                        break
            if not skip:
                submit = (word, score)
                break
        for word in toRemove:
            wordScores[score].remove(word)
        if len(wordScores[score]) == 0:
            invalidScores.append(score)
        else:
            break

    for score in invalidScores:
        del wordScores[score]

    if submit == -1:
        topScore = max(wordScores.keys())
        submit = (wordScores[topScore][0], topScore)
    return submit, wordScores


screen = getScreen()
screen.show()
screen.save('testScreen.png')
input('\nIf image looks correct, press enter to continue\n')

wordScoresOrig = pickle.load(open('data/wordScores.pickle', 'rb'))

(w, h) = (get_monitors()[0].width, get_monitors()[0].height)

cropDim = (w*0.164, h*.3, w*0.336, h*0.669)

pgui.click(x=cropDim[0], y=cropDim[1]-10)

for round in range(284):
    wordScores = copy.deepcopy(wordScoresOrig)
    guesses = []
    solDat = {'inWrong': {}, 'inPos': {}, 'out': []}
    solved = False
    for y in range(6):
        if solved:
            break
        (guess, score), wordScores = nextGuess(guesses, solDat, wordScores)
        guesses.append(guess)
        print(f'Guessing {guess.upper()} with a word score of {score}...')
        pgui.typewrite(f'{guess}\n', interval=.06)
        screen = getScreen()
        screen.save('tmp.png')
        coordLst = ((x*40+7, int(y*33.33+15)) for x in range(5))
        inPosCount = 0
        for idx, coord in enumerate(coordLst):
            color = screen.getpixel(coord)
            if color[0] > 200:
                if guess[idx] not in solDat['inWrong'].keys():
                    solDat['inWrong'][guess[idx]] = [idx]
                else:
                    solDat['inWrong'][guess[idx]].append(idx)
            elif color[1] > 150:
                solDat['inPos'][idx] = guess[idx]
                inPosCount += 1
                if inPosCount == 5:
                    solved = True
            else:
                if guess[idx] not in solDat['out']:
                    solDat['out'].append(guess[idx])
        print(f'Derived solution data: {solDat}\n')
    if solved:
        print(f'\nSolved in {y+1} attempts! Word is {guess.upper()}\n')
    if round != 283:
        time.sleep(.5)
        pgui.click(x=w*.249, y=h*.755)
        time.sleep(.2)
        pgui.click(x=w*.329, y=h*.206)
"""elif screen.getpixel((121, 35))[2] > 200:
    solved = True"""
