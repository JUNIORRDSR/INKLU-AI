/**
 * Dashboard functionality
 */

// Import SessionManager and UserStorage (assuming they are in separate files)
import { SessionManager } from "./session-manager.js"
import { UserStorage } from "./user-storage.js"

document.addEventListener("DOMContentLoaded", () => {
  // Check if user is authenticated
  if (!SessionManager.isAuthenticated()) {
    // Redirect to login page
    window.location.href = "login.html"
    return
  }

  // Load user data
  loadUserData()

  // Setup logout button
  const logoutButton = document.getElementById("logoutButton")
  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      // Clear session
      SessionManager.clearSession()

      // Redirect to login page
      window.location.href = "login.html"
    })
  }

  // Setup change password button
  const changePasswordButton = document.querySelector(".dashboard-card button:nth-child(2)")
  if (changePasswordButton) {
    changePasswordButton.addEventListener("click", () => {
      window.location.href = "configuration.html"
    })
  }
})

// Load user data into the dashboard
function loadUserData() {
  const session = SessionManager.getSession()

  if (!session) {
    return
  }

  // Find user by ID
  const users = UserStorage.getUsers()
  const user = users.find((u) => u.id === session.userId)

  if (!user) {
    return
  }

  // Update user display name
  const userDisplayName = document.getElementById("userDisplayName")
  if (userDisplayName) {
    userDisplayName.textContent = user.username
  }

  // Update profile information
  const profileUsername = document.getElementById("profileUsername")
  const profileEmail = document.getElementById("profileEmail")
  const profileCreated = document.getElementById("profileCreated")

  if (profileUsername) {
    profileUsername.textContent = user.username
  }

  if (profileEmail) {
    profileEmail.textContent = user.email
  }

  if (profileCreated && user.createdAt) {
    // Format date
    const createdDate = new Date(user.createdAt)
    profileCreated.textContent = createdDate.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }
}
