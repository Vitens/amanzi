<template>
    <div id="micros">
        
    <h3>{{ $t('models.groundwater.design.vocs') }}</h3>
    <table >
        <thead>
            <tr>
                <th>{{ $t('models.groundwater.design.name') }}</th>
                <th>{{ $t('models.groundwater.design.chemical_formula') }}</th>
                <th>{{ $t('models.groundwater.design.concentration') }}</th>
                <th>{{ $t('models.groundwater.design.henry') }} @15°C</th>
                <th>{{ $t('models.groundwater.design.dw') }} @15°C</th>
                <th>{{ $t('models.groundwater.design.dg') }} @15°C</th>
                
            </tr>
        </thead>
        <tbody>
        <tr v-for="(item,index) in $project.scenario.metaData.customMicroComponents['VOC']" :key="item.name" >
            <td> {{ $t('general.solution.components.'+item.name) }}</td>
            <td v-html="chemform(item.chemical)"> </td>
            <td>
                <number-input v-model="item.concentration" :min=0 :max=1000 class="cheminput" :step=1.0 :placeholder="String(0)" />
                <select class="unitselect" v-model="item.unit">
                        <option value="mg/l"selected>mg/l</option>
                        <option value="μg/l">μg/l</option>
                        <option value="ng/l" >ng/l</option>
                </select>
            </td>
            <td > {{ parseFloat(findHenryNumber(item.name, 'henry')).toFixed(4) }}</td>
            <td >{{ parseFloat(findHenryNumber(item.name, 'dw')).toExponential(4) }} m²/s</td>
            <td >{{ parseFloat(findHenryNumber(item.name, 'dg')).toExponential(3) }} m²/s</td>
         
        </tr>
        <tr v-for="(item,index) in $project.scenario.metaData.customMicroComponents['VOC'].slice(nVOC)" :key="index" >
            <td>  <el-input  v-model="item.name"></el-input></td>
            <td>  <el-input  v-model="item.chemical"></el-input> </td>
            <td>
                <number-input v-model="config.parameters[item.name]" :min=0 :max=1000 class="cheminput" :step=1.0 :placeholder="String(0)" />
                <select class="unitselect" v-model="item.unit">
                        <option value="mg/l" selected>mg/l</option>
                        <option value="μg/l">μg/l</option>
                        <option value="ng/l">ng/l</option>
                </select>
            </td>
           
            <td >  <el-input type="number" v-model="item.henry">{{ parseFloat(item.henry).toFixed(4) }}</el-input></td>
            <td > <el-input  type="number" v-model="item.dw">{{ parseFloat(item.dw).toExponential(4) }} m²/s</el-input></td>
            <td > <el-input  type="number" v-model="item.dg" class="Input"> {{ parseFloat(item.dg).toExponential(3) }} m²/s</el-input></td>
            <td>
                <button @click="deleteRow(index, 'VOC',item.name)" class="delete-button">X</button>
            </td>
        </tr>
        <tr>
                <td colspan="6" class="add-component" @click="addCustomComponent('VOC')">{{ $t('models.groundwater.design.addCompound') }}</td> 
            </tr>
        
            <!-- Add more rows as needed -->
        </tbody>
        </table>
        <br>
    <h3>{{ $t('models.groundwater.design.pfas') }}</h3>
    <table >
        <thead>
            <tr>
                <th>{{ $t('models.groundwater.design.name') }}</th>
                <th>{{ $t('models.groundwater.design.abreviation') }}</th>
                <th>{{ $t('models.groundwater.design.chemical_formula') }}</th>
                <th>{{ $t('models.groundwater.design.concentration') }}</th>
                <th>{{ $t('models.groundwater.design.pfoa-factor') }}</th>
                <th>{{ $t('models.groundwater.design.removal_akf') }}</th>
                <th>{{ $t('models.groundwater.design.removal_ro') }}</th>
                <th>{{ $t('models.groundwater.design.removal_iex') }}</th>
                
            </tr>
        </thead>
        <tbody>
            <tr v-for="(item, index) in $project.scenario.metaData.customMicroComponents['PFAS']" :key="index">
                <td > {{ $t('general.solution.components.'+item.name) }} </td>
                <td> {{ item.name.toUpperCase() }} </td>
                <td v-html="chemform(item.chemical)" ></td>
                <td >                 
                    <number-input
                        v-model="config.parameters[item.name]"
                        :unit="item.unit"
                        :min="0" :max="1000000" class="cheminput" :step="1.0" :placeholder="String(0)"
                    />
                    <select class="unitselect" v-model="item.unit">
                        <option value="mg/l">mg/l</option>
                        <option value="μg/l">μg/l</option>
                        <option value="ng/l" selected>ng/l</option>
                    </select>
                </td>
                <td > {{ item.PEQ }} </td>


                <td> <el-input type="number" v-model="item.removalAKF" :min="0" :max="100" :step="1"></el-input> </td>
                <td>
                    <el-input type="number" v-model="item.removalRO" :min="0"  :max="100" :step="1"></el-input>
                </td>
                <td>
                    <el-input type="number" v-model="item.removalIEX" :min="0"  :max="100" :step="1"></el-input> 
                </td>
                
                    
            </tr>
            <tr v-for="(item,index) in $project.scenario.metaData.customMicroComponents['PFAS'].slice(nPFAS)" :key="index">
                <td>  <el-input type="text" v-model="item.name"></el-input> </td>
                <td>  <el-input type="text" v-model="item.shortname"></el-input></td>
                <td><el-input  v-model="item.chemical"></el-input></td>
                <td>                 
                    <number-input
                        v-model="item.concentration"
                        :unit="item.unit"
                        :min="0" :max="1000000" class="cheminput" :step="1.0" :placeholder="String(0)"
                    />
                    <select class="unitselect" v-model="item.unit">
                        <option value="mg/l">mg/l</option>
                        <option value="μg/l">μg/l</option>
                        <option value="ng/l" selected>ng/l</option>
                    </select>
                </td>
                <td> <el-input type="number" v-model="item.PEQ"></el-input></td>
                <td> <el-input type="number" v-model="item.removalAKF" :min="0"  :max="1" :step="0.01" ></el-input> </td>
                <td>
                    <el-input type="number" v-model="item.removalRO" :min="0"  :max="1" :step="0.01"></el-input>
                </td>
                <td>
                    <el-input type="number" v-model="item.removalIEX" :min="0" :max="1" :step="0.01"></el-input>
                </td>
                <td>
                    <button @click="deleteRow(index+nPFAS, 'PFAS',item.name)" class="delete-button">X</button>
                </td>
            </tr>
            <tr>
                <td colspan="8" class="add-component" @click="addCustomComponent('PFAS')">{{ $t('models.groundwater.design.addCompound') }}</td> 
            </tr>
            
            <!-- Add more rows as needed  <number-input v-if="config['removal'][item.name]" v-model="config['removal'][item.name]['IEX']" :min=0 :max=100 class="cheminput" :step=1.0 :placeholder="String(0)" /> -->
        </tbody>
        </table>
        <br>

        <div>
        <h3>{{ $t('models.groundwater.design.user_input') }}</h3>

    <table >
        <thead>
            <tr>
                <th>{{ $t('models.groundwater.design.name') }}</th>
                <th>{{ $t('models.groundwater.design.chemical_formula') }}</th>
                <th>{{ $t('models.groundwater.design.concentration') }}</th>
                <th>{{ $t('models.groundwater.design.removal_akf') }}</th>
                <th>{{ $t('models.groundwater.design.removal_ro') }}</th>
                <th>{{ $t('models.groundwater.design.removal_iex') }}</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(item,index) in $project.scenario.metaData.customMicroComponents['Other']" :key="index" >
            <td><el-input type="text" v-model="item.name"></el-input> </td>

            <td><el-input v-model="item.chemical"></el-input></td>
            <td >                 
                <number-input v-model="item.concentration" :min=0 :max=1000 class="cheminput" :step=1.0 :placeholder="String(0)" />
                <select class="unitselect" v-model="item.unit">
                        <option value="mg/l">mg/l</option>
                        <option value="μg/l">μg/l</option>
                        <option value="ng/l" selected>ng/l</option>
                </select>
            </td>
            <td> <el-input type="number" v-model="item.removalAKF" :min="0"  :max="1" :step="0.01"></el-input> </td>
            <td>
                <el-input type="number" v-model="item.removalRO" :min="0"  :max="1" :step="0.01"></el-input>
            </td>
            <td>
                <el-input type="number" v-model="item.removalIEX"  :min="0" :max="1" :step="0.01"></el-input>
            </td>
            <td>
                <button @click="deleteRow(index, 'Other',item.name)" class="delete-button">X</button>
            </td>
            </tr>


            <tr>
                <td colspan="7" class="add-component" @click="addCustomComponent('Other')">{{ $t('models.groundwater.design.addCompound') }}</td> 
            </tr>
            <!-- Add more rows as needed -->
        </tbody>
    </table>

        </div>
    </div>
