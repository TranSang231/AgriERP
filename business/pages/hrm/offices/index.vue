<template>
    <div class="flex flex-col mt-20" v-if="tree && tree.length > 0">
        <div>
            <el-input :placeholder="t('filter_name')" v-model="filterText" clearable></el-input>
        </div>
        <div class="mt-4">
            <p v-if="error" class="flex self-center justify-center text-red-800 mb-2">{{ error }}</p>
            <el-tree ref="treeRef" :data="tree" node-key="id" default-expand-all :props="treeProps"
                :expand-on-click-node="false" :filter-node-method="filterNode" v-loading="loading">
                <template #default="{ node, data }">
                    <tree-element v-bind:node="node" v-bind:data="data" :subElementTypes="elementTypes"
                        :node-label="getLabelNode" :add="create"
                        :update="data.type.id == 'office' ? updateOffice : updateGroup"
                        :remove="data.type.id == 'office' ? deleteOffice : deleteGroup" :detailRoute="data.type.id == 'office' ? 'hrm-offices-id': 'hrm-groups-id'"
                        @onAdded="addNode" @onUpdated="update" @onRemoved="remove" :editable="true">
                        <template #editingForm="{ editingForm }">
                            <el-form-item prop="name" :label="t('office_name')" class="col-12 col-md-3 mt-1 mt-md-0">
                                <el-input v-model="editingForm.data.name" :placeholder="t('office_name')" />
                            </el-form-item>
                            <el-form-item prop="email" :label="t('email')" class="col-12 col-md-3 mt-1 mt-md-0">
                                <el-input v-model="editingForm.data.email" :placeholder="t('Email')" />
                            </el-form-item>
                            <el-form-item prop="manager_id" :label="t('manager')" class="col-12 col-md-3 mt-1 mt-md-0">
                                <el-select v-model="editingForm.data.manager_id" filterable placeholder="Select Manager"
                                    value-key="name">
                                    <el-option v-for="e in employeesStore.allEmployees" :key="e.id"
                                        :label="e.first_name + ' ' + e.last_name" :value="e.id" />
                                </el-select>
                            </el-form-item>
                            <!-- <el-form-item prop="address" :label="t('Address')" class="col-12 col-md-3 mt-1 mt-md-0"
                                    v-if="formData.type_id === 'office'">
                                    <el-input v-model="formData.address" :placeholder="t('Address')" />
                                </el-form-item>
                                <el-form-item prop="established_date" :label="t('established_date')"
                                    class="col-12 col-md-3 mt-1 mt-md-0" v-if="formData.type_id === 'office'">
                                    <el-date-picker size="small" :placeholder="t('established_date')"
                                        v-model="formData.established_date" type="date" value-format="yyyy-MM-dd" />
                                </el-form-item> -->
                        </template>

                        <template #addingForm="{ addingForm }">
                            <el-form-item prop="name" :label="t('Name')">
                                <el-input v-model="addingForm.data.name" :placeholder="t('Name')" />
                            </el-form-item>
                            <el-form-item prop="manager_id" :label="t('manager')">
                                <el-select v-model="addingForm.data.manager_id" filterable
                                    :placeholder="t('pick_managers')" value-key="name">
                                    <el-option v-for="e in employeesStore.allEmployees" :key="e.id"
                                        :label="e.first_name + ' ' + e.last_name" :value="e.id" />
                                </el-select>
                            </el-form-item>
                            <el-form-item prop="email" :label="t('office_email')">
                                <el-input v-model="addingForm.data.email" :placeholder="t('email')" />
                            </el-form-item>
                            <!-- <input type="hidden" v-model="addingForm.data.parent_id"/> -->
                        </template>
                    </tree-element>
                </template>
            </el-tree>
        </div>
    </div>
    <!-- Create -->
    <div v-else-if="canEdit && !loading" class="m-3 mt-20">
        <el-card class="box-card mb-4 card-detail">
            <span>{{ t('create_root_group') }}: </span>
            <el-form label-width="auto" class="row" :model="newRoot" ref="rootNodeForm" :rules="groupRules">
                <el-form-item prop="name" :label="t('office_name')" class="col-12 col-md-3 mt-1">
                    <el-input v-model="newRoot.name" autofocus :placeholder="t('Name')" class="field-input" />
                </el-form-item>
                <el-form-item prop="manager_id" :label="t('manager')" class="col-12 col-md-3 mt-1">
                    <el-select v-model="newRoot.manager_id" filterable :placeholder="t('manager')" value-key="name">
                        <el-option v-for="e in employeesStore.allEmployees" :key="e.id"
                            :label="e.first_name + ' ' + e.last_name" :value="e.id" />
                    </el-select>
                </el-form-item>
                <el-form-item prop="email" :label="t('email')" class="col-12 col-md-3 mt-1">
                    <el-input v-model="newRoot.email" autofocus :placeholder="t('email')" class="field-input" />
                </el-form-item>
            </el-form>
            <div class="mt-2 flex-row-reverse">
                <el-button type="primary" @click="createRootNode()">
                    Create
                </el-button>
            </div>
        </el-card>
    </div>

    <div class="row ml-3 mt-20" v-else>
        <span>{{ t('data_not_available') }}</span>
    </div>
