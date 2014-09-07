import math
import copy

# Example
class Example:
	def __init__(self, rows, label, weight):
		self.rows = rows
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

		print(" " * indent + "Attribute: " + str(self.attr_index))
		if self.attr_type == "C":
			print(" " * indent + "threshold: " + str(self.attr_th))
		for value, childNode in self.childNodes.iteritems():
			print(" " * (indent + 4) + "[value: " + str(value) + "]")
			childNode.display(indent + 4)

	def predict(self, row):
		if self.isLeaf == True:
			return self.label
		elif self.attr_type == "B":
			return self.childNodes[row[self.attr_index]].predict(row)
		else:
			if float(row[self.attr_index]) < self.attr_th:
				return self.childNodes["<"].predict(row)
			else:
				return self.childNodes[">"].predict(row)

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

	# read test data
	rows = readfile("train.txt")

	rootNode = createSubTree(rows, attrs, maxDepth)
	rootNode.display(0)

	labels = []
	numCorrect = 0
	for i in xrange(len(rows)):
		label = rootNode.predict(rows[i])
		if rows[i][15] == label:
			numCorrect += 1
		labels.append(label)

	print(labels)
	print("Accuracy: " + str(float(numCorrect) / float(len(rows))))

	return

# create subtree of the decision tree
def createSubTree(rows, attrs, maxDepth):
	attr_index, attr_th = findBestAttribute(rows, attrs)
	if attr_index == -1:
		print("Unexpected error!!!!")
		return TreeNode(-1, "", 0, True, "?")

	node = TreeNode(attr_index, attrs[attr_index], attr_th, False, "")

	splitted_rows = split(rows, attr_index, attrs[attr_index], attr_th)
	for value, subset in splitted_rows.iteritems():
		if len(subset) == 0: continue
		#elif maxDepth == 0: continue
		elif entropy(subset) == 0:
			label_index = len(subset[0]) - 1
			child = TreeNode(-1, "", 0, True, subset[0][label_index])
			node.addChildNode(value, child)
		else:
			child = createSubTree(subset, attrs, maxDepth - 1)
			node.addChildNode(value, child)

	return node

# find the best attribute to get the highest information gain
def findBestAttribute(rows, attrs):
	e = entropy(rows)

	max_gain = 0
	attr_index = -1
	attr_th = 0

	for index, type in attrs.iteritems():
		if type == "B":
			splitted_rows = split(rows, index, type, 0)
			e2 = totalEntropy(splitted_rows)
			gain = e - e2
			if gain > max_gain:
				max_gain = gain
				attr_index = index
		else:
			thresholds = findThreshold(rows, index)
			for i in xrange(len(thresholds)):
				splitted_rows = split(rows, index, type, thresholds[i])
				e2 = totalEntropy(splitted_rows)
				gain = e - e2
				if gain > max_gain:
					max_gain = gain
					attr_index = index
					attr_th = thresholds[i]

	return attr_index, attr_th

# find the threshold
def findThreshold(rows, attr_index):
	thresholds = []

	if len(rows) == 0: return thresholds

	label_index = len(rows[0]) - 1

	# extract only valid values
	rows2 = []
	for i in xrange(len(rows)):
		if rows[i][attr_index] == "?": continue
		rows2.append(rows[i])

	# sort
	#rows2 = sorted(rows, key=lambda row: float(row[attr_index]))
	rows2.sort(key=lambda row: float(row[attr_index]))

	previous_label = rows2[0][label_index]
	previous_value = float(rows2[0][attr_index])
	for i in xrange(len(rows2)):
		if rows2[i][label_index] != previous_label:
			previous_label = rows2[i][label_index]
			thresholds.append((previous_value + float(rows2[i][attr_index])) * 0.5)
		previous_value = float(rows2[i][attr_index])

	return thresholds

# split data by a given attribute
def split(rows, attr_index, attr_type, attr_th):
	splitted_rows = {}
	if attr_type == "B":
		for i in xrange(len(rows)):
			value = rows[i][attr_index]
			if not value in splitted_rows:
				splitted_rows[value] = []
			splitted_rows[value].append(rows[i])
	else:
		splitted_rows["<"] = []
		splitted_rows[">"] = []
		for i in xrange(len(rows)):
			value = float(rows[i][attr_index])
			if value < attr_th:
				splitted_rows["<"].append(rows[i])
			else:
				splitted_rows[">"].append(rows[i])

	return splitted_rows

# compute Entropy of all the subset
def totalEntropy(splitted_rows):
	total = 0
	total_num = 0
	keys = splitted_rows.keys()

	for i in xrange(len(keys)):
		num = len(splitted_rows[keys[i]])
		e = entropy(splitted_rows[keys[i]])
		total += e * num
		total_num += num

	return total / total_num

# compute Entropy for a given data set
def entropy(rows):
	if len(rows) == 0: return 0

	label_index = len(rows[0]) - 1

	num_positive = 0
	num_negative = 0
	for i in xrange(len(rows)):
		if rows[i][label_index] == '+':
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
def readfile(filename):
    f = open(filename).read()
    rows = []
    for line in f.split('\r'): # for mac, we use \r
        rows.append(line.split('\t'));

    return rows


if __name__ == '__main__':

	DecisionTree(10)