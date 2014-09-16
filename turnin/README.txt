1. How to run?
$ python Solution.py

First, it builds decision trees with maxDepth changing from 0 to 9.
Next, based on the accuracy on the validation data, it choose the best maxDepth.
Finally, it builds the decision tree with the best maxDepth and computes the accuracy on the test data.

2. How many thresholds to use for continuous attributes?
You can change the value of the global variable "maxSplitForContinuous" from 2 to 3 or 4 so that for the continous attributes. Then, more than one thresholds are also considered and find the best one will be chosen in terms of the information gain. Note that if you change the value of "maxSplitForContinuous" to 4, then the computation time will be almost exploded. Please be patient until you get the result.
