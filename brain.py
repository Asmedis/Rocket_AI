import random

DEFAULT_NEURON_LINKS = 8
MAX_THINKING_STEPS = 3
RADATION = 10

class neuron:
    def __init__(self):
        self.value = random.randint(0,100)
        self.links = []
        self.weights = []

class brain:
    def __init__(self, neuron_amount=400):
        self.neurons = []
        self.neuron_amount = 100
        for x in range(neuron_amount):
            new_neuron = neuron()
            self.neurons.append(new_neuron)

        for n in self.neurons:
            for x in range(DEFAULT_NEURON_LINKS):
                n.links.append(random.randint(0, neuron_amount - 1))
                n.weights.append((random.random()*2) - 1)

    def think(self, inputs, outputs):
        # 1 Neuron > 50: end thinking cycle
        # 2 - (input amount) Input neurons
        # (input amount) - (output_amount) Neurons - output neurons
        steps = 0
        for i in range(len(inputs)):
            self.neurons[i+1].value = inputs[i]

        while steps < MAX_THINKING_STEPS:
            for n in self.neurons:
                #print(len(n.links))
                #for aaa in range(len(n.links)):
                #    print(n.links[aaa], " ")
                for x in range(len(n.links)):
                    self.neurons[n.links[x]].value += n.value * n.weights[x]   #note: should calculate to a new network, because newer calculations influence future one's
            
            for n in self.neurons:
                if n.value > 100:
                    n.value = 100
                elif n.value < 0:
                    n.value = 0


            if(self.neurons[0].value > 50):
                out = []
                for o in range(outputs):
                    out.append(self.neurons[len(inputs)+ 1 + o].value)
                return out
            
            steps += 1

        out = []
        for o in range(outputs):
            out.append(self.neurons[len(inputs)+ 1 + o].value)
        return out
    
    def mutate(self):
        #mutate current genes
        for neuron in self.neurons:
            #mutate gene
            if random.random()*100 <= RADATION:                  #RADIARION neurons will be affected
                for link in range(len(neuron.links)):                           
                    if random.random() > 0.5:                    #50% links will mutate
                        if random.random()*100 <= RADATION:      #RADIATION links will be deleted or new one created
                            if random.random() > 0.5:            #50% deleted
                                if len(neuron.links) > 1:
                                    del neuron.links[link]
                                    del neuron.weights[link]
                                    return
                            else:
                                neuron.links.append(random.randint(0, self.neuron_amount - 1))
                                neuron.weights.append((random.random()*2) - 1)
                                return
                        else:
                            neuron.weights[link] += (random.random() - 0.5)/100 * RADATION
                    else:
                        pass
                                                                




