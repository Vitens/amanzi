<template>
    <div id="micros">
        <h3 id="micros-title">{{ $t('models.groundwater.design.pfas') }}</h3>
    <table id="micros-table">
        <thead>
            <tr>
                <th>{{ $t('models.groundwater.design.name') }}</th>
                <th>{{ $t('models.activatedcarbon.design.freundlich_k') }}</th>
                <th>{{ $t('models.activatedcarbon.design.freundlich_1n') }}</th>
                <th>{{ $t('models.groundwater.design.pfoa-factor') }}</th>
                <th>{{ $t('models.groundwater.design.concentration') }}</th>
            </tr>
        </thead>
        <tbody>
            <tr>
              <td>-</td>
              <td>µg/g/L/µg</td>
              <td>-</td>
              <td>-</td>
              <td>ng/L</td>
            </tr>
            <tr v-for="compound in pfasList" :key="compound">
              <td>{{ compound }} </td>
              <td>
                <number-input v-model="config.parameters[compound + '_Freundlich_k']" :min="0" :max="100000"></number-input>

              </td>
              <td>
                <number-input v-model="config.parameters[compound + '_Freundlich_1n']" :min="0" :max="1"></number-input>
              </td>
                <td>
                    <number-input v-model="config.parameters[compound + '_PEQ']" :min="0" :max="1"></number-input>
                </td>
                <td>{{ PFAS_influentConcentration(compound).toFixed(2) }}</td>
            </tr>
        </tbody>
    </table>
    <br>
    <h3 id="micros-doc-title">{{ $t('models.activatedcarbon.design.doc_params') }}</h3>
    <table id="micros-table">
        <thead>
            <tr>
                <th>{{ $t('models.groundwater.design.name') }}</th>
                <th>{{ $t('models.activatedcarbon.design.freundlich_k') }}</th>
                <th>{{ $t('models.activatedcarbon.design.freundlich_1n') }}</th>
                <th>{{ $t('models.groundwater.design.pfoa-factor') }}</th>
            </tr>
        </thead>
        <tbody>
            <tr>
              <td>-</td>
              <td>µg/g/L/µg</td>
              <td>-</td>
              <td>-</td>
            </tr>
            <tr>
              <td>DOC</td>
              <td>
                <number-input v-model="config.parameters['DOC_Freundlich_k']" :min="0" :max="100000"></number-input>
              </td>
              <td>
                <number-input v-model="config.parameters['DOC_Freundlich_1n']" :min="0" :max="1"></number-input>
              </td>
              <td>-</td>
            </tr>

        </tbody>
    </table>
</div>
</template>

<script>
export default {
    name: 'Micropollutants',
    props: ['config'],
    computed: {
        pfasList() {
            return Object.keys(this.$runtime.designState.model?.PFAS ?? {})
        },
    },
    methods: {
        PFAS_influentConcentration(compound) {
            return this.$runtime.designState.model?.PFAS?.[compound] ?? 0
        },
    },
}



</script>

<style scoped>
#micros {
    margin-top: 20px;
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
#micros-table {
    width: 60%;
    border-collapse: collapse;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
}
#micros-title {
    text-align: center;
}
</style>