/**
 * Authentication functionality for signup and login
 */

// Mock implementations (replace with actual implementations or imports)
import { loginUser } from './apis/loginApi.js';
import {registerUser} from './apis/registerApi.js';

const SessionManager = {
  isAuthenticated: () => false, // Replace with actual logic
  createSession: (user, rememberMe) => {
    // Replace with actual session creation logic
    console.log("Session created for user:", user, "Remember me:", rememberMe)
  },
}

const UserStorage = {
  findUser: (identifier) => {
    // Replace with actual user lookup logic
    return null
  },
  addUser: async(username, email, password) => {
    // Replace with actual user creation logic
    
    const data = {
      NombreCompleto:username,
      Correo: email,
      Contrasena:password,
      Rol: "Talento",
      IdDiscapacidad: 2,
      };
      console.log(data)
      // Call the loginUser function with the data object
      try {
        const response = await registerUser(data);
        console.log(response);
      } catch (error) {
        console.error('Error al iniciar sesión:', error);
      }

    console.log("User added:", username, email, password)
    return { username, email } // Return a mock user object
  },
  verifyCredentials: async(identifier, password) => {
    // Replace with actual credential verification logic
    const data = {
      Correo: identifier,
      Contraseña: password
      };
      console.log(data)
      // Call the loginUser function with the data object
      try {
        const response = await loginUser(data);
        console.log(response);
      } catch (error) {
        console.error('Error al iniciar sesión:', error);
      }

    console.log("User:", identifier, password)
    return { username, email } // Return a mock user object
    return null
  },
}

