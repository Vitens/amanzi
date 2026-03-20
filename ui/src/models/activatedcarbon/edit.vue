<template>
  <teleport defer to="#category-operational" v-if="teleport">      <el-form label-position="top">
        <h3>{{$t("ui.design.sections.backwash_programme") }}</h3>
        <table id="backwash_programme">
          <thead>
            <th>{{ $t('models.filtration.backwash_programme.step') }}</th>
            <th>{{ $t('models.filtration.backwash_programme.time') }}</th>
            <th v-html="$t('models.filtration.backwash_programme.q_water')"></th>
            <th v-html="$t('models.filtration.backwash_programme.q_air')"></th>
          </thead>
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
        </table>
      </el-form>
    </teleport>
  <teleport defer to="#category-chemicals" v-if="teleport">
    <el-form>
        <table id="backwash_programme">
          <thead>
            <th>Compound</th>
            <th>Freundlich K</th>
            <th> Freundlich 1/n</th>
            <th> Loading q</th> 
          </thead>
          <tr>
            <td>-</td>
            <td>µg/g/L/µg</td>
            <td>-</td>
            <td>µg/g</td>
          </tr>
          <tr v-for="(value,key) in PFASlist()" :key="key">
            <td>{{ key }} </td>
            <td><number-input type="number" v-model="config['compound'][key][0]" :step="1" :min="0" :max="100000" size="small"></number-input></td>
            <td><number-input type="number" v-model="config['compound'][key][1]" :step="0.01" :min="0" :max="10" size="small"></number-input></td>
            <td><number-input type="number" v-model="config['compound'][key][2]" :step="1" :min="0" :max="100000" size="small"></number-input></td>


          </tr>
          
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
    teleport: true
  }},
beforeUnmount() {
    this.teleport = false
  },
methods:{
    PFASlist(){
        if(!this.$project.designState.model) { return [] }

        return this.$project.designState.model.PFAS
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