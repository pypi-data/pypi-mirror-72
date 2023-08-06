import json

# create a new scoreboard
def newScoreboard(Kara, speak):
    # if

    # get team count
    Kara.speak('How many teams are there?')
    try:
        teams = int(kara.listen())
    except ValueError:
        Kara.speak('Please say a number')
        return

    # get previous

    with open('score.json', 'w') as score:
        # dump data (nicely)
        json.dump(scores, score,
                  sort_keys=True, indent=4, separators=(',', ': '))
