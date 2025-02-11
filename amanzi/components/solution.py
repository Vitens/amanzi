from phreeqpython import Solution

## additional methods for phreeqpython.Solution

def si90(self, phase):

    tmp = self.copy()
    tmp.change_temperature(90)

    si = tmp.si(phase)

    tmp.forget()
    return si

def ccpp(self, temperature=None):
  """ Calculate Calcium Carbonate Precipitation Potential (CCPP)"""
  # create copy of solution
  tmp = self.copy()
  # raise temperature
  if temperature and temperature is not self.temperature:
      tmp.change_temperature(temperature)
  ca_pre = tmp.total_element('Ca')
  # use saturate instead of desaturate to allow dissolution in addition to precipitation
  tmp.equalize('Calcite',0.0)
  # calculate tacc
  ccpp = ca_pre - tmp.total_element('Ca')
  # cleanup
  tmp.forget()

  return ccpp #mmol

@property
def ccpp90(self):
  return self.ccpp(90)

@property
def hardness(self):
   """ Calculate hardness (Ca + Mg)"""
   return self.total('Ca', 'mmol') + self.total('Mg', 'mmol')

@property
def sc20(self):
  """ Calculate conductivity at 20 degrees"""
  # create copy of solution
  tmp = self.copy()
  # raise temperature
  tmp.change_temperature(20)
  # calculate conductivity
  sc = tmp.sc
  # cleanup
  tmp.forget()
  return sc

@property
def osmotic_pressure(self):
    total_moles = sum(self.elements.values())
    # subtract gasses (H2S, CH4, CO2, N2)
    total_moles -= self.total('[C-4]', 'mol') + self.total('Ntg', 'mol') + self.total('[S-2]', 'mol') + self.total('Mtg', 'mol')
    total_moles -= self.total('CO2', 'mol') + self.total('O2', 'mol')
    
    psi = 1.12 * (273 + self.temperature) * total_moles
    
    return psi * 0.06894 # conversion to bar
   
@property
def p(self):
    return self.total('CO2') - self.total('CO3') + self.total('H+') - self.total('OH-')
   
@property
def m(self):
    return self.total('HCO3') + 2*self.total('CO3') - self.total('H+') + self.total('OH-')

def calculate_total_charge(self):
    
    total_cation_charge = 0.0
    total_anion_charge = 0.0

    for ion, molality in self.species.items():
        charge = 0
        # get last characters
        l1 = ion[-1]
        l2 = ion[-2]
        
        if l1 == "+": # eg H+
            total_cation_charge += molality
        elif l1 == "-": # eg OH-
            total_anion_charge += molality
        elif l2 == "+": # eg Ca+2
            total_cation_charge += molality * int(l1)
        elif l2 == "-": # eg CO3-2
            total_anion_charge += molality * int(l1)
        else:
            continue
        #print(ion, molality*1000)
    # return cation, anion charge
    return 1000*total_cation_charge, 1000*total_anion_charge

@property
def charge_balance(self):
    cat,an = self.calculate_total_charge()
    return cat-an

@property
def balance_error(self):
    cat,an = self.calculate_total_charge()
    return 100*(cat-abs(an))/(cat+abs(an))

@property
def aggCO2(self):
    return -1 * min(0, self.ccpp()) * 44.01

@property
def tds(self):
    total = (self.density - self.mass/self.volume) * 1e6
    # suptract dissolved gasses
    total -= self.total('CO2', 'mg')
    total -= self.total('O2', 'mg')
    total -= self.total('Ntg', 'mmol') * 28.0134
    total -= self.total('Mtg', 'mmol') * 16.043
    return total

# return dict with solution summary
@property
def summary(self):
    parameters = [
        {'name': 'pH', 'value': self.pH, 'uom': '-', 'precision': 2},
        {'name': 'sc20', 'value': self.sc20/10, 'uom': 'mS/m', 'precision': 2},
        {'name': 'o2', 'value': self.total('Oxg')*32 + self.total('O2')*32, 'uom': 'mg/l', 'precision': 2},
        {'name': 'hco3', 'value': self.total('HCO3', 'mg'), 'uom': 'mg/l', 'precision': 2},
        {'name': 'hardness', 'value': self.hardness, 'uom': 'mmol/l', 'precision': 2, 'positive': False},
        {'name': 'tds', 'value': self.tds, 'uom': 'mg/l', 'precision': 1, 'positive': False},
        {'name': 'ccpp90', 'value': self.ccpp90, 'uom': 'mmol/l', 'precision': 2, 'positive': False},
        {'name': 'aggco2', 'value': self.aggCO2, 'uom': 'mg/l', 'precision': 2},
        {'name': 'Fe', 'value': self.total('Fe', 'mg'), 'uom': 'mg/l', 'precision': 2},
        {'name': 'Mn', 'value': self.total('Mn', 'mg'), 'uom': 'mg/l', 'precision': 2},
        {'name': 'NH4', 'value': self.total('[N-3]', 'mmol')*18, 'uom': 'mg/l', 'precision': 2},
        {'name': 'Na', 'value': self.total('Na', 'mg'), 'uom': 'mg/l', 'precision': 2},
        {'name': 'Cl', 'value': self.total('Cl', 'mg'), 'uom': 'mg/l', 'precision': 2},
    ]
    return parameters

# extend class
Solution.si90 = si90
Solution.ccpp = ccpp
Solution.ccpp90 = ccpp90
Solution.aggCO2 = aggCO2
Solution.hardness = hardness
Solution.sc20 = sc20
Solution.osmotic_pressure = osmotic_pressure
Solution.p = p
Solution.m = m
Solution.calculate_total_charge = calculate_total_charge
Solution.charge_balance = charge_balance
Solution.balance_error = balance_error
Solution.tds = tds
Solution.summary = summary