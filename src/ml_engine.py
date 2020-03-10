from random import randint
import numpy as np
import torch
import time
import torch.nn as nn
from snake import SnakeGame

################################################################
# RANDOM ENGINE
################################################################


class Random:
    """Engine based on random moves."""

    def __init__(self):
        return None

    def __call__(self, state, speed=0):
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
        time.sleep(speed)
        return randint(-1, 1)


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
        for action in range(-1, 2):
            prev_observation = self.get_observation(state)
            input_data = np.append(action, prev_observation)
            x = torch.tensor(input_data.reshape(-1, 5))
            predictions.append(self.model(x.float()))
            
        # Choose the best action
        return np.argmax(np.array(predictions))-1
        
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

    @staticmethod
    def get_angle(food):
        """Get angle between snake and food in the coordinate system of snake. 
        
        Parameters
        ----------
        food : list, ndarray
            list containing the coordinates of the snake
            in the coordinate system of the snake.
            
        Returns
        -------
        float
            which way the food is in the coordinate system of snake
        
        >>> DNNEngine.get_angle([0, 1])
        1.5707963267948966
        >>> DNNEngine.get_angle([1, 0])
        0.0
        """
        pass

    @staticmethod
    def get_distance(snake_head,food):
        """Get Euclidean distance between snake head and food. 
        
        Parameters
        ----------
        snake_head : list, ndarray
            list containing the coordinates of the snake head
            in the coordinate system of the board.
        food : list, ndarray
            list containing the coordinates of the food in the
            coordinate system of the board.
            
        Returns
        -------
        float
            euclidean distance between snake and food
            
        >>> DNNEngine.get_distance([1,0], [4,0])
        3.0
        >>> DNNEngine.get_distance([1,0], [2,1])
        1.4142135623730951
        """
        pass

    @staticmethod
    def snake_direction(snake):
        """Gives the moving direction of the snake. 
        
        Parameters
        ----------
        snake : list, ndarray
            list containing the coordinates of the snake.
            
        Returns
        -------
        ndarray
            unit vector in the moving direction of the snake.
            
        >>> DNNEngine.snake_direction([[5,6],[5,5],[5,4]])
        array([0, 1])
        >>> DNNEngine.snake_direction([[3,2],[3,1],[4,1]])
        array([0, 1])
        """
        pass

    @staticmethod
    def get_vision(snake_head,snake_dir,snake_dir_ort,board):
        """Get what the snake sees in front of it, to the
        left and to the right.
        
        Parameters
        ----------
        snake_head : ndarray
            list containing the coordinates of the snake head
            in the coordinate system of the board.
        snake_dir : ndarray
            the moving direction of snake
        snake_dir_ort : ndarray
            unit vector that is orthogonal to the moving direction 
            in the left direction
        board : nested list
            the board
            
        Returns
        -------
        list
            list containing what is in the front, to the right and to
            the left of the snake: vision = [FRONT, RIGHT, LEFT]
        """
        pass
        
    @staticmethod
    def transform_coord(coord,snake_head,snake_dir,snake_dir_ort):
        """Transform a coordinate from board coordinates
        to snake coordinates.
        
        Parameters
        ----------
        coord : list, ndarray
            coordinate to be transformed
        snake_head : ndarray
            list containing the coordinates of the snake head
            in the coordinate system of the board.
        snake_dir : ndarray
            the moving direction of snake
        snake_dir_ort : ndarray
            unit vector that is orthogonal to the moving direction
            
        Returns
        -------
        list
            list containing what is in the front, to the right and to
            the left of the snake.
        """
        
        # Define transformation matrix
        matrix = np.array([snake_dir, snake_dir_ort])
        
        # Move coordinate system such that the snake head is origin
        coord = np.array(coord) - np.array(snake_head)
        
        # Rotate coordinate system relative to the snake direction
        trans = matrix.dot(coord)
        return [int(trans[0]), int(trans[1])]
        
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
        
        # Moving direction of snake head
        snake_dir = self.snake_direction(state.snake)
        
        # Unit vector pointing orthogonal to the moving direction
        snake_dir_ort = np.asarray(state._turn_left(snake_dir[0], snake_dir[1]))
            
        # Transform food to snake coordinates
        transform_food = self.transform_coord(state.food, state.snake[0], snake_dir, snake_dir_ort)
        
        # Snake vision
        vision = self.get_vision(state.snake[0], snake_dir, snake_dir_ort, state.board)
        
        # Angle towards the food seen from snake
        angle = self.get_angle(transform_food)
        return np.array([vision[0], vision[1], vision[2], angle])
        
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
            state = SnakeGame()
            prev_food_distance = self.get_distance(state.snake[0], state.food)
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
                    food_distance = self.get_distance(state.snake[0], state.food)
                    
                    # A move is considered as good if the snake 
                    # gets closer to the food or eats the food. 
                    if state.score > prev_score or food_distance < prev_food_distance:
                        target = 1
                    else:
                        target = 0
                    training_data.append(self.pack_data(prev_observation, action, target))
                    prev_observation = self.get_observation(state)
                    prev_food_distance = food_distance
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
        
        # TODO: Append modules (layers and activation functions) to modules
        
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
        x = torch.tensor([i[0] for i in training_data]).reshape(-1, 5)
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
    
    engine = DNN_Engine(initial_games=500, lr=2e-2, max_iter=500)
    player = Player(SnakeGame(), engine, TerminalGui(), speed=1)
    player.play_game()
