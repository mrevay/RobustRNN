# RobustRNN
Contains code the code used to run experiments for:  
-[A Convex Parameterization of Robust Recurrent Neural Networks](https://ieeexplore.ieee.org/abstract/document/9260181)  

In this work, we develop a convex parametrization of recurrent neural networks that are guaranteed to be stable, and have guaranteed incremental l2 gain bounds.

Convexity of the parametrization simplifies model fitting as we can use methods such as projected gradient descent, barrier methods or penalty methods to enforce the constraints. In this project, we used a simple barrier method based on [Nocedal and Writes Primal Interior Point Method] (https://link.springer.com/book/10.1007/978-0-387-40065-5) for enforcing semidefinite programming constraints.

Simulated experiments suggest that these constraints significantly improve robustness and generalizability.
