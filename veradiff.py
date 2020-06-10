#!/usr/bin/python
import sys
import os.path
sys.path.insert(0, '/projects/vera-users-grp/Andrew')
import vera
import numpy as np


if len(sys.argv)==1:
  print 'python veradiff.py file1.h5 file2.h5 [list of cases]'
  exit()

file1=sys.argv[1]
if not os.path.exists(file1):
  print 'file '+file1+' not found'
  exit()

file2=sys.argv[2]
if not os.path.exists(file2):
  print 'file '+file2+' not found'
  exit()

rx1=vera.Reactor(file1)
rx2=vera.Reactor(file2)
lastcase=len(rx2.states)
cases=range(lastcase)

if len(sys.argv)>3:
  cases=sys.argv[3:]
  for i in xrange(len(cases)):
    cases[i]=int(cases[i])-1
    if cases[i]<0 or cases[i]>lastcase-1:
      cases[i]=lastcase-1

print
print ' File 1 = %s' % file1
print ' File 2 = %s' % file2
print 'States  = %i' % lastcase

for case in cases:
  pow1=rx1[case]['pin_powers']
  pow2=rx2[case]['pin_powers']
  pdiff=pow2-pow1
  avg=np.sum(pdiff*rx1.pin_factors)/np.sum(rx1.pin_factors)
  rms=np.sqrt(np.sum(pdiff*pdiff*rx1.pin_factors)/np.sum(rx1.pin_factors))
  max=np.max(pdiff)
  min=np.min(pdiff)
  absmax=max
  if abs(min)>absmax:
    absmax=min
  
  asspow1=rx1.Radial_Assembly(pow1)
  asspow2=rx1.Radial_Assembly(pow2)
  pdiff=asspow2-asspow1
  assavg=np.sum(pdiff*rx1.radial_assy_factors)/np.sum(rx1.radial_assy_factors)
  assrms=np.sqrt(np.sum(pdiff*pdiff*rx1.radial_assy_factors)/np.sum(rx1.radial_assy_factors))
  assmax=np.max(pdiff)
  assmin=np.min(pdiff)
  assabsmax=assmax
  if abs(assmin)>assabsmax:
    assabsmax=assmin

  axpow1=rx1.Axial(pow1)
  axpow2=rx1.Axial(pow2)
  axpdiff=axpow2-axpow1
  axavg=np.sum(axpdiff*rx1.axial_factors)/np.sum(rx1.axial_factors)
  axrms=np.sqrt(np.sum(axpdiff*axpdiff*rx1.axial_factors)/np.sum(rx1.axial_factors))
  axmax=np.max(axpdiff)
  axmin=np.min(axpdiff)
  axabsmax=axmax
  if abs(axmin)>axabsmax:
    axabsmax=axmin
  ao1=rx1.__calculateaxialoffset__(axpow1)
  ao2=rx2.__calculateaxialoffset__(axpow2)

  keff1=rx1[case]['keff']
  keff2=rx2[case]['keff']
  boron1=rx1[case]['boron']
  boron2=rx2[case]['boron']

  print
  print ' State = %i' % (case+1)
  print '  EFPD = %6.3f' % rx2[case]['exposure_efpd']
  print ' Power = %5.2f' % rx2[case]['power']
# print ' BankD = %i' % rx[case].GetBank('D')
  print 
  rx2.PrintCore(pdiff*100.0,'6.3f')
  print ' Average Assembly Power Difference = %6.3f%%' % (assavg*100)
  print '     RMS Assembly Power Difference = %6.3f%%' % (assrms*100)
  print ' Abs Max Assembly Power Difference = %6.3f%%' % (assabsmax*100)
  print

  print ' Level    Elev.     Power 1   Power 2    Diff'
  print '==============================================='
  for i in xrange(rx2.num_axials-1,-1,-1):
    loc=(rx2.axial_mesh[i+1]+rx2.axial_mesh[i])/2.0
    print '  %2i    %7.3f    %6.3f    %6.3f    %6.3f%%' % (i+1,loc,axpow1[i],axpow2[i],axpdiff[i]*100)
  print '==============================================='
  print '  AO     -----     %6.3f    %6.3f    %6.3f%%' % (ao1,ao2,ao2-ao1)
  print ' Average Axial Power Difference = %6.3f%%' % (assavg*100)
  print '     RMS Axial Power Difference = %6.3f%%' % (assrms*100)
  print ' Abs Max Axial Power Difference = %6.3f%%' % (axabsmax*100)
  print '        Axial Offset Difference = %6.3f%%' % (ao2-ao1)
  print
  print '       k-effective Difference = %6.1f pcm' % ((keff2-keff1)*10**5)
  print '               Critical Boron = %6.1f ppmB' % (boron2-boron1)
  print ' Average Pin Power Difference = %6.3f%%' % (avg*100)
  print '     RMS Pin Power Difference = %6.3f%%' % (rms*100)
  print ' Abs Max Pin Power Difference = %6.3f%%' % (absmax*100)
  print
  print '-------------------------------------------------------'