function isValidEmail(email) {
  // Replace with actual email validation logic
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

function checkPasswordStrength(password) {
  // Replace with actual password strength check logic
  const strength = password.length < 10 ? "weak" : "strong"
  return { strength }
}

document.addEventListener("DOMContentLoaded", () => {
  // Check if we're on the signup page
  const signupForm = document.getElementById("signupForm")
  if (signupForm) {
    setupSignupForm()
  }

  // Check if we're on the login page
  const loginForm = document.getElementById("loginForm")
  if (loginForm) {
    setupLoginForm()
    checkRememberMe()
  }

  // Redirect if already logged in
  if (window.location.pathname.includes("login.html") || window.location.pathname.includes("signup.html")) {
    if (SessionManager.isAuthenticated()) {
      window.location.href = "dashboard.html"
    }
  }
})

// Setup signup form
function setupSignupForm() {
  const signupForm = document.getElementById("signupForm")
  const usernameInput = document.getElementById("username")
  const emailInput = document.getElementById("email")
  const passwordInput = document.getElementById("password")
  const confirmPasswordInput = document.getElementById("confirmPassword")
  const termsCheckbox = document.getElementById("termsAgreement")

  const usernameError = document.getElementById("usernameError")
  const emailError = document.getElementById("emailError")
  const passwordError = document.getElementById("passwordError")
  const confirmPasswordError = document.getElementById("confirmPasswordError")
  const termsError = document.getElementById("termsError")

  // Username validation
  usernameInput.addEventListener("blur", function () {
    const username = this.value.trim()

    if (username === "") {
      usernameError.textContent = "Username is required"
      return false
    }

    if (username.length < 3) {
      usernameError.textContent = "Username must be at least 3 characters"
      return false
    }

    // Check if username already exists
    const existingUser = UserStorage.findUser(username)
    if (existingUser) {
      usernameError.textContent = "Username already exists"
      return false
    }

    usernameError.textContent = ""
    return true
  })

  // Email validation
  emailInput.addEventListener("blur", function () {
    const email = this.value.trim()

    if (email === "") {
      emailError.textContent = "Email is required"
      return false
    }

    if (!isValidEmail(email)) {
      emailError.textContent = "Please enter a valid email address"
      return false
    }

    // Check if email already exists
    const existingUser = UserStorage.findUser(email)
    if (existingUser) {
      emailError.textContent = "Email already exists"
      return false
    }

    emailError.textContent = ""
    return true
  })

  // Password validation
  passwordInput.addEventListener("blur", function () {
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
  confirmPasswordInput.addEventListener("blur", function () {
    const confirmPassword = this.value
    const password = passwordInput.value

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

  // Terms agreement validation
  termsCheckbox.addEventListener("change", function () {
    if (!this.checked) {
      termsError.textContent = "You must agree to the terms"
      return false
    }

    termsError.textContent = ""
    return true
  })

  // Form submission
  signupForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // Validate all fields
    const isUsernameValid = validateField(usernameInput, usernameError, () => {
      const username = usernameInput.value.trim()
      if (username === "") return "Username is required"
      if (username.length < 3) return "Username must be at least 3 characters"
      const existingUser = UserStorage.findUser(username)
      if (existingUser) return "Username already exists"
      return ""
    })

    const isEmailValid = validateField(emailInput, emailError, () => {
      const email = emailInput.value.trim()
      if (email === "") return "Email is required"
      if (!isValidEmail(email)) return "Please enter a valid email address"
      const existingUser = UserStorage.findUser(email)
      if (existingUser) return "Email already exists"
      return ""
    })

    const isPasswordValid = validateField(passwordInput, passwordError, () => {
      const password = passwordInput.value
      if (password === "") return "Password is required"
      if (password.length < 8) return "Password must be at least 8 characters"
      const { strength } = checkPasswordStrength(password)
      if (strength === "weak") return "Password is too weak"
      return ""
    })

    const isConfirmPasswordValid = validateField(confirmPasswordInput, confirmPasswordError, () => {
      const confirmPassword = confirmPasswordInput.value
      const password = passwordInput.value
      if (confirmPassword === "") return "Please confirm your password"
      if (confirmPassword !== password) return "Passwords do not match"
      return ""
    })

    const isTermsAgreed = termsCheckbox.checked
    if (!isTermsAgreed) {
      termsError.textContent = "You must agree to the terms"
    } else {
      termsError.textContent = ""
    }

    // Check if all validations passed
    if (!isUsernameValid || !isEmailValid || !isPasswordValid || !isConfirmPasswordValid || !isTermsAgreed) {
      return
    }

    // Create user account
    try {
      const user = UserStorage.addUser(usernameInput.value.trim(), emailInput.value.trim(), passwordInput.value)

      // Show success message
      showNotification("Account created successfully! Redirecting to login...", "success")

      // Redirect to login page after a delay
      setTimeout(() => {
        window.location.href = "login"
      }, 2000)
    } catch (error) {
      showNotification(error.message, "error")
    }
  })
}

// Helper function to validate a field
function validateField(input, errorElement, validationFn) {
  const errorMessage = validationFn()
  errorElement.textContent = errorMessage
  return errorMessage === ""
}

// Setup login form
function setupLoginForm() {
  const loginForm = document.getElementById("loginForm")
  const identifierInput = document.getElementById("loginIdentifier")
  const passwordInput = document.getElementById("loginPassword")
  const rememberMeCheckbox = document.getElementById("rememberMe")

  const identifierError = document.getElementById("identifierError")
  const passwordError = document.getElementById("passwordError")

  // Identifier validation
  identifierInput.addEventListener("blur", function () {
    const identifier = this.value.trim()

    if (identifier === "") {
      identifierError.textContent = "Username or email is required"
      return false
    }

    identifierError.textContent = ""
    return true
  })

  // Password validation
  passwordInput.addEventListener("blur", function () {
    const password = this.value

    if (password === "") {
      passwordError.textContent = "Password is required"
      return false
    }

    passwordError.textContent = ""
    return true
  })

  // Form submission
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // Validate fields
    const isIdentifierValid = validateField(identifierInput, identifierError, () => {
      const identifier = identifierInput.value.trim()
      if (identifier === "") return "Username or email is required"
      return ""
    })

    const isPasswordValid = validateField(passwordInput, passwordError, () => {
      const password = passwordInput.value
      if (password === "") return "Password is required"
      return ""
    })

    if (!isIdentifierValid || !isPasswordValid) {
      return
    }

    // Attempt login
    const identifier = identifierInput.value.trim()
    const password = passwordInput.value
    const rememberMe = rememberMeCheckbox.checked

    // Verify credentials
    const user = UserStorage.verifyCredentials(identifier, password)

    if (user) {
      // Create session
      SessionManager.createSession(user, rememberMe)

      // If remember me is checked, store the identifier
      if (rememberMe) {
        localStorage.setItem("rememberedUser", identifier)
      } else {
        localStorage.removeItem("rememberedUser")
      }

      // Show success message
      showNotification("Login successful! Redirecting...", "success")

      // Redirect to dashboard
      setTimeout(() => {
        window.location.href = "dashboard"
      }, 1500)
    } else {
      showNotification("Invalid username/email or password", "error")
    }
  })
}

// Check if remember me was previously used
function checkRememberMe() {
  const rememberedUser = localStorage.getItem("rememberedUser")
  const identifierInput = document.getElementById("loginIdentifier")
  const rememberMeCheckbox = document.getElementById("rememberMe")

  if (rememberedUser) {
    identifierInput.value = rememberedUser
    rememberMeCheckbox.checked = true
  }
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
