# Ball Bouncing Simulation

## Overview
This Python script simulates the motion of a ball bouncing in the presence of air resistance and gravity. It includes interactions with a floor and a vertical wall. The simulation determines the optimal initial velocity for a given launch angle that minimizes the ball's deviation from its starting height upon return.

## Features
- Simulates projectile motion with air resistance.
- Models collisions with the ground and a vertical wall.
- Finds the optimal initial velocity for a given launch angle.
- Provides an animation of the ball's trajectory.

## Dependencies
The script requires the following Python libraries:
- `numpy` for numerical computations.
- `matplotlib` for visualization and animation.
- `os` for clearing the terminal.
- `math` for trigonometric and mathematical functions.

## Functions and Classes

### `calc_theta(vx, vy)`
Calculates the angle of motion based on velocity components.

### `Lopta` Class
Represents the ball and its motion.

#### Attributes:
- `x`, `y`: Position coordinates.
- `theta`: Angle of motion.
- `v`: Velocity magnitude.
- `greska`: Deviation from the initial height.
- `povijest`: Stores trajectory data.

#### Methods:
- `update()`: Updates the ball's position and velocity per time step.
- `simulacija(animiraj)`: Runs the simulation and optionally animates the motion.

### `optimalna_loptica(theta)`
Finds the optimal initial velocity for a given launch angle by minimizing height deviation.

## Simulation Parameters
- `k = 0.7`: Coefficient of restitution.
- `delta_t = 0.02`: Time step.
- `lambdaa = 0.0003`: Air resistance coefficient.
- `g = 9.81`: Gravitational acceleration.

## User Input
- `theta0`: Initial launch angle (degrees).
- `x_zid`: Distance of the vertical wall from the origin.
- `y_zid = x_zid - 1`: Height of the wall.

## Execution
The program:
1. Clears the terminal.
2. Prompts the user for the initial launch angle and wall distance.
3. Determines the optimal initial velocity.
4. Simulates and optionally animates the ball's trajectory.

## Output
- A plot showing the ball's trajectory, the ground, and the vertical wall.
- An animation illustrating the motion.

## Usage
Run the script in a Python environment and enter the requested parameters when prompted.
