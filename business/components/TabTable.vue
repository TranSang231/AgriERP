<template>
    <el-tabs v-model="activeName" type="card" class="border-none">
        <el-tab-pane v-for="(tab, index) in tabs" :key="index" :label="tab.label" :name="tab.name"
            class="custom-tab-pane">
            <div class="tab-content p-4 border border-t-0 border-red-700 rounded-b-lg ">
                {{ tab.content }}
            </div>
        </el-tab-pane>
    </el-tabs>
</template>

<script setup>
import { ref } from 'vue';

const activeName = ref('1');
const tabs = ref([
    { name: '1', label: 'Tab name', content: 'Content of Tab 1' },
    { name: '2', label: 'Tab name', content: 'Content of Tab 2' },
    { name: '3', label: 'Tab name', content: 'Content of Tab 3' },
    { name: '4', label: 'Tab name', content: 'Content of Tab 4' },
    { name: '5', label: 'Tab name', content: 'Content of Tab 5' },
]);
</script>