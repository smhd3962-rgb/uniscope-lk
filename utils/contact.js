const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const MESSAGES_FILE = path.join(__dirname, '..', 'data', 'contact_messages.json');

function loadMessages() {
  try {
    if (fs.existsSync(MESSAGES_FILE)) {
      return JSON.parse(fs.readFileSync(MESSAGES_FILE, 'utf8'));
    }
  } catch (err) {
    console.error('[Contact] Error reading contact messages file:', err);
  }
  return [];
}

function saveMessages(messages) {
  try {
    fs.writeFileSync(MESSAGES_FILE, JSON.stringify(messages, null, 2), 'utf8');
  } catch (err) {
    console.error('[Contact] Error writing contact messages file:', err);
  }
}

function sanitizeText(str) {
  if (typeof str !== 'string') return '';
  return str.replace(/</g, '&lt;').replace(/>/g, '&gt;').trim();
}

function validateEmail(email) {
  if (!email || typeof email !== 'string') return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

function recordContactMessage({ name, email, message, ip, userAgent }) {
  const cleanName = sanitizeText(name);
  const cleanEmail = (email || '').trim().toLowerCase();
  const cleanMessage = sanitizeText(message);

  if (!cleanName || cleanName.length < 2) {
    throw new Error('Please provide your full name (minimum 2 characters).');
  }

  if (!validateEmail(cleanEmail)) {
    throw new Error('Please enter a valid email address.');
  }

  if (!cleanMessage || cleanMessage.length < 5) {
    throw new Error('Message is too short. Please provide at least 5 characters.');
  }

  const messages = loadMessages();
  const record = {
    id: `msg_${Date.now()}_${crypto.randomBytes(3).toString('hex')}`,
    name: cleanName,
    email: cleanEmail,
    message: cleanMessage,
    receivedAt: new Date().toISOString(),
    ip: ip || 'unknown',
    userAgent: userAgent || 'unknown',
    status: 'recorded'
  };

  messages.push(record);
  saveMessages(messages);
  return record;
}

module.exports = {
  recordContactMessage,
  validateEmail,
  sanitizeText
};
