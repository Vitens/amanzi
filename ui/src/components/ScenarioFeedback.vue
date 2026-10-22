<template>
  <Transition name="scenario-feedback">
    <div v-if="feedback" class="scenario-feedback" :key="feedback.messageKey">
      {{ $t(feedback.messageKey) }}
    </div>
  </Transition>
</template>

<script>
export default {
  computed: {
    feedback() {
      return this.$interface?.lastScenarioFeedback ?? null
    }
  }
}
</script>

<style scoped>
.scenario-feedback {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 20;
  padding: 14px 24px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  font-size: 15px;
  font-weight: 500;
  color: #409EFF;
  border: 1px solid rgba(64, 158, 255, 0.25);
}
.scenario-feedback-enter-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.scenario-feedback-leave-active {
  transition: opacity 0.4s ease 0.2s, transform 0.4s ease 0.2s;
}
.scenario-feedback-enter-from,
.scenario-feedback-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.92);
}
</style>
