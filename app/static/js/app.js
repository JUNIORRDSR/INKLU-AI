/**
 * Main application script
 * Handles global functionality and navigation
 */

document.addEventListener("DOMContentLoaded", () => {
  // Handle navigation errors
  window.addEventListener("error", (event) => {
    // If the error is related to navigation (e.g., missing resource)
    if (event.target.tagName === "LINK" || event.target.tagName === "SCRIPT") {
      console.error("Resource failed to load:", event.target.src || event.target.href)
    }
  })

  // Add active class to current navigation item
  const currentPath = window.location.pathname
  const navLinks = document.querySelectorAll(".main-nav a")

  navLinks.forEach((link) => {
    const linkPath = link.getAttribute("href")
    if (currentPath.includes(linkPath) && linkPath !== "#") {
      link.classList.add("active")
    } else if (currentPath.endsWith("/") && linkPath === "index.html") {
      link.classList.add("active")
    }
  })

  // Handle 404 errors
  if (document.querySelector(".error-container")) {
    console.log("404 page detected")
    // You could add specific 404 page behavior here
  }

  // Global error handler for fetch operations
  window.handleFetchError = (error) => {
    console.error("Network error:", error)
    window.showGlobalNotification("Network error. Please check your connection and try again.", "error")
  }

  // Global notification system
  window.showGlobalNotification = (message, type) => {
    // Create notification if it doesn't exist
    let notification = document.getElementById("globalNotification")

    if (!notification) {
      notification = document.createElement("div")
      notification.id = "globalNotification"
      notification.className = "global-notification"

      const notificationMessage = document.createElement("p")
      notificationMessage.id = "globalNotificationMessage"

      const closeButton = document.createElement("button")
      closeButton.innerHTML = "×"
      closeButton.className = "notification-close"
      closeButton.addEventListener("click", () => {
        notification.classList.remove("show")
      })

      notification.appendChild(notificationMessage)
      notification.appendChild(closeButton)
      document.body.appendChild(notification)
    }

    const notificationMessage = document.getElementById("globalNotificationMessage")
    notificationMessage.textContent = message
    notification.className = "global-notification " + type + " show"

    // Auto-hide notification after 5 seconds
    setTimeout(() => {
      notification.classList.remove("show")
    }, 5000)
  }
})
