/**
 * Form validation utilities
 */

// Email validation using regex
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Password strength checker
function checkPasswordStrength(password) {
  // Initialize score
  let score = 0

  // Check length
  if (password.length >= 8) score += 1
  if (password.length >= 12) score += 1

  // Check complexity
  if (/[A-Z]/.test(password)) score += 1 // Has uppercase
  if (/[a-z]/.test(password)) score += 1 // Has lowercase
  if (/[0-9]/.test(password)) score += 1 // Has number
  if (/[^A-Za-z0-9]/.test(password)) score += 1 // Has special char

  // Return strength level
  if (score >= 6) return { strength: "strong", score: 4 }
  if (score >= 4) return { strength: "good", score: 3 }
  if (score >= 2) return { strength: "medium", score: 2 }
  return { strength: "weak", score: 1 }
}

// Update password strength meter
function updatePasswordStrengthMeter(password) {
  const strengthMeter = document.getElementById("passwordStrength")
  if (!strengthMeter) return

  const segments = [
    document.getElementById("segment1"),
    document.getElementById("segment2"),
    document.getElementById("segment3"),
    document.getElementById("segment4"),
  ]

  const strengthText = document.getElementById("strengthText")

  // Reset all segments
  segments.forEach((segment) => {
    segment.className = "strength-segment"
  })

  if (!password) {
    strengthText.textContent = "Password strength"
    return
  }

  const { strength, score } = checkPasswordStrength(password)

  // Update segments based on score
  for (let i = 0; i < score; i++) {
    segments[i].className = `strength-segment ${strength}`
  }

  // Update text
  strengthText.textContent = `Password strength: ${strength.charAt(0).toUpperCase() + strength.slice(1)}`
}

// Setup password toggle visibility
function setupPasswordToggle() {
  const toggleButtons = document.querySelectorAll('[id^="togglePassword"]')

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const passwordInput = this.parentElement.querySelector("input")
      const type = passwordInput.getAttribute("type") === "password" ? "text" : "password"
      passwordInput.setAttribute("type", type)

      // Update the icon based on password visibility
      const svg = this.querySelector("svg")
      if (type === "text") {
        svg.innerHTML = `
          <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
          <line x1="2" y1="2" x2="22" y2="22"></line>
        `
      } else {
        svg.innerHTML = `
          <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        `
      }
    })
  })
}

// Setup password strength meter
function setupPasswordStrengthMeter() {
  const passwordInputs = document.querySelectorAll("#password, #newPassword")

  passwordInputs.forEach((input) => {
    if (input) {
      input.addEventListener("input", function () {
        updatePasswordStrengthMeter(this.value)
      })
    }
  })
}

// Initialize validation features when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  setupPasswordToggle()
  setupPasswordStrengthMeter()
})
