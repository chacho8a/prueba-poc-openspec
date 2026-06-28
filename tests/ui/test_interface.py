import pytest
import re


class TestAuthUI:
    """Tests de interfaz para autenticación"""

    def test_login_screen_visible(self, page, base_url):
        """Verifica que la pantalla de login es visible al cargar"""
        page.goto(base_url)
        
        # Verificar que el formulario de login está visible
        assert page.is_visible("#login-form")
        assert page.is_visible("#login-email")
        assert page.is_visible("#login-password")
        assert page.is_visible("#login-btn")

    def test_switch_to_register_form(self, page, base_url):
        """Verifica que se puede cambiar al formulario de registro"""
        page.goto(base_url)
        
        # Click en el enlace de registro
        page.click("#show-register")
        
        # Verificar que el formulario de registro está visible
        assert page.is_visible("#register-form")
        assert page.is_visible("#register-username")
        assert page.is_visible("#register-email")
        assert page.is_visible("#register-password")
        assert page.is_visible("#register-btn")

    def test_switch_back_to_login_form(self, page, base_url):
        """Verifica que se puede volver al formulario de login desde registro"""
        page.goto(base_url)
        
        # Ir a registro
        page.click("#show-register")
        assert page.is_visible("#register-form")
        
        # Volver a login
        page.click("#show-login")
        assert page.is_visible("#login-form")

    def test_login_validation_empty_fields(self, page, base_url):
        """Verifica validación de campos vacíos en login"""
        page.goto(base_url)
        
        # Click en login sin llenar campos
        page.click("#login-btn")
        
        # Verificar mensaje de error
        error_msg = page.text_content("#login-error")
        assert "completa todos los campos" in error_msg.lower()

    def test_login_invalid_credentials(self, page, base_url):
        """Verifica mensaje de error con credenciales inválidas"""
        page.goto(base_url)
        
        # Llenar campos con credenciales inválidas
        page.fill("#login-email", "invalid@example.com")
        page.fill("#login-password", "wrongpassword")
        
        # Click en login
        page.click("#login-btn")
        
        # Verificar mensaje de error (esperar a que aparezca)
        page.wait_for_selector("#login-error.show", timeout=5000)
        error_msg = page.text_content("#login-error")
        assert error_msg is not None
        assert len(error_msg) > 0

    def test_register_validation_empty_fields(self, page, base_url):
        """Verifica validación de campos vacíos en registro"""
        page.goto(base_url)
        page.click("#show-register")
        
        # Click en registro sin llenar campos
        page.click("#register-btn")
        
        # Verificar mensaje de error
        error_msg = page.text_content("#register-error")
        assert "completa todos los campos" in error_msg.lower()

    def test_register_validation_short_password(self, page, base_url):
        """Verifica validación de contraseña corta en registro"""
        page.goto(base_url)
        page.click("#show-register")
        
        # Llenar campos con contraseña corta
        page.fill("#register-username", "testuser")
        page.fill("#register-email", "test@example.com")
        page.fill("#register-password", "123")
        
        # Click en registro
        page.click("#register-btn")
        
        # Verificar mensaje de error
        error_msg = page.text_content("#register-error")
        assert "6 caracteres" in error_msg

    def test_successful_registration(self, page, base_url, test_user):
        """Verifica registro exitoso y redirección a pantalla principal"""
        page.goto(base_url)
        page.click("#show-register")
        
        # Llenar formulario de registro
        page.fill("#register-username", test_user["username"])
        page.fill("#register-email", test_user["email"])
        page.fill("#register-password", test_user["password"])
        
        # Click en registro
        page.click("#register-btn")
        
        # Esperar a que cargue la pantalla principal
        page.wait_for_selector("#main-screen", state="visible", timeout=10000)
        
        # Verificar que la pantalla principal está visible
        assert page.is_visible("#main-screen")
        assert page.is_visible("#add-task-btn")

    def test_successful_login(self, page, base_url, test_user):
        """Verifica login exitoso y redirección a pantalla principal"""
        # Primero registrar usuario
        page.goto(base_url)
        page.click("#show-register")
        page.fill("#register-username", test_user["username"])
        page.fill("#register-email", test_user["email"])
        page.fill("#register-password", test_user["password"])
        page.click("#register-btn")
        page.wait_for_selector("#main-screen", state="visible", timeout=10000)
        
        # Logout
        page.click("#logout-btn")
        page.wait_for_selector("#login-form", state="visible", timeout=10000)
        
        # Login
        page.fill("#login-email", test_user["email"])
        page.fill("#login-password", test_user["password"])
        page.click("#login-btn")
        
        # Esperar a que cargue la pantalla principal
        page.wait_for_selector("#main-screen", state="visible", timeout=10000)
        
        # Verificar que la pantalla principal está visible
        assert page.is_visible("#main-screen")

    def test_logout(self, page, base_url, test_user):
        """Verifica que el logout redirige a pantalla de login"""
        # Registrar e iniciar sesión
        page.goto(base_url)
        page.click("#show-register")
        page.fill("#register-username", test_user["username"])
        page.fill("#register-email", test_user["email"])
        page.fill("#register-password", test_user["password"])
        page.click("#register-btn")
        page.wait_for_selector("#main-screen", state="visible", timeout=10000)
        
        # Logout
        page.click("#logout-btn")
        
        # Verificar que vuelve a pantalla de login
        page.wait_for_selector("#login-form", state="visible", timeout=10000)
        assert page.is_visible("#login-form")


