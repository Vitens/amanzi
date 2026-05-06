<template>
  <div id="key-figure-database">
    <div class="key-figure-filter">
    <el-input
      prefix-icon="Search"
      placeholder="Filter..."
      v-model="filter"
      clearable
    /> 
    <el-badge :value="overwritten" :max="10" :hidden="overwritten == 0">
      <el-checkbox-group v-model="filter_modified" :disabled="overwritten==0">
        <el-checkbox-button label="modified" class="key-figure-filter-button"><i class="fa fa-filter"></i></el-checkbox-button>
      </el-checkbox-group>
    </el-badge>
    </div>
    <div class="key_figures">
      <el-affix target="#key-figure-database" :offset="0">
      <div class="key_figures-header">
        <div class="field name">Name</div>
        <div class="field tag">Tag</div>
        <div class="field default">Default</div>
        <div class="field project">Project</div>
        <div class="field scenario">Scenario</div>
        <div class="field uom">UOM</div>
      </div>
      </el-affix>
    <el-skeleton animated :loading='rows.length == 0' class="loading" :count="10">
      <template #template>
        <div class="skeleton">
          <el-skeleton-item variant="rect" v-for="n in 5"></el-skeleton-item>
        </div>
      </template>
    </el-skeleton>
    <div class="category" v-for="(category, key) in dataset" :key="key">
      <div class="category_header">{{ $t('keyfigures.categories.'+key) }}</div>
      <div class="type" v-for="(type, key) in category" :key="key">
        <div class="type_header">{{ $t("keyfigures.types."+key) }}</div>
            <div class="key-figure" v-for="figure in type" :class="{overwritten: isOverwritten(figure[1])}">
              <div class="field name">{{ figure[0] }}</div>
              <div class="field tag">{{ figure[1] }}</div>
              <div class="field default">{{ figure[4] }}</div>
              <div class="field project">
                <el-input type='number' :placeholder="String(figure[4])" v-model="overwrites.project[figure[1]]" @input="checkEmpty('project', figure[1])"></el-input>
                <span class="reset-to-default" @click="delete overwrites.project[figure[1]]" v-if="overwrites.project[figure[1]]"><i class="fa fa-share-square"></i></span>

              </div>
              <div class="field scenario">
                <el-input type='number' :placeholder="String(figure[4])" v-model="overwrites.scenario[figure[1]]" @input="checkEmpty('scenario', figure[1])"></el-input>
                <span class="reset-to-default" @click="delete overwrites.scenario[figure[1]]" v-if="overwrites.scenario[figure[1]]"><i class="fa fa-share-square"></i></span>
              
              </div>
              <div class="field uom">{{ figure[5] }}</div>
            </div>

          </div>
        </div>
    </div>
  </div>
</template>
<script>
import { over } from 'lodash';

export default {
  data() {
    return {
      filter: '',
      filter_modified: [],
      rows: [],
      overwrites: {
        'project': {},
        'scenario': {},
      }
    }
  },
  async mounted() {
    // get project and scenario overwrites
    this.overwrites.project = this.$project.keyfigureOverwrites
    this.overwrites.scenario = this.$project.scenario.keyfigureOverwrites
    this.rows = await this.$project.getKeyFigures()
  },
  methods: {
    checkEmpty(type, key) {
      if(this.overwrites[type][key] == '') {
        delete this.overwrites[type][key]
      }
    },
    isOverwritten(key) {
      return this.overwrites.project[key] || this.overwrites.scenario[key]
    }
  },
  computed: {
    overwritten() {
      var overwritten = this.$project.number_of_overwrites
      if (overwritten == 0) {
        this.filter_modified = []
      }
      return overwritten
    },
    dataset() {
      // return nested object with keys for each category
      let dataset = {}
      const filter_modified = this.filter_modified.length > 0

      this.rows.forEach(row => {
        let [key, category, type, value, unit] = row

        let name = this.$t('keyfigures.name.'+key)
        // add name to beginning of row
        row = [name, ...row]
        
        if (!dataset[category]) {
          dataset[category] = {}
        }
        if (!dataset[category][type]) {
          dataset[category][type] = []
        }

        if(!this.filter && !filter_modified) {
          dataset[category][type].push(row)
          return
        }

        if(filter_modified && !(this.overwrites.project[key] || this.overwrites.scenario[key])) {
          return
        }



        if(this.filter == '') {
          dataset[category][type].push(row)
        }
        else if(name.includes(this.filter) || key.includes(this.filter) || category.includes(this.filter) || type.includes(this.filter) || unit.includes(this.filter)) {
          dataset[category][type].push(row)
        } else {
          return
        }
      })

      dataset = _.mapValues(dataset, (value) =>
        _.pickBy(value, (arr) => _.isArray(arr) && arr.length > 0)
      );

      return dataset
    }
  }

}
</script>
<style>

#key-figure-database {
  padding: 10px;
}

#key-figure-database .key-figure-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
#key-figure-database .loading {
  padding-top: 20px;
}
#key-figure-database .skeleton {
  display: flex;
  gap: 10px;
  padding: 5px;
}
#key-figure-database .skeleton div {
  height: 35px;
}
#key-figure-database .category_header {
  font-size: 16px;
  font-weight: bold;
  padding: 5px 6px;
  color: var(--el-color-primary-dark-2);
  background-color: var(--el-color-primary-light-7);
}

#key-figure-database .key_figures {
  padding: 10px 0px;
}
#key-figure-database .key_figures-header {
  display: flex;
  border-bottom: 1px solid #666;
  background-color: #FFF;
}
#key-figure-database .key_figures-header .field {
  padding: 10px 10px;
  display: flex;
  flex-direction: column;
  font-weight: bold;
  font-size: 14px !important;
  color: #555 !important;
  justify-content: center;
  align-items: flex-start;
}
#key-figure-database .key_figures-header .field.name {
  padding-left: 15px;
}

/* Chrome, Safari, Edge, Opera */
#key-figure-database input::-webkit-outer-spin-button,
#key-figure-database input::-webkit-inner-spin-button {
  margin: 0;
  -webkit-appearance: none;
}

/* Firefox */
#key-figure-database input[type=number] {
  -moz-appearance: textfield;
}

#key-figure-database .type_header {
  background-color: #EEE;
  font-size: 14px;
  font-weight: bold;
  padding: 3px;
  padding-left: 10px;


}
#key-figure-database .key-figure {
  padding-left: 5px;
  display: flex;
  border-bottom: 1px solid #AAA;
  transition: background-color 0.3s;
}
#key-figure-database .key-figure.overwritten {
  background-color: #FFC;
}
#key-figure-database .key-figure .field {
  padding: 2px 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}
#key-figure-database .field.name {
  font-weight: bold;
  width: 250px;
}
#key-figure-database .field.tag {
  width: 250px;
  font-size: 12px;
  color: #888;
}
#key-figure-database .field.default {
  width: 50px;
  align-items: center;
}
#key-figure-database .field.project {
  width: 80px;
  position: relative;
}
#key-figure-database .field.scenario {
  width: 80px;
  position: relative;
}
#key-figure-database .field.uom {
  width: 80px;
  align-items: flex-start;
}

#key-figure-database .reset-to-default {
  position: absolute;
  right: 18px;
  cursor: pointer;
  color: #ff5100;
}
</style>