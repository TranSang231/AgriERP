import { defineStore } from 'pinia';
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useConstantsStore = defineStore('constants', {
    state: () => ({
        application_types: {
            ...createCachedEntry([], 0)
        },
        client_types: {
            ...createCachedEntry([], 0)
        },
        algorithm_types: {
            ...createCachedEntry([], 0)
        },
        grant_types: {
            ...createCachedEntry([], 0)
        },
        account_statuses: {
            ...createCachedEntry([], 0)
        },
        paper_validate_statuses: {
            ...createCachedEntry([], 0)
        },
        publishing_statuses: {
            ...createCachedEntry([], 0)
        },
        access_modes: { 
        ...createCachedEntry([], 0)
        },
        email_template_types: {
            ...createCachedEntry([], 0)
        },
        sms_template_types: {
            ...createCachedEntry([], 0)
        },
        marketing_campaign_meta_data: {
            ...createCachedEntry([], 0)
        },
        payment_methods: {
            ...createCachedEntry([], 0)
        },
        payment_statuses: {
            ...createCachedEntry([], 0)
        },
        shipping_statuses: {
            ...createCachedEntry([], 0)
        },
        nlu_data_types: {
            ...createCachedEntry([], 0)
        },
        nlu_config_template: {
            ...createCachedEntry({}, 0)
        },
        story_step_types: {
            ...createCachedEntry([], 0)
        },
        website_build_statuses: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        applicationTypes: (state) => {
            return getCachedData(state.application_types);
        },
        clientTypes: (state) => {
            return getCachedData(state.client_types);
        },
        algorithmTypes: (state) => {
            return getCachedData(state.algorithm_types);
        },
        grantTypes: (state) => {
            return getCachedData(state.grant_types);
        },
        accountStatuses: (state) => {
            return getCachedData(state.account_statuses);
        },
        paperValidateStatuses: (state) => {
            return getCachedData(state.paper_validate_statuses);
        },
        publishingStatuses: (state) => {
            return getCachedData(state.publishing_statuses);
        },
        publishingStatus: (state) => {
            return (value) => {
                const data = getCachedData(state.publishing_statuses)
                return data.find((o) => o.value === value)
            }
        },
        accessModes: (state) => { 
            return getCachedData(state.access_modes);
         },
        accessMode: (state) => {  
            return (value) => {
                const data = getCachedData(state.access_modes);
                return data.find((o) => o.value === value);
            };
        },
        assesModeDescription: (state) => {  
            return (value) => {
                const data = getCachedData(state.access_modes);
                const mode = data.find((o) => o.value === value);
                return mode ? mode.description : '';
            };
        },
        emailTemplateTypes: (state) => {
            return getCachedData(state.email_template_types);
        },
        smsTemplateTypes: (state) => {
            return getCachedData(state.sms_template_types);
        },
        marketingCampaignMetaData: (state) => {
            return getCachedData(state.marketing_campaign_meta_data);
        },
        paymentMethods: (state) => {
            return getCachedData(state.payment_methods);
        },
        paymentMethod: (state) => {
            return (value) => {
                const data = getCachedData(state.payment_methods)
                return data.find((o) => o.value === value)
            }
        },
        paymentMethodDescription: (state) => {
            return (value) => {
                const data = getCachedData(state.payment_methods)
                const m = data.find((o) => o.value === value)
                return m ? m.description: '';
            }
        },
        paymentStatuses: (state) => {
            return getCachedData(state.payment_statuses);
        },
        paymentStatus: (state) => {
            return (value) => {
                const data = getCachedData(state.payment_statuses)
                return data.find((o) => o.value === value)
            }
        },
        paymentStatusDescription: (state) => {
            return (value) => {
                const data = getCachedData(state.payment_statuses)
                const s = data.find((o) => o.value === value)
                return s ? s.description : '';
            }
        },
        shippingStatuses: (state) => {
            return getCachedData(state.shipping_statuses);
        },
        shippingStatus: (state) => {
            return (value) => {
                const data = getCachedData(state.shipping_statuses)
                return data.find((o) => o.value === value)
            }
        },
        shippingStatusDescription: (state) => {
            return (value) => {
                const data = getCachedData(state.shipping_statuses)
                const s = data.find((o) => o.value === value)
                return s ? s.description : ''
            }
        },
        nluDataTypes: (state) => {
            return getCachedData(state.nlu_data_types);
        },
        nluDataType: (state) => {
            return (value) => {
                const data = getCachedData(state.nlu_data_types)
                return data.find((o) => o.value === value)
            }
        },
        nluDataTypeDescription: (state) => {
            return (value) => {
                const data = getCachedData(state.nlu_data_types)
                const s = data.find((o) => o.value === value)
                return s ? s.description : ''
            }
        },
        nluConfigTemplate: (state) => {
            return getCachedData(state.nlu_config_template);
        },
        storyStepTypes: (state) => {
            return getCachedData(state.story_step_types);
        },
        storyStepType: (state) => {
            return (value) => {
                const data = getCachedData(state.story_step_types)
                return data.find((o) => o.value === value)
            }
        },
        storyStepTypeDescription: (state) => {
            return (value) => {
                const data = getCachedData(state.story_step_types)
                const s = data.find((o) => o.value === value)
                return s ? s.description : ''
            }
        },
        websiteBuildStatus: (state) => {
            return (value) => {
                const data = getCachedData(state.website_build_statuses)
                return data.find((o) => o.value === value)
            }
        },
        getConstant: (state) => {
            return (name) =>  {
                return state[name];
            }
        }
    },
    actions: {
        setConstant(key, value) {
            this.$patch({[key]: value});
        },
        patch(values) {
            this.$patch(values);
        }
    },
})