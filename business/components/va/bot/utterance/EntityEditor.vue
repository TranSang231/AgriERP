<template>
    <tr>
        <td>
            <el-form-item
                :prop="`entities[${index}].entity_id`"
                :rules="rules.entity_id"
                class="flex min-w-80"
            >
                <el-select
                    v-if="editable && entities"
                    :disabled="!editable"
                    filterable
                    collapse-tags
                    value-key="id"
                    v-model="model.entity_id"
                    :placeholder="t('Pick_options')"
                >
                    <el-option
                        v-for="item in entities"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                    />
                </el-select>
                <span>
                {{ model.text }}
                </span>
            </el-form-item>
        </td>
    </tr>
</template>

<script setup>
const { t } = useI18n();

const props = defineProps({
    index: {
        type: Number,
        default: 0
    },
    editable: {
        type: Boolean,
        default: false
    },
    entities: {
        type: Array,
        default: []
    },
    rules: {
        type: Object,
        default: {}
    }
})

const model = defineModel();
</script>