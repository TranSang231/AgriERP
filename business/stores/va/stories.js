import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useStoriesStore = defineStore('story', {
    state: () => ({
        current_story_id: '',
        stories: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentStoryId: (state) => {
            return state.current_story_id;
        },
        allStories: (state) => {
            return getCachedData(state.stories);
        }
    },
    actions: {
        setCurrentStory(story) {
            this.current_story_id = story;
        },
        setStories(stories) {
            this.stories = stories;
        }
    },
})