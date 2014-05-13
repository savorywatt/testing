"""
1. train

    take incoming data
    extract weights and expected class
    classify based on weights
    confirm if classifed == expected class
    if not then we adjust our weights

4. classify


2. test 3. load
"""
from random import random
from random import shuffle

MAX_EPOCHS = 10


class Perceptron(object):

    def __init__(self, weight_keys):

        self.weights = {weight_key: random()
                        for weight_key in weight_keys}
        self.threshold = random()
        #self.threshold = 0.07
        self.learning_rate = random()
        self.epochs = 0

    def update_weights(self, input_values, error):
#        print 'error in:', error
        for key, value in self.weights.iteritems():
            vector_value = input_values.get(key)

            if vector_value:
                correction = self.learning_rate * float(error) * float(vector_value)
#                print 'rate', self.learning_rate
#                print 'error:', error
#                print 'value:', value
#                print 'new value:', vector_value
#                print 'correction:', correction
#                print '++++++++++++++++++++++++++++'
                self.weights[key] = correction

    def weight_response(self, input_values):

        response = 0
        for key, value in self.weights.iteritems():

            vector_value = input_values.get(key)
            if vector_value:
                response += vector_value * value

        #print 'weight response:', response
        return response

    def response(self, input_values):
        weight_response = self.weight_response(input_values)

        if weight_response >= self.threshold:
            return 1
        return -1

    def train(self, data):
        """
        data = list of {} with each dict having a 'class' key
        """

        epochs = 0
        train_error = 0.1
        learning = True
        learned = 0
        correct = 0

        while learning:

            epoch_correct = 0
            for value in data:
                response = self.response(value)

                expected = value.get('class')
                #print 'response:', response
                #print 'expected:', expected
                #print 'value:', value
                error = expected - response
                if expected != response:
                    learned += 1
                    self.update_weights(value, error)
                    train_error += abs(error)
                else:
                    correct += 1
                    epoch_correct += 1
                #print 'current_weights:', self.weights
                #print 'error:', error

            print 'accuracy: ', str((float(epoch_correct) / float(len(data))) * 100)
            print 'cor:', epoch_correct
            print 'total:', len(data)
            epochs += 1
            print '---------------------'
            if epochs >= MAX_EPOCHS or train_error == 0.0:
                learning = False
        print 'train:correctly guessed:', correct
        self.epochs = epochs

        print 'data learned on:', len(data)
        print 'made %d mistakes' % learned

    def test(self, data):

        total = len(data)
        correct = 0
        incorrect = 0

        for datum in data:

            response = self.response(datum)

            expected = datum.get('class')

            if expected != response:
                incorrect += 1
            else:
                correct += 1

        print 'correct:', correct
        self.accuracy = (float(correct) / float(total)) * 100
        print 'accuracy: ', self.accuracy
        print 'trained in %d epochs' % self.epochs
        print 'threshold:', self.threshold


def generate_test_data(features=None, num=10):
    """ assumes even amounts of data, divisible by 2
    """

    if not features:
        features = ['a', 'b', 'c']

    desired_data = xrange(num)
    data = []

    cutoff = num / 2
    variance = -0.5
    target = 1

    for i, desired in enumerate(desired_data):
        if i > cutoff:
            variance = 0.5
            target = -1

        datum = {feature: random() * 2 - 1 / 2 + variance
                 for feature in features}

        datum['class'] = target

        data.append(datum)

    return data


def test_random(num):

    features = ['a', 'b', 'c']

    train_data = generate_test_data(features, num)
    test_data = generate_test_data(features, int(num * 0.9))

    test(features, train_data, test_data)


def test(features, train_data, test_data):

    perceptron = Perceptron(features)
    print 'start weights:', perceptron.weights
    perceptron.train(train_data)
    print 'trained weights:', perceptron.weights
    perceptron.test(test_data)

    return perceptron


def test_vote():

    file_name = 'house-votes-84.data.txt'

    data = []
    features = []

    with open(file_name) as raw_data:

        for line in raw_data:

            values = line.split(',')

            target = values[0]
            classed = 1
            if 'republican' in target:
                classed = -1

            values.remove(target)

            datum = {'class': classed}
            features = []

            for i, value in enumerate(values):
                features.append(i)

                if '?' not in value:

                    if 'y' in value:
                        value = 1

                    if value != 1 and 'n' in value:
                        value = int(-1)

                    datum[i] = value

            data.append(datum)
    shuffle(data)
    print 'data sample is:', len(data)
    offset = len(data) - int(len(data) * 0.9)
    print 'offset:', offset
    train_data = data[:len(data) - offset]
    test_data = data[len(data) - offset:]

    #train_data = data[:10]
    #test_data = data[11:21]

    print 'training %d votes, testing %d votes' % (len(train_data), len(test_data))
    best = None
    best_accuracy = 0.0
    accuracies = []
    for x in xrange(10):
        trial = test(features, train_data, shuffle(train_data))
        best_accuracy = max(trial.accuracy, best_accuracy)

        if trial.accuracy == best_accuracy:
            best = trial

        accuracies.append(trial.accuracy)

    best.test(test_data)

    print 'accuracies:', accuracies
