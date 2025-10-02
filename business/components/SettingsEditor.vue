<template>
  <el-tree
    :data="description"
    :props="treeProps"
    class="w-full"
    node-key="key"
    ref="tree"
  >
    <template #default="{ node, data }">
        <div
          :class="{
            'flex': true,
            'w-full': true,
            'gap-2': true,
            'justify-between': editable && data.type=='array' && data.itemOptions
          }"
        >
            <div
              v-if="editable && data.key && data.key.endsWith(']')"
              class="flex flex-row w-full justify-between"
            >
              <span>{{ node.label }}</span>
              <el-button
                circle :icon="Minus"
                class="text-primary  hover:text-on-primary hover:bg-primary"
                @click="() => removeItem(node)"
              />
            </div>
            <span v-else>{{ `${node.label}:`}}</span>
            
            <el-input
                v-if="data.type=='text'"
                type="text"
                :modelValue="get(settings, data.key)"
                @input="(value) => set(settings, data.key, value)"
            />
            <span v-if="data.type=='label'">
              {{ get(settings, data.key) }}
            </span>
            <el-input
                v-if="data.type=='number'"
                type="number"
                :modelValue="get(settings, data.key)"
                @input="(value) => set(settings, data.key, value)"
            />
            <el-checkbox
                v-if="data.type=='bool'"
                type="text"
                :modelValue="get(settings, data.key)"
                @change="(value) => set(settings, data.key, value)"
            />
            <el-input
                v-else-if="data.type=='color'"
                type="color"
                :value="get(settings, data.key)"
                @input="(value) => set(settings, data.key, value)"
            />
            <el-select
                v-else-if="data.type=='select'"
                :modelValue="get(settings, data.key)"
                @change="(value) => set(settings, data.key, value)"
            >
                <el-option v-for="o in data.options" :value="o.value">{{ o.label }}</el-option>
            </el-select>
            <el-dropdown
              v-if="editable && data.type=='array' && data.itemOptions"
              placement="bottom-start"
              @command="addItem"
              class="self-end"
            >
              <el-button circle :icon="Plus" class="text-primary  hover:text-on-primary hover:bg-primary" />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item
                    v-for="option in data.itemOptions"
                    :command="{ node, data: option}"
                  >
                    {{option.label}}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
        </div>
    </template>
  </el-tree>
</template>

<script setup lang="ts">
import {get, set} from 'lodash'
import { Plus, Minus } from '@element-plus/icons-vue';
import { mergeObjects, objectFromDescription, normalizeDescription } from '@/utils/obj';
const props = defineProps({
	settingsDescription: {
		type: Array,
        required: true,
		default: []
	},
  editable: {
    type: Boolean,
    default: false
  }
});

const treeProps = {
  children: 'children',
  label: 'label',
}

const model = defineModel();
const description = ref<any>(normalizeDescription(_cloneDeep(props.settingsDescription), '', model.value as any));
const tree = ref(null);
const settings = ref(mergeObjects(objectFromDescription(props.settingsDescription, '', model.value as any), model.value, "mine"));

const removeItem = (node: any) => {
  if(!tree.value) {
    return;
  }
  const t = tree.value as any;
  const { key: itemKey } = node.data;
  if (!itemKey || itemKey.length === 0) {
    return;
  }
  const s = itemKey.lastIndexOf('[');
  const e = itemKey.lastIndexOf(']');
  if (s < 0 || e < 0 || e < s) {
    return;
  }
  const n = itemKey.substr(s+1, e-s-1);
  console.log(n);
  let itemIndex = 0;
  try {
    itemIndex = parseInt(n);
  } catch (error) {
    console.error(error);
    return;
  }
  
  const parentNode = node.parent;
  if(parentNode) {
    t.remove(node);
    const { data } = parentNode;
    if(data) {
      // update key and label for the other children nodes.
      let { children, key }  = data;
      if (children && children.length > 0) {
        children = Array.from(children);
        children = normalizeDescription(children, key, {}, true);
        set(parentNode, 'data.children', children);
      }

      // remove item from setings value
      if (itemIndex >=0) {
        const currentSetting = get(settings.value, key);
        let settingValue = currentSetting ? Array.from(currentSetting) : [];
        settingValue.splice(itemIndex, 1);
        set(settings.value, key, settingValue);
      }
    }
  }
};

const addItem = (command: any) => {
  if (!tree.value) {
    return;
  }
  const { node, data } = command;
  const { key } = node.data
  if(!key) {
    return;
  }
  const currentSetting = get(settings.value, key);
  let settingValue = Object.values(currentSetting);
  const index = settingValue.length;
  const label = `[${index}]`;
  settingValue = [ ...settingValue, objectFromDescription(data.children)]
  set(settings.value, key, settingValue);
  let newNodeData = _cloneDeep(data);
  newNodeData = {...newNodeData, label, key: `${key}${label}`, children: normalizeDescription(newNodeData.children, `${key}${label}`)};
  (tree.value as any).append(newNodeData, node);
};

watch(settings, (newValue) => {
    model.value = newValue;
},
{ deep: true }
);
</script>