import { defineStore } from 'pinia'

export const useTimekeepingStore = defineStore('timekeeping', {
  state: () => ({
    timeRecords: [],
    currentSession: null,
    dailySummary: null,
    loading: false,
    error: null
  }),

  getters: {
    allTimeRecords: (state) => state.timeRecords,
    
    getTimeRecordById: (state) => (id) => {
      return state.timeRecords.find(record => record.id === id)
    },

    getTimeRecordsByEmployee: (state) => (employeeId) => {
      return state.timeRecords.filter(record => record.employee_id === employeeId)
    },

    getTimeRecordsByDate: (state) => (date) => {
      return state.timeRecords.filter(record => {
        const recordDate = new Date(record.check_in_at).toDateString()
        return recordDate === new Date(date).toDateString()
      })
    },

    getOpenSessions: (state) => {
      return state.timeRecords.filter(record => !record.check_out_at)
    },

    getClosedSessions: (state) => {
      return state.timeRecords.filter(record => record.check_out_at)
    },

    totalWorkHours: (state) => {
      return state.timeRecords
        .filter(record => record.duration_seconds)
        .reduce((total, record) => total + (record.duration_seconds / 3600), 0)
    }
  },

  actions: {
    setTimeRecords(records) {
      this.timeRecords = records
    },

    addTimeRecord(record) {
      this.timeRecords.unshift(record)
    },

    updateTimeRecord(updatedRecord) {
      const index = this.timeRecords.findIndex(record => record.id === updatedRecord.id)
      if (index !== -1) {
        this.timeRecords[index] = updatedRecord
      }
    },

    removeTimeRecord(id) {
      this.timeRecords = this.timeRecords.filter(record => record.id !== id)
    },

    setCurrentSession(session) {
      this.currentSession = session
    },

    setDailySummary(summary) {
      this.dailySummary = summary
    },

    setLoading(loading) {
      this.loading = loading
    },

    setError(error) {
      this.error = error
    },

    clearError() {
      this.error = null
    },

    // Helper methods
    formatDuration(seconds) {
      if (!seconds) return '0h 0m'
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      return `${hours}h ${minutes}m`
    },

    formatTime(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    formatDate(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('vi-VN')
    },

    isToday(dateString) {
      if (!dateString) return false
      const today = new Date().toDateString()
      const recordDate = new Date(dateString).toDateString()
      return today === recordDate
    }
  }
})
