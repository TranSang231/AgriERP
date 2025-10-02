<template>
    <div class="w-full border p-2">
        <div
            v-if="entries && entries.length>0"
            class="flex flex-col gap-2"
        >
            <div
                v-for="(entry, index) in entries"
                class="flex flex-row, gap-2 items-center"
            >
                <el-input
                    v-if="entry"
                    v-model="entry.key"
                    :placeholder="keyPlaceholder"
                    style="width: 200px"
                    :disabled="disabled"
                />
                <span> → </span>
                <el-cascader
                    v-if="entry"
                    v-model="entry.value"
                    :options="metaData"
                    :props="cascaderProps"
                    clearable
                    :disabled="disabled"
                />
                <el-button
                    v-if="!disabled"
                    circle
                    type="danger"
                    :icon="Minus"
                    size="small"
                    @click="removeEntry(entry)"
                />
            </div>
        </div>
        <div v-if="!disabled" class="flex flex-row mt-2 w-full justify-start">
            <el-button
                circle
                type="danger"
                :icon="Plus"
                size="small"
                @click="newEntry()"
            />
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
import { Plus, Minus } from '@element-plus/icons-vue';
import { diff } from "@/utils/obj";
const props = defineProps({
    keyLabel: {
        type: String,
        default: ""
    },
    valueLabel: {
        type: String,
        default: ""
    },
    keyPlaceholder: {
        type: String,
        default: ""
    },
    newEntryPrefix: {
        type: String,
        default: "entry"
    },
    disabled: {
        type: Boolean,
        default: false
    },
    metaData: {
        type: Array,
        default: [],
        requied: true
    },
})

const cascaderProps = {
    checkStrictly: true,
    emitPath: false
}

const model = defineModel();
const entries = ref(
    model.value
        ? Object.entries(model.value).map(([key,value]) => ({key, value}))
        : [{ key: "", value: ""}]);

const removeEntry = (entry) => {
    entries.value = entries.value.filter((o) => o != entry);
}

const newEntry = () => {
    const keys = entries.value.map((o) => o.key);
    const autoKeys = keys.filter((o) => o.startsWith(props.newEntryPrefix))
    let nextEntryNumber = autoKeys.reduce((max, key) => {
        const rest = key.substr(5)
        const number = parseInt(rest);
        return max < number ? number : max
    }, 0);
    nextEntryNumber += 1;
    entries.value = [...entries.value, {key: `${props.newEntryPrefix}${nextEntryNumber}`, value: ""}]
}

const mappingObject = computed(() => {
	if (!entries.value || entries.value.length === 0) {
       return {}
    }
    const filtered_entries = entries.value.filter((o) => o.key && o.key.length > 0);
    return filtered_entries.reduce((object, entry) => {
        return { ...object, [entry.key]: entry.value}
    }, {});
});

watch(mappingObject, (newValue) => {
    if (diff(newValue, model.value)) {
        model.value = newValue;
    }
});
</script>
<style scoped>
</style>