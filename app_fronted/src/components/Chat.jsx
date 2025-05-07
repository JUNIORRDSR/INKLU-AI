import React, { useState, useEffect, useRef } from 'react';
import '../index.css';

function Chat() {
  // Manejo del tema directamente en el componente (sin contexto)
  const [darkMode, setDarkMode] = useState(false);
  const toggleDarkMode = () => setDarkMode(!darkMode);
  
  // Estados para el chat
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      content: '¡Hola! Soy Inklú-IA, tu asistente personal. ¿En qué puedo ayudarte hoy?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isRecording, setIsRecording] = useState(false); // Nuevo estado para grabación
  const messagesEndRef = useRef(null);

  // Sugerencias
  const sugerencias = [
    "¿Cómo hacer una hoja de vida?",
    "¿Qué es una nómina?",
    "¿Cuáles son mis derechos laborales?",
    "Ayúdame a redactar una carta de presentación"
  ];

  // Auto-scroll al último mensaje
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Simular respuesta de la IA
  const simulateResponse = (userMessage) => {
    setIsTyping(true);
    
    let botResponse = '';
    
    if (userMessage.toLowerCase().includes('hoja de vida') || userMessage.toLowerCase().includes('curriculum')) {
      botResponse = 'Para crear una hoja de vida, es importante destacar tus habilidades y competencias relevantes. Incluye una sección de "Adaptaciones" donde menciones los ajustes que necesitas para desempeñar tu trabajo de manera óptima.';
    } 
    else if (userMessage.toLowerCase().includes('nómina')) {
      botResponse = 'Una nómina es un documento que refleja el pago que recibe un trabajador por sus servicios, incluyendo el salario base, deducciones y beneficios. Las personas con discapacidad pueden tener beneficios fiscales específicos.';
    }
    else if (userMessage.toLowerCase().includes('derechos laborales')) {
      botResponse = 'Las personas con discapacidad tienen garantizados los mismos derechos laborales que cualquier trabajador, además de protecciones adicionales como el derecho a ajustes razonables en el lugar de trabajo.';
    }
    else {
      botResponse = 'Gracias por tu mensaje. Estoy aquí para ayudarte con todo lo relacionado a empleo inclusivo y orientación laboral. ¿En qué más puedo ayudarte?';
    }
    
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: prev.length + 2,
        sender: 'bot',
        content: botResponse,
        timestamp: new Date()
      }]);
      setIsTyping(false);
    }, 1500);
  };

  // Manejar envío de mensaje
  const handleSendMessage = () => {
    if (inputMessage.trim() === '') return;
    
    const newMessage = {
      id: messages.length + 1,
      sender: 'user',
      content: inputMessage,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    simulateResponse(inputMessage);
  };

  // Nueva función para simular grabación de voz
  const handleVoiceRecord = () => {
    setIsRecording(!isRecording);
    
    if (!isRecording) {
      // Simulamos inicio de grabación
      setTimeout(() => {
        // Después de "grabar", simulamos un mensaje transcrito
        const voiceMessage = "Necesito información sobre cómo hacer una hoja de vida";
        setInputMessage(voiceMessage);
        setIsRecording(false);
      }, 2000); // Simular 2 segundos de grabación
    }
  };

  // Componente Header dentro del componente Chat
  const Header = () => {
    return (
      <header className={`header ${darkMode ? 'dark' : 'light'}`}>
        <div className="header-container">
          <h1 className="header-title">INKLU-AI</h1>
          <button onClick={toggleDarkMode} className="theme-toggle">
            {darkMode ? '☀️ Modo Claro' : '🌙 Modo Oscuro'}
          </button>
        </div>
      </header>
    );
  };

  // Icono de micrófono SVG
  const MicrophoneIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
      <path d="M8.25 4.5a3.75 3.75 0 117.5 0v8.25a3.75 3.75 0 11-7.5 0V4.5z" />
      <path d="M6 10.5a.75.75 0 01.75.75v1.5a5.25 5.25 0 1010.5 0v-1.5a.75.75 0 011.5 0v1.5a6.751 6.751 0 01-6 6.709v2.291h3a.75.75 0 010 1.5h-7.5a.75.75 0 010-1.5h3v-2.291a6.751 6.751 0 01-6-6.709v-1.5A.75.75 0 016 10.5z" />
    </svg>
  );

  return (
    <div className={`chat-container ${darkMode ? 'dark' : 'light'}`}>
      <Header />
      
      <div className="chat-main">
        <div className="chat-box">
          <div className="chat-header">
            <div className="header-content">
              <div className="avatar-info">
                <h2>Asistente Virtual</h2>
                <p>Inklú-IA</p>
              </div>
            </div>
          </div>
          
          <div className="messages-container">
            {/* Sugerencias al inicio */}
            {messages.length === 1 && (
              <div className="suggestions-container">
                {sugerencias.map((sugerencia, index) => (
                  <button 
                    key={index}
                    className={`suggestion-button ${darkMode ? 'dark' : 'light'}`}
                    onClick={() => {
                      const newMessage = {
                        id: messages.length + 1,
                        sender: 'user',
                        content: sugerencia,
                        timestamp: new Date()
                      };
                      setMessages(prev => [...prev, newMessage]);
                      simulateResponse(sugerencia);
                    }}
                  >
                    {sugerencia}
                  </button>  
                ))}
              </div>
            )}
            
            {/* Mensajes */}
            <div className="message-list">
              {messages.map((message) => (
                <div 
                  key={message.id} 
                  className={`message-wrapper ${message.sender}`}
                >
                  <div className={`message ${message.sender} ${darkMode ? 'dark' : 'light'}`}>
                    <p className="message-content">{message.content}</p>
                    <span className="message-time">
                      {message.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </span>
                  </div>
                </div>
              ))}
              
              {/* Indicador de escritura */}
              {isTyping && (
                <div className="typing-indicator">
                  <div className={`typing-indicator-content ${darkMode ? 'dark' : 'light'}`}>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef}></div>
            </div>
          </div>
          
          <div className="input-container">
            <div className="input-wrapper">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Escribe tu mensaje..."
                className={`message-input ${darkMode ? 'dark' : 'light'}`}
              />
              
              {/* Botón de micrófono */}
              <button 
                onClick={handleVoiceRecord}
                className={`voice-button ${isRecording ? 'recording' : ''}`}
              >
                <MicrophoneIcon />
              </button>
              
              {/* Botón de enviar */}
              <button 
                onClick={handleSendMessage}
                className="send-button"
                disabled={inputMessage.trim() === ''}
              >
                Enviar
              </button>
            </div>
            
            {/* Indicador de grabación */}
            {isRecording && (
              <div className="recording-indicator">
                <span className="recording-dot"></span>
                <span>Grabando audio...</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;


