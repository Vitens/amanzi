<template>
  <el-tab-pane>
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <div id="sandtrap-design">
      <div class="process">
        <div class="metric valid">
          <span class="value">Design valid:</span>
          <span>{{ format(outputs.settling_velocity_check) }}</span>
        </div>
        <div class="metric inlet_height">
          <span class="value">{{ params.height_at_inlet.toFixed(1) }}</span>
          <span class="units">m</span>
        </div>
        <div class="metric outlet_height">
          <span class="value">{{ params.height_at_outlet }}</span>
          <span class="units">m</span>
        </div>
        <div class="metric length">
          <span class="value">{{ params.length }}</span>
          <span class="units">m</span>
        </div>
        <div class="metric surface_loading">
          <span class="value">{{ format(outputs.surface_loading) }}</span>
          <span class="units">m<sup>3</sup>/m<sup>3</sup>/h</span>
        </div>
      </div>
    </div>

  </el-tab-pane>
</template>
<script>
export default {
  props: ['config'],
  methods: {
    format(value) {

      if (value === undefined) {
        return '-'
      }
      if (typeof value.value === 'string') {
        return value.value
      }
      return value.value.toFixed(value.precision)
    },
  },
  computed: {
    outputs() {
      if(this.$runtime.designState === undefined) return {}
      if(this.$runtime.designState.outputs === undefined) return {}

      return this.$runtime.designState.outputs
    },
    params() {
      return this.config.parameters
    }
  }
}
</script>
<style>
#sandtrap-design {
  padding: 0px 10px;
  border: 1px solid #CCC;
  border-radius: 5px;
}
#sandtrap-design .process {
  width: 800px;
  margin: auto;
  overflow: hidden;
  height: 400px;
  background: url('./assets/process.png') no-repeat center;
  border: none;
}
#sandtrap-design .metric {
  position: absolute;
  font-size: 14px;
  color: #333;
  padding: 5px;
  margin: 5px;
}
#sandtrap-design .value {
  display: inline-block;
  margin-right: 3px;
}
#sandtrap-design .inlet_height {
  top: 37%;
  left: 5%;
}
#sandtrap-design .outlet_height {
  top: 50%;
  right: 5%;
}
#sandtrap-design .length {
  bottom: 5%;
  left: 50%;
}
#sandtrap-design .surface_loading {
  top: 15%;
  left: 48%;
}
#sandtrap-design .valid {
  top: 5%;
  left: 20%;
  width: 200px;
}
</style>


