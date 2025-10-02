<template>
    <el-form
        ref="formRef"
        :label-width="props.labelWidth ? props.labelWidth.valueOf(): 'auto'"
        :label-position="props.labelPosition ? props.labelPosition : 'right'"
        label-suffix=":"
        :model="current"
        :rules="props.rules"
        v-loading="loading"
        :class="{
            'border': border,
            'bg-on-primary': true,
            'w-full' : fullWidth
        }"
    >
        <div
            v-if="title && title.length || collapsible || onClose || forceShowHeader"
            :class="{
                'w-full': fullWidth,
                'bg-on-primary': true,
                'pt-5': true,
                'px-5': true,
                'border-b': border
            }"
        >
            <div class="flex flex-row w-full justify-between align-middle gap-2">
                <slot name="title" :current="current" :editing="editing">
                    <span v-if="title && title.length > 0" class="text-primary font-bold">{{title}}</span>
                </slot>
                <div class="flex flex-row">
                    <slot name="buttons" :current="current" :editing="editing" />
                    <el-button
                        v-if="editable && !editing"
                        circle
                        :icon="Edit"
                        @click="edit()"
                        class="text-primary hover:text-on-primary hover:bg-primary"
                    />
                    <el-button
                        v-if="editing && changed"
                        circle
                        :icon="Discard"
                        @click="discard()"
                        class="text-primary hover:text-on-primary hover:bg-primary"
                    />
                    <el-button
                        v-if="editing && saveable"
                        circle
                        :icon="Save"
                        @click="onSave()"
                        class="text-primary  hover:text-on-primary hover:bg-primary"
                    />
                    <el-button
                        v-if="collapsible && collapsed"
                        circle
                        :icon="CaretBottom"
                        @click="expand()"
                        class="text-primary  hover:text-on-primary hover:bg-primary"
                    />
                    <el-button
                        v-if="collapsible && !collapsed"
                        circle
                        :icon="CaretTop"
                        @click="collapse()"
                        class="text-primary  hover:text-on-primary hover:bg-primary"
                    />
                    <el-button
                        v-if="onClose"
                        circle :icon="Close"
                        @click="onClose()"
                        class="text-primary  hover:text-on-primary hover:bg-primary"
                    />
                </div>
            </div>
        </div>
        <div v-if="current" :class="collapsed? 'hidden m-5': 'block m-5'">
            <slot :current="current" :editing="editing"/>
        </div>
        <p v-if="error" class="flex self-center justify-center text-red-800 mb-2">{{error}}</p>
    </el-form>
</template>

<script setup lang="ts" generic="S extends BaseService">
import { CaretTop, CaretBottom, Edit, Close } from '@element-plus/icons-vue'
import Save from '@/assets/icons/save.svg'
import Discard from '@/assets/icons/discard.svg'
import { ref } from 'vue';
import BaseService from  '@/services/base';
import { nestedDiff, toFormData, overrideFieldIfNullOrEmpty } from "@/utils/obj";
import { getErrorMessage } from '@/utils/error';

const props = defineProps<{
    service: S,
    title?: String,
    parentId?: String,
    forceShowHeader?: Boolean,
    border?: Boolean,
    collapsible?: Boolean,
    fullWidth?: Boolean,
    labelWidth?: String | Number | null
    labelPosition?: 'left' | 'right' | null
    nestedFields?: String[] | null,
    editable?: Boolean
    overrideIfFieldNullOrEmpty?: any | null,
    rules?: any | null,
    contentType?: String | null,
    customCreateResponseParser?: (response: any) => any
    onClose?: Function | null
    onItemCreated?: Function | null,
    onItemSaved?: Function | null
}>();

const { t } = useI18n();
const formRef = ref(null);
const collapsed = ref(false);
const loading = ref(false);
const model = defineModel();
const editing = ref(model.value &&
    (!(model.value as any).id || (model.value as any).parent_id != props.parentId));
const current = ref({
    ..._cloneDeep(overrideFieldIfNullOrEmpty(model.value, props.overrideIfFieldNullOrEmpty)),
    parent_id: props.parentId
});
const error = ref(null);

const changes = computed(() => {
    const o = model.value;
    const c = current.value;
    if (!c) {
        return null;
    }
    //Todo: implement comparing 2 object
    return nestedDiff(c, o, props.nestedFields? props.nestedFields : []);
});

const changed = computed(()=> {
    const c = changes.value
    if (!c) {
        return false;
    }
    return Object.keys(c).length > 0;
});

const saveable = computed(() => {
    return (current.value && !current.value.id) || changed.value;
})

const edit = () => {
    editing.value = true;
};

const collapse = () => {
    collapsed.value = true;
};

const expand = () => {
    collapsed.value = false;
};

const onSave = () => {
    if (!formRef.value) {
        return;
    }

    (formRef.value as any).validate(async (valid:boolean) => {
        if(!valid) {
            return;
        }
        saveEntry();
    });
};

const saveEntry = async () => {
    let value = current.value && !current.value.id ? current.value : changes.value;

    if (!value) {
        return;
    }
    const { id } = value;
    const contentType = props.contentType
    if (contentType && contentType.includes('form-data')) {
        value = toFormData(value);
    }
    error.value = null;
    if (id) {
        props.service.update(value)
        .then((response: any) => {
            let data = response;
            if (props.overrideIfFieldNullOrEmpty) {
                data = overrideFieldIfNullOrEmpty(data, props.overrideIfFieldNullOrEmpty)
            }
            model.value = _cloneDeep(data);
            current.value = _cloneDeep(data);
            if (props.onItemSaved) {
                props.onItemSaved(model.value);
            }
        })
        .catch((e: any) => {
            error.value = getErrorMessage(e, t('an_error_occurred'));
        })
    } else {
        props.service.create(value)
        .then((response: any) => {
            let data = response;
            if(props.customCreateResponseParser) {
                data = props.customCreateResponseParser(data)
            }
            if (props.overrideIfFieldNullOrEmpty) {
                data = overrideFieldIfNullOrEmpty(data, props.overrideIfFieldNullOrEmpty)
            }
            model.value = _cloneDeep(data);
            current.value = _cloneDeep(data);
            if (props.onItemCreated) {
                props.onItemCreated(model.value);
            }
        })
        .catch((e: any) => {
            error.value = getErrorMessage(e, t('an_error_occurred'));
        })
    }
};

const discard = () => {
    if (model.value) {
        current.value = _cloneDeep(overrideFieldIfNullOrEmpty(model.value, props.overrideIfFieldNullOrEmpty));
    }
};

watch(
  () => props.parentId,
  (newValue) => {
    console.log('node\n', newValue);
  },
  {deep: true}
);

defineExpose({
  current,
  changes,
  editing,
  formRef
});
</script>