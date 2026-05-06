// Resin properties for UI display. Keep in sync with amanzi/models/ionexchange.py RESIN_LIBRARY
export default {
  'Purolite-A860S': {
    resin_bulk_density: 705, // (0.68+0.73)/2 * 1000 kg/m³
    resin_capacity_eq_l: 0.8,
    particle_diameter_mm: 0.81,
    porosity: 0.35,
    specific_gravity: 1.08,
    doc_charge_factor: 0.1,
    doc_removal_fraction: 0.90,
    color_charge_factor: 0.02,
    color_removal_fraction: 0.90,
    so4_removal_fraction: 0.95,
  },
  'Purofine-PFA694EBF': {
    resin_bulk_density: 675, // (0.65+0.70)/2 * 1000 kg/m³
    resin_capacity_eq_l: 0.9,
    particle_diameter_mm: 0.70,
    porosity: 0.36,
    specific_gravity: 1.05,
    pfas_removal_fraction: 0.99,
  },
}
