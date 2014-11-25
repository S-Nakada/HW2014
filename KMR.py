from __future__ import division
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
from mc_tools import mc_compute_stationary, mc_sample_path
      
"""
This file is based on D.Oyama's class file, KMR_2x2.
      
"""
    
"""
Parameters for KMR game.
      
N; number of players.
p; number of threshhold to take an action 1 for best response.
epsilon; probability of random choice (experiment, mutation).
x; number of agents playing action 1.
"""
    
"""
(1) Simultenious revisions.
   
"""
def KMR_2x2_P_simultaneous(N, p, epsilon):
          P = np.empty((N+1, N+1), dtype=float)
          for x in range(N+1):
            P[x,:]  = \ # transition probability where current state is x.
                 (x/N < p) * binom.pmf(range(N+1), N, epsilon/2) + \ 
                 (x/N == p) * binom.pmf(range(N+1), N, 1/2) + \      # Each prob.dist affected by current state.
                 (x/N > p) * binom.pmf(range(N+1), N, 1-epsilon/2)
          return P
      
     
"""           
(2) Sequential revisions
I allow each agent to play the game with himself.
      
"""
                
def KMR_2x2_P_sequential(N, p, epsilon):
          P = np.zeros((N+1, N+1), dtype=float)
          
          P[0, 0], P[0, 1] = 1 - epsilon * (1/2), epsilon * (1/2) # transition where current state is x=0.
          P[N, N-1], P[N, N] = epsilon * (1/2), 1 - epsilon * (1/2) # transiiton where current state is x=N.
      
          for x in range(1, N):
             P[x, x-1] = \ # transiton to one decreased state.
                  (x/N) * (
                            (x/N >p)*epsilon * (1/2)
                            (x/N == p) * (1/2))
                            (x/N < p)*(1 - epsilon*(1/2))
                           )
              
              P[x, x+1] = \ #transition to one increased state.
                  (1-(x/N)) * (
                                (x/N >p)*(1 - epsilon*(1/2))
                                (x/N == p) * (1/2))
                                (x/N < p)*epsilon * (1/2)
                               )
                  
              P[x, x] = 1 - P[x, x-1] - P[x, x+1] #transition to be remained current state.
              
          return P
      
class KMR_2x2:
      # Determine dynamics senario; simultenious or sequential
   def __init__(self, N, p, epsilon, move='simultaneous'):
              self._epsilon = epsilon
              self.N, self.p, self.move = N, p, move
              self.set_P() # game what to use, simultenious or sequential.
      
   def get_epsilon(self):
        return self._epsilon
      
   def set_epsilon(self, new_value):
              self._epsilon = new_value
              self.set_P()
      
    epsilon = property(get_epsilon, set_epsilon)
      
    def set_P(self): # Command to recognize each senario to use.
        if self.move == 'sequential':
            self.P = KMR_2x2_P_sequential(self.N, self.p, self._epsilon)
        else:
            self.P = KMR_2x2_P_simultaneous(self.N, self.p, self._epsilon)
                  
      #Simulation code
      
    def simulate(self, T=100000, x0=0):
             
  """
  Generates a NumPy array containing a sample path of length T
  with initial state x0 = 0
  
  """
  self.s = mc_sample_path(self.P, x0, T)
      
    def get_sample_path(self):
        return self.s
      
      #Plot a sample path\n",
      
    def plot_sample_path(self, ax=None, show=True):
        if show:
                  fig, ax = plt.subplots()
              ax.plot(self.s, alpha=0.5)
              ax.set_ylim(0, self.N)
              ax.set_title(r'Sample path: $\\varepsilon = {0}$'.format(self._epsilon))
              ax.set_xlabel('time')
              ax.set_ylabel('state space')
        if show:
                  plt.show()
      
    def plot_emprical_dist(self, ax=None, show=True):
         if show:
                  fig, ax = plt.subplots()
              hist, bins = np.histogram(self.s, self.N+1)
              ax.bar(range(self.N+1), hist, align='center')
              ax.set_title(r'Emprical distribution: $\\varepsilon = {0}$'.format(self._epsilon))
              ax.set_xlim(-0.5, self.N+0.5)
              ax.set_xlabel('state space')
              ax.set_ylabel('frequency')
        @if show:
                  plt.show()
      
      # Compute a stationary distribution\n",
      
          def compute_stationary_dist(self):
              
             """                               
              Generates a NumPy array containing the stationary distribution
             """ 
              
              self.mu = mc_compute_stationary(self.P)
    
          def get_stationary_dist(self):
              return self.mu
      
          def plot_stationary_dist(self, ax=None, show=True):
              if show:
                  fig, ax = plt.subplots()
              ax.bar(range(self.N+1), self.mu, align='center')
              ax.set_xlim(-0.5, self.N+0.5)
              ax.set_ylim(0, 1)
              ax.set_title(r'Stationary distribution: $\\varepsilon = {0}$'.format(self._epsilon))
              ax.set_xlabel('state space')
              ax.set_ylabel('probability')
              if show:
                  plt.show()
      
      if __name__ == '__main__':
          p = 1/3
          N = 10
          epsilon = 0.03
          T = 300000
      
          kmr = KMR_2x2(N, p, epsilon)
          kmr.simulate(T)
          kmr.plot_sample_path()
    