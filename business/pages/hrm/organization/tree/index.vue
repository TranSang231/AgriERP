<template>
    <div class="flex flex-col mt-20" v-if="tree && tree.length > 0" v-loading="loading">
        <div>
            <el-input placeholder="Filter Name" v-model="filterText"></el-input>
        </div>
        <div class="mt-4">
            <el-tree :data="tree" node-key="id" default-expand-all :props="treeProps" :expand-on-click-node="false"
                ref="tree" :filter-node-method="filterNode" v-loading="loading">
                <template #default="{ node, data }">
                    <tree-element v-bind:node="node" v-bind:data="data" :add="create"
                        :update="data.type && data.type.id == 'member' ? null : updateUnit" :remove="remove(data.type)"
                        @onAdded="addNode" @onUpdated="updateNode" @onRemoved="removeNode" :nodeLabel="getLabelNode"
                        :subElementTypes="data.type && data.type.id === 'member' ? null : elementFullTypes"
                        :detailRoute="data.type && data.type.id == 'member' ? 'hrm-employees-id' : 'hrm-organization-tree-id'"
                        :editable="true">
                        <template #editingForm="{ editingForm }">
                            <div class="row">
                                <el-form-item prop="name" label="Name" class="col-12 col-md-3 mt-1 mt-md-0">
                                    <el-input v-model="editingForm.data.name" placeholder="Name" autofocus
                                        class="field-input" />
                                </el-form-item>
                                <el-form-item prop="email" label="Email" class="col-12 col-md-3 mt-1 mt-md-0">
                                    <el-input v-model="editingForm.data.email" placeholder="Email" autofocus
                                        class="field-input" />
                                </el-form-item>
                                <el-form-item prop="manager_id" :label="t('manager')" class="col-12 col-md-2 mt-1">
                                    <el-select v-model="editingForm.data.manager_id" filterable
                                        :placeholder="t('pick_managers')" value-key="name">
                                        <el-option v-for="e in employeesStore.allEmployees" :key="e.id"
                                            :label="e.first_name + '' + e.last_name" :value="e.id" />
                                    </el-select>
                                </el-form-item>
                                <el-form-item prop="slack_channel" label="Slack channel" class="col-18 col-md-3 mt-1">
                                    <el-input v-model="editingForm.data.slack_channel" placeholder="Slack chanel" />
                                </el-form-item>
                            </div>
                        </template>

                        <template #addingForm="{ addingForm }">
                            <div class="row" v-if="addingForm.type.id === 'member'">
                                <el-form-item prop="employee_id" class="col-12 mt-1">
                                    <el-select v-model="addingForm.data.employee_id" filterable
                                        placeholder="Select Employee" value-key="name">
                                        <el-option v-for="user in availableUsers(data.children)" :key="user.id"
                                            :label="user.first_name + ' ' + user.last_name" :value="user.id" />
                                    </el-select>
                                </el-form-item>
                            </div>
                            <div class="row" v-else>
                                <el-form-item prop="name" :label="t('Name')" class="col-12 col-md-2 mt-1">
                                    <el-input v-model="addingForm.data.name" :placeholder="t('Name')" />
                                </el-form-item>
                                <el-form-item prop="manager_id" :label="t('manager')" class="col-12 col-md-2 mt-1">
                                    <el-select v-model="addingForm.data.manager_id" filterable
                                        :placeholder="t('pick_managers')" value-key="name">
                                        <el-option v-for="e in employeesStore.allEmployees" :key="e.id"
                                            :label="e.first_name + '' + e.last_name" :value="e.id" />
                                    </el-select>
                                </el-form-item>
                                <el-form-item prop="email" :label="t('email')" class="col-12 col-md-2 mt-1">
                                    <el-input v-model="addingForm.data.email" :placeholder="t('email')" />
                                </el-form-item>
                                <el-form-item prop="slack_channel" label="Slack channel" class="col-18 col-md-3 mt-1">
                                    <el-input v-model="addingForm.data.slack_channel" placeholder="Slack chanel" />
                                </el-form-item>
                            </div>
                        </template>
                    </tree-element>
                </template>
            </el-tree>
        </div>
    </div>
    <!-- Create -->
    <div v-else-if="canEdit" class="mt-20">
        <el-card class="box-card mb-4 card-detail">
            <span>{{ $t('create_root_unit') }}</span>
            <el-form class="row" :model="newRoot" ref="rootNodeForm" :rules="groupRules">
                <el-form-item prop="type_id" class="col-12 col-md-3 mt-1">
                    <el-select v-model="newRoot.type_id" filterable placeholder="Unit type" value-key="name">
                        <el-option v-for="t in elementTypes()" :key="t.id" :label="t.name" :value="t.id" />
                    </el-select>
                </el-form-item>
                <el-form-item prop="name" class="col-12 col-md-3 mt-1">
                    <el-input v-model="newRoot.name" autofocus placeholder="Name" class="field-input" />
                </el-form-item>
                <el-form-item prop="manager_id" class="col-12 col-md-3 mt-1">
                    <el-select v-model="newRoot.manager_id" filterable placeholder="Select Manager" value-key="name">
                        <el-option v-for="e in employeesStore.allEmployees" :key="e.id"
                            :label="e.first_name + ' ' + e.last_name" :value="e.id" />
                    </el-select>
                </el-form-item>
                <el-form-item prop="email" class="col-12 col-md-3 mt-1">
                    <el-input v-model="newRoot.email" placeholder="Email" class="field-input" />
                </el-form-item>
            </el-form>
            <div class="mt-2 flex-row-reverse">
                <el-button type="primary" @click="createRootNode()">
                    {{ $t('Save') }}
                </el-button>
            </div>
        </el-card>
    </div>

    <div class="row ml-3" v-else>
        <span>Data is not available.</span>
    </div>
