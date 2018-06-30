# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We first iterate through each boxes in a unit grouping them by the value they contain. 
Example 1 : 	Two boxes (eg. A1, D1) contain the same value (13, 13) then the dictionary will look something like this:
				{
					...
					"13" : ['A1', 'D1']
					...
				}

				In this case, we see that the length of string "13" is 2 and the length of list that it is associated with is also 2. So we remove the digits 1 and 3 from all the boxes other than A1 and D1 in the unit

Example 2 : 	Three boxes (eg. A1, D1, F1) contain the same value (123, 123) then the dictionary will look something like this:
				{
					...
					"123" : ['A1', 'D1', 'F1']
					...
				}

				In this case, we see that the length of string "123" is 3 and the length of list that it is associated with is also 3. So we remove the digits 1, 2, and 3 from all the boxes other than A1, D1, and F1.

We repeat this process for all the units.
And then reapply constraint propogation technique until we stop seeing any change.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In this case, only change that we will have to make is to add 2 additional units to the unit_list. We do that by first forming the list of boxes in both the diagonals. And then we attach these two lists to our already existing unit_list which now contains the row units, column units, diagonal units, and square units. Making use of this unit_list, we now apply constraing propogation until we stop seeing any changes.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

