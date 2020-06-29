import numpy as np

class QlearningAgent:
    def __init__(self, env, Q=None):
        self.env = env
        self.step_size = 0.3
        self.gamma = 0.9 # discount rate
        self.epsilon = 1.0 # exploration rate
        self.epsilon_decay_rate = 0.95
        self.min_epsilon = 0.001
        self.q = dict()
        self.actions = self.env.action_space

    def act(self, state):
        """ epsilon-greedy algorithm """
        if state not in self.q:
            self.q[state] = {a: 0 for a in self.actions}

        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.actions)
        
        # pick the action with highest Q value
        q_values = {a: self.q[state][a] for a in self.actions}
        max_q = max(q_values.values())

        # random sampling for actions that have the same maximum Q value
        actions_with_max_q = [a for a, q in q_values.items() if q == max_q]
        return np.random.choice(actions_with_max_q)

    def update_q_value(self, state, reward, action, next_state, done):
        """ Q(s, a) += alpha * (r(s, a) + gamma * max Q(s', .) - Q(s, a)) """
        if next_state not in self.q:
            self.q[next_state] = {a: 0 for a in self.actions}

        max_q_next = max([self.q[next_state][a] for a in self.actions])
        # no need to include the value of the next state if done
        self.q[state][action] += self.step_size * (
            reward + self.gamma * max_q_next * (1.0 - done) - self.q[state][action]
        )