</template>
<script lang="ts" setup>
import TreeElement from "@/components/TreeElements.vue";
import { useOauthStore } from '@/stores/oauth';
import EmployeeService from "@/services/hrm/employees";
import { useEmployeesStore } from '@/stores/business/employee';
import { useUnitTypesStore } from "@/stores/organization/unit-types";
import UnitTypesService from '~/services/organization/unit-types';
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
import { ElTree } from 'element-plus';
import { useUnitsStore } from "@/stores/organization/units";
import UnitService from "~/services/organization/units";

const oauthStore = useOauthStore();
const unitTypeStore = useUnitTypesStore();
const employeesStore = useEmployeesStore();
const unitStore = useUnitsStore();

const { t } = useI18n();

definePageMeta({
    layout: "hrm",
});

interface Tree {
    [key: string]: any
}

const treeProps = {
    children: 'children',
    label: 'label',
}

const loading = ref(false);
const rootNodeForm = ref<FormInstance>()
const units = ref<any[]>([]);
const filterText = ref('')
const filterNode = (value: string, data: Tree) => {
    if (!value) return true
    return data.label.includes(value)
}
const newRoot = ref({
    name: null,
    email: null,
    manager_id: '',
    slack_id: '',
    type_id: null
})

const addMember = (data: any) => {
    console.log("add member", data);

    const { local_id, ...postData } = data;
    return UnitService.addMember(postData);
}

const addUnit = (data: any) => {
    return UnitService.create(data);
}

const nodeAdded = (tree:any, node:any, parent_key:any) => {
    let root = _cloneDeep(tree);
    if (Array.isArray(root)) {
        const length = root.length;
        let parent_key_value = null;
        let data = null;
        if (parent_key === "unit_id") {
            const { unit_id, ...nodeData } = node;
            parent_key_value = unit_id;
            data = nodeData;
        } else {
            const { parent_id, ...nodeData } = node;
            parent_key_value = parent_id;
            data = nodeData;
        }
        for (let i = 0; i < length; i++) {
            const { id, local_id, name } = root[i];
            const compareID = id ? id : local_id;
            if (compareID == parent_key_value) {
                console.log("name: ",name);
                if (parent_key === "unit_id") {
                    // Add member
                    const members = root[i].members
                        ? [...root[i].members, data.employee]
                        : [data.employee];
                    root[i] = { ...root[i], members };
                } else {
                    const units = root[i].units ? [...root[i].units, data] : [data];
                    root[i] = { ...root[i], units };
                }
                return root;
            } else if (root[i].units) {
                const units = nodeAdded(root[i].units, node, parent_key);
                if (!_isEqual(root[i].units, units)) {
                    root[i].units = units;
                    return root;
                }
            }
        }
    }
    return root;
}

const addNode = (data) => {
    console.log("added data", data);
    const parent_key = Object.hasOwn(data, "parent_id")
        ? "parent_id"
        : "unit_id";
    units.value = nodeAdded(units.value, data, parent_key);
}

function updateUnit(data: any) {
    return UnitService.update(data);
}
function deleteUnit(data: any) {
    return UnitService.delete(data.id);
}

const updateNode = (node: any) => {
    units.value = nodeUpdated(units.value, node);
};

const nodeUpdated = (tree:any, node:any) => {
    let root = _cloneDeep(tree);
    if (Array.isArray(tree)) {
        const length = root.length;
        const { id: nodeId, local_id: nodeLocalID, type_id: nodeTypeId } = node;
        let { parent_id, ...data } = node;
        let updateData = nodeId ? node : data;
        const nodeCompareID = nodeId ? nodeId : nodeLocalID;
        for (let i = 0; i < length; i++) {
            const { id, local_id, type_id } = root[i];
            const compareId = id ? id : local_id;
            if (
                nodeCompareID &&
                nodeCompareID === compareId &&
                type_id === nodeTypeId
            ) {
                root[i] = { ...root[i], ...updateData };
                return root;
            } else if (root[i].units) {
                const units = nodeUpdated(root[i].units, node);
                if (!_isEqual(root[i].units, units)) {
                    root[i].units = units;
                    return root;
                }
            }
        }
    }
    return root;
}

