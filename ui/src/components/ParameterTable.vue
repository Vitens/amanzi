<template>
  
  <div class="design-table-container">
  <copy-button :target="'.design-table.'+table.name"></copy-button>
  <table :class="['design-table', table.name]">
    <!-- header -->
    <thead @dblclick="collapseAll">
      <tr>
        <th>{{  $t('ui.design.tables.parameter') }}</th>
        <th>Min.</th>
        <th>Nom.</th>
        <th>Max.</th>
        <th>{{  $t('ui.design.tables.units') }}</th>
      </tr>
    </thead>  
      <tbody v-for="section in filterEmpty(table.sections)">
        <tr class="section" @click="toggle">
          <td>{{ $t('models.'+section.namespace+'.sections.'+section.name) }}</td>
          <td colspan="3" v-if="singleValue(section)">{{ formatSection(section.nom, section) }}</td>
          <template v-else>
            <td>{{ formatSection(section.min, section) }}</td>
            <td>{{ formatSection(section.nom, section) }}</td>
            <td>{{ formatSection(section.max, section) }}</td>
          </template>
          <td v-html="formatUnits(section.uom)"></td>

        </tr>
        <tr v-for="output, index in outputs(section)" :class="{indent: output.indent}" class="output-row">
          <td>
            <i class="fa fa-minus-square-o" v-if="collapsable(section, index)" @click="toggleIndent"></i>

            {{ $t('models.'+output.namespace+'.outputs.'+output.name) }}</td>
          <td colspan="3" v-if="singleValue(output)" :class="{invalid: output.nom_invalid}">{{ format(output.nom, output) }}</td>
          <template v-else>
            <td :class="{invalid: output.min_invalid}">{{ format(output.min, output) }}</td>
            <td :class="{invalid: output.nom_invalid}">{{ format(output.nom, output) }}</td>
            <td :class="{invalid: output.max_invalid}">{{ format(output.max, output) }}</td>
          </template>
          <td><span v-html="formatUnits(output.uom)" class="uom" :class="{convertable: convertable(output.uom)}" @click="toggleConversion(output.uom)"></span></td>
        </tr>
      </tbody>
      <tfoot v-if="table.totals">
        <tr class="sum">
          <td>{{ $t('ui.design.tables.totals') }}</td>
          <td colspan="3" v-if="singleValue(table.totals)">{{ format(table.totals.nom, table) }}</td>
          <template v-else>
            <td>{{ format(table.totals.min, table) }}</td>
            <td>{{ format(table.totals.nom, table) }}</td>
            <td>{{ format(table.totals.max, table) }}</td>
          </template>
          <td><span class='uom' v-html="formatUnits(table.totals.uom)"></span></td>
        </tr>
      </tfoot>

  </table>
  </div>
</template>
<script>
import CopyButton from './CopyButton.vue';

let conversions = {
  'm3/h': {
    'm3/h': 1,
    'm3/d': 24,
    'l/s': 0.27777777777778,
  },
  'mH2O': {
    'mH2O': 1,
    'kPa': 9.80665,
    'bar': 0.0980665,
  },
  'bar': {
    'bar': 1,
    'kPa': 100,
    'mH2O': 10.1972,
  },
  'm': {
    'm': 1,
    'mm': 1000,
    'cm': 100,
  },
  'MJ/Nm3': {
    'MJ/Nm3': 1,
    'kWh/Nm3': 1/3.6
  },
  'Nm3/h': {
    'Nm3/h': 1,
    'Nm3/d': 24,
    'Nm3/y': 8760,
  },
  'h': {
    'h': 1,
    'min': 60,
    'd': 1/24,
  }
}


