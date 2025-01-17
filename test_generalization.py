import torch
import numpy as np
# import data.load_data as load_data
from scipy.optimize import minimize, NonlinearConstraint
import multiprocessing
import scipy.io as io
import argparse
import os

import models.rnn as rnn
import models.lstm as lstm
import models.RobustRnn as RobustRnn
import models.ciRNN as ciRNN
import models.dnb as dnb

import data.n_linked_msd as msd

torch.set_default_dtype(torch.float64)
torch.set_printoptions(precision=4)
multiprocessing.set_start_method('spawn', True)


def test_performance(model, period, sd, samples=100, sim_len=1000, wash_per=200):
    model.eval()
    sim = msd.msd_chain(N=4, T=sim_len, u_sd=sd, period=period, Ts=0.5, batchsize=samples)
    loader = sim.sim_rand_ic(sim_len, samples, mini_batch_size=samples)

    for idx, U, Y in loader:
        with torch.no_grad():
            Yest = model(U)
            SE = (Y[:, :, wash_per:] - Yest[:, :, wash_per:]).norm(dim=(1, 2)).detach()
            NSE = ((Y[:, :, wash_per:] - Yest[:, :, wash_per:]).norm(dim=(1, 2)) / Y[:, :, wash_per:].norm(dim=(1, 2))).detach()

    res = {"NSE": NSE, "SE": SE}
    return res

if __name__ == "__main__":

    N = 4

    train_seq_len = 1000
    training_batches = 100
    mini_batch_size = 1

    nu = 1
    ny = 1
    width = 10
    batches = training_batches

    path = './results/msd/'

    if not os.path.exists(path + 'lip/'):
        os.mkdir(path + 'lip/')
        os.mkdir(path + 'wcg/')
        os.mkdir(path + 'wcp/')
        print("Directory ", path, "lip/ Created")

    def vary_amplitude(model):
        print("\t Testing amplitude")
        samples = 300
        test_points = 21
        period = 100

        NSE_dist = np.zeros((test_points, samples))
        SE_dist = np.zeros((test_points, samples))
        amps = np.linspace(0.5, 10.5, test_points)

        for idx in range(test_points):
            res = test_performance(model, period, amps[idx], samples=samples)
            NSE_dist[idx, :] = res["NSE"]
            SE_dist[idx, :] = res["SE"]

        return {"amps": amps, "NSE": NSE_dist, "SE": SE_dist, "period": period}

    # Test generalization of Robust RNNs
    print("Running tests on robust-RNN")
    name = 'iqc-rnn_w10_gamma0.0_n4'
    model = RobustRnn.RobustRnn(nu, width, ny, width, nBatches=batches, method='Neuron')
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    name = 'iqc-rnn_w10_gamma3.0_n4'
    model = RobustRnn.RobustRnn(nu, width, ny, width, nBatches=batches, method='Neuron')
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    name = 'iqc-rnn_w10_gamma5.0_n4'
    model = RobustRnn.RobustRnn(nu, width, ny, width, nBatches=batches, method='Neuron')
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    name = 'iqc-rnn_w10_gamma8.0_n4'
    model = RobustRnn.RobustRnn(nu, width, ny, width, nBatches=batches, method='Neuron')
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    name = 'iqc-rnn_w10_gamma10.0_n4'
    model = RobustRnn.RobustRnn(nu, width, ny, width, nBatches=batches, method='Neuron')
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    name = 'iqc-rnn_w10_gamma15.0_n4'
    model = RobustRnn.RobustRnn(nu, width, ny, width, nBatches=batches, method='Neuron')
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    # # lstm
    print("Running tests on LSTM")
    name = 'lstm_w10_gamma0.0_n4'
    model = lstm.lstm(nu, width, ny, layers=1, nBatches=batches)
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    # rnn
    print("Running tests on RNN")
    name = 'rnn_w10_gamma0.0_n4'
    model = rnn.rnn(nu, width, ny, 1, nBatches=batches)
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    # cirnn
    print("Running tests on cirnn")
    name = 'cirnn_w10_gamma0.0_n4'
    model = ciRNN.ciRNN(nu, width, ny, 1, nBatches=100)
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)

    # srnn
    print("Running tests on srnn")
    name = 'dnb_w10_gamma0.0_n4'
    model = dnb.dnbRNN(nu, width, ny, layers=1, nBatches=batches)
    model.load_state_dict(torch.load(path + name + ".params"))
    res = vary_amplitude(model)
    io.savemat('./results/msd/generalization/amp_' + name + '.mat', res)