const removeMember = (data:any) => {
    const { unit_id, id } = data;
    return UnitService.removeMember({ unit_id:unit_id, employee_id: id });
}

const remove = (type: any) => {
    return type && type.id === "member" ? removeMember : deleteUnit;
}

const nodeRemoved = (tree:any, node:any) => {
    if (Array.isArray(tree)) {
        let root = _cloneDeep(tree);
        const length = root.length;
        const { id: nodeID, local_id: nodeLocalId } = node;
        for (let i = 0; i < length; i++) {
            if (!root[i]) {
                continue;
            }
            const { id, local_id } = root[i];
            if (nodeID && nodeID === id) {
                return root.filter((o) => o.id !== nodeID);
            }
            if (nodeLocalId && nodeLocalId === local_id) {
                return root.filter((o) => o.local_id !== nodeLocalId);
            }
            if (root[i].members) {
                const members = nodeRemoved(root[i].members, node);
                if (!_isEqual(root[i].members, members)) {
                    root[i].members = members;
                    return root;
                }
            }
            if (root[i].units) {
                const units = nodeRemoved(root[i].units, node);
                if (!_isEqual(root[i].units, units)) {
                    root[i].units = units;
                    return root;
                }
            }
        }
    }
    return tree;
}

const removeNode = (data) => {
    units.value = nodeRemoved(units.value, data);
}

const canEdit = computed(() => {
    const res = oauthStore.hasOneOfScopes(['organization:edit']);
    return res
});


const create = (data: any) => {
    const { type_id, ...postData } = data;
    if (type_id == "member") {
        if (addMember) {
            return addMember(postData);
        }
    }
    return addUnit(data)
}

function createRootNode() {
    if (!rootNodeForm.value) return;
    rootNodeForm.value.validate((valid) => {
        if (valid) {
            UnitService.create(newRoot.value)
                .then((response) => {
                    units.value = [...units.value, response];
                })
                .catch((error) => {
                });
        }
    });
}


const tree = computed(() => {
    if (!units.value || units.value.length === 0) {
        return []
    }
    const temp = units.value.map((o) => createTree(o))
    return temp;
})


const createTree = (node:any) => {
    const { id, name, email, manager_id, parent_id, type } = node;
    const unit_id = id
    let children: any[] = [];
    if (node.members && node.members.length > 0) {
        const items = node.members.map((o: any) => {
            console.log("check o", o);
            const { id, first_name, last_name } = o;
            return {
                id,
                first_name,
                last_name,
                // name,
                unit_id,
                type: {
                    id: "member",
                    name: "Member",
                },
            };
        });
        if (items && items.length > 0) {
            children = [...children, ...items];
        }
    }

    if (node.units && node.units.length > 0) {
        const items = node.units.map((o: any) => createTree(o));
        if (items && items.length > 0) {
            children = [...children, ...items];
        }
    }

    return {
        id,
        name,
        email,
        manager_id,
        parent_id,
        children,
        type,
    };
};

const loadData = async () => {
    loading.value = true;
    try {
        // await Promise.all([
        EmployeeService.fetch();
        UnitTypesService.fetch();
        UnitService.fetch();
        // ]);
        units.value = unitStore.allUnits;
    } catch (error) {
        console.log(error);
    } finally {
        loading.value = false;
    }
}

const allUnitTypes = computed(() => {
    return unitTypeStore.allUnitTypes;
})

const elementTypes = () => {
    let types = [];
    if (allUnitTypes.value) {
        allUnitTypes.value.forEach((type: any) => {
            types = [
                ...types,
                {
                    id: type.id,
                    name: type.name,
                    initData: {
                        id: null,
                        name: null,
                        email: null,
                        slack_channel: null,
                        manager_id: null,
                        type_id: type.id
                    },
                    parent_key: "parent_id",
                },
            ];
        });
    }
    return types;
}
const elementFullTypes = computed(() => {
    const items = [
        ...elementTypes(),
        {
            id: "member",
            name: "Member",
            initData: {
                user_id: null,
                type_id: 'member',
            },
            parent_key: "unit_id",
        },
    ];
    return items;
});

const getLabelNode = (node: any) => {
    console.log("label node", node);
    
    if (node.type.id == "member") {
        return '[' + node.type.name + "] " + node.first_name + " " + node.last_name;
    }
    return '[' + node.type.name + "] " + node.name;
}

const availableUsers = (children) => {
    const members = children ? children.filter((o) => o.unit_id) : [];
    const available = employeesStore.allEmployees.filter(
        (o) => members.findIndex((m) => m.id && m.id === o.id) === -1
    );
    return available;
}

onMounted(() => {
    loadData();
})
const groupRules = {
    type_id: [
        {
            required: true,
            message: t('validate_error_required'),
            trigger: "change",
        },
    ],
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
}
</script>