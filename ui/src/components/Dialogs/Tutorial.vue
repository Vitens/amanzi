<template>
      <div class="tutorial-content">

        <div class="tutorial-image">
          <transition name="fade" mode="out-in" v-if="currentStep === 0">
            <img :src="currentTutorial" alt="Tutorial Animation" :key="currentStep" v-if="currentStep === 0"> 
          </transition>
          <transition name="fade" mode="out-in" v-if="currentStep > 0">
            <video :src="currentTutorial" autoplay muted loop :key="currentStep" ></video>
          </transition>
          <div class="tutorial-gradient-overlay"></div>
        </div>

        <div class="tutorial-text">
          <transition name="slide-fade" mode="out-in">
            <div :key="currentStep">
              <h3>{{ $t('tutorial.' + currentStep + '.title') }}</h3>
              <p v-html="$t('tutorial.' + currentStep + '.body').replace(/\n/g, '<br>')"></p>
            </div>
          </transition>
        </div>
      </div>
    <div class="tutorial-controls">
      <el-checkbox class="skip" @change="skipTutorial" border>{{ $t('ui.tutorial.skip') }}</el-checkbox>
      <el-button :disabled="currentStep === 0" type="default" @click="currentStep--">{{ $t('ui.tutorial.previous') }}</el-button>
      <el-button :disabled="currentStep === tutorials.length - 1" type="default" @click="currentStep++">{{ $t('ui.tutorial.next') }}</el-button>
      <el-button type="primary" @click="closeTutorial">{{ $t('ui.tutorial.close') }}</el-button>
    </div>
</template>

<script>
import Tutorial1 from '@/assets/tutorial/Tutorial-1.png'
import Tutorial2 from '@/assets/tutorial/Tutorial-2.mp4'
import Tutorial3 from '@/assets/tutorial/Tutorial-3.mp4'
import Tutorial4 from '@/assets/tutorial/Tutorial-4.mp4'
import Tutorial5 from '@/assets/tutorial/Tutorial-5.mp4'
import Tutorial6 from '@/assets/tutorial/Tutorial-6.mp4'
import Tutorial7 from '@/assets/tutorial/Tutorial-7.mp4'

export default {
    name: 'Tutorial',
    data() {
        return {
            currentStep: 0,
            tutorials: [Tutorial1, Tutorial2, Tutorial3, Tutorial4, Tutorial5, Tutorial6, Tutorial7]
        }
    },
    computed: {
        currentTutorial() {
            return this.tutorials[this.currentStep]
        }
    },
    methods: {
        closeTutorial() {
            this.$project.tutorial = false
        },
        skipTutorial() {
            // Set cookie to remember tutorial has been skipped
            this.$cookies.set('tutorial-skip', true, '300d')
        }
    }
}
</script>

<style>

.tutorial-controls {
    position: relative;
    bottom: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 20px;
}

.tutorial-controls .backward,
.tutorial-controls .forward {
    background-color: rgb(241, 241, 245);
    color: black;
}

.tutorial-controls .close {
    background-color: rgb(51, 126, 204);
    color: white;
}

.tutorial-controls .skip {
    background-color: transparent;
    color: black;
}

.tutorial-content {
    width: 90%;
    height: 400px;
    display: flex;
    flex-direction: row;
    gap: 50px;
    flex: 1 1 auto;
}


.tutorial-image img {
    object-fit: contain;
    width: 100%;
    height: 100%;
    transform-origin: top left;
}

.tutorial-image {
    flex: 1 0 auto;
    position: relative;
    width: 75%;
    height: 100%;
}

.tutorial-image video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.tutorial-text {
    position: relative;
    width: auto;
    min-width: 25%;
    height: auto;
    flex: 1 1 auto;
}

.tutorial-gradient-overlay {
    position: absolute;
    top: 0;
    right: 0px;
    width: 12%;
    height: 100%;
    background: linear-gradient(
        to right,
        rgba(255, 255, 255, 0) 0%,
        /* rgba(255, 255, 255, 0.5) 30%, */
        rgba(255, 255, 255, 1) 100%
    );
    pointer-events: none;
}

#tutorial-title {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    background-color: blue;
    padding: 5px 15px;
    border-radius: 4px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.25s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.25s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(30px);
  opacity: 0;
}
</style>
