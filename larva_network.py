import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from brian2 import *

start_scope()
num_inputs_LN = 100
num_inputs_B1 = 100
num_inputs_B2 = 20
input_rate_LNa = 50*Hz
input_rate_LNb = 50*Hz
input_rate_B1 = 20*Hz
input_rate_B2 = 20*Hz
weight_LNa = 0.6
weight_LNb = 0.6
weight_B1 = 0.6
weight_B2 = 0.25
tau = 100*ms
output_rates_1 = []
output_rates_2 = []
output_rates_3 = []
output_rates_4 = []
time=range(1000)

# Construct the network just once
PLNa = PoissonGroup(num_inputs_LN, rates=input_rate_LNa)
PLNb = PoissonGroup(num_inputs_LN, rates=input_rate_LNb)
PB1 = PoissonGroup(num_inputs_B1, rates=input_rate_B1)
PB2 = PoissonGroup(num_inputs_B2, rates=input_rate_B2)
eqs = '''
dv/dt = -v/tau : 1
'''
G1 = NeuronGroup(2, eqs, threshold='v>1', reset='v=0', method='exact')
G2 = NeuronGroup(2, eqs, threshold='v>1', reset='v=0', method='exact')
S1 = Synapses(PLNa, G1, on_pre='v += weight_LNa')
S1.connect(condition='j!=1')
S2 = Synapses(PB1, G1, on_pre='v += weight_B1')
S2.connect(condition='j!=0')
S3 = Synapses(PLNb, G2, on_pre='v += weight_LNb')
S3.connect(condition='j!=1')
S4 = Synapses(PB2, G2, on_pre='v += weight_B2')
S4.connect(condition='j!=0')
S5 = Synapses(G1, G2, on_pre = "v -= 0.5")
S5.connect(i=[0,0], j=[0,1])
S6 = Synapses(G2, G1, on_pre = "v -= 0.5")
S6.connect(i=[0,0], j=[0,1])



LN = SpikeMonitor(G1)
Basin = SpikeMonitor(G2)
statemonLNa = StateMonitor(G1, 'v', record=0)
statemonLNb = StateMonitor(G2, 'v', record=0)
statemonbasin1 = StateMonitor(G1, 'v', record=1)
statemonbasin2 = StateMonitor(G2, 'v', record=1)

# Store the current state of the network
store()

#for i in t:
run(1*second)
LNa=LN.t[where(LN.i==0)[0]]
LNb=LN.t[where(LN.i==1)[0]]
Basin1=Basin.t[where(Basin.i==0)[0]]
Basin2=Basin.t[where(Basin.i==1)[0]]
print(LN.t[where(LN.i==0)[0]][:10])
print(LN.t[where(LN.i==1)[0]][:10])
print(Basin.t[where(Basin.i==1)[0]][:10])
print(Basin.t[where(Basin.i==0)[0]][:10])
for i in time:
    output_rates_1.append(where((LNa>=i*ms) & (LNa<(i+1)*ms))[0].size)
    output_rates_2.append(where((LNb>=i*ms) & (LNb<(i+1)*ms))[0].size)
    output_rates_3.append(where((Basin1>=i*ms) & (Basin1<(i+1)*ms))[0].size)
    output_rates_4.append(where((Basin2>=i*ms) & (Basin2<(i+1)*ms))[0].size)


rows = ["firing rate for Lateral neuron a","firing rate for Lateral neuron b", "firing rate for Basin1","firing rate for Basin2"]
cols = ["skyblue", "royalblue", "darkorange", "burlywood"]
vas=[output_rates_1, output_rates_2, output_rates_3, output_rates_4]

fig, axs = plt.subplots(4, sharex=True)


for ax, row in zip(axs, rows):
    ax.annotate(row, xy=(0.5, 1), xytext=(0, 5),
                xycoords='axes fraction', textcoords='offset points',
                size='large', ha='center', va='baseline')


for ax,var, col in zip(axs, vas, cols):
	ax.plot(time, var, c=col)

plt.rc('font', size=10)


fig.savefig('firing_rates.png', dpi=300)
plt.close()
fig.clear()

rows = ["Lateral neuron a","Lateral neuron b", "basin1", "basin2"]
cols = ["skyblue", "royalblue", "darkorange", "burlywood"]
vas=[statemonLNa.v[0], statemonLNb.v[0], statemonbasin1.v[0], statemonbasin2.v[0]]

fig, axs = plt.subplots(4, sharex=True)


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
