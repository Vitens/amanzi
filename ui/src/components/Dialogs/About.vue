<template>
  <div class="about-dialog">
    <img class="vitens-logo" src="/logo.jpg" alt="Vitens logo">
    <div class="amanzi-logo"></div>
    <div class="about-text">
      <h1>Amanzi v{{ $version }}</h1>
      <p>{{ $t('ui.dialogs.about.developed_by') }}</p>
      <p class="remark">{{ $t('ui.dialogs.about.remark') }}</p>
    </div>
    <el-collapse accordion>
      <el-collapse-item name="changelog">
        <pre>{{ changelog }}</pre>
        <template #title><i class="fa fa-history"></i> {{ $t('ui.dialogs.about.changelog') }}</template>
      </el-collapse-item>
      <el-collapse-item name="acknowledgements">
        <pre>{{ acknowledgements }}</pre>
        <template #title><i class="fa fa-users"></i> {{ $t('ui.dialogs.about.acknowledgements') }}</template>
      </el-collapse-item>
      <el-collapse-item name="citation">
        <div class="citation-section">
          <p class="citation-hint">
            {{ $t('ui.dialogs.about.citation.description') }}
          </p>
          <div class="citation-block">
            <h3>{{ $t('ui.dialogs.about.citation.plain_text') }}</h3>
            <pre>{{ plainTextCitation }}</pre>
            <el-button size="small" @click="copyCitation(plainTextCitation)">
              {{ $t('ui.dialogs.about.citation.copy_plain_text') }}
            </el-button>
          </div>
          <div class="citation-block">
            <h3>{{ $t('ui.dialogs.about.citation.bibtex') }}</h3>
            <pre>{{ bibtexCitation }}</pre>
            <el-button size="small" @click="copyCitation(bibtexCitation)">
              {{ $t('ui.dialogs.about.citation.copy_bibtex') }}
            </el-button>
          </div>
        </div>
        <template #title><i class="fa fa-quote-right"></i> {{ $t('ui.dialogs.about.citation.title') }}</template>
      </el-collapse-item>
      <el-collapse-item :title="$t('ui.dialogs.about.license')" name="license">
        <pre>{{ license }}</pre>
        <template #title><i class="fa fa-balance-scale"></i> {{ $t('ui.dialogs.about.license') }}</template>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>
<script>
import changelog from '@@/changelog.md?raw'
import acknowledgements from '@@/ACKNOWLEDGEMENTS?raw'
import license from '@@/LICENSE?raw'
export default {
  computed: {
    plainTextCitation() {
      return `Vitens. Amanzi (Version ${this.$version}) [Computer software]. ${new Date().getFullYear()}. https://github.com/Vitens/Amanzi`
    },
    bibtexCitation() {
      return `@software{amanzi_${new Date().getFullYear()},\n  author = {Vitens},\n  title = {Amanzi},\n  version = {${this.$version}},\n  year = {${new Date().getFullYear()}},\n  url = {https://github.com/Vitens/Amanzi}\n}`
    }
  },
  methods: {
    copyCitation(value) {
      if (navigator?.clipboard?.writeText) {
        navigator.clipboard.writeText(value)
        return
      }

      const textarea = document.createElement('textarea')
      textarea.value = value
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.focus()
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }
  },
  data() {
    return {
      changelog,
      acknowledgements,
      license
    }
  }
}
</script>

<style>
.about-dialog {
  width: 600px;
}
.about-text {
  padding: 20px 50px;
  text-align: center;
}
.vitens-logo {
  display: block;
  width: 180px;
  max-width: 100%;
  height: auto;
  margin: 16px auto 0;
  padding: 6px 0 18px;
}
.amanzi-logo {
  width: 500px;
  margin-left: 50px;
  margin-top: 20px;
  height: 80px;
  background-image: url('@/assets/logo.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
}
.about-dialog pre {
  max-height: 500px;
  font-size: 11px;
  background-color: #f5f7fa;
  padding: 10px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  text-align: justify;
}
.about-dialog .el-collapse-item__header {
  font-size: 1.0em;
}
.about-dialog .el-collapse-item__header i {
  margin-right: 10px;
  font-size: 1.0em;
}
.remark {
  font-size: 0.9em;
  color: #666;
  text-align: justify;
}
.citation-section {
  margin-top: 4px;
  text-align: left;
}
.citation-hint {
  margin-bottom: 12px;
}
.citation-block {
  margin-bottom: 12px;
}
.citation-block h3 {
  margin-bottom: 6px;
  font-size: 1em;
}
.citation-block pre {
  margin: 0 0 8px;
}
</style>