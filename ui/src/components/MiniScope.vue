<template>
  <div class="mini-scope">
    <table>
      <tbody>
        <tr v-for="(item, index) in components" :key="index">
          <td class="label">{{ item.label }}</td>
          <td class="value">{{ item.value }}</td>
          <td class="uom">{{ item.uom }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    components: {
      type: Array,
      default: () => [],
    },
  },
};
</script>

<style>
.mini-scope {
  border-radius: 5px; /* Rounded corners for the container */
  overflow: hidden; /* Clip any overflowing content */
  background-color: #FAFAFA;
  position: absolute;
  border: 1px solid #AAA;
}

.mini-scope table {
  font-size: 12px;
  font-weight: bold;
  width: 100%; 
  border-collapse: collapse; 
}

.mini-scope table td {
  padding: 1px 4px;
}

.mini-scope .label {
  padding-left: 3px;
  font-weight: 500;
  color: #666;
  /* border-bottom: 1px solid #ccc; Light gray line between rows */
}
.mini-scope .value {
  padding-left: 3px;
  text-align:center;
  font-weight: 500;
  color: #666;
  /* border-bottom: 1px solid #ccc; Light gray line between rows */
}
.mini-scope .uom {
  padding-left: 2px;
  font-weight: 200;
  color: #666;
}

.mini-scope tr {
  border-bottom: 1px solid #cccccc8b; /* Light gray line between rows */
}

.mini-scope tr:last-child {
  border-bottom: none;
}
</style>