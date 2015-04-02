"""Example pybrain network training to predict the weather

Installation:

    pip install pug-ann

Examples:

    >>> predict_weather('San Francisco, CA', epochs=2, years=range(2010,2015), delays=[1,2], verbosity=0)  # doctest: +ELLIPSIS
    <RPropMinusTrainer 'RPropMinusTrainer-...'>
"""

from pug.ann.data import weather
from pug.ann import util

def predict_weather(
            location='Camas, WA',
            years=range(2012, 2015),
            delays=[1,2,3], 
            inputs=['Min TemperatureF', 'Max TemperatureF', 'Min Sea Level PressureIn', u'Max Sea Level PressureIn', 'WindDirDegrees'], 
            outputs=[u'Max TemperatureF'],
            epochs=30,
            verbosity=2):
    """Predict the weather for tomorrow based on the weather for the past few days

    Builds a linear single-layer neural net (multi-dimensional regression).
    The dataset is a basic SupervisedDataSet rather than a SequentialDataSet, so there may be
    "accuracy left on the table" or even "cheating" during training, because training and test
    set are selected randomly so historical data for one sample is used as target (furture data)
    for other samples.

    Uses CSVs scraped from wunderground (no api key required) to get daily weather for the years indicated.

    Arguments:
        location (str): City and state in standard US postal service format: "City, ST" or an airport code like "PDX"
        delays (list of int): sample delays to use for the input tapped delay line.
            Positive and negative values are treated the same as sample counts into the past.
            default: [1, 2, 3], in z-transform notation: z^-1 + z^-2 + z^-3
        years (int or list of int): list of 4-digit years to download weather from wunderground
        inputs (list of int or list of str): column indices or labels for the inputs
        outputs (list of int or list of str): column indices or labels for the outputs

    Returns:
        3-tuple: tuple(dataset, list of means, list of stds)
            means and stds allow normalization of new inputs and denormalization of the outputs

    """
    df = weather.daily(location, years=years, verbosity=verbosity).sort()
    ds, means, stds = util.dataset_from_dataframe(df, delays=delays, inputs=inputs, outputs=outputs, verbosity=verbosity)
    nn = util.ann_from_ds(ds, verbosity=verbosity)
    trainer = util.build_trainer(nn, ds, verbosity=verbosity)
    training_err, validation_err = trainer.trainUntilConvergence(maxEpochs=epochs, verbose=bool(verbosity))
    return trainer

# from pybrain.rl.environments.function import FunctionEnvironment

# class SupplyEnvironment(FunctionEnvironment):
#     desiredValue = 0

#     def __init__(self, *args, **kwargs):
#         FunctionEnvironment.__init__(self, *args, **kwargs)

#     def f(self, x):
#         return min(dot(x - 2.5 * ones(self.xdim), x - 2.5 * ones(self.xdim)), \
#             self.funnelDepth * self.xdim + self.funnelSize * dot(x + 2.5 * ones(self.xdim), x + 2.5 * ones(self.xdim)))


def thermostat(
    location='Camas, WA',
    days=100,
    capacity=1000,
    max_eval=1000,  
    ):
    """ Control the thermostat on an AirCon system with finite thermal energy capacity (chiller)

    Useful for controlling a chiller (something that can cool down overnight and heat up during the
    hottest part of the day (in order to cool the building).

    Builds a linear single-layer neural net (multi-dimensional regression).
    The dataset is a basic SupervisedDataSet rather than a SequentialDataSet, so there may be
    "accuracy left on the table" or even "cheating" during training, because training and test
    set are selected randomly so historical data for one sample is used as target (furture data)
    for other samples.

    Uses CSVs scraped from wunderground (no api key required) to get daily weather for the years indicated.

    Arguments:
        location (str): City and state in standard US postal service format: "City, ST" or an airport code like "PDX"
        days (int): Number of days of weather data to download from wunderground
        delays (list of int): sample delays to use for the input tapped delay line.
            Positive and negative values are treated the same as sample counts into the past.
            default: [1, 2, 3], in z-transform notation: z^-1 + z^-2 + z^-3
        years (int or list of int): list of 4-digit years to download weather from wunderground
        inputs (list of int or list of str): column indices or labels for the inputs
        outputs (list of int or list of str): column indices or labels for the outputs

    Returns:
        3-tuple: tuple(dataset, list of means, list of stds)
            means and stds allow normalization of new inputs and denormalization of the outputs

    """
    pass


