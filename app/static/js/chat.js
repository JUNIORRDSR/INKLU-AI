/**
 * Chat functionality
 */

// Mock SessionManager for demonstration purposes.  In a real application,
// this would be handled by a proper authentication system.

import { chatUser } from "./apis/chatApi.js"

document.addEventListener("DOMContentLoaded", () => {
  
  // Check if user is authenticated
  //if (typeof SessionManager !== "undefined" && !SessionManager.isAuthenticated()) {
    // Redirect to login page
    //window.location.href = "login.html"
    //return
  //}

  // DOM Elements
  const chatMessages = document.getElementById("chatMessages")
  const chatForm = document.getElementById("chatForm")
  const messageInput = document.getElementById("messageInput")
  const sendButton = document.getElementById("sendButton")
  const uploadButton = document.getElementById("uploadButton")
  const fileInput = document.getElementById("fileInput")
  const attachmentPreview = document.getElementById("attachmentPreview")
  const recordButton = document.getElementById("recordButton")
  const recordingModal = document.getElementById("recordingModal")
  const stopRecordingButton = document.getElementById("stopRecordingButton")
  const cancelRecordingButton = document.getElementById("cancelRecordingButton")
  const recordingTimer = document.getElementById("recordingTimer")
  const logoutButton = document.getElementById("logoutButton")
  const userDisplayName = document.getElementById("userDisplayName")

  // State variables
  let selectedFiles = []
  let mediaRecorder = null
  let audioChunks = []
  let recordingInterval = null
  let recordingStartTime = 0
  let isWaitingForResponse = false

  // Initialize user display name
  if (typeof SessionManager !== "undefined") {
    const session = SessionManager.getSession()
    if (session && session.username) {
      userDisplayName.textContent = session.username
    }
  }

  // Setup logout button
  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      if (typeof SessionManager !== "undefined") {
        SessionManager.clearSession()
      }
      window.location.href = "login.html"
    })
  }

  // Auto-resize textarea as user types
  messageInput.addEventListener("input", () => {
    messageInput.style.height = "auto"
    messageInput.style.height = messageInput.scrollHeight + "px"

    // Enable/disable send button based on input
    sendButton.disabled = messageInput.value.trim() === "" && selectedFiles.length === 0
  })

  // Handle file upload button click
  uploadButton.addEventListener("click", () => {
    fileInput.click()
  })

  // Handle file selection
  fileInput.addEventListener("change", (e) => {
    const files = Array.from(e.target.files)
    if (files.length > 0) {
      files.forEach((file) => {
        selectedFiles.push(file)
        displayFilePreview(file)
      })
      sendButton.disabled = false
    }
    fileInput.value = "" // Reset file input
  })

  // Handle record button click
  recordButton.addEventListener("click", () => {
    startRecording()
  })

  // Handle stop recording button click
  stopRecordingButton.addEventListener("click", () => {
    stopRecording()
  })

  // Handle cancel recording button click
  cancelRecordingButton.addEventListener("click", () => {
    cancelRecording()
  })

  // Handle form submission
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault()

    const message = messageInput.value.trim()

    if (message === "" && selectedFiles.length === 0) {
      return
    }

    // Send message
    sendMessage(message)

    // Clear input
    messageInput.value = ""
    messageInput.style.height = "auto"
    sendButton.disabled = true
  })

  // Function to display file preview
  function displayFilePreview(file) {
    const previewElement = document.createElement("div")
    previewElement.className = "attachment-preview"

    const removeButton = document.createElement("div")
    removeButton.className = "remove-attachment"
    removeButton.innerHTML = "×"
    removeButton.addEventListener("click", () => {
      // Remove file from selected files
      selectedFiles = selectedFiles.filter((f) => f !== file)
      previewElement.remove()
      sendButton.disabled = messageInput.value.trim() === "" && selectedFiles.length === 0
    })

    if (file.type.startsWith("image/")) {
      const img = document.createElement("img")
      img.src = URL.createObjectURL(file)
      previewElement.appendChild(img)

      const typeLabel = document.createElement("div")
      typeLabel.className = "attachment-type"
      typeLabel.textContent = "Image"
      previewElement.appendChild(typeLabel)
    } else if (file.type.startsWith("audio/")) {
      const audioIcon = document.createElement("div")
      audioIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin: 30px auto; display: block; color: #6b7280;">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      `
      previewElement.appendChild(audioIcon)

      const typeLabel = document.createElement("div")
      typeLabel.className = "attachment-type"
      typeLabel.textContent = "Audio"
      previewElement.appendChild(typeLabel)
    } else {
      const fileIcon = document.createElement("div")
      fileIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin: 30px auto; display: block; color: #6b7280;">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
      `
      previewElement.appendChild(fileIcon)

      const typeLabel = document.createElement("div")
      typeLabel.className = "attachment-type"
      typeLabel.textContent = getFileExtension(file.name).toUpperCase()
      previewElement.appendChild(typeLabel)
    }

    previewElement.appendChild(removeButton)
    attachmentPreview.appendChild(previewElement)
  }

  // Function to get file extension
  function getFileExtension(filename) {
    return filename.slice(((filename.lastIndexOf(".") - 1) >>> 0) + 2)
  }

  // Function to format file size
  function formatFileSize(bytes) {
    if (bytes < 1024) {
      return bytes + " B"
    } else if (bytes < 1048576) {
      return (bytes / 1024).toFixed(1) + " KB"
    } else {
      return (bytes / 1048576).toFixed(1) + " MB"
    }
  }

  // Function to send a message
  function sendMessage(text) {
    // Create message element
    const messageElement = document.createElement("div")
    messageElement.className = "message user-message"

    // Add message content
    const messageContent = document.createElement("div")
    messageContent.className = "message-content"

    if (text) {
      const textParagraph = document.createElement("p")
      textParagraph.textContent = text
      messageContent.appendChild(textParagraph)
    }

    // Add files if any
    if (selectedFiles.length > 0) {
      selectedFiles.forEach((file) => {
        if (file.type.startsWith("image/")) {
          const imageContainer = document.createElement("div")
          imageContainer.className = "image-message"

          const image = document.createElement("img")
          image.src = URL.createObjectURL(file)
          image.alt = "Uploaded image"

          imageContainer.appendChild(image)
          messageContent.appendChild(imageContainer)
        } else if (file.type.startsWith("audio/")) {
          const audioContainer = document.createElement("div")
          audioContainer.className = "audio-message"

          const audio = document.createElement("audio")
          audio.controls = true
          audio.className = "audio-player"
          audio.src = URL.createObjectURL(file)

          audioContainer.appendChild(audio)
          messageContent.appendChild(audioContainer)
        } else {
          const fileContainer = document.createElement("div")
          fileContainer.className = "file-message"

          const fileIcon = document.createElement("div")
          fileIcon.className = "file-icon"
          fileIcon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          `

          const fileInfo = document.createElement("div")
          fileInfo.className = "file-info"

          const fileName = document.createElement("div")
          fileName.className = "file-name"
          fileName.textContent = file.name

          const fileSize = document.createElement("div")
          fileSize.className = "file-size"
          fileSize.textContent = formatFileSize(file.size)

          fileInfo.appendChild(fileName)
          fileInfo.appendChild(fileSize)

          const fileDownload = document.createElement("a")
          fileDownload.className = "file-download"
          fileDownload.href = URL.createObjectURL(file)
          fileDownload.download = file.name
          fileDownload.textContent = "Download"

          fileContainer.appendChild(fileIcon)
          fileContainer.appendChild(fileInfo)
          fileContainer.appendChild(fileDownload)

          messageContent.appendChild(fileContainer)
        }
      })
    }

    messageElement.appendChild(messageContent)

    // Add message time
    const messageTime = document.createElement("div")
    messageTime.className = "message-time"
    messageTime.textContent = getCurrentTime()
    messageElement.appendChild(messageTime)

    // Add message to chat
    chatMessages.appendChild(messageElement)

    // Scroll to bottom
    scrollToBottom()

    // Show AI is typing indicator
    showTypingIndicator()

    // Clear selected files
    selectedFiles = []
    attachmentPreview.innerHTML = ""

    // Simulate AI response after a delay
    simulateAIResponse(text)
  }

  // Function to show typing indicator
  function showTypingIndicator() {
    if (isWaitingForResponse) return

    isWaitingForResponse = true

    const loadingElement = document.createElement("div")
    loadingElement.className = "loading-indicator"
    loadingElement.id = "typingIndicator"

    for (let i = 0; i < 3; i++) {
      const dot = document.createElement("div")
      dot.className = "loading-dot"
      loadingElement.appendChild(dot)
    }

    chatMessages.appendChild(loadingElement)
    scrollToBottom()
  }

  // Function to hide typing indicator
  function hideTypingIndicator() {
    const indicator = document.getElementById("typingIndicator")
    if (indicator) {
      indicator.remove()
    }
    isWaitingForResponse = false
  }

  // Function to simulate AI response
  async function simulateAIResponse(userMessage) {
    // Mostrar indicador de carga
    showTypingIndicator();
    
    // Añadir un mensaje de espera después de 15 segundos
    const waitMessageTimeout = setTimeout(() => {
      updateWaitingMessage("La IA está procesando tu consulta. Esto puede tomar un tiempo...");
    }, 15000);
    
    try {
      if (!userMessage || userMessage.trim() === "") {
        if (selectedFiles.length > 0) {
          userMessage = "He recibido archivos del usuario";
        } else {
          userMessage = "Saludo inicial";
        }
      }
      
      // Preparar datos para enviar al backend
      const userData = {
        message: userMessage
      };
      
      console.log("Enviando mensaje al backend:", userData);
      
      // Llamar a la API del backend sin timeout
      const response = await chatUser(userData);
      console.log("Respuesta del backend recibida:", response);
      
      // Limpiar el timeout del mensaje de espera
      clearTimeout(waitMessageTimeout);
      
      // Ocultar indicador de escritura una vez que tengamos la respuesta
      hideTypingIndicator();
      
      // Obtener respuesta del backend
      let aiResponse = "";
      
      // Verificar si la respuesta existe y tiene el formato esperado
      if (response) {
        console.log("Estructura completa de la respuesta:", JSON.stringify(response));
        
        if (response.status === "success" && response.response) {
          aiResponse = response.response;
        } else if (response.message) {
          aiResponse = response.message;
          console.warn("Respuesta con estado no exitoso:", response);
        } else {
          aiResponse = "Recibí una respuesta del servidor, pero no pude interpretarla correctamente. Por favor, intenta de nuevo.";
          console.error("Formato de respuesta inesperado:", response);
        }
      } else {
        aiResponse = "No se recibió una respuesta válida del servidor. Por favor, intenta de nuevo.";
        console.error("Respuesta vacía o nula del servidor");
      }
      
      // Crear elemento de mensaje AI
      const messageElement = document.createElement("div");
      messageElement.className = "message ai-message";
      
      // Añadir contenido del mensaje
      const messageContent = document.createElement("div");
      messageContent.className = "message-content";
      
      // Usar innerHTML para preservar posible formato HTML (si lo hay)
      const textParagraph = document.createElement("p");
      
      // Verificar si hay contenido
      if (aiResponse && aiResponse.trim() !== "") {
        textParagraph.textContent = aiResponse;
      } else {
        textParagraph.textContent = "El servidor no envió una respuesta con contenido. Por favor, intenta nuevamente.";
        console.error("Respuesta vacía del servidor");
      }
      
      messageContent.appendChild(textParagraph);
      messageElement.appendChild(messageContent);
      
      // Añadir hora del mensaje
      const messageTime = document.createElement("div");
      messageTime.className = "message-time";
      messageTime.textContent = getCurrentTime();
      messageElement.appendChild(messageTime);
      
      // Añadir mensaje al chat
      chatMessages.appendChild(messageElement);
      
      // Scroll hasta abajo
      scrollToBottom();
      
    } catch (error) {
      console.error("Error al comunicarse con el backend:", error);
      
      // Limpiar el timeout del mensaje de espera
      clearTimeout(waitMessageTimeout);
      
      // Ocultar indicador de escritura
      hideTypingIndicator();
      
      // Mostrar mensaje de error
      const messageElement = document.createElement("div");
      messageElement.className = "message ai-message";
      
      const messageContent = document.createElement("div");
      messageContent.className = "message-content";
      
      const textParagraph = document.createElement("p");
      textParagraph.textContent = `Error de conexión: ${error.message || "No se pudo establecer conexión con el servidor"}. Por favor, verifica tu conexión e intenta de nuevo.`;
      messageContent.appendChild(textParagraph);
      
      messageElement.appendChild(messageContent);
      
      // Añadir hora del mensaje
      const messageTime = document.createElement("div");
      messageTime.className = "message-time";
      messageTime.textContent = getCurrentTime();
      messageElement.appendChild(messageTime);
      
      // Añadir mensaje al chat
      chatMessages.appendChild(messageElement);
      
      // Scroll hasta abajo
      scrollToBottom();
    }
  }

  // Función para actualizar el mensaje de espera
  function updateWaitingMessage(message) {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) {
      const waitingMsg = document.createElement("div");
      waitingMsg.className = "waiting-message";
      waitingMsg.style.marginTop = "5px";
      waitingMsg.style.fontSize = "12px";
      waitingMsg.style.color = "#666";
      waitingMsg.textContent = message;
      
      // Eliminar mensajes anteriores si existen
      const existingMsg = indicator.querySelector(".waiting-message");
      if (existingMsg) {
        existingMsg.remove();
      }
      
      indicator.appendChild(waitingMsg);
      scrollToBottom();
    }
  }

  // Function to get current time
  function getCurrentTime() {
    const now = new Date()
    let hours = now.getHours()
    const minutes = now.getMinutes()
    const ampm = hours >= 12 ? "PM" : "AM"

    hours = hours % 12
    hours = hours ? hours : 12 // the hour '0' should be '12'

    return `${hours}:${minutes < 10 ? "0" + minutes : minutes} ${ampm}`
  }

  // Function to scroll to bottom of chat
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight
  }

  // Function to start recording
  function startRecording() {
    // Check if browser supports getUserMedia
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert("Your browser doesn't support audio recording.")
      return
    }

    // Request audio permission
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        // Show recording modal
        recordingModal.classList.add("active")

        // Initialize media recorder
        mediaRecorder = new MediaRecorder(stream)
        audioChunks = []

        // Handle data available event
        mediaRecorder.addEventListener("dataavailable", (event) => {
          audioChunks.push(event.data)
        })

        // Handle recording stop event
        mediaRecorder.addEventListener("stop", () => {
          // Create audio blob
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" })

          // Create file from blob
          const audioFile = new File([audioBlob], "recording.wav", { type: "audio/wav" })

          // Add to selected files
          selectedFiles.push(audioFile)

          // Display file preview
          displayFilePreview(audioFile)

          // Enable send button
          sendButton.disabled = false

          // Hide recording modal
          recordingModal.classList.remove("active")

          // Stop all tracks
          stream.getTracks().forEach((track) => track.stop())
        })

        // Start recording
        mediaRecorder.start()

        // Start timer
        recordingStartTime = Date.now()
        updateRecordingTimer()
        recordingInterval = setInterval(updateRecordingTimer, 1000)
      })
      .catch((error) => {
        console.error("Error accessing microphone:", error)
        alert("Could not access your microphone. Please check permissions.")
      })
  }

  // Function to stop recording
  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop()
      clearInterval(recordingInterval)
    }
  }

  // Function to cancel recording
  function cancelRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop()

      // Clear selected files
      selectedFiles = selectedFiles.filter((file) => file.name !== "recording.wav")

      // Hide recording modal
      recordingModal.classList.remove("active")

      // Clear interval
      clearInterval(recordingInterval)
    }
  }

  // Function to update recording timer
  function updateRecordingTimer() {
    const elapsedTime = Date.now() - recordingStartTime
    const seconds = Math.floor((elapsedTime / 1000) % 60)
    const minutes = Math.floor((elapsedTime / (1000 * 60)) % 60)

    recordingTimer.textContent = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
  }

  // Initial scroll to bottom
  scrollToBottom()
})
