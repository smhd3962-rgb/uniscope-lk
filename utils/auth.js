const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const USERS_FILE = path.join(__dirname, '..', 'data', 'users.json');

// In-memory active sessions (token -> { userId, expiresAt })
const sessions = new Map();
const SESSION_TTL_MS = 14 * 24 * 60 * 60 * 1000; // 14 days

function loadUsers() {
  try {
    if (fs.existsSync(USERS_FILE)) {
      const data = fs.readFileSync(USERS_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (err) {
    console.error('[Auth] Error reading users file:', err);
  }
  return [];
}

function saveUsers(users) {
  try {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), 'utf8');
  } catch (err) {
    console.error('[Auth] Error writing users file:', err);
  }
}

function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.scryptSync(password, salt, 64).toString('hex');
  return `${salt}:${hash}`;
}

function verifyPassword(password, stored) {
  if (!stored || !stored.includes(':')) return false;
  try {
    const [salt, key] = stored.split(':');
    const hashed = crypto.scryptSync(password, salt, 64);
    const keyBuf = Buffer.from(key, 'hex');
    return crypto.timingSafeEqual(hashed, keyBuf);
  } catch (err) {
    return false;
  }
}

// Initialize default student account if users file does not exist
function initUserStore() {
  let users = loadUsers();
  if (users.length === 0) {
    const defaultUser = {
      id: 'usr_sample_01',
      name: 'UniScope Student',
      email: 'student@uniscope.lk',
      passwordHash: hashPassword('UniScope@2026!'),
      district: 'Colombo',
      stream: 'Physical Science',
      createdAt: new Date().toISOString()
    };
    users.push(defaultUser);
    saveUsers(users);
    console.log('[Auth] Initialized users store with verified sample user (student@uniscope.lk)');
  }
}

initUserStore();

function findUserByEmail(email) {
  if (!email) return null;
  const cleanEmail = email.trim().toLowerCase();
  const users = loadUsers();
  return users.find(u => u.email.toLowerCase() === cleanEmail) || null;
}

function findUserById(id) {
  if (!id) return null;
  const users = loadUsers();
  return users.find(u => u.id === id) || null;
}

function createUser({ name, email, password, district, stream }) {
  const cleanEmail = email.trim().toLowerCase();
  const users = loadUsers();
  
  if (users.some(u => u.email.toLowerCase() === cleanEmail)) {
    throw new Error('An account with this email address already exists. Please sign in instead.');
  }

  const newUser = {
    id: `usr_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`,
    name: name.trim(),
    email: cleanEmail,
    passwordHash: hashPassword(password),
    district: district || 'Colombo',
    stream: stream || 'Physical Science',
    createdAt: new Date().toISOString()
  };

  users.push(newUser);
  saveUsers(users);
  return newUser;
}

function validateCredentials(email, password) {
  const user = findUserByEmail(email);
  if (!user) return null;
  if (!verifyPassword(password, user.passwordHash)) return null;
  return user;
}

function createSession(userId) {
  const token = crypto.randomBytes(32).toString('hex');
  const expiresAt = Date.now() + SESSION_TTL_MS;
  sessions.set(token, { userId, expiresAt });
  return token;
}

function getUserFromSession(token) {
  if (!token) return null;
  const session = sessions.get(token);
  if (!session) return null;
  if (Date.now() > session.expiresAt) {
    sessions.delete(token);
    return null;
  }
  return findUserById(session.userId);
}

function destroySession(token) {
  if (token) {
    sessions.delete(token);
  }
}

module.exports = {
  findUserByEmail,
  findUserById,
  createUser,
  validateCredentials,
  createSession,
  getUserFromSession,
  destroySession,
  hashPassword,
  verifyPassword
};
