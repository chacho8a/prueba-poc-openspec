const API = {
    getAuthHeaders() {
        const token = Auth.getToken();
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
        console.log('getAuthHeaders() - headers generados:', headers);
        return headers;
    },

    async handleResponse(response) {
        console.log('handleResponse() - status:', response.status);
        if (response.status === 401) {
            console.log('handleResponse() - 401 detectado, removiendo token');
            Auth.removeToken();
            window.location.reload();
            throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
        }
        if (!response.ok) {
            const error = await response.json();
            console.error('handleResponse() - error:', error);
            let errorMessage = 'Error en la operación';
            if (error.detail) {
                if (typeof error.detail === 'string') {
                    errorMessage = error.detail;
                } else if (Array.isArray(error.detail)) {
                    errorMessage = error.detail.map(e => e.msg).join(', ');
                } else if (error.detail.msg) {
                    errorMessage = error.detail.msg;
                }
            }
            throw new Error(errorMessage);
        }
        return response.json();
    },

    async fetchTasks() {
        try {
            const headers = this.getAuthHeaders();
            console.log('fetchTasks() - headers:', headers);
            const response = await fetch('/api/tasks/', {
                method: 'GET',
                headers: headers
            });
            console.log('fetchTasks() - response status:', response.status);
            return await this.handleResponse(response);
        } catch (error) {
            console.error('fetchTasks() - error:', error);
            throw error;
        }
    },

    async createTask(taskData) {
        try {
            const response = await fetch('/api/tasks/', {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(taskData)
            });
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    },

    async getTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'GET',
                headers: this.getAuthHeaders()
            });
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    },

    async updateTask(taskId, taskData) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(taskData)
            });
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    },

    async deleteTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE',
                headers: this.getAuthHeaders()
            });
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }
};
