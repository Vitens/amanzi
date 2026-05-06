<template>
  <teleport defer to="#category-operational">      <el-form label-position="top">
        <h3>{{$t("ui.design.sections.backwash_programme") }}</h3>
        <table id="backwash_programme">
          <thead>
            <tr>
              <th>{{ $t('models.filtration.backwash_programme.step') }}</th>
              <th>{{ $t('models.filtration.backwash_programme.time') }}</th>
              <th v-html="$t('models.filtration.backwash_programme.q_water')"></th>
              <th v-html="$t('models.filtration.backwash_programme.q_air')"></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td></td>
              <td>sec</td>
              <td>m/h</td>
              <td>Nm<sup>3</sup>/h&middot;m<sup>-2</sup></td>
            </tr>
            <tr v-for="step,i in modelValue.backwash_programme">
              <td>{{ i+1 }}</td>
              <td><number-input v-model="step.time" :min="0" :max="1000"></number-input></td>
              <td><number-input v-model="step.water" :min="0" :max="100"></number-input></td>
              <td><number-input v-model="step.air" :min="0" :max="100"></number-input></td>
              <td>
                <i class='fa fa-times-circle remove-step' @click="removeStep(i)" :class="{disabled: modelValue.backwash_programme.length == 1}"></i>
              </td>
            </tr>
            <tr>
              <td colspan="4">
                <el-button @click="addStep" type="success" class="add_step_button">{{ $t('models.filtration.backwash_programme.add_step') }}</el-button>
              </td>
            </tr>
          </tbody>
        </table>
      </el-form>
    </teleport>

  <teleport defer to="#category-model">
    <el-form v-if="!advancedCalculation">
      <table>
        <thead>
          <tr>
            <th>{{ $t('models.activatedcarbon.design.compound') }}</th>
            <th>{{ $t('models.activatedcarbon.design.removal_akf') }}</th>
            <th>{{ $t('models.activatedcarbon.design.adsorption_capacity') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="compound in pfasList" :key="compound">
            <td>{{ compound }}</td>
            <td>
              <number-input
                :model-value="compoundRemovalRate('PFAS', compound)"
                @update:modelValue="setCompoundRemovalRate('PFAS', compound, $event)"
                :min="0"
                :max="100"
              ></number-input>
              <span>%</span>
            </td>
            <td>
              <number-input
                :model-value="adsorptionCapacity('PFAS', compound)"
                @update:modelValue="setAdsorptionCapacity('PFAS', compound, $event)"
                :min="0"
                :max="500"
                :defaultValue="100"
              ></number-input>
              <span>mg/g</span>
            </td>
          </tr>
        </tbody>
      </table>
    </el-form>

    <el-form v-else>
        <table id="backwash_programme">
          <thead>
            <tr>
              <th>{{ $t('models.activatedcarbon.design.compound') }}</th>
              <th>{{ $t('models.activatedcarbon.design.freundlich_k') }}</th>
              <th>{{ $t('models.activatedcarbon.design.freundlich_1n') }}</th>
              <th>{{ $t('models.activatedcarbon.design.loading_q') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>-</td>
              <td>µg/g/L/µg</td>
              <td>-</td>
              <td>µg/g</td>
            </tr>
            <tr v-for="compound in pfasList" :key="compound">
              <td>{{ compound }} </td>
              <td>
                <number-input
                  :model-value="compoundParameter('PFAS', compound, 'freundlich_k', 100)"
                  @update:modelValue="setCompoundParameter('PFAS', compound, 'freundlich_k', $event)"
                  :min="0"
                  :max="100000"
                ></number-input>
              </td>
              <td>
                <number-input
                  :model-value="compoundParameter('PFAS', compound, 'freundlich_1n', 0.4)"
                  @update:modelValue="setCompoundParameter('PFAS', compound, 'freundlich_1n', $event)"
                  :min="0"
                  :max="1"
                  :step="0.01"
                ></number-input>
              </td>
              <td>
                <number-input
                  :model-value="compoundParameter('PFAS', compound, 'initial_loading_q', 0)"
                  @update:modelValue="setCompoundParameter('PFAS', compound, 'initial_loading_q', $event)"
                  :min="0"
                  :max="100000"
                ></number-input>
              </td>
            </tr>
          </tbody>
          
        </table>
    </el-form>
  </teleport> 
</template>

<script>
const defaultFreundlichParameters = {
  PFBS: { freundlich_k: 456.94, freundlich_1n: 0.411, initial_loading_q: 1 },
  PFPeS: { freundlich_k: 1521, freundlich_1n: 0.3521, initial_loading_q: 1 },
  PFHxS: { freundlich_k: 3840, freundlich_1n: 0.3134, initial_loading_q: 1 },
  PFHpS: { freundlich_k: 4588.9, freundlich_1n: 0.286, initial_loading_q: 1 },
  PFOS: { freundlich_k: 7222, freundlich_1n: 0.2525, initial_loading_q: 1 },
  PFDS: { freundlich_k: 0.1, freundlich_1n: 1, initial_loading_q: 1 },
  TFA: { freundlich_k: 2.3 * (1000 / (1000 ** 0.343)), freundlich_1n: 0.343, initial_loading_q: 1 },
  PFBA: { freundlich_k: 255, freundlich_1n: 0.4942, initial_loading_q: 1 },
  PFPeA: { freundlich_k: 1160, freundlich_1n: 0.4252, initial_loading_q: 1 },
  PFHxA: { freundlich_k: 4179, freundlich_1n: 0.3607, initial_loading_q: 1 },
  PFHpA: { freundlich_k: 498, freundlich_1n: 0.3144, initial_loading_q: 1 },
  PFOA: { freundlich_k: 1718, freundlich_1n: 0.2808, initial_loading_q: 1 },
  PFDA: { freundlich_k: 6371, freundlich_1n: 0.2415, initial_loading_q: 1 },
  PFUnDA: { freundlich_k: 14603, freundlich_1n: 0.2233, initial_loading_q: 1 },
  PFDoDA: { freundlich_k: 18106, freundlich_1n: 0.2076, initial_loading_q: 1 },
  PFTrDA: { freundlich_k: 25862, freundlich_1n: 0.1972, initial_loading_q: 1 },
  PFTeDA: { freundlich_k: 30582, freundlich_1n: 0.1858, initial_loading_q: 1 },
}

export default {
props: ['config', 'modelValue'],
  data() { return {
    backwash_steps: 5,
    backwash: 'increasing'
  }},
computed: {
    pfasList(){
        return Object.keys(this.$project.designState.model?.PFAS ?? {})
    },
    advancedCalculation(){
      return this.modelValue.parameters.advanced
    }
},
methods:{
    ensureCompound(group, compound){
      if (!this.modelValue.compound_removal_rates) {
        this.modelValue.compound_removal_rates = {}
      }
      if (!this.modelValue.compound_removal_rates[group]) {
        this.modelValue.compound_removal_rates[group] = {}
      }
      if (!this.modelValue.compound_removal_rates[group][compound]) {
        this.modelValue.compound_removal_rates[group][compound] = { name: compound }
      }
      this.modelValue.compound_removal_rates[group][compound].name = compound
      return this.modelValue.compound_removal_rates[group][compound]
    },
    compoundParameter(group, compound, key, defaultValue){
      const configured = this.modelValue.compound_removal_rates?.[group]?.[compound]?.[key]
      if (configured !== undefined) {
        return Number(configured)
      }
      const item = this.ensureCompound(group, compound)
      const fallback = defaultFreundlichParameters[compound]?.[key] ?? defaultValue
      item[key] = fallback
      return fallback
    },
    setCompoundParameter(group, compound, key, value){
      const item = this.ensureCompound(group, compound)
      item[key] = Number(value)
    },
    adsorptionCapacity(group, compound){
      const configured = this.modelValue.compound_removal_rates?.[group]?.[compound]?.adsorptionCapacity_simple
      if (configured !== undefined) {
        return Number(configured)
      }

      const defaultValue = 100
      const item = this.ensureCompound(group, compound)
      item.adsorptionCapacity_simple = defaultValue
      return defaultValue
    },
    setAdsorptionCapacity(group, compound, value){
      const item = this.ensureCompound(group, compound)
      item.adsorptionCapacity_simple = Number(value)
    },
    compoundRemovalRate(group, compound){
      const configured = this.modelValue.compound_removal_rates?.[group]?.[compound]?.removalAKF_simple
      if (configured !== undefined) {
        return Number(configured)
      }

      const metadata = this.$project.scenario?.metaData?.customMicroComponents?.[group] ?? []
      const fallback = metadata.find(item => item.name === compound)?.removalAKF
      return fallback !== undefined ? Number(fallback) : 0
    },
    setCompoundRemovalRate(group, compound, value){
      const item = this.ensureCompound(group, compound)
      item.removalAKF_simple = Number(value)
    },
    addStep() {
      this.modelValue.backwash_programme.push({time: 0, water: 0, air: 0})
    },
    removeStep(i) {
      if (this.modelValue.backwash_programme.length > 1) {
        this.modelValue.backwash_programme.splice(i, 1)
      }
    }
}
}
</script>
<style>
.backwash-icon {
  font-size: 28px !important;
}
#backwash_programme {
  width: 310px;
}
#backwash_programme td {
  text-align: center;
}
#backwash_programme .add_step_button {
  width: 100%;
  opacity: 0.8;
}
#backwash_programme .add_step_button:hover {
  opacity: 1;
}
#backwash_programme .remove-step {
  cursor: pointer;
  opacity: 0.5;
}
#backwash_programme .remove-step.disabled {
  color: #ccc;
  cursor: not-allowed;
}
#backwash_programme .remove-step:hover {
  opacity: 1;
}

</style>