</template>
<script lang="ts" setup>
import TreeElement from "@/components/TreeElements.vue";
import { useOauthStore } from '@/stores/oauth';
import GroupService from "@/services/group"
import OfficeService from "@/services/offices"
import EmployeeService from "@/services/hrm/employees"
import { useEmployeesStore } from '@/stores/business/employee';
import { useGroupsStore } from '@/stores/groups';
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
import { ElTree } from 'element-plus'

const oauthStore = useOauthStore();
const employeesStore = useEmployeesStore();
const groupStore = useGroupsStore();
const { t } = useI18n();

definePageMeta({
    layout: "hrm",
});

interface Tree {
    [key: string]: any
}

const treeProps = {
    children: 'children',
    label: 'name',
}
const treeRef = ref(null);

const loading = ref(false)
const error = ref('')
const rootNodeForm = ref<FormInstance>()
const groups = ref<any[]>([])

const elementTypes = computed(() => {
    return [
        {
            id: "office",
            name: "Office",
            initData: {
                id: null,
                name: '',
                address: '',
                manager_id: '',
                type_id: "office",
            },
            parent_key: "group_id",
        },
        {
            id: "group",
            name: "Group",
            initData: {
                id: null,
                name: null,
                manager_id: null,
                type_id: "group",
            },
            parent_key: "parent_id",
        },
    ];
});

const filterText = ref('')

const filterNode = (value: string, data: any) => {
    if (!value) return true;
    return data.name && data.name.toLowerCase().includes(value.toLowerCase());
};
// Watcher to trigger tree filtering
watch(filterText, (value) => {
    if (treeRef.value) {
        treeRef.value.filter(value);
    }
});



const newRoot = ref({
    name: null,
    email: null,
    manager_id: ''
})


const createTree = (node: any) => {
    const { id, name, email, manager_id, parent_id } = node;
    let children = [];
    if (node.offices && node.offices.length > 0) {
        children = node.offices.map(o => ({
            id: o.id,
            name: o.name,
            email: o.email,
            manager_id: o.manager_id,
            group_id: o.group_id,
            type_id: "office",
            type: { id: "office", name: "Office" },
        }));
    }
    if (node.groups && node.groups.length > 0) {
        children = [...children, ...node.groups.map(createTree)];
    }
    return {
        id,
        name,
        email,
        manager_id,
        parent_id,
        children,
        type_id: "group",
        type: { id: "group", name: "Group" },
    };
    // let representativeOffice = null;
    // if (node.offices && node.offices.length > 0) {
    //     return representativeOffice = {
    //         id: node.offices[0].id,
    //         name: node.offices[0].name,
    //         email: node.offices[0].email,
    //         manager_id: node.offices[0].manager_id,
    //         parent_id: id,
    //         type_id: "office",
    //         type: { id: "office", name: "Office" },
    //         children,
    //     };
    // } else {
    //     return representativeOffice = {
    //         id: id,
    //         name: name,
    //         email: email,
    //         manager_id: manager_id,
    //         parent_id: id,
    //         type_id: "office",
    //         type: { id: "office", name: "Office" },
    //         children,
    //     };
    // }
};

const getLabelNode = (node: any) => {
    return node.name;
}

const tree = computed(() => {
    if (!groups.value || groups.value.length === 0) {
        return []
    }
    console.log("check groups: ", groups.value);
    const newGroups = groups.value.map((o) => createTree(o));
    return newGroups;

})

const create = (data: any) => {
    const { type_id, ...postData } = data;
    if (type_id == "office") {
        return OfficeService.create(postData);
    }
    return GroupService.create(postData);
}

