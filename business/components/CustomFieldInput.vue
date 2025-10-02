<template>
    <div>
        <el-date-picker v-if="dataType === 'DateField' || dataType === 'DateTimeField'"
            v-model="model"
            :type="dataType === 'DateField' ? 'date': 'datetime'"
            :placeholder="dataType === 'DateField' ? $t('pick_a_day') : $t('pick_date_time')"
            :format="dataType === 'DateField' ? FORMAT.DATE : FORMAT.DATE_TIME"
            :value-format="dataType === 'DateField' ? FORMAT.DATE : FORMAT.DATE_TIME"
        />
        <el-input v-else
            :type="inputType"
            v-model="model"
        />
    </div>
</template>

<script setup lang="ts">
import { FORMAT } from '@/utils/time';
const props = defineProps({
    dataType: {
        type: String,
        default: false
    },
    maxLength: {
        type: Number,
        default: 50,
    },
});

const model = defineModel();
const inputType = computed(() => {
    const typesMap = {
        CharField: 'text',
        TextField: 'text',
        IntegerField: 'number',
        BigIntegerField: 'number',
        FloatField: 'number'
    };
    const t = typesMap[props.dataType];
    if (!t) return 'text';
    return t;
});
</script>