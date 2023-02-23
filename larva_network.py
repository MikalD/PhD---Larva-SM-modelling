import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from brian2 import *

start_scope()
num_inputs_LNa = 112
num_inputs_LNb = 42
num_inputs_B1 = 60
num_inputs_B2 = 17
input_rate_LNa = 30*Hz
input_rate_LNb = 30*Hz
input_rate_B1 = 20*Hz
input_rate_B2 = 20*Hz
weight_LNa = 0.2
weight_LNb = 0.2
weight_B1 = 0.2
weight_B2 = 0.2
tau = 10*ms
output_rates_1 = []
output_rates_2 = []
output_rates_3 = []
output_rates_4 = []
defaultclock.dt = 0.01*ms
sim_duration = 0.001*second


# Construct the network
stim_times = zeros((round(float(sim_duration/defaultclock.dt)),2))
stim_times[:int(len(stim_times)/4), 0], stim_times[int(0.5*len(stim_times)):int(0.75*len(stim_times)), 0] = 100, 100
stim_times[:int(len(stim_times)/4), 1], stim_times[int(0.5*len(stim_times)):int(0.75*len(stim_times)), 1] = 1000, 1000
#print(stim_times[:int(len(stim_times)/4)+10, :])
stimulus = TimedArray(stim_times, dt=defaultclock.dt)

eqs_stim = '''
dv/dt = (I1+I2-v)/tau : 1
I1 = stimulus(t, i) : 1
I2 : 1
'''
eqs = '''
dv/dt = (I-v)/tau : 1
I = 0 : 1
'''

G1 = NeuronGroup(2, eqs_stim, threshold='v>1', reset = 'v = 0', method='exact')
G2 = NeuronGroup(2, eqs, threshold='v>1', reset='v=0', method='exact')
#P1 = PoissonInput(G1[0], 'I2', 50, 20*Hz, 0.2)
#P2 = PoissonInput(G1[1], 'I2', 50, 20*Hz, 0.2)
#P3 = PoissonInput(G2[0], 'I', 50, 20*Hz, 0.2)
#P4 = PoissonInput(G2[1], 'I', 50, 20*Hz, 0.2)

S5 = Synapses(G1, G1, on_pre = "v -= 3")
S5.connect(i=[0,1], j=[1,0])
S6 = Synapses(G1, G2, on_pre = "v -= 3")
S6.connect(i=[0,0], j=[0,1])
S6.connect(i=[1,1], j=[0,1])


LN = SpikeMonitor(G1)
Basin = SpikeMonitor(G2)
statemonLNa = StateMonitor(G1, variables = True, record=0)
statemonLNb = StateMonitor(G1, 'v', record=1)
statemonbasin1 = StateMonitor(G2, 'v', record=0)
statemonbasin2 = StateMonitor(G2, 'v', record=1)

# Store the current state of the network
store()

#run
run(sim_duration)


rows = ["Lateral neuron a","Lateral neuron b", "basin1", "basin2", "stimulation current"]
cols = ["skyblue", "royalblue", "darkorange", "burlywood", "black"]
vas=[statemonLNa.v[0], statemonLNb.v[0], statemonbasin1.v[0], statemonbasin2.v[0], statemonLNa.I1[0]]

fig, axs = plt.subplots(5, sharex=True)


for ax, row in zip(axs, rows):
    ax.annotate(row, xy=(0.5, 1), xytext=(0, 5),
                xycoords='axes fraction', textcoords='offset points',
                size='large', ha='center', va='baseline')


for ax,var, col in zip(axs, vas, cols):
	ax.plot(statemonLNa.t/ms, var, c=col)

plt.rc('font', size=10)


fig.savefig('statemon.png', dpi=300)
plt.close()
fig.clear()
