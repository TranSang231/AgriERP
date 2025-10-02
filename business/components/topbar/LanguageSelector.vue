<template>
    <el-select
        v-if="localeStore && localeStore.supportedLanguages"
        v-model="selected"
        value-key="code"
        :placeholder="t('pick_a_language')"
        class="min-w-36"
    >
        <template #prefix>
            <FlagIcon
                v-if="selected.flag"
                :code="selected.flag as CountryCode"
            />
        </template>
        <el-option
            v-for="language in localeStore.supportedLanguages"
            :key="language.code"
            :label="language.name"
            :value="language"
            class="flex flex-row gap-2 px-2"
        >
            <FlagIcon
                v-if="language.flag"
                :code="(language.flag as CountryCode)"
            />
            <span>{{language.name}}</span>
        </el-option>
    </el-select>
</template>

<script setup lang="ts">
import 'vue3-flag-icons/styles'
import FlagIcon from 'vue3-flag-icons'
import type { CountryCode } from 'vue3-flag-icons';
import { useLocaleStore } from '@/stores/locale';
const localeStore = useLocaleStore();
const { t, locale, setLocale } = useI18n();
if (locale && localeStore && locale.value != localeStore.currentLangue.code) {
    setLocale(localeStore.currentLangue.code);
}
const selected = ref(localeStore.currentLangue);
watch(selected, (newVal) => {
    localeStore.setCurrentLangue(newVal);
    setLocale(newVal.code);
});
</script>