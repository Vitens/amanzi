<template>
  <div id="loading" :class="{loading: $interface.loading}">
    <div class="bar"></div>
  </div>
</template>
<style>
#loading {
  position: fixed;
  top: -8px;
  left: 0px;
  right: 0px;
  z-index: 100000;
  height: 7px;
  border-bottom: 1px solid #66b1ff;
  background: #66b1ff;
  transition: all 0.1s ease-out;
}
#loading.loading {
  top: 0px;
}
#loading .bar {
  position: absolute;
  width: 100%;
  height: 100%;
  transform-origin: 0% 50%;
  background: linear-gradient(90deg, transparent, rgb(176, 239, 255) 90%, transparent);
  animation: loading 1.2s linear infinite;
}
@keyframes loading {
  0% {
    transform:  translateX(0) scaleX(0);
  }
  40% {
    transform:  translateX(0) scaleX(0.6);
  }
  100% {
    transform:  translateX(100%) scaleX(0.8);
  }
}


</style>