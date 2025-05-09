/**
 * Password reset functionality
 */

// Mock implementations (replace with actual implementations or imports)
const isValidEmail = (email) => {
  // Basic email validation regex
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const UserStorage = {
  findUser: (email) => {
    const users = UserStorage.getUsers()
    return users.find((user) => user.email === email)
  },
  getUsers: () => {
    const users = localStorage.getItem("users")
    return users ? JSON.parse(users) : []
  },
  saveUsers: (users) => {
    localStorage.setItem("users", JSON.stringify(users))
  },
}

const checkPasswordStrength = (password) => {
  let strength = "weak"
  if (password.length >= 8) {
    strength = "medium"
  }
  if (/[A-Z]/.test(password) && /[0-9]/.test(password)) {
    strength = "strong"
  }
  return { strength }
}

const hashPassword = (password) => {
  // In a real application, use a proper hashing algorithm like bcrypt
  return "hashed_" + password
}

document.addEventListener("DOMContentLoaded", () => {
  // Check if we're on the reset request page
  const resetRequestForm = document.getElementById("resetRequestForm")
  if (resetRequestForm) {
    setupResetRequestForm()
  }

  // Check if we're on the new password page
  const newPasswordForm = document.getElementById("newPasswordForm")
  if (newPasswordForm) {
    setupNewPasswordForm()

    // Get token from URL
    const urlParams = new URLSearchParams(window.location.search)
    const token = urlParams.get("token")

    if (token) {
      document.getElementById("resetToken").value = token
    } else {
      // No token provided, redirect to request page
      window.location.href = "configuration.html"
    }
  }
})

// Setup reset request form
function setupResetRequestForm() {
  const resetRequestForm = document.getElementById("resetRequestForm")
  const resetEmailInput = document.getElementById("resetEmail")
  const emailError = document.getElementById("emailError")

  // Email validation
  resetEmailInput.addEventListener("blur", function () {
    const email = this.value.trim()

    if (email === "") {
      emailError.textContent = "Email is required"
      return false
    }

    if (!isValidEmail(email)) {
      emailError.textContent = "Please enter a valid email address"
      return false
    }

    emailError.textContent = ""
    return true
  })

  // Form submission
  resetRequestForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // Validate email
    const isEmailValid = validateField(resetEmailInput, emailError, () => {
      const email = resetEmailInput.value.trim()
      if (email === "") return "Email is required"
      if (!isValidEmail(email)) return "Please enter a valid email address"
      return ""
    })

    if (!isEmailValid) {
      return
    }

    const email = resetEmailInput.value.trim()

    // Check if email exists in our system
    const user = UserStorage.findUser(email)

    if (!user) {
      // For security reasons, don't reveal if the email exists or not
      showNotification("If this email exists in our system, you will receive a reset link", "info")
      return
    }

    // Generate a reset token (in a real app, this would be a secure random token)
    const resetToken = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)

    // Store the token (in a real app, this would be stored in a database with an expiration)
    localStorage.setItem(`reset_token_${user.id}`, resetToken)

    // In a real app, this would send an email with the reset link
    // For demo purposes, we'll just redirect to the reset page with the token

    showNotification("Reset link sent! For demo purposes, we will redirect you directly.", "success")

    setTimeout(() => {
      window.location.href = `reset-password.html?token=${resetToken}`
    }, 2000)
  })
}

// Helper function to validate a field
function validateField(input, errorElement, validationFn) {
  const errorMessage = validationFn()
  errorElement.textContent = errorMessage
  return errorMessage === ""
}

// Setup new password form
function setupNewPasswordForm() {
  const newPasswordForm = document.getElementById("newPasswordForm")
  const newPasswordInput = document.getElementById("newPassword")
  const confirmNewPasswordInput = document.getElementById("confirmNewPassword")
  const resetTokenInput = document.getElementById("resetToken")

  const passwordError = document.getElementById("passwordError")
  const confirmPasswordError = document.getElementById("confirmPasswordError")

  // Password validation
  newPasswordInput.addEventListener("blur", function () {
    const password = this.value

    if (password === "") {
      passwordError.textContent = "Password is required"
      return false
    }

    if (password.length < 8) {
      passwordError.textContent = "Password must be at least 8 characters"
      return false
    }

    const { strength } = checkPasswordStrength(password)
    if (strength === "weak") {
      passwordError.textContent = "Password is too weak"
      return false
    }

    passwordError.textContent = ""
    return true
  })

  // Confirm password validation
  confirmNewPasswordInput.addEventListener("blur", function () {
    const confirmPassword = this.value
    const password = newPasswordInput.value

    if (confirmPassword === "") {
      confirmPasswordError.textContent = "Please confirm your password"
      return false
    }

    if (confirmPassword !== password) {
      confirmPasswordError.textContent = "Passwords do not match"
      return false
    }

    confirmPasswordError.textContent = ""
    return true
  })

  // Form submission
  newPasswordForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // Validate passwords
    const isPasswordValid = validateField(newPasswordInput, passwordError, () => {
      const password = newPasswordInput.value
      if (password === "") return "Password is required"
      if (password.length < 8) return "Password must be at least 8 characters"
      const { strength } = checkPasswordStrength(password)
      if (strength === "weak") return "Password is too weak"
      return ""
    })

    const isConfirmPasswordValid = validateField(confirmNewPasswordInput, confirmPasswordError, () => {
      const confirmPassword = confirmNewPasswordInput.value
      const password = newPasswordInput.value
      if (confirmPassword === "") return "Please confirm your password"
      if (confirmPassword !== password) return "Passwords do not match"
      return ""
    })

    if (!isPasswordValid || !isConfirmPasswordValid) {
      return
    }

    const newPassword = newPasswordInput.value
    const resetToken = resetTokenInput.value

    // In a real app, we would validate the token against the database
    // For demo purposes, we'll just check if the token exists in localStorage

    let tokenFound = false
    let userId = null

    // Get all users
    const users = UserStorage.getUsers()

    // Find user with matching reset token
    for (const user of users) {
      const storedToken = localStorage.getItem(`reset_token_${user.id}`)
      if (storedToken && storedToken === resetToken) {
        tokenFound = true
        userId = user.id
        break
      }
    }

    if (!tokenFound) {
      showNotification("Invalid or expired reset token", "error")
      return
    }

    // Update the user's password
    const updatedUsers = users.map((user) => {
      if (user.id === userId) {
        return {
          ...user,
          password: hashPassword(newPassword),
        }
      }
      return user
    })

    // Save updated users
    UserStorage.saveUsers(updatedUsers)

    // Remove the used token
    localStorage.removeItem(`reset_token_${userId}`)

    // Show success message
    showNotification("Password reset successful! Redirecting to login...", "success")

    // Redirect to login page
    setTimeout(() => {
      window.location.href = "login"
    }, 2000)
  })
}

// Show notification message
function showNotification(message, type) {
  const notification = document.getElementById("notification")
  const notificationMessage = document.getElementById("notificationMessage")

  if (!notification || !notificationMessage) return

  notificationMessage.textContent = message
  notification.className = "notification " + type

  // Auto-hide notification after 5 seconds
  setTimeout(() => {
    notification.className = "notification"
  }, 5000)
}
