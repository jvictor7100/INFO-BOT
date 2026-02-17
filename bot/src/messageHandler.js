const { sendToPython } = require("./services/pythonService");
require('dotenv').config()

const admins = process.env.ADMINS.split(",");
const users = process.env.USERS.split(",");
const requestCharacter = "/";

function isAdmin(id) {
  return admins.includes(id);
}

function isAuthorized(id) {
  return users.includes(id) || admins.includes(id);
}

function getStatus(id) {
  if (isAdmin(id)) {
    return "admin";
  }

  if (isAuthorized(id)) {
    return "user";
  }
}

function red(text) {
  return `\x1b[31m${text}\x1b[0m`;
}

function blue(text) {
  return `\x1b[34m${text}\x1b[0m`;
}

function printRequest(userId, messageBody, reply = '') {

  if (!isAuthorized(userId)) {
    console.log('\n' + userId + ': ' + red('UNAUTHORIZED'));
    console.log('Request:', messageBody);
    return;
  }

  console.log('\n' + userId + ': ' + blue('AUTHORIZED'));
  console.log('Status:', isAdmin(userId) ? 'admin' : 'user');
  console.log('Request:', messageBody);

  if (reply) {
    console.log('Reply:', reply);
  }
}

async function handleMessage(message, client) {

  // if (message.fromMe) return;
  if (message.type !== "chat") return;
  if (!message.body?.startsWith(requestCharacter)) return;

  const messageBody = message.body.replace(requestCharacter, '');
  const userId = message.author || message.from;

  if (!isAuthorized(userId)) {
    printRequest(userId, messageBody);
    await client.sendMessage(message.from, "Você não tem permissão para usar o BOT.");
    return;
  }

  try {
    const status = getStatus(userId);
    let reply = await sendToPython(messageBody, userId, status);

    if (reply?.startsWith(requestCharacter)) {
      reply = reply.slice(1);
    }

    await client.sendMessage(message.from, reply);

    printRequest(userId, messageBody, reply);

  } catch (error) {
    console.error("Erro: ", error);
    await client.sendMessage(message.from, "Erro ao processar mensagem.");
  }
}

module.exports = handleMessage;