const nodeAdded = (tree: any, node: any, parent_key: any) => {
    let root = _cloneDeep(tree);
    if (Array.isArray(tree)) {
        const length = root.length;
        for (let i = 0; i < length; i++) {
            if (root[i].id == node[parent_key]) {
                if (parent_key === "group_id") {
                    const offices = root[i].offices
                        ? [...root[i].offices, node]
                        : [node];
                    root[i] = { ...root[i], offices };
                } else {
                    const groups = root[i].groups
                        ? [...root[i].groups, node]
                        : [node];
                    root[i] = { ...root[i], groups };
                }
                return root;
            } else if (root[i].groups) {
                const groups = nodeAdded(root[i].groups, node, parent_key);
                if (!_isEqual(root[i].groups, groups)) {
                    root[i].groups = groups;
                    return root;
                }
            }
        }
    }
    return root;
}

const addNode = (data: any) => {
    const parent_key = Object.hasOwn(data, "parent_id")
        ? "parent_id"
        : "group_id";
    groups.value = nodeAdded(groups.value, data, parent_key);
    groupStore.setGroups(groups.value);
}
const updateOffice = (data: any) => {
    return OfficeService.update(data);
}
const deleteOffice = (data: any) => {
    return OfficeService.delete(data.id);
}
const updateGroup = (data: any) => {
    return GroupService.update(data);
}
const deleteGroup = (data: any) => {
    return GroupService.delete(data.id);
}

const updateNode = (tree: any, node: any) => {
    let root = _cloneDeep(tree);
    if (Array.isArray(tree)) {
        const length = root.length;
        for (let i = 0; i < length; i++) {
            if (root[i].id == node.id) {
                root[i] = { ...root[i], ...node };
                return root;
            }
            if (root[i].offices) {
                const offices = updateNode(root[i].offices, node);
                if (!_isEqual(root[i].offices, offices)) {
                    root[i].offices = offices;
                    return root;
                }
            }
            if (root[i].groups) {
                const groups = updateNode(root[i].groups, node);
                if (!_isEqual(root[i].groups, groups)) {
                    root[i].groups = groups;
                    return root;
                }
            }
        }
    }
    return root;
};

const update = (node: any) => {
    groups.value = updateNode(groups.value, node)
    groupStore.setGroups(groups.value);
}

const removeNode = (tree: any, node: any) => {
    if (Array.isArray(tree)) {
        let root = _cloneDeep(tree);
        const length = root.length;
        for (let i = 0; i < length; i++) {
            if (root[i].id == node.id) {
                return root.filter((o) => o.id !== node.id);
            }
            if (root[i].offices) {
                const offices = removeNode(root[i].offices, node);
                if (!_isEqual(root[i].offices, offices)) {
                    root[i].offices = offices;
                    return root;
                }
            }
            if (root[i].groups) {
                const groups = removeNode(root[i].groups, node);
                if (!_isEqual(root[i].groups, groups)) {
                    root[i].groups = groups;
                    return root;
                }
            }
        }
    }
    return tree;
}

const remove = (node: any) => {
    groups.value = removeNode(groups.value, node);
    groupStore.setGroups(groups.value);
}


function createRootNode() {
    if (!rootNodeForm.value) return;
    rootNodeForm.value.validate((valid) => {
        if (valid) {
            console.log("newRoot.value", newRoot.value);
            GroupService.create(newRoot.value)
                .then((response) => {
                    if (response) {
                        groups.value = [...groups.value, response];
                        ElNotification({
                            title: 'Success',
                            message: 'Create office successfully',
                            type: 'success',
                        })
                    }
                })
                .catch((error) => {
                    console.log('error: ', error)
                    let errorMessage = 'An error occurred';
                    if (error && error.data) {
                        const errorData = error.data;
                        errorMessage = Object.keys(errorData)
                            .map((key) => `${key}: ${errorData[key].join(', ')}`)
                            .join('\n');
                    }
                    ElNotification({
                        title: 'Fail',
                        message: errorMessage,
                        type: 'error',
                    });
                });
        }
    });
}


const loadData = async () => {
    try {
        loading.value = true;
        GroupService.fetch();
        EmployeeService.fetch();
        groups.value = groupStore.allGroups;
    } catch (err) {
        console.error(err);
    } finally {
        loading.value = false;
    }

}

const canEdit = computed(() => {
    const res = oauthStore.hasOneOfScopes(['offices:edit']);
    return res
});

onMounted(() => {
    loadData()
})
const groupRules = {
    name: [
        {
            required: true,
            message: t('validate_error_required'),
            trigger: "change",
        },
    ],
    manager_id: [
        {
            required: true,
            message: t('validate_error_required'),
            trigger: "change",
        },
    ],
    email: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { type: 'email', message: t('validate_error_email_format'), trigger: ['blur'] },
    ],
}
</script>
<style scoped></style>