<template>
  <el-tab-pane id="groundwater-composition">
    <template #label>
      <el-icon size="14px"><i class='fa fa-flask'></i></el-icon><span>Waterkwaliteit</span>
    </template>

    <div class="quality">
      <div class="composition">
        <el-select :placeholder="$t('models.groundwater.select-preset')" v-model="preset">
          <el-option v-for="p, name of presets" :key="name" :label="$t('models.groundwater.presets.'+name)" :value="name">
          </el-option>
        </el-select>
        <br />
        <div class="quality_category" v-for="group, name of components">
          <h3>{{ $t('models.groundwater.composition.groups.'+name) }}</h3>
          <div class="components">

          <div v-for="component of group" :key="component.name" class="component">
            <label> {{ $t('general.solution.components.'+component.name) }}</label>
            <div class="chemform" v-html="chemform(component.chemical)"></div>

            <number-input v-model="config.parameters[component.name]" :min="component.range[0]" :max="component.range[1]" class="cheminput" :step="component.max < 100 ? 0.1 : 1.0" :placeholder="String(component.default)" />
            

            <div class="units">
              {{ component.uom }}
            </div>

          </div>
          </div>
        </div>

      </div>
      <div class="results">
        <div class="result-block orange">
          <h3>{{ $t('models.groundwater.design.calculated-properties') }}</h3>
          <div class="components">
            <div class="component">
              <label>{{ $t('models.groundwater.design.conductivity') }}</label>
              <div class="result">{{ output('sc20', 1) }}</div>
              <div class="units">mS/m</div>
            </div>
            <div class="component">
              <label>{{  $t('models.groundwater.design.m-number') }}</label>
              <div class="result">{{ output('m', 2) }}</div>
              <div class="units">meq/l</div>
            </div>
            <div class="component">
              <label>{{  $t('models.groundwater.design.p-number') }}</label>
              <div class="result">{{ output('p', 2) }}</div>
              <div class="units">meq/l</div>
            </div>
            <div class="component">
              <label>{{  $t('models.groundwater.design.redox-potential') }}</label>
              <div class="result">{{  output('pe', 2) }}</div>
              <div class="units">-</div>
            </div>
            <div class="component">
              <label>H<sup>+</sup> {{ $t('models.groundwater.design.activity') }}</label>
              <div class="result">{{  output('h_activity', 2) }}</div>
              <div class="units">-</div>
            </div>
            <div class="component">
              <label>{{ $t('models.groundwater.design.tds') }}</label>
              <div class="result">{{ output('tds', 1) }}</div>
              <div class="units">mg/l</div>
            </div>
            <div class="component">
              <label>{{ $t('models.groundwater.design.osmotic-pressure') }}</label>
              <div class="result">{{ output('osmotic_pressure') }}</div>
              <div class="units">bar</div>
            </div>
          </div>
        </div>
        <div class="result-block green">
          <h3>{{ $t('models.groundwater.design.charge') }}</h3>
          <div class="components">
            <div class="component">
              <label>{{ $t('models.groundwater.composition.groups.cations') }}</label>
              <div class="result">{{  output('cations') }}</div>
              <div class="units">meq/l</div>
            </div>
            <div class="component">
              <label>{{ $t('models.groundwater.composition.groups.anions') }}</label>
              <div class="result">{{ output('anions') }}</div>
              <div class="units">meq/l</div>
            </div>
            <div class="component">
              <label>{{ $t('models.groundwater.design.charge-balance') }}</label>
              <div class="result">{{ output('charge_balance') }}</div>
              <div class="units">meq/l</div>
            </div>
            <div class="component total" :class="{warning: chargeWarning}">
              <label>{{ $t('models.groundwater.design.charge-derivation') }}</label>
              <div class="result">{{ output('balance_error') }}</div>
              <div class="units">%</div>
              <el-tooltip :content="$t('models.groundwater.design.charge-inbalance-warning')" placement="top">
              <div class="component-warning" v-if="chargeWarning"><i class='fa fa-warning'></i></div>
              </el-tooltip>
              <el-tooltip :content="$t('models.groundwater.design.balance-charge-tooltip')" placement="top" >
                <el-button type="success" size="small" @click="balanceCharge" :disabled="!chargeWarning" class="balance-charge-button">{{ $t('models.groundwater.design.balance-charge') }}</el-button>
              </el-tooltip>
            </div>
          </div>
        </div>

        <div class="result-block blue">
          <h3>{{ $t('models.groundwater.design.carbon-equilibrium') }}</h3>
          <div class="components">
            <div class="component">
              <label v-html="chemform('CO2')"></label>
              <div class="result">{{output('CO2', 1)}}</div>
              <div class="units">mg/l</div>
            </div>
            <div class="component">
              <label v-html="chemform('HCO3')"></label>
              <div class="result">{{ output('HCO3', 1) }}</div>
              <div class="units">mg/l</div>
            </div>
            <div class="component">
              <label v-html="chemform('CO3')"></label>
              <div class="result">{{ output('CO3', 1) }}</div>
              <div class="units">mg/l</div>
            </div>
            <div class="component total">
              <label>{{ $t('models.groundwater.design.tac') }}</label>
              <div class="result">{{ output('tac', 1) }}</div>
              <div class="units">mg/l</div>
            </div>
          </div>
        </div>

        <div class="result-block gray">
          <h3>{{ $t('models.groundwater.design.scaling-potential') }}</h3>
          <div class="components">
            <div class="component">
              <label>{{ $t('models.groundwater.design.hardness') }}</label>
              <div class="result">{{ output('hardness') }}</div>
              <div class="units">mmol/</div>
            </div>
            <div class="component" :class="{warning: SIWarning}" >
              <label>{{ $t('models.groundwater.design.SI') }}</label>
              <div class="result">{{ output('SI') }}</div>
              <div class="units">-</div>
              <el-tooltip :content="$t('models.groundwater.design.scaling-warning')" placement="right">
                <div class="component-warning" v-if="SIWarning"><i class='fa fa-warning'></i></div>
              </el-tooltip>
            </div>
            <div class="component">
              <label>{{ $t('models.groundwater.design.ccpp') }}</label>
              <div class="result">{{ output('CCPP') }}</div>
              <div class="units">mmol/l</div>
            </div>
            <div class="component">
              <label>{{ $t('models.groundwater.design.ccpp90') }}</label>
              <div class="result">{{ output('CCPP90') }}</div>
              <div class="units">mmol/l</div>
            </div>
          </div>
        </div>

        <div class="result-block red">
          <h3>{{ $t('models.groundwater.design.oxygen-consumption') }}</h3>
          <div class="components">
            <div class="component">
              <label>Fe + Mn + NH<sub>4</sub></label>
              <div class="result">{{ output('oxygen_consumption_ions') }}</div>
              <div class="units">mg/l</div>
            </div>
            <div class="component">
              <label>CH<sub>4</sub> + H<sub>2</sub>S</label>
              <div class="result">{{ output('oxygen_consumption_gas') }}</div>
              <div class="units">mg/l</div>
            </div>
            <div class="component total">
              <label>{{ $t('models.groundwater.design.total') }}</label>
              <div class="result">{{  output('oxygen_consumption') }}</div>
              <div class="units">mg/l</div>
            </div>
          </div>
        </div>

      </div>
    </div>
    </el-tab-pane>
    <el-tab-pane id="groundwater-design" :disabled="false">
      <template #label>
        <el-icon size="14px"><i class='fa fa-flask'></i></el-icon><span>Micropollutants</span>
      </template>
      <OMP :design="design" :config="config"></OMP>
    </el-tab-pane>




