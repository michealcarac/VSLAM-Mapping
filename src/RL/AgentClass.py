# This file contains the agents that will be made and used for training
import numpy as np
from EnvironmentClasses import Base
from keras.layers import Input, Dense, Softmax
from keras.optimizers import Adam
from keras.models import Model
from keras.losses import mse
import tensorflow as tf



class InvalidMove(ArithmeticError):
    pass


class Manual():

    def __init__(self, x, y, theta, FOV, env, LINEAR=5, ROTATIONAL=5):
        # Constructor for the Manual Agent class
        # Requires:
        #   x: The x position of the agent
        #   y: The y position of the agent
        #   theta: The rotation of the agent, 0 is along the x axis
        #   FOV: The list of angle difference to look in from theta
        #   LINEAR: The speed of the agent in the forward direction
        #   ROTATIONAL: The speed of the agent in rotation
        #   env: An environment object used for making observations in
        # Returns:
        #   The constructed agent object
        self.x, self.y, self.theta = x, y, theta
        self.POS = (x, y, theta)
        self.FOV = FOV
        self.LINEAR, self.ROTATIONAL = LINEAR, ROTATIONAL
        self.env = env

    def move(self, dir):
        # A function to control the movement of an agent based on the specified direction
        # Requires:
        #   dir: The direction to move in, either 0, 1, 2 for straight, left, right respectively
        # Modifies:
        #   x, y,theta: The postions and rotation of the agent is modified according to the direction of movement
        # Returns:
        #   Nothing
        # Raises:
        #   InvalidMove: Raised if the agent is going to collide with an obstacle after the move is performed

        if dir == 0:
            dists = self.env.get_observation(self.x, self.y, self.theta)
            if dists[self.theta] <= self.LINEAR+0.001:
                raise InvalidMove
            else:
                theta = np.radians(self.theta)
                self.x += self.LINEAR * np.math.cos(theta)
                self.y += self.LINEAR * np.math.sin(theta)
        elif dir == 1:
            self.theta += self.ROTATIONAL
            if self.theta >= 360:
                self.theta -= 360
        else:
            self.theta -= self.ROTATIONAL
            if self.theta < 0:
                self.theta += 360

    def make_heading(self):
        # Helper function to show the heading of the agent
        # Requires:
        #   Nothing
        # Returns:
        #   line: a line from the agent to its next forward position

        x1 = self.x
        y1 = self.y
        theta = np.radians(self.theta)
        x2 = self.x + self.LINEAR * np.math.cos(theta)
        y2 = self.y + self.LINEAR * np.math.sin(theta)
        return [(x1, y1), (x2, y2)]

    def show_agent(self, counter, show=False, path=None, save=True):
        # A function to show the agent in the environment and the direction its facing
        # Requires:
        #   Counter: to track the steps of the agent
        # Returns:
        #   Nothing
        heading = self.make_heading()
        rays = self.env.get_rays(self.x, self.y, self.theta, self.FOV)
        self.env.show_env(lines=[heading], point=(self.x, self.y), step=counter, show=show, path=path, save=save)


