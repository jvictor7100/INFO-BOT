const axios = require("axios");
const { PYTHON_API_URL } = require("../config");

async function sendToPython(message, userId, status) {
  try {
    const response = await axios.post(`${PYTHON_API_URL}/chat`, {
      message,
      userId,
      status
    });

    return response.data.reply;

  } catch (error) {
    console.error("Python API error:", error.response?.data);
    return "Erro interno";
  }
}

module.exports = { sendToPython };
