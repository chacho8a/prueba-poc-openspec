const Auth = {
    TOKEN_KEY: 'task_manager_token',
    USER_KEY: 'task_manager_user',

    getToken() {
        const token = localStorage.getItem(this.TOKEN_KEY);
        console.log('getToken() - token from localStorage:', token ? token.substring(0, 20) + '...' : 'null');
        return token;
    },

    setToken(token) {
        console.log('setToken() - guardando token:', token.substring(0, 20) + '...');
        localStorage.setItem(this.TOKEN_KEY, token);
        console.log('setToken() - token guardado en localStorage');
    },

    removeToken() {
        console.log('removeToken() - removiendo token');
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
    },

    isAuthenticated() {
        const token = this.getToken();
        console.log('isAuthenticated() - token exists:', !!token);
        return !!token;
    },

    async login(email, password) {
        console.log('login() - intentando login con email:', email);
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            console.log('login() - response status:', response.status);
            if (!response.ok) {
                const error = await response.json();
                let errorMessage = 'Error al iniciar sesión';
                
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
            const data = await response.json();
            console.log('login() - login exitoso, token recibido');
            this.setToken(data.access_token);
            return data;
        } catch (error) {
            console.error('login() - error:', error);
            throw error;
        }
    },

    async register(username, email, password) {
        console.log('register() - intentando registro con username:', username, 'email:', email);
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
            console.log('register() - response status:', response.status);
            if (!response.ok) {
                const error = await response.json();
                let errorMessage = 'Error al registrarse';
                
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
            const data = await response.json();
            console.log('register() - registro exitoso, token recibido');
            this.setToken(data.access_token);
            return data;
        } catch (error) {
            console.error('register() - error:', error);
            throw error;
        }
    },

    logout() {
        this.removeToken();
        window.location.reload();
    },

    async handleLogin() {
        console.log('handleLogin - iniciando proceso de login');
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const errorDiv = document.getElementById('login-error');
        const loginBtn = document.getElementById('login-btn');
        errorDiv.classList.remove('show');

        if (!email || !password) {
            errorDiv.textContent = 'Por favor completa todos los campos';
            errorDiv.classList.add('show');
            return;
        }

        loginBtn.disabled = true;
        loginBtn.textContent = 'Iniciando sesión...';

        try {
            await this.login(email, password);
            console.log('handleLogin - login exitoso, haciendo reload');
            window.location.reload();
        } catch (error) {
            console.error('handleLogin - error:', error);
            errorDiv.textContent = error.message;
            errorDiv.classList.add('show');
        } finally {
            loginBtn.disabled = false;
            loginBtn.textContent = 'Iniciar Sesión';
        }
    },

    async handleRegister() {
        console.log('handleRegister - iniciando proceso de registro');
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const errorDiv = document.getElementById('register-error');
        const registerBtn = document.getElementById('register-btn');
        errorDiv.classList.remove('show');

        if (!username || !email || !password) {
            errorDiv.textContent = 'Por favor completa todos los campos';
            errorDiv.classList.add('show');
            return;
        }

        if (password.length < 6) {
            errorDiv.textContent = 'La contraseña debe tener al menos 6 caracteres';
            errorDiv.classList.add('show');
            return;
        }

        registerBtn.disabled = true;
        registerBtn.textContent = 'Registrando...';

        try {
            await this.register(username, email, password);
            console.log('handleRegister - registro exitoso, haciendo reload');
            window.location.reload();
        } catch (error) {
            console.error('handleRegister - error:', error);
            errorDiv.textContent = error.message;
            errorDiv.classList.add('show');
        } finally {
            registerBtn.disabled = false;
            registerBtn.textContent = 'Registrarse';
        }
    },

    initAuthUI() {
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const showRegister = document.getElementById('show-register');
        const showLogin = document.getElementById('show-login');
        const loginBtn = document.getElementById('login-btn');
        const registerBtn = document.getElementById('register-btn');
        const logoutBtn = document.getElementById('logout-btn');

        showRegister.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.style.display = 'none';
            registerForm.style.display = 'block';
        });

        showLogin.addEventListener('click', (e) => {
            e.preventDefault();
            registerForm.style.display = 'none';
            loginForm.style.display = 'block';
        });

        loginBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        registerBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        logoutBtn.addEventListener('click', () => {
            this.logout();
        });
    }
};
