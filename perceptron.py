from random import random
from random import shuffle

MAX_EPOCHS = 10


class Perceptron(object):

    def __init__(self, weight_keys):

        self.weights = {weight_key: random()
                        for weight_key in weight_keys}
        self.threshold = random()
        self.learning_rate = random()
        self.epochs = 0

    def update_weights(self, features, error):
        """Update weights for the incoming features based on error"""

        for key, value in self.weights.iteritems():
            vector_value = features.get(key)

            if vector_value:
                correction = (self.learning_rate * error * float(vector_value))
                self.weights[key] = correction

    def score(self, features):
        """Based on passed in features find the dot product of any matching
        features.
        """

        response = 0
        for key, value in self.weights.iteritems():

            vector_value = features.get(key)
            if vector_value:
                response += vector_value * value

        return response

    def classify(self, features):
        """Classify using the score and threshold."""

        score = self.score(features)

        if score >= self.threshold:
            return 1
        return -1

    def train(self, data):
        """Based on the data learn the features by adjusting weights when
        the perceptron incorrectly classifies a peice of training data.
        """

        epochs = 0
        train_error = 0.1
        learning = True
        learned = 0
        correct = 0

        while learning:

            epoch_correct = 0
            for features in data:
                response = self.classify(features)

                expected = features.get('class')

                error = float(expected - response)
                if expected != response:
                    learned += 1
                    self.update_weights(features, error)
                    train_error += abs(error)
                else:
                    correct += 1
                    epoch_correct += 1

            epochs += 1

            if epochs >= MAX_EPOCHS or train_error == 0.0:
                learning = False
        self.epochs = epochs

    def test(self, data):
        """Used to report and record statistics for how accurate the perceptron
        was at classifying the new data set.
        """

        total = len(data)
        correct = 0
        incorrect = 0

        for datum in data:

            response = self.classify(datum)

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
    perceptron.train(train_data)
    perceptron.test(test_data)

    return perceptron


def parse_vote_file():
    """Read the csv file and turn it into weights and appropriate tags"""

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

    return data, features


def test_vote():
    """Test the vote data using multiple trials to try and find the 'best'
    perceptron to test with."""

    data, features = parse_vote_file()

    #shuffle(data)

    offset = len(data) - int(len(data) * 0.9)
    train_data = data[:len(data) - offset]
    test_data = data[len(data) - offset:]

    print 'training %d testing %d' % (len(train_data), len(test_data))

    best = None
    best_accuracy = 0.0
    accuracies = []
    for x in xrange(10):
        train_test = train_data
        shuffle(train_test)
        trial = test(features, train_data, train_data)
        best_accuracy = max(trial.accuracy, best_accuracy)

        if trial.accuracy == best_accuracy:
            best = trial

        accuracies.append(trial.accuracy)
    print '-----------------------------------------------------'
    print 'final against real test data'
    best.test(test_data)

    # This is to look at overfitting and to eventually see if a highly accurate
    # trained perceptron does the best on the tests
    print 'accuracies:', accuracies
