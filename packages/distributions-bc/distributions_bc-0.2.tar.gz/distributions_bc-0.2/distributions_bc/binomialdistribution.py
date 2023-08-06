import matplotlib.pyplot as plt
import math
from .generaldistribution import Distribution


# Type autopep8 -i binomialdistribution.py in terminal to prevent formatting errors

class Binomial(Distribution):

    def __init__(self, prob=0.5, n_trials=10):
        self.n = n_trials
        self.k = 0
        self.p = prob

        Distribution.__init__(self, self.calculate_mean(),
                              self.calculate_stdev())

    def calculate_length(self):
        """Function to calculate n from the dataset. Updates the value of n

        Args:
            None

        Returns:
            float: the n value

        """

        self.n = len(self.data)

        return self.n

    def calculate_successes(self):
        """Function to calculate k from self.n and self.p. Updates the value of k

        Args:
            None

        Returns:
            float: the n value

        """

        self.k = math.fsum(self.data)

        return self.k

    def calculate_probability(self):
        """Function to calculate p from the dataset. Updates the value of p

        Args:
            None

        Returns:
            float: the p value

        """

        self.p = self.k / self.n

        return self.p

    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """

        self.mean = self.n * self.p

        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """
        self.stdev = math.sqrt((self.p * (1 - self.p)) * self.n)

        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.

        Args:
            None

        Returns:
            float: the p value
            float: the n value

        """

        self.n = self.calculate_length()
        self.k = self.calculate_successes()
        self.p = self.calculate_probability()
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n

        # Exercise doesn't want read_data method to update

    def read_data_file(self, file_name):
        with open(file_name) as file:
            data_list = []
            for line in file:
                data_list.append(float(line))
        file.close()

        self.data = data_list
        self.replace_stats_with_data()

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """

        plt.bar(x=['0', '1'], height=[(1 - self.p) * self.n, self.p * self.n])
        plt.title("Barchart of Data")
        plt.xlabel('Outcome')
        plt.ylabel('Count')

        plt.show()

    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """

        factorial = math.factorial(
            self.n) / (math.factorial(self.n - k) * math.factorial(k))
        probability = self.p**k * (1 - self.p)**(self.n - k)

        return factorial * probability

    def plot_bar_pdf(self, nspaces=50):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        x, y = [], []

        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        fig, axes = plt.subplots(nrows=2, ncols=1)

        axes[0].bar(x=['0', '1'], height=[
                    (1 - self.p) * self.n, self.p * self.n])
        axes[0].set_ylabel('Count')
        axes[0].set_xlabel('Outcome')
        axes[0].set_title('Barchart of Data')

        axes[1].bar(x, y)
        axes[1].set_ylabel('Probability')
        axes[1].set_title(
            'Binomial Distribution of Outcomes with n = {} and p = {}'.format(self.n, round(self.p, 2)))
        axes[1].set_xlabel('Outcome')

        plt.tight_layout()
        plt.show()

        return x, y

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        result.calculate_mean()
        result.calculate_stdev()

        return result

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Binomial object

        """
        return "mean = {}, standard deviation = {}, p = {}, n = {}, k = {}".format(self.mean, self.stdev, self.p, self.n, self.k)
