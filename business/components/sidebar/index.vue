<template>
    <div class="absolute sm:relative flex flex-col z-20 sm:bg-primary min-h-screen">
        <div class="flex sm:hidden h-16 items-center px-2">
            <el-button size="large" :icon="showMobiSideBar ? Expand : Fold" @click="toggleMobileSideBar"></el-button>
        </div>
        <SideBarContent v-if="showMobiSideBar" class="block sm:hidden" :isMobile="true">
            <template #header>
                <slot name="header" />
            </template>
            <template #default>
                <slot />
            </template>
        </SideBarContent>
        <SideBarContent class="hidden sm:block" :isMobile="false">
            <template #header>
                <slot name="header" />
            </template>
            <template #default>
                <slot />
            </template>
        </SideBarContent>
    </div>
</template>

<script lang="ts" setup>
import { Expand, Fold } from '@element-plus/icons-vue'
import SideBarContent from './content.vue'

const showMobiSideBar = ref(false)

const toggleMobileSideBar = () => {
    showMobiSideBar.value = !showMobiSideBar.value;
}
</script>