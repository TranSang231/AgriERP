<template>
  <div class="flex flex-col bg-primary">
    <el-col>
      <el-menu
        class="el-menu-sidebar"
        :collapse="!isMobile && isCollapse"
        @open="handleOpen"
        @close="handleClose"
        :router="true"
        :default-active="$route.fullPath"
      >
        <div
          v-if="!isCollapse"
          class="text-white flex flex-col items-center pt-2"
        >
          <slot name="header" />
          <el-divider border-style="solid" class="my-4"/>
          <div
            v-if="!isCollapse && !isMobile"
            class="hidden sm:block absolute self-end px-3 py-2"
            @click="collapseSideBar"
          >
            <el-icon color="white" style="cursor: pointer">
              <DArrowLeft />
            </el-icon>
          </div>
        </div>
        <div
          v-if="isCollapse && !isMobile"
          class="flex flex-col items-center px-3 py-2"
          @click="expandSideBar"
        >
          <el-icon color="white" style="cursor: pointer">
            <DArrowRight />
          </el-icon>
        </div>
        <slot />
      </el-menu>
    </el-col>
  </div>
</template>

<script lang="ts" setup>
import { DArrowLeft, DArrowRight } from "@element-plus/icons-vue";
const props = defineProps({
  isMobile: {
    type: Boolean,
    default: false,
  },
});
const isCollapse = ref(props.isMobile);

const collapseSideBar = () => {
  isCollapse.value = true;
};
const expandSideBar = () => {
  isCollapse.value = false;
};

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
</script>

<style>
.el-menu-sidebar:not(.el-menu--collapse) {
  width: 220px;
  min-height: 400px;
}
</style>
