<template>
    <el-form
        ref="formRef"
        :model="model"
        :label-width="props.labelWidth ? props.labelWidth.valueOf(): 'auto'"
        :label-position="props.labelPosition ? props.labelPosition : 'right'"
        label-suffix=":"
        :rules="rules"
        class="py-0"
    >
        <div class="flex flex-row items-center justify-between">
            <el-form-item :label="t('Path')" prop="path" class="mt-1">
                <el-input
                    v-if="editable"
                    v-model="current.path"
                    :placeholder="t('default_place_holder')"
                    type="text"
                />
                <span v-else>{{ current.path }}</span>
            </el-form-item>
            <div class="flex flex-row gap-1">
                <el-button type="primary" v-if="editing && changed" size="small" :icon="Discard" @click="discard()"/>
                <el-button v-if="editable && saveable" circle size="small" :icon="Save" @click="onSave()"/>
                <el-button v-if="editable && collapsed" circle size="small" :icon="CaretBottom" @click="expand()"/>
                <el-button v-if="editable && !collapsed" circle size="small" :icon="CaretTop" @click="collapse()"/>
            </div>
        </div>
        <p v-if="error" class="flex self-center justify-center text-red-800 mb-2">{{error}}</p>
        <div
            v-if="!collapsed"
        >
            <el-form-item v-if="localeStore" :label="t('Title')" prop="title">
                <ShortContentEditor
                    :editable="editable"
                    v-model="current.title"
                    :languages="localeStore.supportedLanguages"
                    :placeholder="t('default_place_holder')"
                />
            </el-form-item>
            <el-form-item v-if="localeStore" :label="$t('Description')" prop="description">
                <ShortContentEditor
                    :editable="editable"
                    v-model="current.description"
                    :languages="localeStore.supportedLanguages"
                    :placeholder="t('default_place_holder')"
                />
            </el-form-item>
            <el-form-item :label="t('Keywords')" prop="keywords">
                <el-input
                    v-if="editable"
                    v-model="current.keywords"
                    :placeholder="t('keywords_placeholder')"
                    type="textarea"
                    autosize
                />
                <span v-else>{{ current.keywords }}</span>
            </el-form-item>
            <el-form-item v-if="localeStore" :label="t('Content')" prop="content" class="flex flex-col">
                <LongContentEditor
                :editable="editable"
                :readOnly="!editable"
                v-model="current.content"
                :languages="localeStore.supportedLanguages"
                @change="onContentChange"
                />
            </el-form-item>
        </div>
    </el-form>
</template>
  
<script setup>
import RouteService from '@/services/websites/route';
import { Delete, CaretBottom, CaretTop } from '@element-plus/icons-vue';
import Save from '@/assets/icons/save.svg';
import Discard from '@/assets/icons/discard.svg';
import { nestedDiff } from "@/utils/obj";
import { useLocaleStore } from '@/stores/locale';
import { useOauthStore } from "@/stores/oauth";
import ConstantsService from '@/services/constants';

const props = defineProps({
    labelWidth: {
        type: String | Number | null,
        required: false,

    },
    labelPosition: {
        type: String | null,
        required: false
    },
    editable: {
        type: Boolean,
        required: false
    }
});

const model = defineModel();
const current = ref(_cloneDeep(model.value));
const error = ref(null);
const { t } = useI18n();
const localeStore = useLocaleStore();
const oauthStore = useOauthStore();
const formRef = ref(null);
const collapsed = ref(false);
const collapse = () => {
    collapsed.value = true;
};
const expand = () => {
    collapsed.value = false;
};

const nestedFields = [
  "title",
  "title.translates",
  "description",
  "description.translates",
  "content",
  "content.translates"
];

const changes = computed(() => {
    const o = model.value;
    const c = current.value;
    if (!c) {
        return null;
    }
    //Todo: implement comparing 2 object
    return nestedDiff(c, o, nestedFields);
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

const rules = {
    path: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 20, message: t('validate_error_min_max', { min: 1, max: 255 }), trigger: 'blur' },
    ],
    title: [
        {
            validator: (rule, value, callback) => {
                if (!current.value.title || ! current.value.title.origin) {
                    callback(new Error(t('validate_error_required')));
                }
                callback();
            },
            trigger: 'blur'
        }
    ],
    content: [
        {
            validator: (rule, value, callback) => {
                //Todo: review the limitation later.
                const max_content_size = 83886080; //80MB
                if (current.value && current.value.content && current.value.content.origin) {
                    const size = new Blob([current.value.content.origin]).size;
                    if (size > max_content_size) {
                        callback(new Error(t('validate_error_content_max', {max: max_content_size})));
                        return;
                    }
                }
                if (current.value && current.value.content && current.value.content.translates && current.value.content.translates.length > 0) {
                    const sizeError = current.value.content.translates.some((translate) => {
                        if (translate.value) {
                        const size = new Blob([translate.value]).size;
                        if (size > max_content_size) {
                            let language = localeStore && localeStore.supported_languages
                            ? localeStore.supported_languages.find((l) => l.code == translate.language)
                            : null;
                            language = language ? language.name: translate.language;
                            callback(new Error(`${language}: ${t('validate_error_content_max', {max: max_content_size})}`));
                            return true;
                        }
                        }
                        return false;
                    })
                    if (sizeError) {
                        return;
                    }
                }
                callback();
            },
            trigger: 'blur'
        }
    ]
};

const onContentChange = () => {
  if (formRef.value) {
    formRef.value.validateField('content');
  }
};

const onSave = () => {
    if (!formRef.value) {
        return;
    }

    (formRef.value).validate(async (valid) => {
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
    error.value = null;
    if (id) {
        RouteService.update(value)
        .then((response) => {
            model.value = _cloneDeep(response);
            current.value = _cloneDeep(response);
        })
        .catch((e) => {
            console.error(e);
            error.value = getErrorMessage(e, t('an_error_occurred'));
        })
    } else {
        RouteService.create(value)
        .then((response) => {
            model.value = _cloneDeep(response);
            current.value = _cloneDeep(data);
        })
        .catch((e) => {
            console.error(e);
            error.value = getErrorMessage(e, t('an_error_occurred'));
        })
    }
};

const discard = () => {
    if (model.value) {
        current.value = _cloneDeep(model.value);
    }
};
</script>
  