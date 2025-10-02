<template>
  <div class="flex flex-row justify-start">
    <el-tabs tab-position="left" class="w-full">
      <el-tab-pane :label="t('All_articles')">
        <PaginationTable
          :page-size="5"
          :service="ArticleService"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :filter="filter"
        >
          <el-table-column prop="thumbnail" :label="t('Thumbnail')" min-width="86">
            <template #default="scope">
              <el-image
                v-if="scope.row.thumbnail"
                :src="scope.row.thumbnail"
                fit="fill"
                style="width: 60px; height: 60px"
              />
            </template>
          </el-table-column>
          <el-table-column prop="name" :label="t('Title')" min-width="150">
            <template #default="scope">
              {{ scope.row.title?.origin }}
            </template>
          </el-table-column>
          <el-table-column prop="slug" :label="t('Slug')" min-width="180" />
          <el-table-column
            prop="status"
            :label="t('Status')"
          >
            <template
              v-if="constantsStore && constantsStore.publishingStatuses"
              #default="scope"
            >
              {{ constantsStore.publishingStatus(scope.row.status).description }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ formatDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
      <el-tab-pane
        v-for="(section, index) in sections"
        :label="t(`Section_${section.name}`)"
        class="w-full h-full"
      >
        <WebsiteSiteSection v-model="sections[index]" :siteArticles="articles"/>
      </el-tab-pane>
    </el-tabs>
    
  </div>
</template>

<script setup>
import ArticleService from "@/services/websites/article";
import SectionService from '@/services/websites/section';
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useConstantsStore } from '@/stores/constants';
import { useOauthStore } from "@/stores/oauth";
import ConstantsService from '@/services/constants';

const props = defineProps({
	siteId: {
		type: [String,null],
		default: null
	},
});

const { t } = useI18n();
const constantsStore = useConstantsStore();
const oauthStore = useOauthStore();
const { tokenInfo } = storeToRefs(oauthStore);
const sections = ref([]);
const articles = ref([]);

const filter = computed(() => {
  if (!props.siteId) {
    return {}
  }
  return { sites__id: [props.siteId, props.siteId] };
})

const fetchData = () => {
  ConstantsService.fetch("publishing_statuses");
  if (props.siteId) {
    // Fetch sections
    SectionService.getSiteSections(props.siteId)
      .then((response) => {
        sections.value = response;
      })
      .catch(() => {
        sections.value = [];
      });
    // Fetch articles
    ArticleService.getSiteArticles(props.siteId)
      .then((response) => {
        articles.value = response;
      })
      .catch((error) => {
        console.error(error);
        articles.value =  [];
      });
  }
};

const canEdit = computed(() => oauthStore.hasOneOfScopes(["websites:articles:edit"]))

onMounted(() => {
  fetchData();
});

watch(tokenInfo, () => {
    fetchData();
});
</script>