class DQAgent(Manual):

    def __init__(self, layers, inputs, start, env, path=None):
        # Constructor for the Deep Q agent
        # Requires:
        #   Layers: The number of dense layers to add to the Neural Network
        #   inputs: The sensor inputs, typically just FOV
        #   start: The starting location of the agent in (x, y, theta)
        #   env: The environment object the agent is in
        #   path: The desired path for the agent to follow, should be of the structure [(x, y, theta)]
        # Returns:
        #   The constructed Deep Q agent object
        super().__init__(start[0], start[1], start[2], inputs, env)
        self.path = path
        self.PATH = path
        self.step = 0
        self.model = self.construct_model(layers, len(inputs), start)
        self.LR = .1
        self.DF = .3
        self.EPSILON = 0

    def reset(self):
        (self.x, self.y, self.theta) = self.POS
        angle = np.random.randint(-10,10)
        self.theta += angle
        self.path = self.PATH

    def construct_model(self, num_layers, sensor_data_shape, position):
        # Create the model for the agent to decide the best move from the given input data
        # Requires:
        #   num_layers: The number of dense layers to add to the model, there will always be at least 1
        #   sensor_data_shape: The shape of the incoming sensor data, must be an array for now
        #   position: The starting position of the model, just for input size
        # Returns:
        #   Model: The model used to predict the best move

        # Input layer
        model_in = Input(shape=(sensor_data_shape + 2*len(position)))

        # Making the dense layers with decreasing node count each layer
        nodes = 8 * pow(2, num_layers)
        x = Dense(nodes, activation='relu')(model_in)
        for i in range(num_layers):
            nodes = nodes // 2
            x = Dense(nodes, activation='relu')(x)

        # Output layer, size 3 for the 3 available directions, forward, left, right
        model_out = Dense(3, activation='softmax')(x)
        return Model(inputs=[model_in], outputs=[model_out])

    def get_model_input(self):
        # A helper function to get and format the data for the model
        # Requires:
        #   Nothing
        # Returns:
        #   Data: The formatted data for the model to predict on

        sensor_data = self.env.get_observation(self.x, self.y, self.theta, self.FOV)
        sensor_data = list(sensor_data.values())
        position = [self.x, self.y, self.theta]
        target = self.path[0]
        data = np.concatenate([sensor_data, position, target])
        data = np.expand_dims(data, -1)
        data = np.expand_dims(data, 0)
        return data

    def predict_q_val(self):
        # A functions to predict the q value from the agents current position and perspective
        # Requires:
        #   Nothing
        # Returns:
        #   q_val: The predicted quality of each move

        # Gathers simulated sensor data from the environment and structures it for the model
        data = self.get_model_input()

        # Predicts the q_value for each move possibility and returns it
        return self.model(data)

    def get_reward(self, pos, target, hit):
        # A function to calculate the reward at a certain point in time
        # Requires:
        #   Pos: The position of the agent to evaluate
        #   Target: The current goal position of the agent
        #   Hit: Boolean if the agent hit an object, results in very negative reward
        # Returns:
        #   reward: The reward for the agent for taking an action towards the target, max value of 1

        pos_error = mse(target, pos)
        reward = 1/pos_error - (self.step*5)
        if hit:
            reward -= 50
        if pos_error < self.LINEAR:
            reward += 50
        return reward

    def training_step(self):
        # A helper function that performs one step of the training
        # Requires:
        #   Nothing
        # Returns:
        # Nothing

        # This try - except block is an attempt at letting the agent learn from hitting something without ending the simulation.
        # WIP
        softmax = Softmax(axis=1)
        try:
            with tf.GradientTape() as tape:

                # Get current q_values
                q_vals = self.predict_q_val()

                # Make a move
                if np.random.rand() < self.EPSILON:
                    move = np.random.randint(0, 3)
                else:
                    move = tf.argmax(q_vals, axis=1)
                    move = move.numpy()[0]
                self.move(move)

                # Get reward
                pos = (self.x, self.y, self.theta)
                target = self.path[0]
                reward = self.get_reward(pos, target, hit=False)
                # Calculate the loss
                # print(tf.cast(mse(pos, target), tf.float32))
                reward = tf.cast(reward, dtype='float32')
                reward = reward.numpy()
                temp = [0,0,0]
                temp[move] = reward
                reward = tf.convert_to_tensor(temp, dtype='float32')
                loss = tf.squeeze(softmax(q_vals+reward))

            # Get gradients
            grads = tape.gradient(loss, self.model.trainable_weights)
            # Apply the gradients
            opt = Adam(0.1)
            opt.apply_gradients(zip(grads, self.model.trainable_weights))
            return 1
        except InvalidMove:
            with tf.GradientTape() as tape:

                # Get current q_values
                q_vals = self.predict_q_val()

                # Get reward
                pos = (self.x, self.y, self.theta)
                target = self.path[0]
                reward = self.get_reward(pos, target, hit=True)
                # Calculate the loss
                reward = tf.cast(reward, dtype='float32')
                loss = tf.squeeze(softmax(q_vals + reward))

            # Get gradients
            grads = tape.gradient(loss, self.model.trainable_weights)
            # Apply the gradients
            opt = Adam(0.1)
            opt.apply_gradients(zip(grads, self.model.trainable_weights))
            return -1

    def training_episode(self, max_iter):
        # A function to handle the process of training the entire episode
        # An episode is defined as the agents life from start to when it reaches the target
        # Requires:
        #   max_iter: The max iterations to train for
        # Returns:
        #   Nothing

        finished = False
        counter = 0
        while not finished and counter <= max_iter:
            # if counter % (max_iter/10) == 0:
            #     print(counter)
            # Make one training step
            if self.training_step() == 1:
                # Check if position is close enough to the current target
                pos = (self.x, self.y)
                target = self.path[0][:2]
                dist = mse(pos, target)
                if len(self.path) == 1:
                    finished = True
                if dist <= self.LINEAR:
                    self.path = self.path[1:]
                    self.step = 0

                self.show_agent(counter, False, self.path, save=False)
                counter += 1
            else:
                self.show_agent(counter, False, self.path, save=False)
                finished = True

    def eval_step(self):
        # A helper function that performs one step of the training
        # Requires:
        #   Nothing
        # Returns:
        # Nothing

        # This try - except block is an attempt at letting the agent learn from hitting something without ending the simulation.
        # WIP
        try:
            # Get current q_values
            q_vals = self.predict_q_val()
            move = tf.argmax(q_vals, axis=1)
            self.move(move)
            return 1
        except InvalidMove:
            return -1

    def eval_episode(self, max_iter):
        # A function to handle the process of evaluating the entire episode
        # An episode is defined as the agents life from start to when it reaches the target
        # Requires:
        #   max_iter: The max iterations to train for
        # Returns:
        #   Nothing

        finished = False
        counter = 0
        while not finished and counter <= max_iter:
            # Make one training step
            if self.eval_step() == 1:
                # Check if position is close enough to the current target
                pos = (self.x, self.y)
                target = self.path[0][:2]
                dist = mse(pos, target)
                if len(self.path) == 1:
                    finished = True
                if dist <= self.LINEAR:
                    self.path = self.path[1:]
                    self.step = 0
                self.show_agent(counter, False, self.path)
                counter += 1
            else:
                self.show_agent(counter, False, self.path)
                finished = True


