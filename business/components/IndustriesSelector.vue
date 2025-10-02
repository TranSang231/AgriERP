<template>
    <el-select
        v-model="currentValue"
        :placeholder="placeholder"
        style="width: 240px"
        :multiple="multiple"
        @change="onSeletedChange"
        :filterable="true"
        popper-class="max-w-[500px]"
        :disabled="disabled"
    >
        <el-option-group
            v-for="group in groups"
            :key="group.key"
            :label="`${group.key} - ${group.label}`"
        >
        <el-option
            v-for="item in group.options"
            :key="item.code"
            :label="`${replaceAncestorCode(item.code)} - ${item.value}`"
            :value="item.code"
        />
        </el-option-group>
  </el-select>
</template>

<script setup lang="ts">

const props = defineProps({
    options: {
        type: Array,
        default: []
    },
    multiple: {
        type: Boolean,
        default: false
    },
    placeholder: {
        type: String,
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    }
});

const model = defineModel();
const currentValue = ref(
    props.multiple
        ? model.value 
            ? model.value.split(' ')
            : []
        : model.value
);
const groups = computed (() => {
    if (!props.options) {
        return [];
    }
    const options = props.options;
    return options.reduce((a, c: any) => {
        const level1 = c.code.split('_')[0];
        const group = a.find((o: any) => o.key === level1);
        if (!group) {
            return [ ...a, { key: level1, label: c.value, options: [] }];
        } else {
            group.options = [...group.options, c];
            return a;
        }
        
    },[]);
});

const onSeletedChange = (value: any) => {
    if(!props.multiple) {
        model.value = value;
    } else {
        model.value = value.join(' ');
    }
}

const replaceAncestorCode = (code: string)  => {
    const index = code.lastIndexOf("_");
    const lenght = code.length;
    if(index >=0) {
        const value = code.substring(index+1);
        return value.padStart(lenght, ' ');
    }
    return code;
}
</script>