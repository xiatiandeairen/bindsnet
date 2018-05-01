import sys
import torch
import numpy as np
import matplotlib.pyplot as plt


class Pipeline:
	
	def __init__(self, Network, Environment, plot=False, **kwargs):
		'''
		Initializes the pipeline
		
		Inputs:
			Network (bindsnet.Network): Arbitrary network (e.g ETH)
			Environment (bindsnet.Environment): Arbitrary environment (e.g MNIST, Space Invaders)
			plot (bool): plot monitor variables 
		'''
		# Plot interval?
		
		self.network = Network
		self.env = Environment
		
		# Create figures based on desired plots inside kwargs
		self.plot = plot
		
		if self.plot:
			self.axs, self.ims = self.plot()
		
		# Kwargs being assigned to the pipeline
		self.time = kwargs['time']
		self.render = kwargs['render']
		self.history = {n: 0 for n in range(kwargs['history'])}
		
		self.iteration = 0		
		
#		self.fig = plt.figure()
#		self.axes = self.fig.add_subplot(111)
#		self.f_pic = self.axes.imshow(np.zeros( (78, 84)), cmap='gray')
		
		
	def step(self):
		'''
		Step through an iteration 
		'''
		
		if self.iteration % 100 == 0:
			print('Iteration %d' % self.iteration)
		
		# Based on the environment we could want to render
		if self.render:
			self.env.render()
			
		# Choose action based on readout neuron spiking.
		if self.network.layers['R'].s.sum() == 0 or self.iteration == 0:
			action = np.random.choice(range(6))
		else:
			action = torch.multinomial((self.network.layers['R'].s.float() / self.network.layers['R'].s.sum()).view(-1), 1)[0] + 1
#			action = torch.max( (self.network.layers['R'].s.float() / self.network.layers['R'].s.sum()).view(-1) , -1)[1][0] + 1
		
		# If an instance of OpenAI gym environment
		obs, reward, done, info = self.env.step(action)
		
		# Recording initial observations
		if self.iteration < len(self.history):
			self.history[self.iteration] = obs
		else:
			new_obs = torch.clamp(obs - sum(self.history.values()), 0, 1)		
#			self.f_pic.set_data(new_obs.numpy().reshape(78, 84))
#			self.fig.canvas.draw()
			self.history[self.iteration%len(self.history)] = obs
			
			obs = new_obs			
			
		# Run the network
		self.network.run(inpts={'X': obs}, time=self.time)
		
		# Plot any relevant information
		if self.plot:
			self.plot()
		
		self.iteration += 1

		return done
		
	
	def plot(self):
		'''
		Plot monitor variables or desired variables?
		'''
		if self.ims == None and self.axs == None:
			# Initialize plots
			pass
		else: # Update the plots dynamically
			pass
		
	
	def normalize(self, src, target, norm):
		self.network.connections[(src, target)].normalize(norm)
	
	
	def reset(self):
		'''
		Reset the entire pipeline
		'''
		self.env.reset()
		self.network._reset()
		self.iteration = 0
		self.history = {n: 0 for n in len(self.history)}
		
		# Reset plots
	
	
	
	
	
	
	
	
	
		