if __name__ == "__main__":
    import os
    from shutil import rmtree
    if 'Figures' in os.listdir():
        rmtree('Figures', ignore_errors=True)
    os.mkdir('Figures')
    env = Base(width=100, height=210, num_obstables=0, box_h=100, box_w=100)
    fov = []
    for i in range(-45, 45):
        fov.append(i)
    path = [[0, 2, 0],
            [0, 3, 0], [0, 4, 0],
            [0, 5, 0], [0, 6, 0],
            [0, 7, 0], [0, 8, 0],
            [0, 9, 0], [0, 10, 90],
            [1, 10, 90], [2, 10, 90],
            [3, 10, 90], [4, 10, 90],
            [5, 10, 90], [6, 10, 90],
            [7, 10, 0], [7, 11, 0],
            [7, 12, 0], [7, 13, 0],
            [7, 14, 0], [7, 15, 0],
            [7, 16, 0], [7, 17, 0],
            [7, 18, 0], [7, 19, 0],
            [7, 20, 0]]
    for i in range(len(path)):
        temp = path[i]
        path[i][0] = temp[0] * 10 + 10
        path[i][1] = temp[1] * 10
    print(path)
    agent = DQAgent(4, fov, (10, 10, 90), env, path)
    try:
        os.chdir('Figures')
        for i in range(1000000000):
            os.mkdir(f"Epoch_{i}")
            os.chdir(f"Epoch_{i}")
            print(f"Starting epoch {i}")
            agent.training_episode(100)
            print(f"{len(agent.path)} points left")
            agent.reset()
            os.chdir('..')
            # agent.EPSILON -= .01


        os.mkdir('Eval')
        os.chdir('Eval')
        agent.reset()
        agent.eval_episode(100)
        agent.model.save('this_model_sucks')
    except KeyboardInterrupt:
        agent.reset()
        agent.eval_episode(100)
        agent.model.save('this_model_sucks')