from pybrain.rl.environments.cartpole.balancetask import BalanceTask
from pybrain.tools.shortcuts import buildNetwork, NetworkError
from pybrain.optimization.hillclimber import HillClimber
import time
import numpy as np

def compete_carts(builders=[], task=BalanceTask(), Optimizer=HillClimber, attempts=100, max_eval=1000, N_hidden=6, verbosity=0):
    """ pybrain buildNetwork builds a subtly different network than build_ann... so compete them!

    buildNetwork connects the bias to the output
    build_ann does not

    build_ann allows heterogeneous layer types but the output layer is always linear
    buildNetwork allows specification of the output layer type

    build_network performs better 65% of the time
    and has an average performance metric that is about 20 "points" greater (out of 2000)
    """
    results = []
    builders = list(builders) + [buildNetwork, util.build_ann]

    for attempt in range(attempts):
        heat = []

        # FIXME: shuffle the order of the builders to keep things fair 
        #        (like switching sides of the tennis court)
        for builder in builders:
            try:
                competitor = builder(task.outdim, N_hidden, task.indim, verbosity=verbosity)
            except NetworkError:
                competitor = builder(task.outdim, N_hidden, task.indim)

            # TODO: verify that a full reset is actually happening
            task.reset()
            optimizer = Optimizer(task, competitor, maxEvaluations=max_eval)
            t0 = time.time()
            nn, nn_best = optimizer.learn()
            t1 = time.time()
            heat += [(nn_best, t1-t0, nn)]
        results += [tuple(heat)]
        if verbosity >= 0:
            print([h[:2] for h in heat])


    # # alternatively:
    # agent = ( pybrain.rl.agents.OptimizationAgent(net, HillClimber())
    #             or
    #           pybrain.rl.agents.LearningAgent(net, pybrain.rl.learners.ENAC()) )
    # exp = pybrain.rl.experiments.EpisodicExperiment(task, agent).doEpisodes(100)

    print('Mean Performance:')
    for j in range(2):
        print([np.array([r[i][j] for r in results]).mean() for i in range(len(results[0]))])
    return results


def maze():
    from scipy import array
    # import sys, time
    from pybrain.rl.environments.mazes import Maze, MDPMazeTask
    from pybrain.rl.learners.valuebased import ActionValueTable
    from pybrain.rl.agents import LearningAgent
    from pybrain.rl.learners import Q # , SARSA
    from pybrain.rl.experiments import Experiment
    # from pybrain.rl.environments import Task
    import pylab
    pylab.gray()
    pylab.ion()
    # The goal appears to be in the upper right
    structure = array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 0, 0, 1, 0, 0, 0, 0, 1],
                       [1, 0, 0, 1, 0, 0, 1, 0, 1],
                       [1, 0, 0, 1, 0, 0, 1, 0, 1],
                       [1, 0, 0, 1, 0, 1, 1, 0, 1],
                       [1, 0, 0, 0, 0, 0, 1, 0, 1],
                       [1, 1, 1, 1, 1, 1, 1, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1]])
    environment = Maze(structure, (7, 7))
    controller = ActionValueTable(81, 4)
    controller.initialize(1.)
    learner = Q()
    agent = LearningAgent(controller, learner)
    task = MDPMazeTask(environment)
    experiment = Experiment(task, agent)

    for i in range(100):
        experiment.doInteractions(100)
        agent.learn()
        agent.reset()
        # 4 actions, 81 locations/states (9x9 grid)
        # max(1) gives/plots the biggest objective function value for that square
        pylab.pcolor(controller.params.reshape(81,4).max(1).reshape(9,9))
        pylab.draw()
        # pylab.show()


if __name__ == '__main__':
    print(predict_weather())