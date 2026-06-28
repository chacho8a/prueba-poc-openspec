const App = {
    tasks: [],
    filteredTasks: [],
    editingTaskId: null,
    deletingTaskId: null,

    init() {
        console.log('App.init() - isAuthenticated:', Auth.isAuthenticated());
        console.log('Token:', Auth.getToken());
        
        if (!Auth.isAuthenticated()) {
            document.getElementById('auth-screen').style.display = 'flex';
            document.getElementById('main-screen').style.display = 'none';
            Auth.initAuthUI();
            return;
        }

        document.getElementById('auth-screen').style.display = 'none';
        document.getElementById('main-screen').style.display = 'block';
        this.initEventListeners();
        this.loadTasks();
    },

    initEventListeners() {
        document.getElementById('add-task-btn').addEventListener('click', () => this.openCreateModal());
        document.getElementById('modal-close').addEventListener('click', () => this.closeModal());
        document.getElementById('modal-cancel').addEventListener('click', () => this.closeModal());
        document.getElementById('modal-save').addEventListener('click', () => this.saveTask());
        document.getElementById('delete-modal-close').addEventListener('click', () => this.closeDeleteModal());
        document.getElementById('delete-cancel').addEventListener('click', () => this.closeDeleteModal());
        document.getElementById('delete-confirm').addEventListener('click', () => this.confirmDelete());
        document.getElementById('logout-btn').addEventListener('click', () => Auth.logout());
        document.getElementById('search-input').addEventListener('input', () => this.applyFilters());
        document.getElementById('status-filter').addEventListener('change', () => this.applyFilters());
        document.getElementById('priority-filter').addEventListener('change', () => this.applyFilters());
        document.getElementById('sort-by').addEventListener('change', () => this.applyFilters());
        document.getElementById('clear-filters-btn').addEventListener('click', () => this.clearFilters());
    },

    async loadTasks() {
        console.log('loadTasks() - iniciando carga de tareas');
        try {
            this.tasks = await API.fetchTasks();
            console.log('loadTasks() - tareas cargadas:', this.tasks);
            this.applyFilters();
        } catch (error) {
            console.error('loadTasks() - error:', error);
            this.showToast(error.message, 'error');
        }
    },

    applyFilters() {
        const searchTerm = document.getElementById('search-input').value.toLowerCase();
        const statusFilter = document.getElementById('status-filter').value;
        const priorityFilter = document.getElementById('priority-filter').value;
        const sortBy = document.getElementById('sort-by').value;

        this.filteredTasks = this.tasks.filter(task => {
            const matchesSearch = !searchTerm || 
                task.title.toLowerCase().includes(searchTerm) ||
                (task.description && task.description.toLowerCase().includes(searchTerm));
            const matchesStatus = statusFilter === 'all' || task.status === statusFilter;
            const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter;
            return matchesSearch && matchesStatus && matchesPriority;
        });

        this.sortTasks(sortBy);
        this.renderTasks();
        this.updateTaskCount();
    },

    sortTasks(sortBy) {
        switch(sortBy) {
            case 'newest':
                this.filteredTasks.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                break;
            case 'oldest':
                this.filteredTasks.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
                break;
            case 'due_date':
                this.filteredTasks.sort((a, b) => {
                    if (!a.due_date) return 1;
                    if (!b.due_date) return -1;
                    return new Date(a.due_date) - new Date(b.due_date);
                });
                break;
            case 'priority':
                const priorityOrder = { high: 0, medium: 1, low: 2 };
                this.filteredTasks.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
                break;
            case 'title':
                this.filteredTasks.sort((a, b) => a.title.localeCompare(b.title));
                break;
        }
    },

    renderTasks() {
        const taskList = document.getElementById('task-list');
        const emptyState = document.getElementById('empty-state');

        if (this.filteredTasks.length === 0) {
            taskList.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        taskList.innerHTML = this.filteredTasks.map(task => `
            <div class="task-item ${task.status === 'completed' ? 'completed' : ''}" data-id="${task.id}">
                <div class="task-content">
                    <div class="task-title">${this.escapeHtml(task.title)}</div>
                    ${task.description ? `<div class="task-description">${this.escapeHtml(task.description)}</div>` : ''}
                    <div class="task-meta">
                        <span class="task-badge badge-${task.status}">${task.status === 'pending' ? 'Pendiente' : 'Completada'}</span>
                        <span class="task-badge badge-${task.priority}">${task.priority === 'high' ? 'Alta' : task.priority === 'medium' ? 'Media' : 'Baja'}</span>
                        ${task.due_date ? `<span class="task-due-date">📅 ${task.due_date}</span>` : ''}
                    </div>
                </div>
                <div class="task-actions">
                    <button class="btn btn-secondary" onclick="App.toggleStatus(${task.id})">
                        ${task.status === 'pending' ? 'Completar' : 'Reabrir'}
                    </button>
                    <button class="btn btn-primary" onclick="App.openEditModal(${task.id})">Editar</button>
                    <button class="btn btn-danger" onclick="App.openDeleteModal(${task.id})">Eliminar</button>
                </div>
            </div>
        `).join('');
    },

    updateTaskCount() {
        const countDiv = document.getElementById('task-count');
        const total = this.tasks.length;
        const filtered = this.filteredTasks.length;
        if (filtered === total) {
            countDiv.textContent = `${total} tarea${total !== 1 ? 's' : ''}`;
        } else {
            countDiv.textContent = `Mostrando ${filtered} de ${total} tarea${total !== 1 ? 's' : ''}`;
        }
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    openCreateModal() {
        this.editingTaskId = null;
        document.getElementById('modal-title').textContent = 'Nueva Tarea';
        document.getElementById('task-title').value = '';
        document.getElementById('task-description').value = '';
        document.getElementById('task-priority').value = 'medium';
        document.getElementById('task-due-date').value = '';
        document.getElementById('status-group').style.display = 'none';
        document.getElementById('task-form-error').classList.remove('show');
        document.getElementById('task-modal').style.display = 'flex';
    },

    openEditModal(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) return;

        this.editingTaskId = taskId;
        document.getElementById('modal-title').textContent = 'Editar Tarea';
        document.getElementById('task-title').value = task.title;
        document.getElementById('task-description').value = task.description || '';
        document.getElementById('task-priority').value = task.priority;
        document.getElementById('task-due-date').value = task.due_date || '';
        document.getElementById('task-status').value = task.status;
        document.getElementById('status-group').style.display = 'block';
        document.getElementById('task-form-error').classList.remove('show');
        document.getElementById('task-modal').style.display = 'flex';
    },

    closeModal() {
        document.getElementById('task-modal').style.display = 'none';
        this.editingTaskId = null;
    },

    async saveTask() {
        const title = document.getElementById('task-title').value.trim();
        const description = document.getElementById('task-description').value.trim();
        const priority = document.getElementById('task-priority').value;
        const dueDate = document.getElementById('task-due-date').value;
        const status = document.getElementById('task-status').value;
        const errorDiv = document.getElementById('task-form-error');

        if (!title) {
            errorDiv.textContent = 'El título es obligatorio';
            errorDiv.classList.add('show');
            return;
        }

        const taskData = {
            title,
            description: description || null,
            priority,
            due_date: dueDate || null
        };

        if (this.editingTaskId) {
            taskData.status = status;
        }

        const saveBtn = document.getElementById('modal-save');
        saveBtn.disabled = true;
        saveBtn.textContent = 'Guardando...';

        try {
            if (this.editingTaskId) {
                await API.updateTask(this.editingTaskId, taskData);
                this.showToast('Tarea actualizada', 'success');
            } else {
                await API.createTask(taskData);
                this.showToast('Tarea creada', 'success');
            }
            this.closeModal();
            await this.loadTasks();
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.add('show');
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = 'Guardar';
        }
    },

    async toggleStatus(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) return;

        const newStatus = task.status === 'pending' ? 'completed' : 'pending';
        try {
            await API.updateTask(taskId, { status: newStatus });
            this.showToast('Estado actualizado', 'success');
            await this.loadTasks();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    openDeleteModal(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) return;

        this.deletingTaskId = taskId;
        document.getElementById('delete-task-title').textContent = task.title;
        document.getElementById('delete-modal').style.display = 'flex';
    },

    closeDeleteModal() {
        document.getElementById('delete-modal').style.display = 'none';
        this.deletingTaskId = null;
    },

    async confirmDelete() {
        if (!this.deletingTaskId) return;

        const confirmBtn = document.getElementById('delete-confirm');
        confirmBtn.disabled = true;
        confirmBtn.textContent = 'Eliminando...';

        try {
            await API.deleteTask(this.deletingTaskId);
            this.showToast('Tarea eliminada', 'success');
            this.closeDeleteModal();
            await this.loadTasks();
        } catch (error) {
            this.showToast(error.message, 'error');
        } finally {
            confirmBtn.disabled = false;
            confirmBtn.textContent = 'Eliminar';
        }
    },

    clearFilters() {
        document.getElementById('search-input').value = '';
        document.getElementById('status-filter').value = 'all';
        document.getElementById('priority-filter').value = 'all';
        document.getElementById('sort-by').value = 'newest';
        this.applyFilters();
    },

    showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
