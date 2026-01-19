/**
 * Centralized API Service for GutIQ
 * Handles all HTTP requests to the backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class ApiService {
  /**
   * Generic request handler with error handling
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      // Handle non-2xx responses
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail ||
          errorData.message ||
          `HTTP ${response.status}: ${response.statusText}`
        );
      }

      // Handle 204 No Content (e.g., DELETE responses)
      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (error) {
      // Re-throw with additional context
      console.error(`API Error [${options.method || 'GET'} ${endpoint}]:`, error);
      throw error;
    }
  }

  /**
   * Create a new event (meal, exercise, or symptom)
   * @param {Object} eventData - Event data matching EventCreate schema
   * @returns {Promise<{event_id: number}>}
   */
  async createEvent(eventData) {
    return this.request('/events', {
      method: 'POST',
      body: JSON.stringify(eventData),
    });
  }

  /**
   * Get all events
   * @returns {Promise<Array>} Array of event objects
   */
  async getEvents() {
    return this.request('/events', {
      method: 'GET',
    });
  }

  /**
   * Get a single event by ID
   * @param {number} eventId - Event ID
   * @returns {Promise<Object>} Event object
   */
  async getEvent(eventId) {
    return this.request(`/events/${eventId}`, {
      method: 'GET',
    });
  }

  /**
   * Delete an event by ID
   * @param {number} eventId - Event ID
   * @returns {Promise<null>}
   */
  async deleteEvent(eventId) {
    return this.request(`/events/${eventId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Health check endpoint
   * @returns {Promise<Object>}
   */
  async healthCheck() {
    return this.request('/health', {
      method: 'GET',
    });
  }
}

// Export singleton instance
export default new ApiService();
