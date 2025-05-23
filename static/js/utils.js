// utils.js

// Utilidades para el manejo de fechas y formato
export const dateUtils = {
    formatTimestamp: (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    formatDate: (date) => {
        return new Date(date).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
};

// Utilidades para el manejo del DOM
export const domUtils = {
    createElement: (tag, className, text = '') => {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (text) element.textContent = text;
        return element;
    },

    scrollToBottom: (element) => {
        element.scrollTo({
            top: element.scrollHeight,
            behavior: 'smooth'
        });
    },

    showElement: (element) => {
        element.classList.remove('hidden');
    },

    hideElement: (element) => {
        element.classList.add('hidden');
    },

    createMessageElement: (message, isUser = false) => {
        const messageWrapper = domUtils.createElement('div', `message-wrapper ${isUser ? 'user' : 'assistant'}`);
        const messageContent = domUtils.createElement('div', 'message-content');
        const textContent = domUtils.createElement('p', 'message-text', message.content);

        messageContent.appendChild(textContent);
        messageWrapper.appendChild(messageContent);

        return messageWrapper;
    },

    adjustTextareaHeight: (textarea) => {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
    }
};

// Utilidades para la gestión del almacenamiento local
export const storageUtils = {
    saveToLocal: (key, data) => {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('Error saving to localStorage:', error);
            return false;
        }
    },

    getFromLocal: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return null;
        }
    },

    clearLocal: (key) => {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Error clearing localStorage:', error);
            return false;
        }
    },

    saveChat: (chatId, messages) => {
        return storageUtils.saveToLocal(`chat_${chatId}`, messages);
    },

    getChat: (chatId) => {
        return storageUtils.getFromLocal(`chat_${chatId}`) || [];
    }
};

// Utilidades para el manejo de errores
export const errorUtils = {
    handleError: (error) => {
        console.error('Error:', error);

        if (axios.isAxiosError(error)) {
            if (error.response) {
                return error.response.data.message || 'Error en la respuesta del servidor';
            } else if (error.request) {
                return 'Error de conexión. Por favor, verifica tu conexión a internet.';
            }
        }

        return 'Ha ocurrido un error inesperado';
    },

    showErrorMessage: (message) => {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;

        document.body.appendChild(errorDiv);

        setTimeout(() => {
            errorDiv.classList.add('fade-out');
            setTimeout(() => {
                document.body.removeChild(errorDiv);
            }, 300);
        }, 4700);
    }
};

// Utilidades para la validación
export const validationUtils = {
    isValidMessage: (message) => {
        return message && message.trim().length > 0 && message.trim().length <= 1000;
    },

    sanitizeInput: (input) => {
        return input.trim().replace(/[<>]/g, '');
    }
};