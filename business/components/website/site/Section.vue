<template>
  <div class="flex flex-col w-full h-full">
    <p v-if="error" class="flex self-center justify-center text-red-800 mb-2">{{error}}</p>
    <div class="flex flex-row justify-start gap-6 w-full h-full">
      <div class="flex flex-col w-full h-full">
        <span class="text-primary font-bold">{{ t('Articles_in_this_section') }}</span>
        <draggable
          v-if = articles
          :list="articles"
          group="articles"
          itemKey="id"
          class="flex flex-col h-full p-2 gap-2 border border-gray-200"
        >
          <template #item="{ element }">
            <div class="flex flex-row items-start p-2 gap-2 border shadow border-gray-200">
              <el-image 
                v-if="element.thumbnail"
                :src="element.thumbnail"
                fit="fill"
                style="width: 40px; height: 40px"
              />
              <span>{{ element.title?.origin }}</span>
            </div>
          </template>
        </draggable>
      </div>
      <div class="flex flex-col w-full h-full">
        <span class="flex flex-row items-start text-primary font-bold">{{ t('Can_be_added') }}</span>
        <draggable
          v-if="availableArticles"
          :list="availableArticles"
          group="articles"
          itemKey="id"
          class="flex flex-col h-full p-2 gap-2 border border-gray-200"
        >
          <template #item="{ element }">
            <div class="flex flex-row items-start p-2 gap-2 border shadow border-gray-200">
              <el-image 
                v-if="element.thumbnail"
                :src="element.thumbnail"
                fit="fill"
                style="width: 40px; height: 40px"
              />
              <span>{{ element.title?.origin }}</span>
            </div>
          </template>
        </draggable>
      </div>
    </div>
    <span class="py-2 italic text-[10px] text-secondary">{{ t('Drag_articles_to_arrange') }}</span>
    <div v-if="canEdit && changed">
      <el-button type="primary" size="small" :icon="Discard" @click="discard()">
        {{t('Discard')}}
      </el-button>
      <el-button type="primary" size="small" :icon="Save" @click="onSave()">
        {{t('Save')}}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import SectionService from '@/services/websites/section';
import { useOauthStore } from "@/stores/oauth";
import ConstantsService from '@/services/constants';
import draggable from 'vuedraggable'
import { nestedDiff, toFormData } from "@/utils/obj";
import Save from '@/assets/icons/save.svg'
import Discard from '@/assets/icons/discard.svg'

const props = defineProps({
	siteArticles: {
		type: [Array, null],
		default: null
	},
});


const { t } = useI18n();
const model = defineModel();
const oauthStore = useOauthStore();
const current = ref(model.value? _cloneDeep(model.value) : null);
const articles = ref(model.value && model.value.articles
    ? _cloneDeep(model.value.articles.map((o) => o.article))
    : []
);
const availableArticles = ref([]);
const error = ref(null);

const changes = computed(() => {
    const o = model.value;
    const c = current.value;
    if (!c) {
        return null;
    }
    return nestedDiff(c, o, ["articles"]);
});

const changed = computed(()=> {
    const c = changes.value
    if (!c) {
        return false;
    }
    return Object.keys(c).length > 0;
});

const fetchData = () => {
  ConstantsService.fetch("publishing_statuses");
}

const discard = () => {
  current.value = model.value? _cloneDeep(model.value) : null;
  articles.value = current.value && current.value.articles
    ? _cloneDeep(current.value.articles)
    : []
  const sectionActicleIds = articles.value.map((o) => o.id);
  availableArticles.value = props.siteArticles
    ? props.siteArticles.filter((o) => !sectionActicleIds.includes(o.id))
    : [];
};

const onSave = () => {
  let value = changes.value;
  if (!changes.value) {
      return;
  }
  error.value = null;
  // value = toFormData(value);
  SectionService.update(value)
    .then((response) => {
        current.value = _cloneDeep(response);
        model.value = response;
        const newarticles = response.articles ? response.articles : [];
        articles.value = newarticles.map((o) => o.article);
        const newarticleIds = articles.value.map((o) => o.id)
        availableArticles.value = props.siteArticles
          ? props.siteArticles.filter((o) => !newarticleIds.includes(o.id))
          : [];

    })
    .catch((e) => {
        error.value = getErrorMessage(e, t('an_error_occurred'));
    })
};

const canEdit = computed(() => oauthStore.hasOneOfScopes(["websites:articles:edit"]));

onMounted(() => {
  fetchData();
});

watch(
  () => props.siteArticles,
  (newValue) => {
    const sectionActicleIds = articles.value
      ? articles.value.map((o) => o.id)
      : [];
    availableArticles.value = newValue
      ? newValue.filter((o) => !sectionActicleIds.includes(o.id))
      : [];
  },
  { immediate: true, deep: true }
);

watch(
  articles,
  (newValue) => {
    const values = newValue ? newValue : [];
    const currentArticles = current.value && current.value.articles
      ? current.value.articles
      : [];
    const newArticles = values.map((article, index) => {
      const existItem = currentArticles.find((o) => o.article && o.article.id === article.id);
      if (existItem) {
        return { ...existItem, order: index }; //Keep relationship model id
      } else {
        return { article: {id: article.id}, order: index }; //Just need the id, don't update other field
      }
    });

    current.value = {
      ...current.value,
      articles: newArticles
    }
  },
  { immediate: true, deep: true }
)
</script>
