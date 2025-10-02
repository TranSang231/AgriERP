<template>
  <div class="flex flex-col justify-center pt-2 px-5 gap-2 w-full">
    <el-tabs v-if="model" type="border-card" class="w-full my-3" v-model="tab">
      <el-tab-pane :lazy=true :label="t('Raw_training_data')" name="raw">
        <YamlEditor v-model="model.raw" />
      </el-tab-pane>
      <el-tab-pane :lazy=true :label="t('Config')" name="config">
        <YamlEditor v-model="model.config" />
      </el-tab-pane>
      <el-tab-pane :lazy=true :label="t('NLU_data')" name="nlu">
        <YamlEditor v-model="model.nlu" />
      </el-tab-pane>
      <el-tab-pane :lazy=true :label="t('Stories')" name="stories"> 
        <YamlEditor v-model="model.stories" />  
      </el-tab-pane>
      <el-tab-pane :lazy=true :label="t('Rules')" name="rules"> 
        <YamlEditor v-model="model.rules" />  
      </el-tab-pane>
      <el-tab-pane :lazy=true :label="t('NLU_domain')" name="domain">
        <YamlEditor v-model="model.domain" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import yaml from 'js-yaml';

const props = defineProps({
	bot: {
		type: Object,
		default: null
	},
});

const { t } = useI18n();
const route = useRoute();
const tab = ref<string>(route.query.tab ? route.query.tab as string : 'general')
const model = defineModel<any>();

const markEntity = (text: string, entities: any) => {
  if (!entities || entities.length === 0) {
    return text;
  }
  const ens = entities.sort((a: any, b: any) => {
    const astart = a.start? a.start : 0;
    const bstart = b.start? b.start : 0;
    return bstart - astart;
  });
  console.log('ens:\n', ens);
  let result = text;
  ens.forEach((e: any) => {
    const entityString = `[${e.text}](${e.entity.name})`;
    console.log(entityString);
    result = result.substring(0,e.start) + entityString + result.substring(e.end);
    console.log(result);
  })
  return result;
}

const generateData = (bot: any) => {
  const { 
    id,
    config,
    entities,
    intents,
    synonyms,
    responses,
    stories,
    rules
  } = bot;
  let result: any = { config };

  // Config 
  if (config) {
    const merge = { ...config, assistant_id: id }
    result = {...result, config: yaml.dump(merge)};
  }

  // Domain
  let domain:any = {};
  if (entities && entities.length > 0) {
    const es = entities.map((o: any) => o.name);
    domain = { ...domain, entities: es };
  }
  if (intents && intents.length > 0) {
    const is = intents.map((i: any) => i.name);
    domain = { ...domain, intents: is };
  }
  if (responses) {
    let rs = {};
    responses.forEach((r: any) => {
      let {text, image, custom } = r;
      let m = {};
      if (text) {
        m = { ...m, text: text as string }
      }
      if (image) {
        m = { ...m, image: image as string }
      }
      if (custom) {
        m = { ...m, custom }
      }
      rs = {...rs, [r.name]: [m]};
    });
    domain = { ...domain, responses: rs };
  }
  result = {...result, domain: yaml.dump(domain)};

  // NLU
  let nlu = '';
  let nluData: any[] = [];
  // if(synonyms && synonyms.length > 0) {
  //   const syns = synonyms.map((s: any) => {
  //     const { reference, variants } = s;
  //     const examples = variants
  //       .map((u: any) => u.value || '')
  //       .filter((e: string) => e && e.trim().length > 0);
  //     return {
  //       synonym: reference,
  //       examples
  //     }
  //   });
  //   if (syns && syns.length > 0) {
  //     nluData = [...nluData, ...syns];
  //   }
  // }
  if(intents && intents.length > 0) {
    const ins = intents
      .map((i: any) => {
        const { name, utterances } = i;
        const us = utterances.map((u: any) => {
          const { text, entities } = u;
          return markEntity(text, entities);
        });
        const examples = us && us.length > 0
          ? yaml.dump(us, {
            styles: {
              '!!str': 'literal'
            }
          })
          :null;
        return {
          intent: name,
          examples
        }
      })
      .filter((i: any) => i.examples && i.examples.length > 0)
    if (ins && ins.length > 0) {
      nluData = [...nluData, ...ins];
    }
  }
  nlu = yaml.dump({nlu: nluData});
  result = {...result, nlu};

  // Stories
  // Todo: optimize later
  if(stories && stories.length > 0) {
    const ss = stories
      .map((s: any) => {
        let { name, steps } = s;
        steps = steps
          .sort((a: any, b: any) => {
            const ao = a.order? a.order : 0;
            const bo = b.order? b.order : 0;
            return ao - bo;
          })
          .map((i: any) => {
            const { type, payload } = i;
            if (type === 'intent') {
              const { name: n } = payload;
              return { [type]: n}
            }
            if (type === 'response') {
              const { name: n } = payload;
              return { action: n}
            }
          });
        return {
          story: name,
          steps
        }
      });
    if (ss && ss.length > 0) {
      result = { ...result, stories: yaml.dump({stories: ss})};
    }
  }

  // Rules
  // Todo: optimize later
  if(rules && rules.length > 0) {
    const rs = rules
      .map((r: any) => {
        let { name, steps, conversation_start,  wait_for_user_input} = r;
        steps = steps
          .sort((a: any, b: any) => {
            const ao = a.order? a.order : 0;
            const bo = b.order? b.order : 0;
            return ao - bo;
          })
          .map((i: any) => {
            const { type, payload } = i;
            if (type === 'intent') {
              const { name: n } = payload;
              return { [type]: n}
            }
            if (type === 'response') {
              const { name: n } = payload;
              return { action: n}
            }
          });
        let rule: any = {
          rule: name,
          steps
        };
        if (conversation_start) {
          rule = { ...rule, conversation_start };
        }
        if (!wait_for_user_input) {
          rule = { ...rule, wait_for_user_input };
        }
        return rule;
      });
    if (rs && rs.length > 0) {
      result = { ...result, rules: yaml.dump({rules: rs})};
    }
  }
  
  model.value = result;
}

const trainingData = computed(() => {
  if (!model.value) {
    return null;
  }
  let { config,  domain, nlu, stories, rules } = model.value;
  let data = '';
  data += config ? config: '\n';
  data += domain ? domain: '\n';
  data += nlu ? nlu: '\n';
  data += stories ? stories: '\n';
  data += rules ? rules: '\n';
  return data;
});

watch(tab, (newValue) => {
  // Update the query parameter without redender components.
  const queryParams = new URLSearchParams(window.location.search);
  queryParams.set('tab', newValue);
  history.replaceState(null, '', "?"+queryParams.toString());
});

watch(
  () => props.bot,
  (newValue) => {
    generateData(newValue);
  }
);

watch(
  trainingData,
  (raw) => {
    model.value = {...model.value, raw};
  }
);

onMounted(() => {
    if (props.bot && !model.value) {
      generateData(props.bot);
    }
});
</script>
