/**
 * Storage utilities for handling user data and session management
 */

// Constants
const USER_KEY = "secureauth_users"
const SESSION_KEY = "secureauth_session"
const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000 // 7 days in milliseconds

// Simple hash function for password (for demo purposes only)
// In a real app, this would be done server-side with a proper hashing algorithm
function hashPassword(password) {
  let hash = 0
  for (let i = 0; i < password.length; i++) {
    const char = password.charCodeAt(i)
    hash = (hash << 5) - hash + char
    hash = hash & hash // Convert to 32bit integer
  }
  return hash.toString(16)
}

// User storage functions
const UserStorage = {
  // Get all users
  getUsers: () => {
    const users = localStorage.getItem(USER_KEY)
    return users ? JSON.parse(users) : []
  },

  // Save users
  saveUsers: (users) => {
    localStorage.setItem(USER_KEY, JSON.stringify(users))
  },

  // Add a new user
  addUser: function (username, email, password) {
    const users = this.getUsers()

    // Check if username or email already exists
    if (users.some((user) => user.username === username)) {
      throw new Error("Username already exists")
    }

    if (users.some((user) => user.email === email)) {
      throw new Error("Email already exists")
    }

    // Create new user object
    const newUser = {
      id: Date.now().toString(),
      username,
      email,
      password: hashPassword(password),
      createdAt: new Date().toISOString(),
    }

    // Add to users array and save
    users.push(newUser)
    this.saveUsers(users)

    return { ...newUser, password: undefined } // Return user without password
  },

  // Find user by username or email
  findUser: function (identifier) {
    const users = this.getUsers()
    return users.find((user) => user.username === identifier || user.email === identifier)
  },

  // Verify user credentials
  verifyCredentials: function (identifier, password) {
    const user = this.findUser(identifier)

    if (!user) {
      return null
    }

    if (user.password === hashPassword(password)) {
      const { password, ...userWithoutPassword } = user
      return userWithoutPassword
    }

    return null
  },

  // Add this function to the UserStorage object
  findUserById: function (id) {
    const users = this.getUsers()
    return users.find((user) => user.id === id)
  },
}

// Session management functions
const SessionManager = {
  // Create a new session
  createSession: (user, rememberMe = false) => {
    const session = {
      userId: user.id,
      username: user.username,
      email: user.email,
      createdAt: new Date().toISOString(),
      expiresAt: rememberMe ? new Date(Date.now() + SESSION_DURATION).toISOString() : null,
    }

    localStorage.setItem(SESSION_KEY, JSON.stringify(session))
    return session
  },

  // Get current session
  getSession: function () {
    const sessionData = localStorage.getItem(SESSION_KEY)

    if (!sessionData) {
      return null
    }

    const session = JSON.parse(sessionData)

    // Check if session has expired
    if (session.expiresAt && new Date(session.expiresAt) < new Date()) {
      this.clearSession()
      return null
    }

    return session
  },

  // Clear the session
  clearSession: () => {
    localStorage.removeItem(SESSION_KEY)
  },

  // Check if user is authenticated
  isAuthenticated: function () {
    return this.getSession() !== null
  },
}
