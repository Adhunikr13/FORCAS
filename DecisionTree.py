import math

values = [
		['sunny', 'rainy', 'overcast'],
		['hot', 'mild', 'cool'],
		['high', 'normal'],
		['TRUE', 'FALSE'],
		['yes', 'no']
	]

class DecisionTree(object):


	def __init__(self, attributes):
		self.attributes = attributes
		self.children = []

	def find_entropy_1(self, dataset, attribute_number):
		counts = [0 for i in range(len(values[attribute_number]))]
		for row in dataset:
			for i in range(len(values[attribute_number])):
				if row[attribute_number] == values[attribute_number][i]:
					counts[i] += 1
		probabilities = [x / sum(counts) for x in counts]
		entropy = 0
		for prob in probabilities:
			if (prob != 0):
				entropy += prob * (math.log(prob) / math.log(2))
		return -entropy
		
	def find_entropy(self, dataset, attrib1, attrib2):
		entropy = 0
		child_datasets = self.split(dataset,attrib2)
		for child_attrib_dataset in child_datasets:
			child_prob = len(child_attrib_dataset) / len(dataset)
			child_entropy = child_prob
			if (child_prob != 0): 
				child_entropy *= self.find_entropy_1(child_attrib_dataset, attrib1)
			entropy += child_entropy
		return entropy

	def find_information_gain(self, dataset, attrib1, attrib2):
		return self.find_entropy_1(dataset, attrib1) - self.find_entropy(dataset, attrib1, attrib2)

	
	def train(self, dataset, csf_attribute):
		if (self.find_entropy_1(dataset, csf_attribute) == 0):
			self.value = dataset[0][csf_attribute]
			return self
		largest_information_gain = 0
		splitting_attribute = 0
		for attribute_number in range(len(self.attributes)):
			if (attribute_number != csf_attribute):
				information_gain = self.find_information_gain(dataset, csf_attribute, attribute_number)
				if (information_gain > largest_information_gain):
					largest_information_gain = information_gain
					splitting_attribute = attribute_number
		self.splitting_attribute = splitting_attribute
		#print(str(dataset) + str(splitting_attribute))
		child_datasets_list = self.split(dataset, splitting_attribute)
		for child_dataset in child_datasets_list:
			child = DecisionTree(self.attributes).train(child_dataset, csf_attribute)
			self.children.append(child)
		return self


	def split(self,dataset,attribute_number):
		child_datasets = [[] for x in range(len(values[attribute_number]))]
		for row in dataset:
			for value_number in range(len(values[attribute_number])):
				if (row[attribute_number] == values[attribute_number][value_number]):
					child_datasets[value_number].append(row)
		return child_datasets

	def classify(self,row):
		if (len(self.children) == 0):
			return self.value
		for value_number in range(len(values[self.splitting_attribute])):
			if(row[self.splitting_attribute] == values[self.splitting_attribute][value_number]):
				return self.children[value_number].classify(row)




file = open("weather.csv","r")
attrib = file.readline().split(',')
dataset = []
for line in file:
	dataset.append(line.strip().split(','))
decisionTree = DecisionTree(attrib)
decisionTree = decisionTree.train(dataset, 4)
print(decisionTree.classify(['sunny', 'mild', 'high', 'TRUE']))

