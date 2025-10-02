<template>
    <tr>
        <td>
            <el-form-item
                :prop="`items[${index}].product_id`"
                :rules="rules.product_id"
                class="flex min-w-80"
            >
                <el-select
                    v-if="editable"
                    :disabled="!editable"
                    filterable
                    collapse-tags
                    value-key="id"
                    v-model="model.product_id"
                    :placeholder="t('Pick_options')"
                    @change="onProductChange"
                >
                    <el-option
                        v-for="item in products"
                        :key="item.id"
                        :label="item.name?.origin"
                        :value="item.id"
                    />
                </el-select>
                <span v-else>
                {{ model.product_name }}
                </span>
            </el-form-item>
        </td>
        <td>
            <el-form-item
                :prop="`items[${index}].unit`"
                :rules="rules.unit"
            >
                <el-input
                    v-if="editable"
                    v-model="model.unit"
                    :placeholder="$t('default_place_holder')"
                    type="text"
                />
                <span v-else>{{model.unit}}</span>
            </el-form-item>
        </td>
        <td>
            <el-form-item
                :prop="`items[${index}].price`"
                :rules="rules.unit"
            >
                <el-input-number
                    v-if="editable"
                    v-model="model.price"
                    :controls="false"
                >
                    <template #suffix>
                        <span>VND</span>
                    </template>
                </el-input-number>
                <span v-else>{{model.price}}</span>
            </el-form-item>
        </td>
        <td>
            <el-form-item
                :prop="`items[${index}].quantity`"
                :rules="rules.quantity"
            >
                <el-input
                    v-if="editable"
                    v-model="model.quantity"
                    :placeholder="t('default_place_holder')"
                    type="number"
                />
                <span v-else>{{model.quantity}}</span>
            </el-form-item>
        </td>
        <td>
            <el-form-item
                :prop="`items[${index}].amount`"
                :rules="rules.amount"
            >
                <span class="text-right min-w-60">{{amount.toLocaleString()}} VND</span>
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
    products: {
        type: Array,
        default: []
    },
    rules: {
        type: Object,
        default: {}
    }
})

const model = defineModel();
const amount = computed(() => {
    const v = model.value;
    if(!v) {
        return 0.0;
    }
    const price = v.price ? v.price : 0.0;
    const quantity = v.quantity ? v.quantity : 0.0;
    return price * quantity;
});

const onProductChange = (id) => {
    if (props.products) {
        const product = props.products.find((o) => o.id == id);
        if (product) {
            model.value = {
                ...model.value,
                product_name: product.name.origin,
                unit: product.unit.origin,
                price: product.price
            }
        }
    }
}
</script>