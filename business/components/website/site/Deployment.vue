<template>
	<div v-if="fetching" class="flex flex-col w-full items-center mt-5 gap-5 justify-center content-center">
		<div v-loading="true"/>
		<div class="ps-10"><span>{{ t('Fetching_data') }}</span></div>
	</div>
	<div v-else class="flex flex-col w-full">
		<el-button
			type="primary"
			:disabled="!canEdit"
			@click="deploy"
			class="self-end px-2 my-2"
		>
			New Deploy
		</el-button>
		<el-card v-for="build in builds">
			<div class="w-full grid grid-flow-row grid-cols-4 gap-4">
				<span class="text-right">{{ t('Created_at') }}:</span>
				<span class="col-span-3">{{ utcToLocalDateTime(build.created_at) }}</span>
				<span class="text-right">{{ t('Status') }}:</span>
				<span class="col-span-3">{{ constantsStore.websiteBuildStatus(build.status).description }}</span>
			</div>
		</el-card>
	</div>
</template>

<script setup>
import { utcToLocalDateTime } from "@/utils/time";
import BuildService from '@/services/websites/build';
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
const builds = ref([]);
const fetching = ref(true);

const fetchData = async () => {
	ConstantsService.fetch("website_build_statuses");
	if (props.siteId) {
		fetching.value = true;
    BuildService.getSiteBuilds(props.siteId)
      .then((response) => {
		const results = response.sort((a,b) => Date.parse(b.created_at) - Date.parse(a.created_at))
        builds.value = results;
      })
      .catch(() => {
        builds.value = [];
      })
      .finally(() => {
        fetching.value = false;
      });
	}
}

const canEdit = computed(() => oauthStore.hasOneOfScopes(["websites:sites:edit"]))

const deploy = async () => {
	if (!props.siteId) {
		return;
	}
    BuildService.create({ "site_id": props.siteId })
		.then ((response) => {
			builds.value = [...builds.value, response];
		})
		.catch ((error) => {
			console.error(error);
		});
};

onMounted(() => {
  fetchData();
});

watch(tokenInfo, () => {
  fetchData();
});
</script>