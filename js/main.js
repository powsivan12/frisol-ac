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
            const nav = document.querySelector('nav');
            if (nav.classList.contains('active')) {
                nav.classList.remove('active');
                document.querySelector('.menu-toggle').classList.remove('active');
            }
        }
    });
});

// Efecto de cambio de color del header al hacer scroll
const header = document.querySelector('header');
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

// Configuración inicial de la animación
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
    
    // Configurar el menú móvil
    const menuToggle = document.createElement('div');
    menuToggle.className = 'menu-toggle';
    menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    document.querySelector('header .container').appendChild(menuToggle);
    
    menuToggle.addEventListener('click', () => {
        document.querySelector('nav').classList.toggle('active');
        menuToggle.classList.toggle('active');
    });
    
    // Cerrar menú al hacer clic en un enlace
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', () => {
            document.querySelector('nav').classList.remove('active');
            menuToggle.classList.remove('active');
        });
    });
});

// Animación al hacer scroll
window.addEventListener('scroll', animateOnScroll);

// Manejo del formulario de contacto
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitButton = this.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.innerHTML;
        
        try {
            // Mostrar indicador de carga
            submitButton.disabled = true;
            submitButton.innerHTML = 'Enviando...';
            
            // Obtener los datos del formulario
            const formData = {
                name: this.querySelector('[name="name"]').value,
                email: this.querySelector('[name="email"]').value,
                phone: this.querySelector('[name="phone"]').value || 'No proporcionado',
                message: this.querySelector('[name="message"]').value
            };
            
            // Enviar datos al servidor como JSON
            const response = await fetch('/enviar-mensaje', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Mostrar mensaje de éxito
                showMessage('¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.', 'success');
                // Reiniciar el formulario
                this.reset();
            } else {
                // Mostrar errores de validación
                if (data.errors) {
                    let errorMessage = 'Por favor corrige los siguientes errores:\n';
                    for (const field in data.errors) {
                        errorMessage += `- ${data.errors[field][0]}\n`;
                    }
                    showMessage(errorMessage, 'error');
                } else {
                    showMessage(data.message || 'Error al enviar el mensaje. Por favor, inténtalo de nuevo más tarde.', 'error');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error de conexión. Por favor, verifica tu conexión a Internet e inténtalo de nuevo.', 'error');
        } finally {
            // Restaurar el botón
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonText;
        }
    });
}

// Función para mostrar mensajes
function showMessage(message, type = 'success') {
    const messageDiv = document.getElementById('form-messages');
    if (!messageDiv) return;
    
    messageDiv.textContent = message;
    messageDiv.className = 'form-message ' + type;
    messageDiv.style.display = 'block';
    
    // Ocultar el mensaje después de 5 segundos
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.style.display = 'none';
            messageDiv.style.opacity = '1';
        }, 500);
    }, 5000);
}

// Contador de estadísticas (opcional)
function initCounter() {
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const increment = target / 100;
            
            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(initCounter, 10);
            } else {
                counter.innerText = target;
            }
        });
    }
}

// Iniciar contadores cuando sean visibles
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            initCounter();
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.counter').forEach(counter => {
    observer.observe(counter);
});
