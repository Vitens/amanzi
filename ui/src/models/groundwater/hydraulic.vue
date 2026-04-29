<template>
    <svg>
        <circle :cx="x0+width/2" :cy="y0" r="20" stroke="black" stroke-width="3" fill="transparent" />
        <polygon :points="trianglePoints" style="fill:black;stroke:black;stroke-width:3" />
    </svg>

</template>
<script>
import hydraulicLine from '@/mixins/hydraulicline'

export default {
    name: 'hydraulic-groundwater',
    mixins: [hydraulicLine],
    computed: {
        anchorpoints() {
            return {
                out: { x: this.x0+this.width/2, y: this.y0-20, anchor: 'top' }
            }
        },
        boosterElevation() {
            return 0
        },
        y0() {
            return this.y(this.depth)
        },
        depth() {
            return this.params.average_groundwater_level - this.params.average_drawdown
        },
        dimensions() {
            return {
                bottom: this.depth,
                top: 0
            }
        },
    trianglePoints() {
            const cx = this.x0+this.width/2;
            const cy = this.y0;
            const r = 18;

            const string = `${cx},${cy - r} ${cx - r * 0.866},${cy + r / 2} ${cx + r * 0.866},${cy + r / 2}`;
            return string
        }
    },
}
</script>
<style></style>
