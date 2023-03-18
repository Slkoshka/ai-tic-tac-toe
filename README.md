# AI Tic-Tac-Toe
This game was created entirely by GPT-4 and GPT-3.5 with as little technical details provided by the operator as possible. The implementation is not very efficient because that was not the focus and GPT wasn't allowed to refactor the code. Even this README.md file was written by GPT-3.5.

If you have any questions, you can contact [me (_the operator_)](https://github.com/Slkoshka) on [Twitter](https://twitter.com/Slkoshka).

# Development process
1. GPT was asked to create a skeleton for the main class of the game.
1. GPT implemented the basic version of the game, with a human player only.
1. GPT was asked to add support for playing against an AI player.
1. GPT was asked to add support for different AI strategies.
1. GPT implemented two AI strategies: random and optimal.
1. GPT was asked to add a menu to the game.
1. GPT added a menu with four screens: one/two players selection, AI strategy selection, main game screen, and results screen.
1. The game was tested by the operator, and stack traces were provided to GPT for the bugs that were discovered while testing the game. GPT fixed the bugs.
1. GPT was asked to make the game executable, so it was packaged into a .exe file.
1. GPT was asked to make the game not show a terminal window when launched.

The results of the last two steps are not included in this repository (for reference, GPT came up with a solution using "pyinstaller" library).

# Requirements
To run the game, you need:

* Python 3.x
* pygame library

To launch the game, navigate to the project directory and run the following command:

```bash
python tic_tac_toe.py
```

This will start the game and bring up the main menu.

# License
This game is public domain. You are free to use it for any purpose, commercial or non-commercial.

# How to contribute
Contributions are not accepted for this project. This project was entirely created by AI models, and there are no plans to further develop it.

# Disclaimer
This game and this README.md file were created entirely by AI models. The creator of this repository is not responsible for any issues or damages that may result from the use of this game or this README.md file.
