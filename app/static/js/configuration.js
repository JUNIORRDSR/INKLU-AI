document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos del usuario
    loadUserData();
    
    // Event listeners para formularios
    document.getElementById('personalInfoForm').addEventListener('submit', updatePersonalInfo);
    document.getElementById('passwordForm').addEventListener('submit', updatePassword);
    document.getElementById('accessibilityForm').addEventListener('submit', updateAccessibility);
    document.getElementById('notificationsForm').addEventListener('submit', updateNotifications);
    
    // Mostrar nombre de usuario
    const userDisplayName = document.getElementById('userDisplayName');
    const userData = getUserFromLocalStorage();
    if (userData && userData.name) {
        userDisplayName.textContent = userData.name;
    }
    
    // Botón de logout
    document.getElementById('logoutButton').addEventListener('click', function() {
        localStorage.removeItem('user');
        window.location.href = '/login';
    });
});

function loadUserData() {
    // Simulación: Aquí cargarías datos del usuario desde el servidor o localStorage
    const mockUserData = {
        fullName: 'Juan Pérez',
        email: 'juan.perez@example.com',
        phone: '+57 3001234567',
        preferences: {
            highContrast: false,
            largerText: true,
            voiceSpeed: 'normal'
        },
        notifications: {
            email: true,
            jobAlerts: true,
            news: false
        }
    };
    
    // Llenar formulario de información personal
    document.getElementById('fullName').value = mockUserData.fullName;
    document.getElementById('email').value = mockUserData.email;
    document.getElementById('phoneNumber').value = mockUserData.phone;
    
    // Llenar formulario de accesibilidad
    document.getElementById('highContrast').checked = mockUserData.preferences.highContrast;
    document.getElementById('largerText').checked = mockUserData.preferences.largerText;
    document.getElementById('voiceSpeed').value = mockUserData.preferences.voiceSpeed;
    
    // Llenar formulario de notificaciones
    document.getElementById('emailNotif').checked = mockUserData.notifications.email;
    document.getElementById('jobAlerts').checked = mockUserData.notifications.jobAlerts;
    document.getElementById('newsUpdates').checked = mockUserData.notifications.news;
}

function updatePersonalInfo(event) {
    event.preventDefault();
    // Aquí iría la lógica para enviar los datos al servidor
    alert('Información personal actualizada correctamente');
}

function updatePassword(event) {
    event.preventDefault();
    
    const current = document.getElementById('currentPassword').value;
    const newPass = document.getElementById('newPassword').value;
    const confirm = document.getElementById('confirmPassword').value;
    
    if (newPass !== confirm) {
        alert('Las contraseñas no coinciden');
        return;
    }
    
    // Aquí iría la lógica para validar y cambiar la contraseña
    alert('Contraseña actualizada correctamente');
    
    // Limpiar campos
    document.getElementById('currentPassword').value = '';
    document.getElementById('newPassword').value = '';
    document.getElementById('confirmPassword').value = '';
}

function updateAccessibility(event) {
    event.preventDefault();
    // Aquí iría la lógica para guardar las preferencias
    
    // Aplicar cambios inmediatamente (ejemplo)
    if (document.getElementById('largerText').checked) {
        document.body.style.fontSize = '1.1rem';
    } else {
        document.body.style.fontSize = '1rem';
    }
    
    alert('Preferencias de accesibilidad guardadas');
}

function updateNotifications(event) {
    event.preventDefault();
    // Aquí iría la lógica para actualizar las preferencias de notificaciones
    alert('Preferencias de notificaciones actualizadas');
}

function getUserFromLocalStorage() {
    const userJson = localStorage.getItem('user');
    if (userJson) {
        return JSON.parse(userJson);
    }
    return null;
}