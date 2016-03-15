import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import string
import subprocess as sys
from scipy import stats

output = sys.Popen(["ls /work4/L.r02229011/WRF_3_5_1/WRFV3/run/control_1986_36hr_ts20s/wrfout_d01*|tail -n 32|head -n 30"],shell=True, stdout=sys.PIPE).communicate()[0]
filenames=string.split(output, '\n')
filenames.pop()
Fil=nc.MFDataset(filenames)
#####
outputExp = sys.Popen(["ls /work4/L.r02229011/WRF_3_5_1/WRFV3/run/irr_1986_36hr_both_75/wrfout_d01*|tail -n 32|head -n 30"],shell=True, stdout=sys.PIPE).communicate()[0]
filenamesExp=string.split(outputExp, '\n')
filenamesExp.pop()
FilExp=nc.MFDataset(filenamesExp)
###
print(filenames)
print("Total files: "+str(len(filenames)))
tmpString=[]
Var=[]
VarExp=[]
TimeString=[]
print("Time len: "+str(len(Fil.variables["Times"])))
for i in range(len(Fil.variables["Times"])):
	tmpString.append("".join(Fil.variables["Times"][i,:]))
ygrid=range(119,146)
xgrid=range(139,180)
#ygrid=range(27,66)
#xgrid=range(139,230)
#ygrid=range(210)
#xgrid=range(210)
for i in range(len(filenames)):
	Var.append(Fil.variables['RAINNC'][i*37+36,ygrid,xgrid]-Fil.variables['RAINNC'][i*37+12,ygrid,xgrid])
	VarExp.append(FilExp.variables['RAINNC'][i*37+36,ygrid,xgrid]-FilExp.variables['RAINNC'][i*37+12,ygrid,xgrid])
	TimeString.extend(tmpString[i*37+12:i*37+36])
Var=np.array(Var)
VarExp=np.array(VarExp)
Var1d=np.ravel(Var)
VarExp1d=np.ravel(VarExp)
print("==")
print("Var: "+str(Var.shape))
print("Var1d: "+str(Var1d.shape))
print("VarExp1d: "+str(VarExp1d.shape))
temp=Var1d>8
Var1d=Var1d[temp]
VarExp1d=VarExp1d[temp]
Var=np.average(np.average(Var,1),1)
VarExp=np.average(np.average(VarExp,1),1)
VarAno=VarExp-Var
print("==")
print("monthly CTR: "+str(sum(Var)))
print("monthly Ano: "+str(sum(VarAno)))
print("==")
print("Var1d meets condition: "+str(Var1d.shape))
print("VarExp1d: "+str(VarExp1d.shape))
print(stats.ttest_ind(Var1d, VarExp1d, equal_var = False))
print(stats.ttest_ind(Var1d, VarExp1d, equal_var = True))
print("==")
print("len after discarding spin-up: "+str(len(Var)))
fig=plt.figure()
ax1=fig.add_subplot(111)
ax1.plot(Var,'-ko')
ax1.plot(VarExp,'-bo')
ax2=plt.twinx()
ax2.plot(VarAno,'-ro')
ax2.plot(VarAno*0,'r--')
#fig.suptitle("("+str(ygrid)+", "+str(xgrid)+") Precipitation")
ax1.legend(['CTR', 'IRR'], loc='upper right')
ax2.legend(['IRR-CTR'], loc='upper left')
ax1.grid()
ax1.set_ylabel('Precipitation (mm)')
ax2.set_ylabel('Anomaly(mm)')
#ax2.set_ylim([-1.5,1.5])
plt.show()
