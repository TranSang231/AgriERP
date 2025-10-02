<template>
  <div class="h-screen w-full flex justify-center items-center">
    <div>
      <p>Todo: Use svg to draw the organization chart, let user collapse/expand nodes, allow them download the chart as image.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'hrm'
})

import { Download } from '@element-plus/icons-vue'
import UnitService from '@/services/organization/units';
import { toBlob } from 'html-to-image';
import { useOauthStore } from '@/stores/oauth';
import Unit from '~/components/organization/Unit.vue';
import UnitLinks from '~/components/organization/UnitLinks.vue';
import Members from '~/components/organization/Members.vue';
const oauthStore = useOauthStore();

const loading = ref(false);
const exporting = ref(false);
const units = ref([]);
const zoom = ref(1)
const ZOOM_SPEED = 0.05;
const numberOfRedrawn = ref(0);
const fetchData = async () => {
  loading.value = true;
  UnitService.tree()
    .then((response: any) => {
      units.value = response;
    })
    .catch((error: any) => {
      // this.$toast.error("Could not load data");
    })
    .finally(() => {
      loading.value = false;
    });
}

onMounted(() => {
  fetchData();
})

const printOrganizationChart = async () => {
  var element = document.getElementById("organization-chart-container");
  if (!element) return
  let width = element.scrollWidth,
    height = element.scrollHeight;
  const scaleRegex = /scale\((.*?)\)/;
  const matches = element.style.transform.match(scaleRegex);
  let scale = matches ? parseFloat(matches[1]) : 1.0;
  width *= scale;
  height *= scale;
  const options = { width, height };
  exporting.value = true;
  toBlob(element, options)
    .then(function (blob) {
      if (window.saveAs) {
        window.saveAs(blob, "organization.png");
      } else {
        saveAs(blob, "organization.png");
      }
    })
    .finally(() => {
      exporting.value = false;
    });
},
  scrollToZoom = (e: WheelEvent) => {
    const component = document.getElementById("organization-chart-container");
    const orgOuterBox = document.getElementById("org-outer-box");
    if (!component || !orgOuterBox) return;
    const ratioX = orgOuterBox.scrollLeft / orgOuterBox.scrollWidth;
    const ratioY = orgOuterBox.scrollTop / orgOuterBox.scrollHeight;
    if (e.deltaY < 0) {
      zoom.value = zoom.value + ZOOM_SPEED;
      component.style.transform = `scale(${zoom.value})`;
    } else {
      if (zoom.value - ZOOM_SPEED > 0) {
        zoom.value = zoom.value - ZOOM_SPEED;
        component.style.transform = `scale(${zoom.value})`;
      }
    }
    orgOuterBox.scrollLeft = ratioX * orgOuterBox.scrollWidth;
    orgOuterBox.scrollTop = ratioY * orgOuterBox.scrollHeight;
  }
const scrollViewToCenter = () => {
  const firstUnit =
    units.value && units.value.length > 0 ? units.value[0] : null;
  if (firstUnit) {
    const rootUnitBlockRef = document.querySelector(
      `[ref="unit-${firstUnit.id}"] .content-block`
    );
    if (rootUnitBlockRef) {
      rootUnitBlockRef.scrollIntoView({
        behavior: "smooth",
        inline: "center",
      });
    }
  }
}
const unitRenderCallback = () => {
  numberOfRedrawn.value++;
}
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
}
.org-outer-box {
  overflow: auto;
  width: 100%;
  height: calc(100vh - 150px);
  border: 1px solid gray;
  background-color: aliceblue;

  .organization-chart-container {
    flex: 0 0 auto;
    position: relative;
    z-index: 1;
    cursor: all-scroll;
    transform-origin: left top;
  }

  .path-container {
    position: absolute;
    top: 0px;
    z-index: -1;
  }
}

</style>