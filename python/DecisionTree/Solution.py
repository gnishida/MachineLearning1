import math
import copy
import Check
from statsmodels.sandbox.distributions import examples

# Example
class Example:
	def __init__(self, row, label, weight):
		self.row = row
		self.label = label
		self.weight = weight

# Decision Tree Node class
class TreeNode:
	def __init__(self, attr_index, attr_type, attr_th, isLeaf, label):
		self.attr_index = attr_index
		self.attr_type = attr_type
		self.attr_th = attr_th
		self.childNodes = {}
		self.isLeaf = isLeaf
		self.label = label

	def addChildNode(self, value, childNode):
		self.childNodes[value] = childNode

	def display(self, indent):
		if self.isLeaf:
			print(" " * indent + "Leaf: " + self.label)
			return

		if self.attr_type == "B":
			print(" " * indent + "Attribute: " + str(self.attr_index))
		else:
			print(" " * indent + "Attribute: " + str(self.attr_index) + " (Threshold: " + str(self.attr_th) + ")")
		for value, childNode in self.childNodes.iteritems():
			print(" " * (indent + 2) + "+ [value: " + str(value) + "]")
			childNode.display(indent + 4)

	def predict(self, example):
		if self.isLeaf == True:
			if self.label == "+": return 1.0
			elif self.label == "-": return -1.0
			else: return 0.0
		elif self.attr_type == "B":
			if self.attr_index >= len(example.row):
				print("ERROR")

			if example.row[self.attr_index] == "?":
				ret = 0.0
				for value, childNode in self.childNodes.iteritems():
					ret += childNode.predict(example) / float(len(self.childNodes))
				return ret
			else:
				return self.childNodes[example.row[self.attr_index]].predict(example)
		else:
			if example.row[self.attr_index] == "?":
				ret = 0.0
				for value, childNode in self.childNodes.iteritems():
					ret += childNode.predict(example) / float(len(self.childNodes))
				return ret
			else:
				if float(example.row[self.attr_index]) < self.attr_th:
					return self.childNodes["<"].predict(example)
				else:
					return self.childNodes[">"].predict(example)

def DecisionTree():
	#TODO: Your code starts from here.
	#      This function should return a list of labels.
	#      e.g.:
	#	labels = [['+','-','+'],['+','+','-'],['-','+'],['+','+']]
	#	return labels
	#	where:
	#		labels[0] = original_training_labels
	#		labels[1] = prediected_training_labels
	#		labels[2] = original_testing_labels
	#		labels[3] = predicted_testing_labels




	return


def DecisionTree(maxDepth):
	#TODO: Your code starts from here.
	#      This function should return a list of labels.
	#      e.g.:
	#	labels = [['+','-','+'],['+','+','-'],['-','+'],['+','+']]
	#	return labels
	#	where:
	#		labels[0] = original_training_labels
	#		labels[1] = prediected_training_labels
	#		labels[2] = original_testing_labels
	#		labels[3] = predicted_testing_labels


	# define the attributes
	attrs = {0: "B", 1: "C", 2: "C", 3: "B", 4: "B", 5: "B", 6: "B", 7: "C", 8: "B", 9: "B", 10: "C", 11: "B", 12: "B", 13: "C", 14: "C"}

	# read training data
	examples = readData("train.txt")

	# create a decision tree
	rootNode = createSubTree(examples, attrs, maxDepth)
	rootNode.display(0)

	o_train = truth(examples)
	p_train = predict(rootNode, examples)

	# read test data and predict labels
	tests = readData("train2.txt")
	o_test = truth(tests)
	p_test = predict(rootNode, tests)

	Check.eval(o_train, p_train, o_test, p_test)

	return

# get the ground truth of the labels
def truth(examples):
	labels = []
	for example in examples:
		labels.append(example.label)
	return labels

# predict labels for the given test data
def predict(rootNode, tests):
	labels = []
	for test in tests:
		label = "?"
		if rootNode.predict(test) >= 0:
			label = "+"
		else:
			label = "-"
		labels.append(label)
	return labels

# create subtree of the decision tree
def createSubTree(examples, attrs, maxDepth):
	# if all the examples are labeled the same, return a leaf node with label
	if maxDepth == 0 or isAllExampleLabeledSame(examples):
		return TreeNode(-1, "", 0, True, mostCommonLabel(examples))

	attr_index, attr_th = findBestAttribute(examples, attrs)

	# if there is no available attributes left, then return a leaf node with most common label
	if attr_index == -1:
		return TreeNode(-1, "", 0, True, mostCommonLabel(examples))

	node = TreeNode(attr_index, attrs[attr_index], attr_th, False, "")

	splitted_examples = split(examples, attr_index, attrs[attr_index], attr_th)
	for value, subset in splitted_examples.iteritems():
		if len(subset) == 0:
			print("no data in this subset. unexpected error!!!!")
			continue
		#elif maxDepth == 0: continue
		else:
			child = createSubTree(subset, attrs, maxDepth - 1)
			node.addChildNode(value, child)

	return node

