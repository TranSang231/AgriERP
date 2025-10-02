import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useExpressionsStore = defineStore('expression', {
    state: () => ({
        current_expression_id: '',
        expressions: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentExpressionId: (state) => {
            return state.current_expression_id;
        },
        allExpressions: (state) => {
            return getCachedData(state.expressions);
        }
    },
    actions: {
        setCurrentExpression(expression) {
            this.current_expression_id = expression;
        },
        setExpressions(expressions) {
            this.expressions = expressions;
        }
    },
})