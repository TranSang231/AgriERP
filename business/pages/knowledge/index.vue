<template>
    <div class="pt-24 p-6 bg-gray-50 min-h-screen">
      <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Users Stats -->
            <el-card>
            <div class="flex items-center">
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <el-icon :size="24" class="text-blue-600">
                    <User />
                </el-icon>
                </div>
                <div class="ml-4" v-if="generalSatistics">
                <p class="text-sm font-medium text-gray-600">{{ t('Total_users') }}</p>
                <p class="text-2xl font-bold text-gray-900">{{ generalSatistics.total_users }}</p>
                </div>
            </div>
            </el-card>
    
            <!-- Namespaces Stats -->
            <el-card>
            <div class="flex items-center">
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <el-icon :size="24" class="text-green-600">
                    <Document />
                </el-icon>
                </div>
                <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">{{ t('Total_namespaces') }}</p>
                <p class="text-2xl font-bold text-gray-900">{{ generalSatistics.total_namespaces }}</p>
                </div>
            </div>
            </el-card>
    
            <!-- Pages Stats -->
            <el-card>
            <div class="flex items-center">
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <el-icon :size="24" class="text-purple-600">
                    <Folder />
                </el-icon>
                </div>
                <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">{{ t('Total_pages') }}</p>
                <p class="text-2xl font-bold text-gray-900">{{ generalSatistics.total_pages }}</p>
                </div>
            </div>
            </el-card>
        </div>
        <el-card v-if="pagesCreatedCharData">
            <Line
                :data="pagesCreatedCharData"
                :options="{
                    responsive: true,
                    maintainAspectRatio: false
                }"
            />
        </el-card>
    </div>
  </template>
  
<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { User, Document, Folder } from '@element-plus/icons-vue';
import { formatDate } from '@/utils/time';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

import StatisticService from '@/services/knowledge/statistic';
  
definePageMeta({
layout: 'knowledge',
});

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);
  
const { t } = useI18n();

const generalSatistics = ref({
total_users: 0,
total_namespaces: 0,
total_pages: 0
});

const pagesCreatedByDate = ref([]);

const pagesCreatedCharData = computed(() => {
    const items = pagesCreatedByDate.value as any;
    if (!items || items.length === 0) {
        return null;
    }
    console.log(items);
    const labels = items.map((o: any) => o.date);
    const data = items.map((o: any) => o.count);
    return {
        labels,
        datasets: [
            {
            label: t('Pages_created_by_date'),
                backgroundColor: '#f87979',
                data
            }
        ]
    };
});

const addMissingDates = (rawData: any) => {
    const { start_date, end_date , data} = rawData;
    console.log(start_date, end_date);
    let results: any[] = [];
    const currentDate = new Date(start_date);
    const endDate = new Date(end_date);
    while (currentDate <= endDate) {
        const dateString = formatDate(currentDate);
        console.log(dateString);
        currentDate.setDate(currentDate.getDate() + 1);
        let item = data.find((o: any) => o.date == dateString);
        if (!item) {
            item = {
                date: dateString,
                count: 0
            }
        }
        results = [...results, item];

    }
    return results;
}
  
onMounted(() => {
    StatisticService.getGeneralStatistics()
        .then((response: any) => {
            generalSatistics.value = response;
        })
        .catch((e: any) => {
            console.error(e);
        });
    StatisticService.getPagesCreatedByDate()
        .then((response: any) => {
            pagesCreatedByDate.value = addMissingDates(response);
        })
        .catch((e: any) => {
            console.error(e);
        })
});
</script>