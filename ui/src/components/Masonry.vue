<script lang="ts">
import {
  ref,
  onMounted,
  onUpdated,
  onBeforeUnmount,
  defineComponent,
  useSlots,
  h,
} from 'vue';

export default defineComponent({
  name: 'MasonryGrid',
  props: {
    tag: {
      type: [String],
      default: 'div',
    },
    cols: {
      type: [Object, Number, String],
      default: 2,
    },
    gutter: {
      type: [Object, Number, String],
      default: 0,
    },
    css: {
      type: [Boolean],
      default: true,
    },
    columnTag: {
      type: [String],
      default: 'div',
    },
    columnClass: {
      type: [String, Array, Object],
      default: () => [],
    },
    columnAttr: {
      type: [Object],
      default: () => ({}),
    },
  },
  setup(props) {
    const slots = useSlots();
    const windowWidth = ref(0);
    const displayColumns = ref(0);
    const displayGutter = ref(0);
    const columns = ref<any[]>([]);

    const breakpointValue = (mixed, windowWidth: number) => {
      const valueAsNum = parseInt(mixed);

      if (valueAsNum > -1) {
        return mixed;
      } else if (typeof mixed !== 'object') {
        return 0;
      }

      let matchedBreakpoint = Infinity;
      let matchedValue = mixed.default || 0;

      for (let k in mixed) {
        const breakpoint = parseInt(k);
        const breakpointValRaw = mixed[breakpoint];
        const breakpointVal = parseInt(breakpointValRaw);

        if (isNaN(breakpoint) || isNaN(breakpointVal)) {
          continue;
        }

        const isNewBreakpoint =
          windowWidth <= breakpoint && breakpoint < matchedBreakpoint;

        if (isNewBreakpoint) {
          matchedBreakpoint = breakpoint;
          matchedValue = breakpointValRaw;
        }
      }

      return matchedValue;
    };

    const getColumns = () => {
      const cols = [];
      const childItems = slots?.default()[0]?.children;

      if (!childItems?.length) return [];

      // Loop through child elements
      for (
        let i = 0, visibleItemI = 0;
        i < childItems.length;
        i++, visibleItemI++
      ) {
        // Get the column index the child item will end up in
        const columnIndex = visibleItemI % displayColumns.value;

        if (!cols[columnIndex]) {
          cols[columnIndex] = [];
        }

        cols[columnIndex].push(childItems[i]);
      }
      return cols;
    };

    const reCalculate = () => {
      const previousWindowWidth = windowWidth.value;
      windowWidth.value = window ? window.innerWidth : null || Infinity;

      if (previousWindowWidth === windowWidth.value) {
        return;
      }

      reCalculateColumnCount(windowWidth.value);
      reCalculateGutterSize(windowWidth.value);
      columns.value = getColumns();
    };

    const reCalculateGutterSize = (windowWidth: number) => {
      displayGutter.value = breakpointValue(props.gutter, windowWidth);
    };

    const reCalculateColumnCount = (windowWidth: number) => {
      let newColumns = breakpointValue(props.cols, windowWidth);
      newColumns = Math.max(1, Number(newColumns) || 0);
      displayColumns.value = newColumns;
    };

    onMounted(() => {
      reCalculate();
      if (window) {
        window.addEventListener('resize', reCalculate);
      }
    });

    onUpdated(() => {
      reCalculate();
    });

    onBeforeUnmount(() => {
      if (window) {
        window.removeEventListener('resize', reCalculate);
      }
    });

    return () => {
      const columnsContainingChildren = getColumns();
      const isGutterSizeUnitless =
        parseInt(displayGutter.value) === displayGutter.value * 1;
      const gutterSizeWithUnit = isGutterSizeUnitless
        ? `${displayGutter.value}px`
        : displayGutter.value;

      const columnStyle = {
        width: `${100 / displayColumns.value}%`,
        display: ['-webkit-box', '-ms-flexbox', 'flex'],
        flexDirection: 'column',
        gap: gutterSizeWithUnit,
      };

      const columns = columnsContainingChildren.map((children, index) => {
        /// Create column element and inject the children
        return h(
          props.columnTag,
          {
            key: index + '-' + columnsContainingChildren.length,
            style: props.css ? columnStyle : null,
            class: props.columnClass,
            attrs: props.columnAttr,
          },
          children
        ); // specify child items here
      });

      const containerStyle = {
        display: ['-webkit-box', '-ms-flexbox', 'flex'],
        gap: gutterSizeWithUnit,
      };

      // Return wrapper with columns
      return h(
        props.tag, // tag name
        props.css ? { style: containerStyle } : null, // element options
        columns // column vue elements
      );
    };
  },
});
</script>