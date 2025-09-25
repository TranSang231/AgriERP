import BaseService from '@/services/base'

class TimekeepingService extends BaseService {
  get entity() {
    return 'time-records'
  }

  async fetch(force = false) {
    if (this.store && !force) {
      return this.store.allTimeRecords
    }
    try {
      const response = await this.request({
        url: `${this.entity}/`,
        method: 'GET'
      })
      if (this.store) {
        this.store.setTimeRecords(response.data)
      }
      return response.data
    } catch (error) {
      console.error('Error fetching time records:', error)
      throw error
    }
  }

  async checkIn(data) {
    try {
      const response = await this.request({
        url: `${this.entity}/check-in/`,
        method: 'POST',
        data
      })
      if (this.store) {
        this.store.addTimeRecord(response.data)
      }
      return response.data
    } catch (error) {
      console.error('Error checking in:', error)
      throw error
    }
  }

  async checkOut(id, data = {}) {
    try {
      const response = await this.request({
        url: `${this.entity}/${id}/check-out/`,
        method: 'POST',
        data
      })
      if (this.store) {
        this.store.updateTimeRecord(response.data)
      }
      return response.data
    } catch (error) {
      console.error('Error checking out:', error)
      throw error
    }
  }

  async getCurrentSession(employeeId) {
    try {
      const response = await this.request({
        url: `${this.entity}/current-session/`,
        method: 'GET',
        params: { employee_id: employeeId }
      })
      return response.data
    } catch (error) {
      if (error.response?.status === 404) {
        return null // No open session
      }
      console.error('Error getting current session:', error)
      throw error
    }
  }

  async getDailySummary(employeeId, date) {
    try {
      const response = await this.request({
        url: `${this.entity}/daily-summary/`,
        method: 'GET',
        params: { 
          employee_id: employeeId,
          date: date
        }
      })
      return response.data
    } catch (error) {
      console.error('Error getting daily summary:', error)
      throw error
    }
  }

  async getTimeRecords(params = {}) {
    try {
      const response = await this.request({
        url: `${this.entity}/`,
        method: 'GET',
        params
      })
      return response.data
    } catch (error) {
      console.error('Error getting time records:', error)
      throw error
    }
  }

  async create(data) {
    try {
      const response = await this.request({
        url: `${this.entity}/`,
        method: 'POST',
        data
      })
      if (this.store) {
        this.store.addTimeRecord(response.data)
      }
      return response.data
    } catch (error) {
      console.error('Error creating time record:', error)
      throw error
    }
  }

  async update(id, data) {
    try {
      const response = await this.request({
        url: `${this.entity}/${id}/`,
        method: 'PUT',
        data
      })
      if (this.store) {
        this.store.updateTimeRecord(response.data)
      }
      return response.data
    } catch (error) {
      console.error('Error updating time record:', error)
      throw error
    }
  }

  async delete(id) {
    try {
      await this.request({
        url: `${this.entity}/${id}/`,
        method: 'DELETE'
      })
      if (this.store) {
        this.store.removeTimeRecord(id)
      }
      return true
    } catch (error) {
      console.error('Error deleting time record:', error)
      throw error
    }
  }
}

export default new TimekeepingService()
