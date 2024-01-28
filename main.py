import random
import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt6.QtWidgets import QApplication

from Window import Window


def normalize(vector):
    return vector / np.linalg.norm(vector)


def plot(data, weights, learning_rate):
    plt.scatter(data[:, 0], data[:, 1], c='blue', label='Data')

    for w in weights:
        plt.quiver(0, 0, w[0], w[1], angles='xy', scale_units='xy', scale=1, color='red', width=0.01)

    plt.xlabel('Attribute 1')
    plt.ylabel('Attribute 2')
    plt.title(f"Learning rate is: {learning_rate}")
    plt.legend()
    plt.show()


def kohonen(num_epochs, data, weights, learning_rate, learning_rate_step):
    for epoch in range(num_epochs):
        for input_vector in data:
            distances = np.linalg.norm(weights - input_vector, axis=1)
            winner_index = np.argmin(distances)
            weights[winner_index] += learning_rate * (input_vector - weights[winner_index])
            #weights[winner_index] = normalize(weights[winner_index])
        learning_rate *= learning_rate_step


def parse_file(file):
    with open(file, 'r') as file:
        file_content = file.read()
    return file_content


def get_factor(data):
    min_norm = 0
    for d in data:
        norm = np.linalg.norm(d)
        print(norm)
        if norm > min_norm:
            min_norm = norm
    return min_norm


def normalize_data(data, min_norm):
    return data / min_norm


def denormalize(data, factor):
    return data * factor


def calculate(learning_rate_in, learning_rate_step_in, file, epochs, outputs):
    data_str = parse_file(file)
    data = np.array([list(map(int, line.split())) for line in data_str.split('\n') if line])

    min_norm = get_factor(data)
    temp_data = data
    data = normalize_data(data, min_norm)

    input_size = 2
    output_size = outputs

    if learning_rate_in == 0:
        learning_rate = round(random.uniform(0.3, 0.7), 1)
    else:
        learning_rate = learning_rate_in
    print(f"learning rate is {learning_rate}")

    weights = np.random.rand(output_size, input_size)

    for i in range(output_size):
        weights[i] = normalize(weights[i])

    kohonen(epochs, data, weights, learning_rate, learning_rate_step_in)

    print(weights)
    print("----------------")
    weights = denormalize(weights, min_norm)
    print(weights)
    plot(temp_data, weights, learning_rate)


def main():
    app = QApplication(sys.argv)

    window = Window()
    window.calculate.connect(calculate)
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
