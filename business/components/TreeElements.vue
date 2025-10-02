<template>
    <div :class="viewMode ? 'flex flex-col justify-content-between w-full' : null">
        <div class="flex flex-row align-items-center">
            <slot name="icon" v-if="viewMode"></slot>
            <div v-if="viewMode">
                <span class="d-block title-tree ml-3" v-if="detailRoute && editingForm.data && editingForm.data.id">
                    <NuxtLink :to="{ name: detailRoute, params: { id: editingForm.data?.id } }">
                        {{ label || '' }}
                    </NuxtLink>
                </span>
                <span class="d-block title-tree ml-3" v-else>
                    {{ label || '' }}
                </span>
            </div>
        </div>

        <div v-if="viewMode" class="absolute right-0 mr-5 justify-content-end items-center">
            <el-dropdown trigger="click" @command="newSubItem" size="small" v-if="subElementTypes">
                <el-button :icon="Plus" circle type="primary" class="mr-3" />
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item v-for="sub in subElementTypes" :command="sub" :key="sub.id">
                            {{ t(`${sub.name}`) }}
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
            <el-button v-if="update" @click="showEditingForm" :icon="Edit" circle type="primary">
            </el-button>

            <el-popover placement="top" width="250" :title="$t('deleting_item_confirm_default_message')"
                v-model="confirmDelete" v-if="remove" trigger="click">
                <template #reference>
                    <el-button @click="confirmDelete = true" :icon="Delete" circle type="primary">
                    </el-button>
                </template>
                <div style="text-align: right; margin: 10px 0px">
                    <el-button @click="confirmDelete = false">
                        {{ t('Cancel') }}
                    </el-button>
                    <el-button type="primary" @click="onDelete">
                        {{ t('confirm') }}
                    </el-button>
                </div>
            </el-popover>
        </div>

        <div class="ml-3 p-6 bg-white rounded-lg shadow-lg max-w-md" v-if="addingForm && addingForm.visible">
            <div v-if="addingForm.type" class="mb-4 text-lg font-semibold">
                <span>{{ t('add_new') + ' ' + addingForm.type.name }}</span>
            </div>
            <el-form label-width="auto" :model="addingForm.data">
                <slot name="addingForm" :addingForm="addingForm"></slot>
                <div class="mt-2 flex-row-reverse">
                    <el-button size="small" type="primary" @click="onAdd">
                        {{ t('add_new') }}
                    </el-button>
                    <el-button size="small" type="info" @click="hideAddingForm">
                        {{ t('Cancel') }}
                    </el-button>
                </div>
            </el-form>
        </div>

        <div class="ml-3 p-6 bg-white rounded-lg shadow-lg max-w-md" v-if="editingForm && editingForm.visible">
            <el-form label-width="auto" :model="editingForm.data">
                <slot name="editingForm" :editingForm="editingForm"></slot>
                <div class="mt-2 flex-row-reverse">
                    <el-button size="small" type="primary" @click="onEdit">
                        {{ t('Save') }}
                    </el-button>
                    <el-button size="small" type="info" @click="hideEditingForm">
                        {{ t('Cancel') }}
                    </el-button>
                </div>
            </el-form>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import EmployeeService from '@/services/hrm/employees'
import { useEmployeesStore } from '@/stores/business/employee';
import { Plus, Edit, Delete } from '@element-plus/icons-vue';
import { ElNotification } from 'element-plus';
const { t } = useI18n();
const employeesStore = useEmployeesStore();

type SubElementType = {
    id: string | number;
    name: string;
    initData: Record<string, any>;
    parent_key?: string;
};

const props = defineProps({
    node: Object,
    data: Object,
    detailRoute: String,
    editable: Boolean,
    subElementTypes: {
        type: Array as () => SubElementType[],
        required: false,
    },
    add: Function,
    update: Function,
    remove: Function,
    // getParentField: Function,
    nodeLabel: Function,
})

const emit = defineEmits(['onAdded', 'onUpdated', 'onRemoved', 'update:addingForm']);
const router = useRouter();
const confirmDelete = ref(false);
const errors = ref([])

const initData = () => {
    return clone(props.data);
}

const editingForm = reactive({
    visible: false,
    data: clone(props.data),
    type: props.data?.type,
})

const addingForm = reactive({
    visible: false,
    data: _cloneDeep(props.data),
    // parentNode: null,
    type: null
})

const viewMode = computed(() => {
    return !editingForm.visible;
})

const changes = computed(() => {
    if (!props.data) {
        return null;
    }
    return diff(editingForm.data, props.data);
})
const postData = computed(() => {
    let data = changes;
    if (!data) {
        return null;
    }
    const { id, local_id } = props.data;
    if (id) {
        data = { ...data, id };
    }
    if (local_id) {
        data = { ...data, local_id };
    }
    return data;
});

const label = computed(() => {
    if (props.nodeLabel) {
        return props.nodeLabel(props.data);
    }
    let { name } = props.data;
    let label = name;
    return label;
});

function onAdd() {
    if (props.add) {
        props.add(addingForm.data).then((data: any) => {
            console.log(data);
            emit("onAdded", data);
            addingForm.visible = false;
        });
    }
}
function onEdit() {
    editingForm.visible = true;
    if (props.update) {
        props.update(editingForm.data).then((data: any) => {
            console.log(data);
            emit("onUpdated", data);
            errors.value = [];
            hideEditingForm();
        });
    }
    else {
        router.push({ name: props.detailRoute, params: { id: props.data?.id } });
    }
}

function onDelete() {
    if (props.remove) {
        const data = clone(props.data);
        props.remove(data)
            .then(() => {
                emit("onRemoved", data);
                ElNotification({
                    title: 'Success',
                    message: 'Delete successfully',
                    type: 'success',
                })
            })
            .catch((error: any) => {
                console.log(error);
                // Kiểm tra nếu có `response.data` chứa thông tin lỗi
                let errorMessage = 'An error occurred';
                if (error && error.data) {
                    const errorData = error.data;
                    // In ra tất cả các thông báo lỗi (dạng object với key-value)
                    errorMessage = Object.keys(errorData)
                        .map((key) => `${key}: ${errorData[key].join(', ')}`)
                        .join('\n');
                }
                ElNotification({
                    title: 'Fail',
                    message: errorMessage,
                    type: 'error',
                });
            })
            .finally(() => {
                hideDeleteDialog();
            });
    }
}

function onCancel() {
    editingForm.data = {
        data: clone(props.data),
        type: props.data?.type,
        visible: false,
    };
}
function showEditingForm() {
    editingForm.visible = true;
}

function hideEditingForm() {
    editingForm.visible = false;
}
function hideAddingForm() {
    addingForm.visible = false
}

function showDeleteDialog() {
    confirmDelete.value = true;
}
function hideDeleteDialog() {
    confirmDelete.value = false;
}

function newSubItem(type: any) {
    const parentFieldValue = props.data.id || props.data.local_id;
    addingForm.visible = true;
    addingForm.type = type;
    addingForm.data = {
        ...type.initData,
        [type.parent_key]: parentFieldValue,
        type_id: type.id,
    };
    console.log('adding form after: ', addingForm);
}

</script>