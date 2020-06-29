# Playing Snake with Reinforcement Learning

A snake game controlled by an AI agent. 

<img src="https://i.imgur.com/TpRDZ52.gif" height="436" width="436">

## Introduction

The game is developed using pygame. The goal for the snake is to eat as much as food as possible before it eats itself or hits one of the four borders. The agent is able to score over 50 after 500 episodes of training (which takes less than 15 seconds).

The agent is trained using the Q-learning algorithm. The agent receives a reward of +50 when the the food is eaten, and a penalty of -30 when the snake eats itself or hits a border. To discourage any redundant step, the agent receives a penalty of -1 for each step it has taken.

A navie state space would use the exact positions of the snake and food. In an n^2 board, each square has four possible conditions: empty, occupied by the food, occupied by the head of the snake, or occupied by the body of the snake. In this approach, the number of possible states is (n^2)^4, which makes training difficult. The state space used in this algorithm only considers (a) whether there is an object (food, snake's body, or a border) adjacent to the snake head in the straight, left and right directions, and (b) whether the food is in front of/behind the snake and to the left/right of the snake. The size of the state space is, therefore, reduced to 3^3 x 2^2. However, since the agent can only read one step ahead, it does have a tendency to trap itself into a location when it doesn't have sufficient space to get itself out.

## Installation

```bash
$ git clone https://github.com/kingyiusuen/snake.git
```

## Run

To run the game, type the following command in the terminal:

```bash
$ python play.py --display --retrain --num_episodes=500
```

Argument description:

--display: (Optional) display the game view or not    
--retrain: (Optional) retrain the agent from scratch or continue training the policy stored in ``q.pickle``    
--num_episodes: (Optional) number of episodes to run in this training session (default=500)

Turning off the game display will speed up the training. The action-value function after 500 episodes of training is stored in ``q.pickle``. The file will automatically be loaded when the script is run, and the training will continue. If you want to re-train the agent, simply add the ``--retrain`` argument.

## Acknowledgement

The Stanford students who developed [this project](http://cs229.stanford.edu/proj2016spr/report/060.pdf) - For the idea of using the relative position of the food, instead of the exact position.
