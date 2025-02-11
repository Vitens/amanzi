<template>
  <svg xmlns="http://www.w3.org/2000/svg" id='marker-svg'>
    <defs>
      <marker id="arrow-product" markerWidth="6" markerHeight="6" refX="2" refY="2" orient="auto" markerUnits="strokeWidth"> <path d="M0,0 L0,4 L4,2 z" fill="#1B78F6"></path></marker>
      <marker id="arrow-selected" markerWidth="6" markerHeight="6" refX="2" refY="2" orient="auto" markerUnits="strokeWidth"> <path d="M0,0 L0,4 L4,2 z" fill="orange"></path></marker>
      <marker id="arrow-flush" markerWidth="6" markerHeight="6" refX="2" refY="2" orient="auto" markerUnits="strokeWidth"> <path d="M0,0 L0,4 L4,2 z" fill="#409EFF"></path></marker>
      <marker id="arrow-waste" markerWidth="6" markerHeight="6" refX="2" refY="2" orient="auto" markerUnits="strokeWidth"> <path d="M0,0 L0,4 L4,2 z" fill="brown"></path></marker>
      <marker id="arrow-new" markerWidth="6" markerHeight="6" refX="2" refY="2" orient="auto" markerUnits="strokeWidth"> <path d="M0,0 L0,4 L4,2 z" fill="#333"></path></marker>
    </defs>
  </svg>
</template>
<style>
#marker-svg {
  left: 0px;
  top: 0px;
  position: absolute;
  pointer-events: none;

}
</style>