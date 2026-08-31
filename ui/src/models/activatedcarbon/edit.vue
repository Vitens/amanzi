<template>
  <teleport defer to="#category-operational" v-if="teleport">     
     <el-form label-position="top">
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
            <tr v-for="step,i in modelValue.parameters.backwash_programme">
              <td>{{ i+1 }}</td>
              <td><number-input v-model="step.time" :min="0" :max="1000"></number-input></td>
              <td><number-input v-model="step.water" :min="0" :max="100"></number-input></td>
              <td><number-input v-model="step.air" :min="0" :max="100"></number-input></td>
              <td>
                <i class='fa fa-times-circle remove-step' @click="removeStep(i)" :class="{disabled: modelValue.parameters.backwash_programme.length == 1}"></i>
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

  <teleport defer to="#category-model" v-if="simpleCalculation">
    <el-form >
      <table>
        <thead>
          <tr>
            <th>{{ $t('models.activatedcarbon.design.compound') }}</th>
            <th>{{ $t('models.activatedcarbon.design.removal_akf') }}</th>
          </tr>
          <tr>
            <th></th>
            <th>%</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="compound in pfasList" :key="compound">
            <td>{{ compound }}</td>
            <td>
              <number-input v-model="modelValue.parameters[compound + '_removeAKF']" :min="0" :max="100"></number-input>
            </td>
          </tr>
          <tr>
            <!-- <td>Color</td>
            <td>
            <number-input
                :model-value="compoundRemovalRate('Other', 'Color')"
                @update:modelValue="setCompoundRemovalRate('Other', 'Color', $event)"
                :min="0"
                :max="100"
              ></number-input>
            </td>
          </tr>
          <tr>
            <td>TOC</td>
            <td>
            <number-input
                :model-value="compoundRemovalRate('Other', 'Total-Organic-Carbon')"
                @update:modelValue="setCompoundRemovalRate('Other', 'Total-Organic-Carbon', $event)"
                :min="0"
                :max="100"
              ></number-input>
            </td>-->
          </tr> 
        </tbody>
      </table>
    </el-form>

 
  </teleport> 
  <teleport defer to="#category-model" v-if="advancedCalculation">
    <el-form>
    <table id="backwash_programme">
          <thead>
            <tr>
              <th>{{ $t('models.activatedcarbon.design.compound') }}</th>

              <th>{{ $t('models.activatedcarbon.design.competition_coefficient') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>-</td>
              <td>-</td>
            </tr>
            <tr v-for="compound in pfasList" :key="compound">
              <td>{{ compound }} </td>
              <td>
                <number-input
                  :model-value="Number(modelValue.parameters[compound + '_competition_coefficient']).toFixed(2)"
                  @update:modelValue="onCompetitionCoefficientChange(compound, Number($event).toFixed(2))"
                  :min="0"
                  :max="100"
                  :step="0.01"
                ></number-input>
              </td>
            </tr>
            <tr v-if="modelValue.parameters.include_doc_competition !== false">
              <td>DOC</td>
              <td>
                <number-input
                  :model-value="Number(modelValue.parameters.DOC_competition_coefficient).toFixed(2)"
                  @update:modelValue="onCompetitionCoefficientChange('DOC', Number($event).toFixed(2))"
                  :min="0"
                  :max="100"
                  :step="0.01"
                ></number-input>
              </td>
            </tr>
          </tbody>
          

        </table>
    </el-form>  


  </teleport>
</template>

<script>


export default {
props: ['config', 'modelValue'],
  data() { return {
    backwash_steps: 5,
    backwash: 'increasing',
    teleport: true,
    syncingCoefficients: false,
  }},
  beforeUnmount() {
    this.teleport = false
  },
created() {
  this.ensureDocDefaults()
  this.syncCompetitionCoefficients()
},
computed: {
    pfasList() {
      return Object.keys(this.$runtime.designState.model?.PFAS ?? {})
    },
    freundlichKSignature() {
      const params = this.modelValue.parameters || {}
      const compounds = [...this.pfasList]
      if (!compounds.includes('PFOA')) {
        compounds.push('PFOA')
      }
      compounds.push('DOC')
      return compounds.map(compound => `${compound}:${params[compound + '_Freundlich_k']}`).join('|')
    },
    advancedCalculation(){
      return this.teleport && !this.modelValue.parameters.stationary_calculation
    },
    simpleCalculation(){
      return this.teleport && this.modelValue.parameters.stationary_calculation
    },
},
watch: {
        '$runtime.designState.model.PFAS': {
          deep: true,
          handler() {
            this.syncCompetitionCoefficients()
          },
        },
        '$runtime.designState.competition_coefficients': {
          deep: true,
          immediate: true,
          handler() {
            this.syncCompetitionCoefficients()
          },
        },
        freundlichKSignature() {
          this.syncCompetitionCoefficients()
        },
        'modelValue.parameters.include_doc_competition'() {
          this.syncCompetitionCoefficients()
          this.$project.scenario.unsolved = true
        },
        'modelValue.parameters.DOC_Freundlich_k'() {
          this.syncCompetitionCoefficients()
          this.$project.scenario.unsolved = true
        },
        'modelValue.parameters.DOC_Freundlich_1n'() {
          this.$project.scenario.unsolved = true
        },
    },
methods:{
  ensureDocDefaults() {
    const parameters = this.modelValue.parameters
    if (parameters.include_doc_competition == null) {
      parameters.include_doc_competition = true
    }
    if (parameters.DOC_Freundlich_k == null) {
      parameters.DOC_Freundlich_k = 250
    }
    if (parameters.DOC_Freundlich_1n == null) {
      parameters.DOC_Freundlich_1n = 0.45
    }
  },
  activatedCarbonMeta() {
    const metaData = this.$project.scenario.metaData
    if (!metaData.activatedcarbon) {
      metaData.activatedcarbon = {
        lastPfasCount: null,
        userEditedCoefficients: {},
      }
    }
    if (!metaData.activatedcarbon.userEditedCoefficients) {
      metaData.activatedcarbon.userEditedCoefficients = {}
    }
    if (!('lastPfasCount' in metaData.activatedcarbon)) {
      metaData.activatedcarbon.lastPfasCount = null
    }
    return metaData.activatedcarbon
  },
  getLastPfasCount() {
    const value = this.activatedCarbonMeta().lastPfasCount
    return value == null ? null : Number(value)
  },
  setLastPfasCount(count) {
    this.activatedCarbonMeta().lastPfasCount = count == null ? null : count
  },
  getUserEditedCoefficients() {
    return this.activatedCarbonMeta().userEditedCoefficients
  },
  competitionCoefficientKey(compound) {
    return compound + '_competition_coefficient'
  },
  markUserEditedCoefficient(compound) {
    this.getUserEditedCoefficients()[compound] = true
  },
  pruneUserEditedCoefficients(pfasList) {
    const userEditedCoefficients = this.getUserEditedCoefficients()
    const keep = new Set(pfasList)
    if (this.modelValue.parameters.include_doc_competition !== false) {
      keep.add('DOC')
    }
    for (const compound of Object.keys(userEditedCoefficients)) {
      if (!keep.has(compound)) {
        delete userEditedCoefficients[compound]
      }
    }
  },
  readCoefficient(compound) {
    return Number(this.modelValue.parameters[this.competitionCoefficientKey(compound)]) || 0
  },
  writeCoefficient(compound, value) {
    this.modelValue.parameters[this.competitionCoefficientKey(compound)] = value
  },
  freundlichK(compound) {
    const params = this.modelValue.parameters || {}
    const fromModel = Number(params[compound + '_Freundlich_k'])
    if (Number.isFinite(fromModel) && fromModel > 0) {
      return fromModel
    }
    const fromConfig = Number(this.config?.parameters?.[compound + '_Freundlich_k'])
    if (Number.isFinite(fromConfig) && fromConfig > 0) {
      return fromConfig
    }
    return compound === 'PFOA' ? 1718 : compound === 'DOC' ? 250 : 100
  },
  affinityWeight(compound) {
    const kPfoa = Math.max(this.freundlichK('PFOA'), 1e-12)
    return this.freundlichK(compound) / kPfoa
  },
  looksLikeEqualSplit(pfasList) {
    if (pfasList.length < 2) {
      return false
    }
    const share = 1 / pfasList.length
    const values = pfasList.map(compound => this.readCoefficient(compound))
    const sum = values.reduce((total, value) => total + value, 0)
    const allEqual = values.every(value => Math.abs(value - share) < 0.02)
    return allEqual && Math.abs(sum - 1) < 0.05
  },
  onCompetitionCoefficientChange(compound, value) {
    const pfasList = this.pfasList
    if (!pfasList.includes(compound) && compound !== 'DOC') {
      return
    }

    const changed = Math.min(100, Math.max(0, Number(value) || 0))
    this.syncingCoefficients = true
    try {
      this.writeCoefficient(compound, changed)
      this.markUserEditedCoefficient(compound)
      this.$project.scenario.unsolved = true
    } finally {
      this.$nextTick(() => {
        this.syncingCoefficients = false
      })
    }
  },
  syncCompetitionCoefficients() {
    if (this.syncingCoefficients) {
      return
    }

    const pfasList = Object.keys(this.$runtime.designState.model?.PFAS ?? {})
    this.pruneUserEditedCoefficients(pfasList)
    if (pfasList.length === 0) {
      return
    }

    const userEditedCoefficients = this.getUserEditedCoefficients()
    const migrateEqualSplit = this.looksLikeEqualSplit(pfasList)
    if (migrateEqualSplit) {
      for (const compound of pfasList) {
        delete userEditedCoefficients[compound]
      }
    }

    this.syncingCoefficients = true
    try {
      for (const compound of pfasList) {
        if (userEditedCoefficients[compound] && !migrateEqualSplit) {
          continue
        }
        this.writeCoefficient(compound, this.affinityWeight(compound))
      }
      if (this.modelValue.parameters.include_doc_competition !== false && !userEditedCoefficients.DOC) {
        this.writeCoefficient('DOC', this.affinityWeight('DOC'))
      }
      this.setLastPfasCount(pfasList.length)
    } finally {
      this.$nextTick(() => {
        this.syncingCoefficients = false
      })
    }
  },
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
    addStep() {
      this.modelValue.backwash_programme.push({time: 0, water: 0, air: 0})
    },
    removeStep(i) {
      if (this.modelValue.backwash_programme.length > 1) {
        this.modelValue.backwash_programme.splice(i, 1)
      }
    },
    resultSet(group) {
      if(!(group in this.$runtime.designState)) { return false }

      let data = this.$runtime.designState[group]

      let result = []
      for (let [key, value] of Object.entries(data)) {
        result.push({name: key, value: value, units: 'ng/l'}) // adjust this line as needed
      }
      return result
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
.doc-ebc {
  margin-top: 12px;
}
.doc-ebc table {
  margin-top: 8px;
}

</style>