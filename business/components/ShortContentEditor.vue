<template>
    <div class="flex flex-row w-full justify-between items-start gap-2 align-middle">
        <el-input
            :disabled="!editable"
            v-model="content" 
            :placeholder="placeholder"
            type="text"
        />
        <span
            v-if="languageOptions && languageOptions.length > 0"
            class="min-w-[100px]"
        >
            <el-select
                v-model="selectedLanguage"
                :placeholder="$t('pick_a_language')"
                size="small"
                style="max-width: 8rem"
            >
                <el-option v-for="l in languageOptions"
                    :label="l.name"
                    :value="l.code"
                    :key="l.code"
                />
            </el-select>
        </span>
    </div> 
</template>

<script setup>
const { t } = useI18n();
const empty = ""

const props = defineProps({
    placeholder: {
        type: String,
        default: ''
    },
    editable: {
        type: Boolean,
        default: false
    },
    languages: {
        type: Array,
        default: [],
        requied: false
    }
})

const model = defineModel();
const selectedLanguage = ref('origin');
const content = ref(
    props.languages && props.languages.length
        ? model.value
            ? model.value.origin
            : null
        : model.value);
const languageOptions = computed(() => {
    if (!props.languages || props.languages.length === 0) {
        return [];
    }
    const origin = props.languages.find((o) => o.code === 'origin');
    if (origin) {
        return props.languages;
    }
    return [
        {
            code: 'origin',
            name: t('origin_language')
        },
        ...props.languages  
    ];
})

watch(()=>props.modelValue, (newVal)=>{
    if (!selectedLanguage.value || selectedLanguage.value === 'origin') {
        content.value = newVal ? newVal.origin: null;
        return;
    }
    if (!newVal.translates || newVal.translates.length === 0) {
        content.value = empty;
        return;
    }
    const language = selectedLanguage.value.toLowerCase();
    const translate = newVal.translates.find((o) => o.language === language);
    if (translate) {
        content.value = translate.value;
    } else {
        content.value = empty;
    }
},{
    immediate:true
});

watch(content, (newValue) => {
    if (!props.languages) {
        model.value = newValue;
        return;
    }

    if (!model.value) {
        model.value = {
            origin: null
        }
    }
    const oldModel = model.value;
    if (!selectedLanguage.value || selectedLanguage.value === 'origin') {
        model.value = {
            ...oldModel,
            origin: newValue
        };
        return;
    }
    const language = selectedLanguage.value.toLowerCase();
    if (!oldModel || !oldModel.translates){
        model.value = {
            ...oldModel ? oldModel : {},
            translates: [ 
                { 
                    language: language,
                    value: newValue
                }
            ]
        };
        return;
    }
    const translate = oldModel.translates.find((o) => o.language === language);
    if (translate) {
        translate.value = newValue;
    } else {
        model.value = {
            ...oldModel,
            translates: [
                ...oldModel.translates,
                {
                    language: language,
                    value: newValue
                }
            ]
        };
    }
});

watch(selectedLanguage, (newValue) => {
    if (!props.languages || props.languages.length === 0) {
        return;
    }
    const _modelValue = model.value;
    if (!_modelValue) {
        content.value = empty;
        return;
    }
    if (!newValue || newValue === 'origin') {
        content.value =  _modelValue.origin;
        return;
    }
    if (!_modelValue.translates) {
        content.value = empty;
        return;
    }
    const translate = _modelValue.translates.find((o) => o.language === newValue.toLowerCase());
    if(translate) {
        content.value = translate.value;
    } else {
        content.value = empty;
    }
});
</script>