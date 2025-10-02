<template>
    <QuillEditor
        v-if="editable"
        v-model:content="content"
        contentType="html"
        :theme="theme"
        :enable="editable"
        :readOnly="readOnly"
        :placeholder="placeholder"
        toolbar="#editor-toolbar"
        :modules="modules"
        class="w-full"
    >
        <template #toolbar>
            <div id="editor-toolbar" class="w-full">
                <!-- Common format -->
                <span class="ql-formats">
                    <select class="ql-header">
                        <option value="1">H1</option>
                        <option value="2">H2</option>
                        <option value="3">H3</option>
                        <option value="4">H4</option>
                        <option value="5">H5</option>
                        <option value="0">Normal</option>
                    </select>
                    <select class="ql-font">
                        <option selected>Sans Serif</option>
                        <option value="time-new-roman">Times New Roman</option>
                        <option value="arial">Arial</option>
                        <option value="inconsolata">Inconsolata</option>
                        <option value="mirza">Mirza</option>
                    </select>
                    <select class="ql-size">
                        <option selected="selected">Default</option>
                        <option value="5pt">5</option>
                        <option value="6pt">6</option>
                        <option value="8pt">8</option>
                        <option value="9pt">9</option>
                        <option value="10pt">10</option>
                        <option value="11pt">11</option>
                        <option value="12pt">12</option>
                        <option value="13pt">13</option>
                        <option value="14pt">14</option>
                        <option value="16pt">16</option>
                        <option value="18pt">18</option>
                        <option value="20pt">20</option>
                        <option value="22pt">22</option>
                        <option value="24pt">24</option>
                        <option value="26pt">26</option>
                        <option value="28pt">28</option>
                        <option value="32pt">32</option>
                        <option value="36pt">36</option>
                        <option value="48pt">48</option>
                        <option value="72pt">72</option>
                    </select>
                </span>
                
                <span class="ql-formats">
                    <button class="ql-bold"></button>
                    <button class="ql-italic"></button>
                    <button class="ql-underline"></button>
                    <button class="ql-strike"></button>
                    <select class="ql-align"></select>
                </span>

                <span class="ql-formats">
                    <select class="ql-color"></select>
                    <select class="ql-background"></select>
                </span>

                <!-- Subscript and superscript buttons -->
                <span class="ql-formats">
                    <button class="ql-script" value="sub"></button>
                    <button class="ql-script" value="super"></button>
                </span>

                <!-- List -->
                <span class="ql-formats">
                    <button class="ql-list" value="ordered"></button>
                    <button class="ql-list" value="bullet"></button>
                    <button class="ql-list" value="check"></button>
                </span>

                <!-- media -->
                <span class="ql-formats">
                    <button class="ql-link"></button>
                    <button class="ql-image"></button>
                    <button class="ql-video"></button>
                    <button class="ql-formula"></button>
                    <button class="ql-blockquote"></button>
                    <button class="ql-code-block"></button>
                </span>

                <!-- custom -->
                <span v-if="languageOptions && languageOptions.length > 0">
                    <el-select
                        v-model="selectedLanguage"
                        :placeholder="t('pick_a_language')"
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
    </QuillEditor>
    <div
        v-else
        class="flex flex-col w-full h-fit gap-2"
    >
        <div class="flex flex-row w-fit overflow-visible">
            <el-select
                v-model="selectedLanguage"
                :placeholder="t('pick_a_language')"
                size="small"
                class="min-w-40"
            >
                <el-option v-for="l in languageOptions"
                    :label="l.name"
                    :value="l.code"
                    :key="l.code"
                />
            </el-select>
        </div>
        <div v-html="content"/>
    </div>
</template>


<script setup>
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import Quill from 'quill';
let Font = Quill.import('formats/font')
// We do not add Sans Serif since it is the default
Font.whitelist = ['time-new-roman', 'arial', 'mirza', 'inconsolata']
Quill.register(Font, true)

var Size = Quill.import('attributors/style/size');
Size.whitelist = [
    '5pt',
    '6pt',
    '8pt',
    '9pt',
    '10pt',
    '11pt',
    '12pt',
    '14pt',
    '16pt',
    '18pt',
    '20pt',
    '22pt',
    '24pt',
    '28px',
    '32pt',
    '36pt',
    '48pt',
    '72pt'
];
Quill.register(Size, true);

import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import ImageUploader from 'quill-image-uploader';
import BlotFormatter from 'quill-blot-formatter';
const { t } = useI18n();
const emptyHTML = "<p></p>"

const props = defineProps({
    theme: {
        type: String,
        default: "snow"
    },
    editable: {
        type: Boolean,
        default: true
    },
    readOnly: {
        type: Boolean,
        default: false,
    },
    placeholder: {
        type: String,
        default: ''
    },
    languages: {
        type: Array,
        default: [],
        requied: false
    },
    upload: {
        type: Function,
        default: (file) => {
            return URL.createObjectURL(file);
        },
        requied: false
    }
})

const model = defineModel();
const emit = defineEmits(['change']);
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
});

watch(()=>props.modelValue, (newVal)=>{
    if (!selectedLanguage.value || selectedLanguage.value === 'origin') {
        content.value = newVal ? newVal.origin: null;
        return;
    }
    if (!newVal.translates || newVal.translates.length === 0) {
        content.value = emptyHTML;
        return;
    }
    const language = selectedLanguage.value.toLowerCase();
    const translate = newVal.translates.find((o) => o.language === language);
    if (translate) {
        content.value = translate.value;
    } else {
        content.value = emptyHTML;
    }
},{
    immediate:true
});

watch(
    content,
    (newValue) => {
        if (!props.languages) {
            model.value = newValue;
            emit('change', model.value);
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
            emit('change', model.value);
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
            emit('change', model.value);
            return;
        }
        const translate = oldModel.translates.find((o) => o.language === language);
        if (translate) {
            translate.value = newValue;
            emit('change', model.value);
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
            emit('change', model.value);
        }
    }
);

watch(selectedLanguage, (newValue) => {
    if (!props.languages || props.languages.length === 0) {
        return;
    }
    const _modelValue = model.value;
    if (!_modelValue) {
        content.value = emptyHTML;
        return;
    }
    if (!newValue || newValue === 'origin') {
        content.value =  _modelValue.origin;
        return;
    }
    if (!_modelValue.translates) {
        content.value = emptyHTML;
        return;
    }
    const translate = _modelValue.translates.find((o) => o.language === newValue.toLowerCase());
    if(translate) {
        content.value = translate.value;
    } else {
        content.value = emptyHTML;
    }
});


const modules = [
    // {
    //     name: 'htmlEditButton',
    //     module: htmlEditButton,
    //     options: {
    //         debug: false,              // default:  false
    //         syntax:false,
    //         closeOnClickOverlay: true, // default:  true                       
    //         prependSelector: null,      // default:  null 
    //         buttonHTML: "&lt/&gt;",          // default:  "&lt,&gt;"
    //         buttonTitle: t('editor_html_button_title'),
    //         msg: t('editor_html_msg'),     
    //         okText: t('Save'),
    //         cancelText: t('cancel'),   
    //         editorModules: {
    //         }
    //     }
    // },
    {
        name: 'imageUploader',
        module: ImageUploader,
        options: {
            upload: props.upload,
        }
    },
    {
        name: 'blotFormatter',
        module: BlotFormatter
    }
];
</script>
<style scoped></style>