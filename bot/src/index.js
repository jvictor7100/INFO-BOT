const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const handleMessage = require("./messageHandler");

const client = new Client({
  authStrategy: new LocalAuth()
});

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("Bot está pronto!");
});

client.on("message", (message) => {
  handleMessage(message, client);
});

client.initialize();