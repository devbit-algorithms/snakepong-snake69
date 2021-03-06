# Snakepong game by Timon Claerhout

## Hoe spel starten?

### Linux

Je naar de terminal die zich in de map van dit git-project bevind en je typt hierbij deze command:

```sql
python snakepong.py
```

### Windows

Je opent Ubuntu en gaat naar de map van dit git-project, vervolgens typ je deze command:

```sql
python3 snakepong.py
```

Als je curses wilt installeren op windows, typ deze command:

```sql
pip install windows-curses
```

## Demo

![Demo of game](./img/demo_game.gif)

Je kan de grootte van het veld aanpassen door het venster van de terminal te vergroten/verkleinen.
Hoe kleiner het veld, hoe moeilijker het is om te scoren.

## Analyse van Snake game

### Benodigdheden

Game field\
Muren\
Paddle -> list\
Slang -> list\
Bal -> list\
Scorebord -> int\
Pijl toetsen van toetsenbord kunnen uitlezen om snake te veranderen van positie\
Kijken als slang muur niet raakt of zijn staart -> Game Over\
Kijken als de slang niet tegen de paddle botst -> Game Over\
Bal moet tegen de muren botsen zodat hij in het veld blijft\
Als snake, paddle of rechtermuur bal raakt, moet de bal veranderen van richting\
Als de paddle de bal niet kan opvangen, score verhogen en staart van snake langer maken

### Schema van code

Waarbij sh = Screen Heigh en sw = Screen Width van terminal.

![Schema code](./img/Schema.png)
