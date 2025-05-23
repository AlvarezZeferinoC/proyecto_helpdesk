// chat.js
import { dateUtils, domUtils, storageUtils, errorUtils, validationUtils } from './utils.js';

class ChatManager {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.suggestionButtons = document.querySelectorAll('.suggestion-button');

        this.isProcessing = false;

        this.initialize();
    }

    initialize() {
        // Configurar event listeners
        this.setupEventListeners();

        // Mensaje de bienvenida
        this.addMessage({
            content: '¡Hola! Soy el asistente virtual del Servicio de Encuadernación. ¿En qué puedo ayudarte?',
            type: 'bot'
        });
    }

    setupEventListeners() {
        // Botón de envío
        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Input de mensaje
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize del textarea
        this.messageInput.addEventListener('input', () => {
            domUtils.adjustTextareaHeight(this.messageInput);
        });

        // Sugerencias
        this.suggestionButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.messageInput.value = button.textContent;
                this.sendMessage();
            });
        });
    }

    async sendMessage() {
        if (this.isProcessing) return;

        const content = validationUtils.sanitizeInput(this.messageInput.value);

        if (!validationUtils.isValidMessage(content)) {
            errorUtils.showErrorMessage('El mensaje no puede estar vacío o exceder los 1000 caracteres.');
            return;
        }

        try {
            this.isProcessing = true;

            // Mostrar mensaje del usuario
            this.addMessage({
                content: content,
                type: 'user'
            });

            // Limpiar input
            this.messageInput.value = '';
            domUtils.adjustTextareaHeight(this.messageInput);

            // Mostrar indicador de escritura
            domUtils.showElement(this.typingIndicator);

            // Enviar mensaje al servidor
            const response = await axios.post('/api/chat/message', {
                message: content
            });

            // Ocultar indicador de escritura
            domUtils.hideElement(this.typingIndicator);

            if (response.data.status === 'success') {
                // Mostrar respuesta del bot
                this.addMessage({
                    content: response.data.message.content,
                    type: 'bot'
                });
            } else {
                throw new Error(response.data.message || 'Error al procesar el mensaje');
            }

        } catch (error) {
            domUtils.hideElement(this.typingIndicator);
            const errorMessage = errorUtils.handleError(error);
            errorUtils.showErrorMessage(errorMessage);
        } finally {
            this.isProcessing = false;
        }
    }

    addMessage(message) {
        const messageElement = domUtils.createMessageElement(message, message.type === 'user');
        this.chatMessages.appendChild(messageElement);
        domUtils.scrollToBottom(this.chatMessages);
    }
}

// Inicializar el chat cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ChatManager();
});