<template>
  <div class="copy-button">
    <el-button @click="copy" size="small" icon="CopyDocument" :class="{copied: copytext != 'Copy'}">{{ copytext }}</el-button>
  </div>
</template>
<script>

export default {
  props: ['target', 'short'],
  data() {
    return {
      copytext: 'Copy'
    }
  },
  methods: {
    copy() {
      this.copytext = 'Copied!';
      setTimeout(() => {
        this.copytext = 'Copy';
      }, 800);

      // select and copy table to clipboard
      let range = document.createRange();
      let node = document.querySelector(this.target);
      range.selectNode(node);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
      document.execCommand('copy');
      window.getSelection().removeAllRanges();
    }
  }
}

</script>
<style>
.copy-button .copied span {
  /* blink for 0.1 second */
  animation: blink 0.5s;
}

@keyframes blink {
  0% {
    color: var(--el-color-primary);
  }
  50% {
    color: #355d86;
  }
  100% {
    color: var(--el-color-primary);
  }
}
</style>