<template>
  <div class="copy-button">
    <el-button @click="copy" size="small" icon="CopyDocument" :class="{copied: copytext != 'Copy'}">{{ copytext }}</el-button>
  </div>
</template>
<script>
import { snapdom } from '@zumer/snapdom'

export default {
  props: {
    target: {
      type: String,
      required: true
    },
    image: {
      type: Boolean,
      default: false
    },
    beforeCopy: {
      type: Function,
      default: () => {}
    },
    afterCopy: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      copytext: 'Copy'
    }
  },
  methods: {
    async copy() {
      await this.beforeCopy()

      if (this.image) {
        await this.copyImage()
      } else {
        this.copyText()
      }

      await this.afterCopy()

      this.copytext = 'Copied!';
      setTimeout(() => {
        this.copytext = 'Copy';
      }, 800);
    },
    async copyImage() {
      let node = document.querySelector(this.target);
      let blob = await snapdom.toBlob(node, {type: 'png'});

      const item = new ClipboardItem({
        'image/png': blob
      });
      await navigator.clipboard.write([item]);
      console.log('copied image to clipboard');
    },

    copyText() {

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