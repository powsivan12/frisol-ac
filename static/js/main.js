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
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    });

    // Mostrar elementos visibles al cargar
    setTimeout(animateOnScroll, 300);
    window.addEventListener('scroll', animateOnScroll);

    // Manejo del formulario de contacto
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const formMessages = document.getElementById('form-messages');
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            
            // Mostrar mensaje de carga
            formMessages.textContent = 'Enviando mensaje...';
            formMessages.className = 'form-message form-message-info';
            formMessages.style.display = 'block';
            submitButton.disabled = true;
            submitButton.innerHTML = 'Enviando...';
            
            fetch('/enviar-mensaje', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]')?.value || ''
                },
                body: JSON.stringify(Object.fromEntries(formData))
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    formMessages.textContent = data.message || '¡Mensaje enviado con éxito!';
                    formMessages.className = 'form-message form-message-success';
                    contactForm.reset();
                    
                    // Desaparecer el mensaje después de 5 segundos
                    setTimeout(() => {
                        formMessages.style.display = 'none';
                    }, 5000);
                } else {
                    let errorMessage = data.message || 'Por favor corrige los siguientes errores:';
                    if (data.errors) {
                        errorMessage += '\n';
                        for (const field in data.errors) {
                            errorMessage += `- ${data.errors[field].join(', ')}\n`;
                        }
                    }
                    formMessages.textContent = errorMessage;
                    formMessages.className = 'form-message form-message-error';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                formMessages.textContent = 'Hubo un error al enviar el mensaje. Por favor, intente nuevamente más tarde.';
                formMessages.className = 'form-message form-message-error';
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            });
        });
    }
});