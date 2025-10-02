<template>
    <div>
        <div class="flex flex-row items-center justify-between gap-2">
            <el-input :placeholder="$t('search')" v-model="keyword">
                <template #append>
                    <el-button :icon="Search" />
                </template>
            </el-input>
            <el-checkbox
                v-model="selectAll"
                label="{{ $t('select_all') }}"
                size="small"
                border
                v-show="editable"
            >
                {{ $t('select_all') }}
            </el-checkbox>
        </div>
        <div class="row">
            <el-tree
                ref="tree"
                :data="scopesTree"
                :props="nodeProps"
                :defaultCheckedKeys="defaultCheckedKeys"
                node-key="key"
                :show-checkbox="true"
                :check-strictly="false"
                :highlight-current="true"
                :expand-on-click-node="false"
                :filter-node-method="filterNodes"
                @check-change="onScopeChanged"
            />
        </div>
    </div>
</template>

<script setup lang="ts" generic="S extends BaseService">
import { Search } from '@element-plus/icons-vue'
import { ref, watch } from 'vue';

const props = defineProps({
    scopes: {
        type: Object,
        default: null
    },
    editable: {
        type: Boolean,
        default: false
    },
    defaultScopes: {
        type: Array,
        default: []
    },
    prefix: {
        type: String,
        required: false
    }
});

const model = defineModel();
const keyword = ref('');
const selectAll = ref(false);
const tree = ref(null);

const nodeProps = {
    children: "children",
    label: "label",
    disabled: "disabled",
};

const allKeys = computed (() => {
    const { scopes } = props;
    if (!scopes ) {
        return [];
    }
    return Object.keys(scopes);
});

const scopesTree = computed(() => {
    const { scopes } = props;
    if (!scopes ) {
        return [];
    }
    const prefix = props.prefix;
    const prefixLength = prefix ? prefix.length : 0
    const entries = Object.entries(scopes);
    const allScopes = entries.reduce((accumulator, currentValue) => {
        const [k, v] = currentValue;
        const keyParts = k.split(":");
        if (keyParts.length <= 1) {
            return accumulator;
        }
        const groupKey = prefix && k.startsWith(prefix)
            ? k.substring(prefixLength).split(":")[0]
            : keyParts[0];
        const group = accumulator.find(o => o.key === groupKey);
        const { defaultScopes } = props
        if (group) {
            const children = group.children ? group.children : []
            group.children = [
                ...children,
                {
                    key: k,
                    label: v,
                    disabled: !props.editable || defaultScopes.includes(k)
                }
            ];
            return accumulator;
        } else {
            return [
                ...accumulator,
                {
                    key: groupKey,
                    label: groupKey.charAt(0).toUpperCase() + groupKey.substring(1),
                    disabled: !props.editable || defaultScopes.includes(groupKey),
                    children: [
                        {
                            key: k,
                            label: v,
                            disabled: !props.editable || defaultScopes.includes(k)
                        }
                    ]
                }
            ]
        }
    },[]);
    return allScopes;
});

const defaultCheckedKeys = computed(() => {
      let keys = props.defaultScopes ? props.defaultScopes : [];
      const modelValue = model.value;
      if (modelValue && modelValue != "") {
        const modelKeys = modelValue.split(" ");
        keys = _union(keys, modelKeys);
      }
      return keys;
});

const waitForRef = async (timeout)  => {
      if (!tree.value && timeout > 0) {
        setTimeout(function () {
          if (timeout > 0) {
            waitForRef(timeout - 100);
          }
        }, 100);
      }
};

const setChecked = (keys = []) => {
    if (tree.value && keys) {
        tree.value.setCheckedKeys(keys);
    }
};

const filterNodes = (value, data) => {
      if (!value) return true;

      return data.label.toLowerCase().includes(value.toLowerCase());
};

const onScopeChanged = ()  => {
    const selectedKeys = tree.value.getCheckedKeys(true);
    if (
    model.value == "__all__" &&
    selectedKeys.length == allKeys.value.length
    ) {
        return;
    }
    model.value = selectedKeys.join(" ");
};

// watch works directly on a ref
watch(selectAll, async (newValue, oldValue) => {
    waitForRef(2000)
        .then(() => {
            const keys = allKeys.value;

            if (newValue && keys && keys.length > 0) {
                setChecked(keys);
            } else {
                setChecked(props.defaultScopes);
            }
        });
});

watch(() => props.modelValue, async (newValue, oldValue) => {
    waitForRef(2000)
        .then(() => {
            const checkedKeys = tree.value.getCheckedKeys(true)
            if (newValue === checkedKeys.join(" ")) {
                return;
            }
            const keys = newValue == "__all__" ? allKeys.value : defaultCheckedKeys.value;
            setChecked(keys);
        });
});

// watch works directly on a ref
watch(keyword, async (newValue, oldValue) => {
    tree.value.filter(newValue);
});

onMounted(() => {
    waitForRef(2000)
        .then(() => {
            const defaultScopes = props.defaultScopes;
            if (defaultScopes && defaultScopes.length > 0 && !model.value) {
                model.value = defaultScopes.join(" ");
            } else {
                const keys = model.value == "__all__" ? allKeys.value : defaultCheckedKeys.value;
                setChecked(keys);
            }
        });
})
</script>