</template>

<script>
import OMP from './micropollutants.vue'
import presets from './assets/presets.js'

export default {
  name: 'design-groundwater',
  components: {
    OMP
  },
  props: ['config'],
  data() {
    return {
      preset: '',
      presets: presets
    }
  },
  
  computed: {
    components() {
      // get the components from the config
      let components = {}

      var params = this.$project.modelParameters['groundwater']
      for(var p of params) {
        if (p.category != '_composition') { continue }
        if (p.section === '_micropollutants') { continue }
        components[p.section] = components[p.section] || []
        components[p.section].push(p)
      }
      return components

    },
    chargeWarning() {
      return Math.abs(this.$runtime.designState.balance_error) > 2
    },
    SIWarning() {
      return this.$runtime.designState.SI > 0
    }
  },
  watch: {
    preset: function(val) {

      var preset = JSON.parse(JSON.stringify(this.presets[val]))
      Object.assign(this.config.parameters, preset)
    }
  },
  methods: {
    balanceCharge(element) {
      // balance the charge of the solution
      let error = this.$runtime.designState.charge_balance
      if (error > 0) {
        this.config.parameters['chloride'] += _.round(error * 35.45, 1)
      } else {
        this.config.parameters['sodium'] += _.round(-error * 22.99, 1)
      }

    },
    output(key, precision=2) {
      // if key not in $runtime.designState, return '-'
      if(!(key in this.$runtime.designState)) { return '-' }

      return this.$runtime.designState[key].toFixed(precision)

    },
    chemform(chemical) {
      if(chemical == "" || chemical == undefined) { return "" }

      let parts = chemical.match(/(\d+|[A-Za-z]+|\+|-)/g);

      let result = '';
      for (let part of parts) {
          if (/[A-Za-z]+/.test(part)) {
              result += part;
          } else if (/\d+/.test(part)) {
              for (let char of part) {
                  result += "<sub>"+char+"</sub>";
              }
          } else if (/\+|-/.test(part)) {
              for (let char of part) {
                  result += "<sup>"+char+"</sup>";
              }
          }
      }

      return result;


    }
  }
}


