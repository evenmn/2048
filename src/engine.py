from random import randint, choice
import numpy as np
import time
import torch
import torch.nn as nn
from tzfe import TZFE

################################################################
# RANDOM ENGINE
################################################################


class Random:
    """Engine based on random moves."""

    def __init__(self):
        return None

    def __call__(self, state):
        """This function returns a random integer
        in the interval (-1, 1). 
        
        Parameters
        ----------
        state : object
            object containing information about the 
            state. Is never used in this class, but 
            all engine classes require this parameter.
        speed : int
            speed of snake. speed=0 is the fastest.
            
        Returns
        -------
        int
            which way to turn (-1 is left, 0 is no turn, 1 is right).
        """
        return choice(list(state.ACTIONS.values()))


################################################################
# DNN ENGINE
################################################################


class DNNEngine:
    """Snake engine controlled by a fully connected dense neural
    network. 
    
    Parameters
    ----------
    initial_games : int
        number of games for the training
    goal_steps : int
        max number of steps in a game
    lr : float
            learning rate
    max_iter : int
        maximum number of training iterations (epochs)
    engine : object
        engine to be used in the training process
    """ 
    def __init__(self, initial_games = 1000,
                       goal_steps    = 500,
                       lr            = 2e-2,
                       max_iter      = 500,
                       engine = Random()):
        self.engine = engine
        self.model_torch()
        self.train_torch(lr, max_iter, initial_games, goal_steps)

    def __call__(self, state, speed=0):
        """This function returns the next turn given by the
        neural network. 
        
        Parameters
        ----------
        state : object
            object containing information about the 
            state.
        speed : int
            speed of snake. speed=0 is the fastest.
            
        Returns
        -------
        int
            which way to turn (-1 is left, 0 is no turn, 1 is right).
        """
        time.sleep(speed)
        predictions = []
        
        # Try all possible actions
        for action in list(state.ACTIONS.values()):
            prev_observation = self.get_observation(state)
            input_data = np.append(action, prev_observation)
            x = torch.tensor(input_data.reshape(-1, 17))
            predictions.append(self.model(x.float()))
            
        # Choose the best action
        print(np.array(predictions, dtype=np.int))
        return np.argmax(np.array(predictions))
        
    def generate_action(self, state):
        """Get next action, given an engine self.engine.
        To be used in the training session.
        
        Parameters
        ----------
        state : object
            object containing information about the 
            state.
        """
        return self.engine(state)
        
    def get_observation(self,state):
        """Generate observation to be used as input to
        the neural network. The next action is not known at this point,
        so we need to add it later. 
        
        Parameters
        ----------
        state : object
            object containing information about the 
            state.
            
        Returns
        -------
        ndarray
            array containing the vision of the snake and the food
            direction.
        """
        observations = state.board.flatten()
        self.num_inputs = len(observations)
        return observations
        
    @staticmethod
    def pack_data(observation,action,target):
        """Collect the input data and target for the current move.
        should take the form:
        [(action, vision, angle), target].
        
        Parameters
        ----------
        observation : ndarray
            array obtaining the vision and angle, returned by
            self.get_observation
        action : int
            the current action (which way to go)
        target : int
            evaluation of the move (1 is good, 0 is neutral, -1 is bad)
            
        Returns
        -------
        list
            list where the inputs to the neural network and targets
            are collected
        """
        input_data = np.append(action, observation)
        return [input_data, target]
        
    def generate_training_data(self,initial_games,goal_steps):
        """Generate training data for the neural network 
        based on random action. 
        
        Parameters
        ----------
        initial_games : int
            number of games for the training
        goal_steps : int
            max number of steps in a game
            
        Returns
        -------
        list
            list containing the input data and the targets
        """
        training_data = []
        from tqdm import tqdm
        for i in tqdm(range(initial_games)):
            state = Game()
            prev_score = state.score
            prev_observation = self.get_observation(state)
            for j in range(goal_steps):
                # Get action
                action = self.generate_action(state)
                
                # Update state
                state = state(action)
                
                # We will now evaluate the performed moves, using
                # a target system where -1 means a bad move, 0 means a neutral 
                # move and 1 means a good move. 
                
                # A move is bad if the snake crashes.  
                if state.done:
                    target = -1
                    training_data.append(self.pack_data(prev_observation, action, target))
                    break
                else:
                    # A move is considered as good if the snake 
                    # gets closer to the food or eats the food. 
                    if state.score > prev_score:
                        target = 2
                    else:
                        target = 0
                    training_data.append(self.pack_data(prev_observation, action, target))
                    prev_observation = self.get_observation(state)
                    prev_score = state.score
        return training_data

    def model_torch(self):
        """Model of a dense neural network. 
        
        Returns
        -------
        object
            object containing the pytorch model
        """
        modules = []
        
        modules.append(nn.Linear(17, 10))
        modules.append(nn.ReLU())
        modules.append(nn.Linear(10, 10))
        modules.append(nn.ReLU())
        modules.append(nn.Linear(10, 1))
        self.model = nn.Sequential(*modules)
        return self.model

    def train_torch(self, lr, max_iter, initial_games, goal_steps):
        """Train the naural network model.
        
        Parameters
        ----------
        lr : float
            learning rate
        max_iter : int
            maximum number of training iterations (epochs)
        initial_games : int
            number of games for the training
        goal_steps : int
            max number of steps in a game
        """
        # Get data
        training_data = self.generate_training_data(initial_games, goal_steps)
        x = torch.tensor([i[0] for i in training_data]).reshape(-1, 17)
        t = torch.tensor([i[1] for i in training_data]).reshape(-1, 1)

        # Define loss and optimizer
        loss_func = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

        # Train network
        for epoch in range(max_iter):
            # Forward propagation
            y = self.model(x.float())
            loss = loss_func(y, t.float())
            print("epoch: ", epoch, " loss: ", loss.item())  # Zero the gradients
            optimizer.zero_grad()

            # Backward propagation
            loss.backward()   # perform a backward pass (backpropagation)
            optimizer.step()  # update parameters

if __name__ == "__main__":
    from player import Player
    from gui import MatplotlibGui, TerminalGui
    
    engine = DNNEngine(initial_games=500, lr=2e-2, max_iter=500)
    player = Player(Game(), engine, TerminalGui())
    player.play_game()