</template>

<script>

import components from './assets/components.js'

export default {
    name: 'Micropollutants',
    props: ['design', 'config'],
    data() {
        return {
            VOCparameters: components.micros[0]
        }
    },
    computed: {
        groundwaterParams() {
            return this.$project.modelParameters['groundwater'] || []
        },
        micropollutants() {
            return this.groundwaterParams.filter(param => param.category === '_composition' && param.section === '_micropollutants')
        },
        vocComponents() {
            return this.micropollutants.filter(param => param.uom === 'mg/l')
        },
        pfasComponents() {
            return this.micropollutants.filter(param => param.uom === 'ng/l')
        },
        nVOC() {
            return this.vocComponents.length
        },
        nPFAS() {
            return this.pfasComponents.length
        },
        groundwaterPfasFingerprint() {
            return this.pfasComponents
                .map(param => `${param.name}:${Number(this.config.parameters[param.name] || 0)}`)
                .join('|')
        }
    },


    watch: {
        groundwaterPfasFingerprint() {
            this.$project.scenario.unsolved = true
        },
        '$project.scenario.metaData.customMicroComponents': {
            deep: true, 
            handler() {
                this.$project.scenario.unsolved = true
            }
        }
    },

        
    methods: {
        deleteRow(index, compoundlist, itemName) {
            this.$project.scenario.metaData.customMicroComponents[compoundlist].splice(index, 1);
            delete this.$project.scenario.metaData.customMicroComponents[compoundlist][index] ;
        },
        
        assignName(index, item_name) {
            this.$project.scenario.metaData.customMicroComponents['PFAS'][index].name = item_name;
        },
        assignShortName(index, item_name) {
            this.$project.scenario.metaData.customMicroComponents['PFAS'][index].shortname = item_name;
        },
        assignPEQ(index, peq) {
            this.$project.scenario.metaData.customMicroComponents['PFAS'][index].PEQ = peq;
        },
        

        chemform(chemical) {
            if (chemical == "") { return "" }

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
        findHenryNumber(name, parameter) {
            for (const component of this.VOCparameters.components) {
                if ((component.name.toLowerCase() === name.toLowerCase())) {

                    return component[parameter];
                }
            }
            return 0;
        },
        addCustomComponent(name) {
            if (name === 'VOC') {
                this.$project.scenario.metaData.customMicroComponents[name].push({
                    name: '',
                    chemical: '',
                    henry: 0,
                    dw: 0,
                    dg: 0,
                    unit:'',

                });
            } else if (name === 'PFAS'){
                this.$project.scenario.metaData.customMicroComponents[name].push({
                    name: '',
                    shortname: '',
                    chemical: '',
                    PEQ: 1,
                    removalIEX: 1,
                    removalAKF: 1,
                    removalRO: 1,
                    adsorptionCapacity_simple: 100,
                    unit:'',

                    
                });
            } else {
                this.$project.scenario.metaData.customMicroComponents[name].push({
                    name: '',
                    chemical: '',

                    removalIEX: 1,
                    removalAKF: 1,
                    removalRO: 1,
                    unit:'',

                });
            }
        },

        }
    }

</script>

<style scoped>
#groundwater-composition .unitselect {
display: inline-block;
width: 40px;
height: 30px;
appearance: none;
position: relative;

}
#entireName {
    position: absolute;
    visibility: hidden;
}
button{
    width:auto;
    display: inline-block;
    height: auto;
    padding: 8px;
    text-align: center;

}
.Input {
    width: auto;
}
table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    
    border: 1px solid black;
    padding: 8px;
    text-align: center;
}
.add-component {
  background-color: bisque;
  cursor: pointer;
  text-align: center;
}
.add-component:hover {
  background-color: burlywood;
}
.delete-button {
    background-color: #ff0000; /* Red background */
    border: none; /* Remove border */
    color: white; /* White text */
    text-align: center; /* Centered text */
    text-decoration: none; /* Remove underline */
    display: inline-block;
    font-size: 14px; /* Smaller text size */
    margin: 4px 2px; /* Some margin */
    cursor: pointer; /* Mouse pointer on hover */
    border-radius: 50px; /* Large border radius for round corners */
}

.delete-button:hover {
    background-color: #b30000; /* Darker red on hover */
}
</style>