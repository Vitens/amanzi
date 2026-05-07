<template>
  <div id="library">
    <div id="filter">
      <el-row :gutter="10">
        <el-col :span="17">
          <el-input v-model="filter" :placeholder="$t('ui.sidebar.library.filter')" clearable>
            <template #prefix>
              <el-icon class="el-input__icon">
                <search />
              </el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="7">
          <el-radio-group v-model="displayMode">
            <el-radio-button label="grid"><el-icon size="16px"><Grid /></el-icon></el-radio-button>
            <el-radio-button label="list"><el-icon size="16px"><Expand /></el-icon></el-radio-button>
          </el-radio-group>
        </el-col>

      </el-row>

    </div>
    <el-scrollbar max-height="545px" v-if="displayMode == 'grid'">
      <template v-for="category in categories">
        <div class="blocks-category">{{ $t('ui.sidebar.library.categories.'+category) }}</div>
        <div id="blocks-grid">
          <el-tooltip
          class="box-item"
          effect="dark"
          :show-after="500"
          :enterable="false"
          :content="$t('models.'+block.name+'.name')"
          placement="top-start"
          v-for="block in filteredBlocks(category)" :key="block.name"
          >
          <div class="block" :style="{ 'background-image': getImageUrl(block) }" 
          draggable="true" @dragstart="startDrag(block.name, $event)"  @dblclick="addModel(block)">
          </div>
          </el-tooltip>
        </div>
      </template>
    </el-scrollbar>
    <div id="blocks-list" v-else>
      <el-scrollbar max-height="325px">
        <template v-for="category in categories">
          <div class="blocks-category">{{ $t('ui.sidebar.library.categories.'+category) }}</div>
          <div class="block-li" v-for="block in filteredBlocks(category)" draggable="true" @dragstart="startDrag(block.name, $event)" @dblclick="addModel">
            <div class="image" :style="{ 'background-image': getImageUrl(block) }" :key="block.name">
            </div>
            <div class="name">
              {{ $t('models.'+block.name+'.name')}}
            </div>
          </div>
        </template>
      </el-scrollbar>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      filter: '',
      displayMode: 'grid',
    };
  },
  computed: {
    categories() {
      // get all non hidden blocks
      var blocks = Object.values(this.modelspec).filter(block => !block.hidden);
      // extract unique categories
      return [...new Set(blocks.map(block => block.category))];

    },
  },
  methods: {
    filteredBlocks(category) {
      var blocks = Object.values(this.modelspec).filter(block =>
        this.$t('models.'+block.name+'.name').toLowerCase().includes(this.filter.toLowerCase())
      );
      console.log(blocks);
      // remove blocks that have a hidden property
      blocks = blocks.filter(block => !block.hidden);
      blocks = blocks.filter(block => block.category == category);

      return blocks.sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    },
    addModel(block) {

      var position = {}
      const models = this.$project.scenario.models
      // if no models, set to window position
      if(models.length == 0) { 

        var zoom = this.$interface.canvas.zoom

        position = {x: (-this.$interface.canvas.left + 100) / zoom, y: (-this.$interface.canvas.top + 100) / zoom}
        position.y += 200
      }
      // else, get min y and max x
      else {
        var minY = Math.min(...models.map(m => m.position.y))
        var maxX = Math.max(...models.map(m => m.position.x))
        position = {x: maxX + 200, y: minY}
      }
      let name = this.$t('models.'+block.name+'.name')

      let defaults = this.$project.modelParameters[block.name]

      this.$project.scenario.addModel(this.modelspec, this.$project.modelParameters[block.name],block.name, name, position, true);
    },
    getImageUrl(block) {
      const imageUrl = new URL(`../models/${block.name}/assets/block.png`, import.meta.url).href;
      return `url(${imageUrl})`;
    },
    startDrag(name, evt) {
      // emit transfer to bus, as dataTransfer is not available during dragging
      this.$bus.emit('dragStart');
      evt.dataTransfer.setData('text/plain', name);
      evt.dataTransfer.dropEffect = 'copy';
      evt.dataTransfer.effectAllowed = 'all';
    },
  },
};
</script>

<style>
#blocks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 72px);
  grid-gap: 5px;
  width: 320px;
  margin: 5px 0px;
}

.blocks-category {
  font-size: 12px;
  background: #DDD;
  padding: 0px 7px;
  border: 1px solid #CCC;
}

.block {
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
  width: 72px;
  height: 72px;
  margin-right: 5px;
  border: 1px solid #AAA;
  box-sizing: border-box;
  display: inline-block;
  cursor: move;
}

.block-li {
  border-bottom: 1px solid #DDD;
  cursor: move;
  height: 50px;
}
.block-li .image {
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
  width: 40px;
  height: 40px;
  margin: 3px;
  border: 1px solid #DDD;
  float: left;
}
.block-li .name {
  display: inline-block;
  font-size: 15px;
  padding: 13px 10px;
}

#filter {
  margin-bottom: 10px;
}
#filter .el-radio-button__inner {
  padding: 5px 11px;
}

.box-item {
  pointer-events: none;
}
</style>
