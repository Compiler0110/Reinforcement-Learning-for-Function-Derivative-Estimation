import numpy as np

class DerivativeEnv:
    def __init__(self, func, point, action_space, h=1e-5):
        self.func = func
        self.point = point
        self.action_space = action_space
        self.h = h
        self.state = None
        self.solution = None
        self.done = False

    def reset(self):
        self.state = self.point
        self.solution = self.true_derivative(self.func, self.point)
        self.done = False
        return self.state

    def step(self, action):
        reward = self.calculate_reward(action, self.solution)
        self.done = True
        return self.state, reward, self.done

    def true_derivative(self, func, x):
        return (func(x + self.h) - func(x - self.h)) / (2 * self.h)

    def calculate_reward(self, action, true_derivative):
        return -abs(action - true_derivative)



class QLearningAgent:
    def __init__(self, alpha, gamma, epsilon, num_actions, state_size, state_range):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_actions = num_actions
        self.state_range = state_range
        self.q_table = np.zeros((state_size, num_actions))

    def choose_action(self, state):
        discretized_state = int(min(max(state * (self.q_table.shape[0] - 1) / self.state_range, 0), self.q_table.shape[0] - 1))
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, self.num_actions)
        else:
            return np.argmax(self.q_table[discretized_state])

    def update_q_table(self, state, action, reward, next_state):
        discretized_state = int(min(max(state * (self.q_table.shape[0] - 1) / self.state_range, 0), self.q_table.shape[0] - 1))
        old_value = self.q_table[discretized_state, action]
        discretized_next_state = int(min(max(next_state * (self.q_table.shape[0] - 1) / self.state_range, 0), self.q_table.shape[0] - 1))
        next_max = np.max(self.q_table[discretized_next_state])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[discretized_state, action] = new_value



def train_agent(agent, env, num_episodes):
    rewards = []
    for episode in range(num_episodes):
        state = env.reset()
        episode_reward = 0
        while True:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state
            episode_reward += reward
            if done:
                rewards.append(episode_reward)
                break
    return rewards

def test_agent(agent, env, num_tests):
    total_reward = 0
    for _ in range(num_tests):
        state = env.reset()
        while True:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            total_reward += reward
            state = next_state
            if done:
                break
    return total_reward / num_tests


def main():
    func = lambda x : x**2
    point = 1
    action_space = np.linspace(-10, 10, 100)
    state_range = 1

    env = DerivativeEnv(func, point, action_space)
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1, num_actions=len(action_space), state_size=100, state_range=state_range)

    num_episodes = 5000
    rewards = train_agent(agent, env, num_episodes)

    num_tests = 5
    average_reward = test_agent(agent, env, num_tests)


    print("Problem: Find the derivative of the function f(x) =", func, "at x =", point)
    print("Solution: f'(", point, ") =", env.solution)
    print("Average reward:", round(average_reward, 2))


    episodes_to_solve = np.argmax(np.array(rewards) >= -0.01) + 1
    print("Episodes to solve:", episodes_to_solve)

if __name__ == "__main__":
    main()