# check if all the examples are labeled the same
def isAllExampleLabeledSame(examples):
	if len(examples) == 0: return True

	label = examples[0].label
	for i in xrange(len(examples)):
		if examples[i].label != label: return False
	return True

# return the most common label in the examples
def mostCommonLabel(examples):
	numPositive = 0.0
	numNegative = 0.0

	for example in examples:
		if example.label == "+":
			numPositive += example.weight
		else:
			numNegative += example.weight

	if numPositive >= numNegative: return "+"
	else: return "-"

# find the best attribute to get the highest information gain
def findBestAttribute(examples, attrs):
	e = entropy(examples)

	max_gain = 0
	attr_index = -1
	attr_th = 0

	for index, type in attrs.iteritems():
		if type == "B":
			splitted_examples = split(examples, index, type, 0)
			e2 = totalEntropy(splitted_examples)
			gain = e - e2
			if gain > max_gain:
				max_gain = gain
				attr_index = index
		else:
			thresholds = findThresholds(examples, index)
			for threshold in thresholds:
				splitted_examples = split(examples, index, type, threshold)
				e2 = totalEntropy(splitted_examples)
				gain = e - e2
				if gain > max_gain:
					max_gain = gain
					attr_index = index
					attr_th = threshold

	return attr_index, attr_th

# find the thresholds
def findThresholds(examples, attr_index):
	thresholds = []

	# extract only valid values
	examples2 = []
	for example in examples:
		if example.row[attr_index] == "?": continue
		examples2.append(example)

	if len(examples2) == 0: return thresholds

	# sort
	#rows2 = sorted(rows, key=lambda row: float(row[attr_index]))
	examples2.sort(key=lambda example: float(example.row[attr_index]))

	previous_label = examples2[0].label
	previous_value = float(examples2[0].row[attr_index])
	for example2 in examples2:
		if example2.label != previous_label:
			previous_label = example2.label
			thresholds.append((previous_value + float(example2.row[attr_index])) * 0.5)
		previous_value = float(example2.row[attr_index])

	return thresholds

# split data by a given attribute
def split(examples, attr_index, attr_type, attr_th):
	splitted_examples = {}
	total_num = 0

	if attr_type == "B":

		for example in examples:
			value = example.row[attr_index]
			if value == "?": continue
			if not value in splitted_examples:
				splitted_examples[value] = []
			splitted_examples[value].append(example)
			total_num += 1
	else:
		splitted_examples["<"] = []
		splitted_examples[">"] = []
		for example in examples:
			if example.row[attr_index] == "?": continue
			value = float(example.row[attr_index])
			if value < attr_th:
				splitted_examples["<"].append(example)
			else:
				splitted_examples[">"].append(example)
			total_num += 1

	# compute the proportion of the subsets
	proportions = {}
	for value, subset in splitted_examples.iteritems():
		proportions[value] = float(len(subset)) / float(total_num)

	# for the examples with missing values, assign to the set with probability proportional to the size of the subsets
	for example in examples:
		if value == "?":
			for value, subset in splitted_examples.iteritems():
				subset.append(Example(example.row, example.label, proportions[value]))

	return splitted_examples

# compute Entropy of all the subset
def totalEntropy(splitted_examples):
	total = 0
	total_num = 0

	for value, examples in splitted_examples.iteritems():
		num = len(examples)
		e = entropy(examples)
		total += e * num
		total_num += num

	return total / total_num

# compute Entropy for a given data set
def entropy(examples):
	if len(examples) == 0: return 0

	num_positive = 0
	num_negative = 0
	for example in examples:
		if example.label == '+':
			num_positive += 1
		else:
			num_negative += 1

	if num_positive == 0 or num_negative == 0: return 0

	p = float(num_positive) / float(num_positive + num_negative)
	n = float(num_negative) / float(num_positive + num_negative)

	return -p * math.log(p, 2) - n * math.log(n, 2)

#readfile:
#   Input: filename
#   Output: return a list of rows.
def readData(filename):
	f = open(filename).read()
	examples = []
	for line in f.split('\r'):
		row = line.split('\t')
		label = row[len(row) - 1]
		row.pop(len(row) - 1)
		examples.append(Example(row, label, 1.0))

	return examples

if __name__ == '__main__':
	DecisionTree(2)
