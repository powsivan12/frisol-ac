// Navegación suave para los enlaces del menú
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            // Ajuste para la barra de navegación fija
            const headerOffset = 80;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            // Cerrar menú móvil si está abierto
            const nav = document.querySelector('.main-nav');
            const menuToggle = document.querySelector('.menu-toggle');
            if (nav && nav.classList.contains('active')) {
                nav.classList.remove('active');
                document.body.style.overflow = 'auto';
                const icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        }
    });
});

// Efecto de cambio de color del header al hacer scroll
const header = document.querySelector('header');
if (header) {
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Cambiar el fondo del header al hacer scroll
        if (currentScroll > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.background = 'white';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
        
        lastScroll = currentScroll;
    });
}

// Animación de los elementos al hacer scroll
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

// Configuración inicial cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    // Añadir clase inicial para animaciones
    const elements = document.querySelectorAll('.service-card, .about-content, .contact-container > div');
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    });
    
    // Mostrar elementos visibles al cargar la página
    setTimeout(animateOnScroll, 300);

    // Configuración del menú móvil
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    const body = document.body;

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            mainNav.classList.toggle('active');
            body.style.overflow = mainNav.classList.contains('active') ? 'hidden' : 'auto';
            
            // Cambiar el ícono entre menú y cerrar
            const icon = menuToggle.querySelector('i');
            if (icon) {
                if (mainNav.classList.contains('active')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });

        // Cerrar el menú al hacer clic en un enlace
        const navLinks = document.querySelectorAll('.nav-links a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                mainNav.classList.remove('active');
                body.style.overflow = 'auto';
                const icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            });
        });

        // Cerrar el menú al hacer clic fuera de él
        document.addEventListener('click', (e) => {
            if (!mainNav.contains(e.target) && !menuToggle.contains(e.target)) {
                mainNav.classList.remove('active');
                body.style.overflow = 'auto';
                const icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }

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
                    // Mensaje de éxito
                    formMessages.textContent = data.message || '¡Mensaje enviado con éxito!';
                    formMessages.className = 'form-message form-message-success';
                    contactForm.reset();
                    
                    // Desaparecer el mensaje después de 5 segundos
                    setTimeout(() => {
                        formMessages.textContent = '';
                        formMessages.className = 'form-message';
                    }, 5000);
                } else {
                    // Mostrar errores de validación
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

// Animación al hacer scroll
window.addEventListener('scroll', animateOnScroll);