</script>
<style>


#groundwater-composition {
  padding: 0px 15px;
  padding-bottom: 25px;
}


#groundwater-composition .quality {
  display: flex;
  min-width: 450px;
}
#groundwater-composition .results {
  flex: 1;
  margin-left: 15px;
  min-width: 300px;
  max-width: 500px;
}
#groundwater-composition .results .result-block {
  padding: 5px 15px;
  border-radius: 5px;
  margin-bottom: 10px;
}
#groundwater-composition h3 {
  margin: 10px 0px;
  color: #333;
  font-size: 1.2em;
  font-weight: bold;
}

#groundwater-composition label {
  display: inline-block;
  /* background: #AAA; */
  color: #333;
  padding: 5px 0px;
}
#groundwater-composition .quality label {
  width: 180px;
}
#groundwater-composition .results label {
  width: 100px;
}
#groundwater-composition .quality_category {
  max-width: 500px;
}

#groundwater-composition .component:first-child {
  border-top: 1px solid #EAEAEA;
}

#groundwater-composition .component {
  color: #333;
  padding: 2px 0px;
  border-bottom: 1px solid #EAEAEA;
}

#groundwater-composition .chemform {
  display: inline-block;
  width: 50px;
  text-align: center;
  padding: 5px;
}

#groundwater-composition .cheminput {
  width: 100px;
}

#groundwater-composition .units {
  display: inline-block;
  width: 45px;
  padding: 0px 15px;
}

#groundwater-composition .result {
  display: inline-block;
  width: 45px;
  padding: 0px 15px;
  text-align: right;
}



#groundwater-composition .component.warning .result, #groundwater-composition .component.warning .units, #groundwater-composition .component.warning .component-warning {
  font-weight: bold;
  color: #f56c6c !important;
}

.component-warning {
  display: inline-block;
}

.result-block.orange {
  background-color: #fff3e6;
  border-color: #ebd0ab !important;
}
.result-block.blue {
  background-color: #d9ecff;
  border-color: #a0cfff !important;
}
.result-block.green {
  background-color: #e1f3d8;
  border-color: #b3e19d !important;
}
.result-block.gray {
  background-color: #e9e9eb;
  border-color: #c8c9cc !important;
}
.result-block.red {
  background-color: #fde2e2;
  border-color: #fab6b6 !important;
}

.result-block.orange .component {
  border-color: #ebd0ab !important;
}
.result-block .components .component:last-child {
  border-bottom: 0px !important;
}
.result-block.blue .component {
  border-color: #a0cfff !important;
}
.result-block.green .component {
  border-color: #b3e19d !important;
}
.result-block.gray .component {
  border-color: #c8c9cc !important;
}
.result-block.red .component {
  border-color: #fab6b6 !important;
}

.balance-charge-button {
  margin-left: 15px;
}
.total {
  color: #999;
  font-weight: bold;
  border-top: 1px solid #EAEAEA;
}

</style>