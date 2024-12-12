import random

# Constants
DEFAULT_NEURON_LINKS = 5
MAX_THINKING_STEPS = 3
RADIATION = 10

class Neuron:
    def __init__(self):
        self.value = random.randint(0, 100)
        self.links = []
        self.weights = []

class Brain:
    def __init__(self, neuron_amount=600):
        self.neurons = [Neuron() for _ in range(neuron_amount)]
        self.neuron_amount = neuron_amount

        # Initialize neuron links and weights
        for neuron in self.neurons:
            for _ in range(DEFAULT_NEURON_LINKS):
                neuron.links.append(random.randint(0, neuron_amount - 1))
                neuron.weights.append((random.random() * 2) - 1)

    def think(self, inputs, outputs):
        steps = 0

        # Set input neuron values
        for i, input_value in enumerate(inputs):
            self.neurons[i + 1].value = input_value

        while steps < MAX_THINKING_STEPS:
            new_values = [0] * self.neuron_amount

            # Calculate new values for each neuron
            for neuron in self.neurons:
                for link, weight in zip(neuron.links, neuron.weights):
                    new_values[link] += neuron.value * weight

            # Update neuron values and clamp between 0 and 100
            for i, neuron in enumerate(self.neurons):
                neuron.value = min(max(new_values[i], 0), 100)

            # Check if the first neuron value exceeds 50
            if self.neurons[0].value > 50:
                return [self.neurons[len(inputs) + 1 + o].value for o in range(outputs)]

            steps += 1

        # Return output neuron values after max steps
        return [self.neurons[len(inputs) + 1 + o].value for o in range(outputs)]

    def mutate(self):
        for neuron in self.neurons:
            if random.random() * 100 <= RADIATION:
                for link_index in range(len(neuron.links)):
                    if random.random() > 0.5:
                        if random.random() * 100 <= RADIATION:
                            if random.random() > 0.5:
                                if len(neuron.links) > 1:
                                    del neuron.links[link_index]
                                    del neuron.weights[link_index]
                                    return
                            else:
                                neuron.links.append(random.randint(0, self.neuron_amount - 1))
                                neuron.weights.append((random.random() * 2) - 1)
                                return
                        else:
                            neuron.weights[link_index] += (random.random() - 0.5) / 100 * RADIATION
