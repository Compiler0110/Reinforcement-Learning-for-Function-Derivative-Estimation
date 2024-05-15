# Reinforcement-Learning-for-Function-Derivative-Estimation


An implementation of Reinforcement Learning for estimating derivatives of functions. This Python code utilizes the finite difference method and Q-Learning to approximate the derivative of a given function at a specific point. Users can input their own functions and points of interest to observe the agent learning process.

# Finite Difference Method

The finite difference method is a numerical technique used to approximate the derivative of a function at a given point. In this implementation, I use the central difference formula:
f'(x) ≈ \frac{{f(x + h) - f(x - h)}}{{2h}}

where:
- \( f(x) \) is the function of interest,
- \( f'(x) \) is the derivative of the function at point \( x \),
- \( h \) is a small step size.
