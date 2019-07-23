

From and credit to :
https://github.com/RuairiD/perudo


# Perudo
Love Perudo but have no friends? You'll love this!
### What is it?
A command-line Perudo clone written in Python. Supports an indefinite number of AI players and dice.

### How do I start it?
Clone the repo, `cd` to the repo directory then run:

```sh
$ python perudo.py <name> <bots> <dice>
```

where:
  - `name` is your name
  - `bots` is the number of AI players to play against (default of 3)
  - `dice` is the number of dice each player starts with (default of 5)

For example:
```sh
$ python perudo.py Ruairi 4 5
```
will start a game with 4 AI players and 5 dice per player.

### How do I play?
When it's your turn, type in your bet. Bet inputs consist of two numbers separated by an `x` e.g. to bet 4 6s, enter `4x6`. Alternatively, if you think the last bot is chatting rubbish, type `dudo` to call, er, dudo.

### Why is it slow?
I've added in `sleep` calls to make the game easier to follow and prevent silly amounts of text dumping. You can toggle this in `config.py`.

### I don't know how to play Perudo.
[Check it out.](http://www.perudo.com/perudo-rules.html)

### I don't like Perudo.
This won't change your mind.
