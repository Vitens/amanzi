<template>
  <div class="result-block" :class="[color, name, compactClass, multiple ? 'multiple' : '']" v-if="components !== false">

    <div class="result-block-headers" v-if="headers">
      <div class="result-block-header" v-for="header in headers">{{ header }}</div>
    </div>

    <div class="component" v-for="component in components">
      <label v-html="chemform(component.name)"></label>
      <template v-if="multiple">
        <div class="value" v-for="value in component.value">{{ output(value) }}</div>
      </template>
      <template v-else>
        <div class="value">{{ output(component.value) }}</div>
      </template>
      <div class="unit" v-if="!compact"> {{ component.units }}</div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'ResultBlock',
  props: {
    color: {
      type: String,
      default: 'blue'
    },
    name: {
      type: String,
      default: 'Influent'
    },
    components: {
      type: Array,
      default: () => []
    },
    headers: {
      type: Array,
      default: () => []
    },
    multiple: {
      type: Boolean,
      default: false
    },
    compact: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    compactClass() {
      return this.compact ? 'compact' : ''
    }
  },
  methods: {
    output(val) {
      if(val === undefined) { return 404 }

      if (val > 1000) { return val.toFixed(0) }

      return val > 100 ? val.toFixed(1) : val.toFixed(2)
    },
    chemform(chemical) {
      if(chemical == "") { return "" }

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


    },
  },

}
</script>
<style scoped>
.result-block {
  position: absolute;
  padding: 3px;
  width: 150px;
  border: 2px solid transparent;
  border-radius: 5px;
  font-size: 12px;
}
.result-block.compact {
  width: 85px;
  font-size: 12px;
  padding: 2px;
}
.result-block.multiple {
  width: 200px;
}
.result-block.compact label {
  width: 40px;
}
.result-block.multiple .result-block-headers {
  margin-left: 53px;
  font-weight: bold;
  color: #333;
} 
.result-block.multiple .result-block-header {
  display: inline-block;
  width: 50px;
}
.result-block.compact .value {
  width: 35px;
}

.result-block .component {
  padding: 1.5px 5px;
  border-bottom: 1px solid;
}
.result-block sub {
  font-size: 9px;
  font-weight: 100;
  color: black;
}
.result-block label {
  display: inline-block;
  width: 50px;
  color: black;
  font-weight: bold;
}
.result-block .value {
  display: inline-block;
  color: #333;
  font-weight: 500;
  width: 50px;
}
.result-block .unit {
  display: inline-block;
  width: 40px;
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

.result-block .component {
  border-color: #ebd0ab;
}
.result-block .component:last-child {
  border-bottom: 0px;
}
.result-block.blue .component {
  border-color: #a0cfff;
}
.result-block.green .component {
  border-color: #b3e19d;
}
.result-block.gray .component {
  border-color: #c8c9cc;
}
.result-block.red .component {
  border-color: #fab6b6;
}
</style>
