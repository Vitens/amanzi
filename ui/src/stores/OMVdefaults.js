import _ from 'lodash'

const GROUPS = ['VOC', 'PFAS', 'Other']

const OMVdefaults = {
  VOC: [
    { name: 'Perchloroethylene', chemical: 'C2Cl4', henry: 0.4495, dw: 6.769e-10, dg: 7.395e-06, concentration: 0, unit: 'mg/l' },
    { name: 'Trichloroethylene', chemical: 'C2HCl3', henry: 0.2355, dw: 7.797e-10, dg: 8.138e-06, concentration: 0, unit: 'mg/l' },
    { name: 'cis-1,2-Dichlooretheen', chemical: 'C2H2Cl2', henry: 0.1222, dw: 8.423e-10, dg: 9.161e-06, concentration: 0, unit: 'mg/l' },
    { name: 'Vinylchloride', chemical: 'C2H3Cl', henry: 0.7610, dw: 1.029e-09, dg: 1.109e-05, concentration: 0, unit: 'mg/l' },
    { name: '1,1,1-Trichloroethane', chemical: 'C2H3Cl3', henry: 0.4470, dw: 9.119e-10, dg: 7.336e-06, concentration: 0, unit: 'mg/l' },
    { name: '1,1-Dichloroethane', chemical: 'C2H4Cl2_1_1', henry: 0.1559, dw: 7.930e-10, dg: 8.513e-06, concentration: 0, unit: 'mg/l' },
    { name: '1,2-Dichloroethane', chemical: 'C2H4Cl2_1_2', henry: 0.0333, dw: 7.930e-10, dg: 8.402e-06, concentration: 0, unit: 'mg/l' },
    { name: 'Tetrachlormethane', chemical: 'CCl4', henry: 0.7530, dw: 7.194e-10, dg: 7.677e-06, concentration: 0, unit: 'mg/l' },
    { name: 'Trichloromethane', chemical: 'CHCl3', henry: 0.0948, dw: 8.152e-10, dg: 8.220e-06, concentration: 0, unit: 'mg/l' },
    { name: 'Dichloromethane', chemical: 'CH2Cl2', henry: 0.0712, dw: 9.551e-10, dg: 9.612e-06, concentration: 0, unit: 'mg/l' },
    { name: '1,2-Dichloropropane', chemical: 'C3H6Cl2', henry: 0.0700, dw: 7.024e-10, dg: 1.014e-05, concentration: 0, unit: 'mg/l' },
  ],
  PFAS: [
    { name: 'PFBS', chemical: 'C4HF9O3S', PEQ: 0.001, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFPeS', chemical: 'C5HF11O3S', PEQ: 0.6, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFHxS', chemical: 'C6HF13O3S', PEQ: 0.6, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFHpS', chemical: 'C7HF15O3S', PEQ: 2, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFOS', chemical: 'C8HF17O3S', PEQ: 2, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFDS', chemical: 'C10HF21O3S', PEQ: 2, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'TFA', chemical: 'C2HF3O2', PEQ: 0.002, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFBA', chemical: 'C4HF7O2', PEQ: 0.05, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFPeA', chemical: 'C5HF9O2', PEQ: 0.05, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFHxA', chemical: 'C6HF11O2', PEQ: 0.01, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFHpA', chemical: 'C7HF13O2', PEQ: 1, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFOA', chemical: 'C8HF15O2', PEQ: 1, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFDA', chemical: 'C10HF19O2', PEQ: 10, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFUnDA', chemical: 'C11HF21O2', PEQ: 4, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFDoDA', chemical: 'C12HF23O2', PEQ: 3, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFTrDA', chemical: 'C13HF25O2', PEQ: 3, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
    { name: 'PFTeDA', chemical: 'C14HF27O2', PEQ: 0.3, concentration: 0, unit: 'ng/l', removalIEX: 0, removalAKF: 0, removalRO: 0, adsorptionCapacity_simple: 100 },
  ],
  Other: [],
}
// TFA data source : Polypyrrole-Tailored Activated Carbon for Trifluoroacetate Removal from Groundwater
function mergeCompound(defaultItem, storedItem, group) {
  const merged = _.merge({}, defaultItem, storedItem)
  if (group === 'PFAS' && merged.PEQ == null && storedItem.PFOAequviliant != null) {
    merged.PEQ = storedItem.PFOAequviliant
  }
  return merged
}

export function cloneOMVdefaults() {
  return _.cloneDeep(OMVdefaults)
}

/** Merge stored scenario metaData with defaults; preserves user values and custom compounds. */
export function mergeOMVmetaData(metaData) {
  const merged = cloneOMVdefaults()
  const stored = metaData?.customMicroComponents ?? {}

  for (const group of GROUPS) {
    const defaults = merged[group]
    const storedItems = stored[group] ?? []
    const defaultIndexByName = Object.fromEntries(defaults.map((item, index) => [item.name, index]))
    const custom = []

    for (const storedItem of storedItems) {
      if (!storedItem?.name) {
        custom.push(_.cloneDeep(storedItem))
        continue
      }
      const defaultIndex = defaultIndexByName[storedItem.name]
      if (defaultIndex !== undefined) {
        defaults[defaultIndex] = mergeCompound(defaults[defaultIndex], storedItem, group)
      } else {
        custom.push(mergeCompound({}, storedItem, group))
      }
    }

    merged[group] = [...defaults, ...custom]
  }

  return {
    ...(metaData ?? {}),
    customMicroComponents: merged,
    activatedcarbon: {
      lastPfasCount: null,
      userEditedCoefficients: {},
      ...(metaData?.activatedcarbon ?? {}),
    },
  }
}

export default OMVdefaults
