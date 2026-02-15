require("dotenv").config();

module.exports = {
  PYTHON_API_URL: process.env.PYTHON_API_URL || "http://localhost:5000"
};