export default {
  components: {
    CopyButton
  },
  data() {
    return {
      mounted: false,
      uomConversions: {},
      copytext: 'Copy'
    }
  },
  mounted() {
    this.mounted = true;
  },
  props: ['table'],
  computed: {
  },
  methods: {
    filterEmpty(sections) {
      return sections.filter(section => this.outputs(section).length > 0);
    },
    outputs(section) {
      return this.table.outputs.filter(p => p.section === section.name);
    },
    collapsable(section, index) {
      let outputs = this.outputs(section);
      if(index == outputs.length - 1) return false; // last item cannot be collapsed
      if(!outputs[index].indent && outputs[index + 1].indent) return true; // next item is indented
      return false
    },
    convertable(uom) {
      return uom in conversions;
    },
    collapseAll(event) {
      const sections = event.target.closest('table').querySelectorAll('.section');
      sections.forEach(section => section.closest('tbody').classList.toggle('collapsed'));
    },
    toggle(event) {
      const section = event.target.closest('tbody');
      section.classList.toggle('collapsed');
    },
    toggleIndent(event) {
      // toggle the indent class on the parent row
      event.target.classList.toggle('fa-minus-square-o');
      event.target.classList.toggle('fa-plus-square-o');
      // get all sibling rows until the next non-indented row
      let row = event.target.closest('tr');
      for(let next = row.nextElementSibling; next; next = next.nextElementSibling) {
        if(next.classList.contains('indent')) {
          next.classList.toggle('hidden');
        } else {
          break;
        }
      }


    },
    toggleConversion(uom) {
      if (!this.convertable(uom)) return;

      // cycle through available conversions
      let keys = Object.keys(conversions[uom]);
      let index = keys.indexOf(this.uomConversions[uom]);
      if (index == -1) index = 0;
      let nextIndex = (index + 1) % keys.length;
      this.uomConversions[uom] = keys[nextIndex];
    },
    formatUnits(uom) {
  if (uom == undefined) return '-';

  if (uom in this.uomConversions) {
    return this.uomConversions[uom];
  }

  // Regular expression to detect chemical formulas (e.g., CO2, H2O, CH4)
  // ignore skip Nm3
  uom = uom.replace(/Nm3/g, 'Nm<sup>3</sup>');
  const chemicalRegex = /([A-Z][a-z]*)(\d*)/g;
  
  // Regular expression to detect metric units with superscript (e.g., m3, km2)
  const metricRegex = /([a-zA-Z]+)(\d+)/g;

  // Replace chemical formulas with subscripts for numbers
  uom = uom.replace(chemicalRegex, (match, element, number) => {
    return element + (number ? `<sub>${number}</sub>` : '');
  });

  // Replace metric units with superscripts for numbers
  uom = uom.replace(metricRegex, (match, unit, power) => {
    return `${unit}<sup>${power}</sup>`;
  });

  return uom;
},
    formatValue(value, precision) {
      return value.toLocaleString('nl-NL', { minimumFractionDigits: precision, maximumFractionDigits: precision });
    },
    singleValue(parameter) {
      return parameter.value !== undefined || (parameter.min === parameter.nom && parameter.nom === parameter.max) || (parameter.min === undefined && parameter.max == undefined);
    },
    format(value, parameter) {

      if (typeof value === 'string') return value;
      if (typeof value === 'boolean') return value ? 'Yes' : 'No';

      let precision = parameter.precision
      value = parameter.uom == '%' ? value * 100 : value

      // apply unit conversion if necessary
      if (parameter.uom in this.uomConversions) {
        value = value * conversions[parameter.uom][this.uomConversions[parameter.uom]];
      }

      if (value === undefined) return '-';

      // if (precision != undefined) return 123
      if (precision != undefined) return this.formatValue(value, precision);
      if (value === 0) return '0.0';
      if (value < 1) return this.formatValue(value, 3);
      return this.formatValue(value, 1);
    },
    formatSection(value, section) {
      if (value === undefined) { return '-' }
      return this.formatValue(value,section.precision)
    }
  }
}

</script>
<style>
.design-table-container {
  position: relative;
}
.design-table-container .copy-button {
  position: absolute;
  left: 550px;
  width: 70px;
  top: -33px;
  z-index: 100;
}

.design-table {
  border: 1px solid #666;
  text-align: center;
  width: 620px;
  border-spacing: 0px;
  color: #000;
}
.design-table thead {
  background: #337ecc;
  color: white;
  font-size: 14px;
}


.design-table sup, .design-table sub {
  font-size: 8px;
}
.design-table th:first-child {
  text-align: left;
  width: 300px;
}
.design-table th:last-child {
  width: 110px;
}
.design-table tr td:first-child {
  text-align: left;
}

.design-table th {
  padding: 2px;
  margin: 0px;
  border-bottom: 1px solid #333;
}

.design-table th, .design-table td {
  padding: 5px;
}
.design-table tbody td {
  border-left: 1px solid #BBB;
}
.design-table tbody td:first-child {
  border-left: none;
}
.design-table td {
  padding: 5px 18px;
  margin: 0px;
  border-bottom: 1px solid #BBB;
}
.design-table tr:last-child td {
  border-bottom: none;
}
.design-table tr.indent td {
  background: #F9F9F9;
  color: #333;
}
.design-table tr.indent td:first-child {
  padding-left: 30px;
}
.design-table .section {
  background-color: #d9ecff;
  color: #1b4069;
  font-weight: bold;
}
.design-table .output-row {
  position: relative;
}
.design-table .output-row.hidden {
  display: none;
}

.design-table .output-row i {
  cursor: pointer;
  opacity: 0.8;
  font-size: 11px;
  position: absolute;
  left: 5px;
  top: 9px;
}


.design-table .section td {
  border-left: none;
}

.design-table .collapsed tr:not(:first-child) {
  display: none;
}
.design-table .section td {
  border-top: 1px solid #aaa;
  cursor: pointer;
}
.design-table .section td:first-child {
  position: relative;
  padding-left: 18px;
}
.design-table .section td:first-child::before {
  color: #355d86;
  left: 5px;
  position: absolute;
  font-family: monospace;
  content: "▶︎";
  display: inline-block;
  transition: all 0.2s;
  transform: rotate(90deg);
}
.design-table .collapsed .section td::before {
  transform: rotate(0deg);
}

.design-table tfoot td {
  background: #F5F7FA;
  border-top: 2px solid #409EFF;
  font-weight: bold;
}


.design-table .invalid {
  background-color: #fce2e2;
  color: #c70c0c;
}

.uom.convertable {
  text-decoration: dotted underline;
  text-decoration-skip: edges;
  text-decoration-color: #1104cc;
  cursor: pointer;
}
/* Custom styling */
/* Energy table */
.design-table.energy .section {
  background-color: #fffeb2;
  color: #7d5b28;
}
.design-table.energy thead {
  background: #E6A23C;
}
.design-table.energy tfoot td {
  border-top: 2px solid #E6A23C;
}
/* Sustainability table */
.design-table.sustainability .section {
  background-color: #a4d38c;
  color: #2d481f;
}
.design-table.sustainability thead {
  background: #67C23A;
}
.design-table.sustainability tfoot td {
  border-top: 2px solid #67C23A;
}

/* Chemicals table */
.design-table.chemicals .section {
  background-color: #e5aeed;
  color: #611e6c;
}
.design-table.chemicals thead {
  background: #b437a1;
}
.design-table.chemicals tfoot td {
  border-top: 2px solid #a63aa8;
}


</style>