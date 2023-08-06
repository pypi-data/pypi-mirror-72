JPong
========

This is a simple implementation of the classic video game written in Python with the Pygame library.
The J stands for Jeff.

Installation
------------

To install, simply run `pip install JPong`. That's it! To start playing, enter the command `jpong`
in a terminal.

Play
----

To play, use the up and down array keys on your keyboard to control the paddle. To pause, press P.
To continue playing, press S. To quit, press the escape key, or select the "X" in the top right
of the game window. When you lose, you can simply press R to start a new game.

There are four game modes: easy, medium, hard, and impossible. The default is medium, but if you want to make
the game easier or harder, simply pass the desired difficulty using the `--mode` option. For example

```
jpong --mode impossible
```

or

```
jpong -m impossible
```

Modifications and Bugs
----------------------

Please feel free to email me at jeff.moorhead1@gmail.com about problems with the game or suggestions for modifications. I'm always
open to new ideas.
