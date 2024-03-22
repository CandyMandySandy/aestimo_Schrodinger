#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Aestimo's database module. Contains a materialproperty dict containing 
sub-dicts of values for each material and similar alloyproperty dict for the
alloys of the materials. See the source for details on the required keys for
each material or alloy.

 References:
  - GaAs,AlAs parameters:
    Properties of Semiconductor Alloys: Group-IV, III-V and II-VI Semiconductors Sadao AdAchi?2009 John Wiley & Sons, Ltd.
    Basic Semiconductor Physics Second Edition,Prof. Chihiro Hamaguchi 2010 Springer
    Physics of Optoelectronic Devices ,S-L.CHUANG ,1995 by John Wiley & Sons. Inc
  
"""
"""
 Aestimo 1D Schrodinger-Poisson Solver
 Copyright (C) 2013-2016 Sefer Bora Lisesivdin and Aestimo group

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. See ~/COPYING file or http://www.gnu.org/copyleft/gpl.txt .

    For the list of contributors, see ~/AUTHORS
"""


from EdgeEmitterData.Utils.MaterialParams import BandParameters as bp
from aestimo_database import materialproperty, alloyproperty
from copy import copy

class adatabase(object):
  def __init__(self, temp = 300, valley = 'Gamma' ):
    self._temp = temp
    self._valley = valley
  
  
  def set_options(self, temp, valley):
    self._temp = temp
    self._valley = valley    
    
  @property 
  def temp(self):
    return self._temp

  @property 
  def valley(self):
    return self._valley
    
  @property
  def materialproperty(self):
    matprop = copy(materialproperty)
    for mat in matprop:
      try :
        mato = getattr(bp, mat)
        own_mat = True
      except AttributeError:
        own_mat = False
      if own_mat:
        mato.temp = self.temp
        mato.valley = self.valley
        try:
          matprop[mat]['m_e'] = mato.mstar_qw
        except :
          print(mat, mato._mstar, mato._mstar_params, self.temp, self.valley)
        matprop[mat]['Eg'] = mato.gap
        matprop[mat]['cbo'] =  mato.cbo
    return matprop
  
  @property
  def alloyproperty(self):  
    allprop = copy(alloyproperty)
    for alloy in allprop:
      try :
        mato = getattr(bp, alloy)
        own_mat = True
      except AttributeError:
        own_mat = False
      if own_mat:
        mato.temp = self.temp
        mato.valley = self.valley
        allprop[alloy]['cbo'] =  mato.bow_params['cbo'] if 'cbo' in mato.bow_params else 0
    return allprop
    




