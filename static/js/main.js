// Navegación suave
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const headerOffset = 80;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            closeMobileMenu();
        }
    });
});

// Efecto de cambio de color del header
const header = document.querySelector('header');
if (header) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.background = 'white';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });
}

// Función para cerrar el menú móvil
function closeMobileMenu() {
    const mainNav = document.querySelector('.main-nav');
    const navOverlay = document.getElementById('navOverlay');
    const menuToggle = document.getElementById('menuToggle');
    const icon = menuToggle?.querySelector('i');
    
    if (mainNav) mainNav.classList.remove('active');
    if (navOverlay) navOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
    
    if (icon) {
        icon.className = 'fas fa-bars';
    }
}

// Configuración del menú móvil
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menuToggle');
    const mainNav = document.querySelector('.main-nav');
    const navOverlay = document.getElementById('navOverlay');

    if (menuToggle && mainNav && navOverlay) {
        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const isMenuOpen = !mainNav.classList.contains('active');
            
            // Alternar clases
            mainNav.classList.toggle('active', isMenuOpen);
            navOverlay.classList.toggle('active', isMenuOpen);
            document.body.style.overflow = isMenuOpen ? 'hidden' : 'auto';
            
            // Cambiar ícono
            const icon = menuToggle.querySelector('i');
            if (icon) {
                icon.className = isMenuOpen ? 'fas fa-times' : 'fas fa-bars';
            }
        });

        // Cerrar menú al hacer clic en el overlay
        navOverlay.addEventListener('click', closeMobileMenu);

        // Cerrar menú al hacer clic en un enlace
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });

        // Cerrar menú al hacer clic fuera de él
        document.addEventListener('click', (e) => {
            if (!mainNav.contains(e.target) && !menuToggle.contains(e.target)) {
                closeMobileMenu();
            }
        });
    }

    // Animaciones al hacer scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.service-card, .about-content, .contact-container > div');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Inicializar animaciones
    const animatedElements = document.querySelectorAll('.service-card, .about-content, .contact-container > div');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
    });

    // Mostrar elementos visibles al cargar
    setTimeout(animateOnScroll, 300);
    window.addEventListener('scroll', animateOnScroll);

    // Manejo del formulario de contacto
    const contactForm = document.getElementById('contactForm');
    const formMessages = document.getElementById('form-messages');

    if (contactForm && formMessages) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Mostrar mensaje de carga
            showFormMessage('Enviando mensaje...', 'info');
            
            // Obtener datos del formulario
            const formData = {
                nombre: contactForm.querySelector('[name="nombre"]').value.trim(),
                email: contactForm.querySelector('[name="email"]').value.trim(),
                telefono: contactForm.querySelector('[name="telefono"]').value.trim(),
                mensaje: contactForm.querySelector('[name="mensaje"]').value.trim()
            };

            // Validar campos requeridos
            if (!formData.nombre || !formData.email || !formData.mensaje) {
                showFormMessage('Por favor completa todos los campos requeridos', 'error');
                return;
            }

            // Validar formato de email
            if (!isValidEmail(formData.email)) {
                showFormMessage('Por favor ingresa un correo electrónico válido', 'error');
                return;
            }

            // Deshabilitar el botón de enviar
            const submitButton = contactForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Enviando...';

            // Enviar datos al servidor
            fetch('/enviar-mensaje', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showFormMessage('Mensaje enviado correctamente. ¡Gracias por contactarnos!', 'success');
                    contactForm.reset();
                } else {
                    throw new Error(data.message || 'Error al enviar el mensaje');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showFormMessage('Ocurrió un error al enviar el mensaje. Por favor, inténtalo de nuevo más tarde.', 'error');
            })
            .finally(() => {
                // Rehabilitar el botón de enviar
                submitButton.disabled = false;
                submitButton.textContent = 'Enviar Mensaje';
            });
        });
    }

    // Función para mostrar mensajes en el formulario
    function showFormMessage(message, type) {
        if (!formMessages) return;
        
        formMessages.textContent = message;
        formMessages.className = 'form-message';
        formMessages.classList.add(type);
        formMessages.style.display = 'block';
        
        // Ocultar mensaje después de 5 segundos (excepto si es un mensaje de éxito)
        if (type !== 'success') {
            setTimeout(() => {
                formMessages.style.opacity = '0';
                setTimeout(() => {
                    formMessages.style.display = 'none';
                    formMessages.style.opacity = '1';
                }, 300);
            }, 5000);
        }
    }

    // Función para validar email
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});