from scipy.integrate import odeint
import numpy as np
import matplotlib
matplotlib.use('Agg')
import numpy as np
#%matplotlib inline

import matplotlib.pyplot as plt
# Définition des paramètres du système
w_LNb_LNa = -0.35
w_LNa_LNb = -0.35
w_LNb_B1 = -1.03
w_LNa_B2 = -1.03
rho=1
## For basal activity : w_LNb_LNa = -0.4, w_LNa_LNb = -0.35, w_LNb_B1 = -1.3, w_LNa_B2 = -1.1

# Définition des conditions initiales
densityLNa_0 = 0.740741040045
densityLNb_0 = 0.740740441828
densityBasin1_0 = 0.236995038524
densityBasin2_0 = 0.236945892453
## For basal activity : densityLNa_0 = 69, densityLNb_0 = 73, densityBasin1_0 = 0.001, densityBasin2_0 =  0.2325

## Définition du système d'équation différentielle


def systeme(Y, t, lbd, w_LNb_LNa, w_LNa_LNb, w_LNb_B1, w_LNa_B2, I1, I2, I3, I4):
    densityLNa = Y[0]
    densityLNb = Y[1]
    densityBasin1 = Y[2]
    densityBasin2 = Y[3]

    # Competition entre LNs
    ddensityLNa_dt = densityLNa*(1-densityLNa + densityLNb*w_LNb_LNa) + I1
    ddensityLNb_dt = lbd*densityLNb*(1-densityLNb + densityLNa*w_LNa_LNb) +I2
   
    # Amensalisme entre LNs et Basins
    densityBasin1_dt = densityBasin1*(1 - densityBasin1 + w_LNb_B1*densityLNb) + I4
    densityBasin2_dt = densityBasin2*(1 - densityBasin2 + w_LNa_B2*densityLNa) +I3
   
   
    return [ddensityLNa_dt, ddensityLNb_dt, densityBasin1_dt, densityBasin2_dt]


a,b,c = 40, 1,20
d = a+b+c
i,j,k = int(a*10), int(b*10), int(c*10)
l = i+j+k

t=np.linspace(0,a,i)


# Résolution
solution1 = odeint(systeme, [densityLNa_0, densityLNb_0, densityBasin1_0, densityBasin2_0], t, args=(rho,
    w_LNb_LNa, w_LNa_LNb, w_LNb_B1, w_LNa_B2, 0, 0, 0, 0))

t=np.linspace(0,b,j)
solution2 = odeint(systeme, solution1[len(solution1)-1,:], t, args=(rho,
    w_LNb_LNa, w_LNa_LNb, w_LNb_B1, w_LNa_B2, 0.07,0.0, 0,0.04 ))

t=np.linspace(0,5,50)
solution3 = odeint(systeme, solution2[len(solution2)-1,:], t, args=(rho,
    w_LNb_LNa, w_LNa_LNb, w_LNb_B1, w_LNa_B2, 0.07,0.07,0.15, 0.16))

t=np.linspace(0,c,k)
solution4 = odeint(systeme, solution3[len(solution3)-1,:], t, args=(rho,
    w_LNb_LNa, w_LNa_LNb, w_LNb_B1, w_LNa_B2, 0, 0, 0, 0))

t=np.linspace(0,d+5,l+50)

solution = np.vstack((solution1,solution2, solution3, solution4))
print(solution4[len(solution4)-1,0], solution4[len(solution4)-1,1], solution4[len(solution4)-1,2], solution4[len(solution4)-1,3])


fig, axs = plt.subplots(4, 1)
plt.rc('legend',fontsize=3)
axs[0].plot(t[390:500], solution[390:500,:2])
axs[0].legend(["density LNa","density LNb"])
axs[1].plot(t[390:500], solution[390:500,2] )
axs[1].legend(["density Basin1"])
axs[2].plot(t[390:500], solution[390:500,3] )
axs[2].legend(["density Basin2"])
axs[3].plot(t[390:500], solution[390:500,2] - solution[390:500,3])
axs[3].legend(["fraction hunching"])
fig.savefig('firing_rates_odeint.png', dpi=300)

#add in equation bend-hunch sequence to correct basin2 so add densityBasin1_dt => delayed differential equation ? + probabilité
# ou syst lent rapide donc epsilon