class TestTasksUI:
    """Tests de interfaz para gestión de tareas"""

    def _register_and_login(self, page, base_url, test_user):
        """Helper para registrar un usuario y estar en la pantalla principal"""
        page.goto(base_url)
        page.click("#show-register")
        page.fill("#register-username", test_user["username"])
        page.fill("#register-email", test_user["email"])
        page.fill("#register-password", test_user["password"])
        page.click("#register-btn")
        page.wait_for_selector("#main-screen", state="visible", timeout=10000)

    def test_main_screen_elements(self, page, base_url, test_user):
        """Verifica que los elementos principales de la pantalla están visibles"""
        self._register_and_login(page, base_url, test_user)
        assert page.is_visible("#add-task-btn")
        assert page.is_visible("#search-input")
        assert page.is_visible("#status-filter")
        assert page.is_visible("#priority-filter")
        assert page.is_visible("#sort-by")

    def test_empty_state_visible(self, page, base_url, test_user):
        """Verifica que el estado vacío se muestra cuando no hay tareas"""
        self._register_and_login(page, base_url, test_user)
        assert page.is_visible("#empty-state")
        empty_text = page.text_content("#empty-state")
        assert "no hay tareas" in empty_text.lower()

    def test_open_create_task_modal(self, page, base_url, test_user):
        """Verifica que se abre el modal de crear tarea"""
        self._register_and_login(page, base_url, test_user)
        page.click("#add-task-btn")
        
        # Verificar que el modal está visible
        assert page.is_visible("#task-modal")
        assert page.is_visible("#task-title")
        assert page.is_visible("#task-description")
        assert page.is_visible("#task-priority")
        assert page.is_visible("#task-due-date")

    def test_create_task_validation(self, page, base_url, test_user):
        """Verifica validación de título vacío al crear tarea"""
        self._register_and_login(page, base_url, test_user)
        page.click("#add-task-btn")
        
        # Intentar guardar sin título
        page.click("#modal-save")
        
        # Verificar mensaje de error
        error_msg = page.text_content("#task-form-error")
        assert "título es obligatorio" in error_msg.lower()

    def test_create_task_success(self, page, base_url, test_user):
        """Verifica creación exitosa de tarea"""
        self._register_and_login(page, base_url, test_user)
        page.click("#add-task-btn")
        
        # Llenar formulario
        page.fill("#task-title", "Tarea de prueba")
        page.fill("#task-description", "Descripción de prueba")
        page.select_option("#task-priority", "high")
        
        # Guardar
        page.click("#modal-save")
        
        # Verificar que el modal se cerró
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Verificar que la tarea aparece en la lista
        page.wait_for_selector(".task-item", timeout=5000)
        task_title = page.text_content(".task-title")
        assert "Tarea de prueba" in task_title

    def test_create_multiple_tasks(self, page, base_url, test_user):
        """Verifica creación de múltiples tareas"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear primera tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea 1")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Crear segunda tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea 2")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Crear tercera tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea 3")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Verificar que hay 3 tareas
        tasks = page.query_selector_all(".task-item")
        assert len(tasks) == 3

    def test_toggle_task_status(self, page, base_url, test_user):
        """Verifica cambio de estado de tarea"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea para completar")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        page.wait_for_selector(".task-item", timeout=5000)
        
        # Verificar estado inicial (pendiente)
        badge = page.text_content(".badge-pending, .badge-completed")
        assert "pendiente" in badge.lower()
        
        # Click en completar
        page.click("button:has-text('Completar')")
        
        # Esperar a que se actualice
        page.wait_for_timeout(1000)
        
        # Verificar nuevo estado
        page.wait_for_selector(".badge-completed", timeout=5000)
        badge = page.text_content(".badge-completed")
        assert "completada" in badge.lower()

    def test_open_edit_modal(self, page, base_url, test_user):
        """Verifica que se abre el modal de editar tarea"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea para editar")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        page.wait_for_selector(".task-item", timeout=5000)
        
        # Click en editar
        page.click("button:has-text('Editar')")
        
        # Verificar que el modal está visible con datos de la tarea
        page.wait_for_selector("#task-modal", state="visible", timeout=5000)
        title_value = page.input_value("#task-title")
        assert "Tarea para editar" in title_value

    def test_edit_task_success(self, page, base_url, test_user):
        """Verifica edición exitosa de tarea"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Título original")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        page.wait_for_selector(".task-item", timeout=5000)
        
        # Editar tarea
        page.click("button:has-text('Editar')")
        page.wait_for_selector("#task-modal", state="visible", timeout=5000)
        page.fill("#task-title", "Título modificado")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Verificar que el título cambió
        page.wait_for_timeout(1000)
        task_title = page.text_content(".task-title")
        assert "Título modificado" in task_title

    def test_open_delete_modal(self, page, base_url, test_user):
        """Verifica que se abre el modal de confirmación de eliminación"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea para eliminar")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        page.wait_for_selector(".task-item", timeout=5000)
        
        # Click en eliminar
        page.click("button:has-text('Eliminar')")
        
        # Verificar que el modal de confirmación está visible
        page.wait_for_selector("#delete-modal", state="visible", timeout=5000)
        assert page.is_visible("#delete-modal")
        delete_text = page.text_content("#delete-task-title")
        assert "Tarea para eliminar" in delete_text

    def test_cancel_delete(self, page, base_url, test_user):
        """Verifica que se puede cancelar la eliminación"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea para no eliminar")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        page.wait_for_selector(".task-item", timeout=5000)
        
        # Click en eliminar
        page.click("button:has-text('Eliminar')")
        page.wait_for_selector("#delete-modal", state="visible", timeout=5000)
        
        # Cancelar
        page.click("#delete-cancel")
        
        # Verificar que el modal se cerró
        page.wait_for_selector("#delete-modal", state="hidden", timeout=5000)
        
        # Verificar que la tarea aún existe
        tasks = page.query_selector_all(".task-item")
        assert len(tasks) == 1

    def test_confirm_delete(self, page, base_url, test_user):
        """Verifica eliminación exitosa de tarea"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea a eliminar")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        page.wait_for_selector(".task-item", timeout=5000)
        
        # Confirmar eliminación
        page.click("button:has-text('Eliminar')")
        page.wait_for_selector("#delete-modal", state="visible", timeout=5000)
        page.click("#delete-confirm")
        
        # Verificar que la tarea fue eliminada
        page.wait_for_selector(".task-item", state="detached", timeout=5000)
        tasks = page.query_selector_all(".task-item")
        assert len(tasks) == 0

    def test_search_tasks(self, page, base_url, test_user):
        """Verifica búsqueda de tareas"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tareas
        for i in range(3):
            page.click("#add-task-btn")
            page.fill("#task-title", f"Tarea {i}")
            page.click("#modal-save")
            page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Buscar
        page.fill("#search-input", "Tarea 1")
        page.wait_for_timeout(500)
        
        # Verificar que solo se muestra la tarea buscada
        tasks = page.query_selector_all(".task-item")
        assert len(tasks) == 1
        task_title = page.text_content(".task-title")
        assert "Tarea 1" in task_title

    def test_filter_by_status(self, page, base_url, test_user):
        """Verifica filtro por estado"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tareas
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea pendiente")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea completada")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Completar segunda tarea
        page.click(".task-item >> nth=0 >> button:has-text('Completar')")
        page.wait_for_timeout(1000)
        
        # Filtrar por pendientes
        page.select_option("#status-filter", "pending")
        page.wait_for_timeout(500)
        
        # Verificar que solo se muestran pendientes
        tasks = page.query_selector_all(".task-item")
        assert len(tasks) == 1

    def test_clear_filters(self, page, base_url, test_user):
        """Verifica que se pueden limpiar los filtros"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tarea
        page.click("#add-task-btn")
        page.fill("#task-title", "Tarea de prueba")
        page.click("#modal-save")
        page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Aplicar filtro
        page.fill("#search-input", "xyz")
        page.wait_for_timeout(500)
        
        # Limpiar filtros
        page.click("#clear-filters-btn")
        page.wait_for_timeout(500)
        
        # Verificar que la tarea vuelve a aparecer
        tasks = page.query_selector_all(".task-item")
        assert len(tasks) == 1

    def test_task_count_display(self, page, base_url, test_user):
        """Verifica que se muestra el conteo de tareas"""
        self._register_and_login(page, base_url, test_user)
        
        # Crear tareas
        for i in range(3):
            page.click("#add-task-btn")
            page.fill("#task-title", f"Tarea {i}")
            page.click("#modal-save")
            page.wait_for_selector("#task-modal", state="hidden", timeout=5000)
        
        # Verificar conteo
        count_text = page.text_content("#task-count")
        assert "3" in count_text
        assert "tarea" in count_text.lower()
