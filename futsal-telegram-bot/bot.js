require("dotenv").config();
const TelegramBot = require("node-telegram-bot-api");
const exercises = require("./exercises");

// Inicializar bot
const bot = new TelegramBot(process.env.Futsalgymbot, { polling: true });

// Comando /start
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    `¡Hola ${msg.from.first_name}! Soy tu bot de futsal.\nElige tipo de rutina:`,
    {
      reply_markup: {
        keyboard: [["Gym", "Técnica"]],
        resize_keyboard: true,
        one_time_keyboard: true
      }
    }
  );
});

// Manejar selección de tipo de rutina
bot.on("message", (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text.toLowerCase();

  if (text === "gym" || text === "técnica") {
    bot.sendMessage(chatId, "Selecciona tu nivel:", {
      reply_markup: {
        keyboard: [["Beginner", "Intermediate", "Advanced"]],
        resize_keyboard: true,
        one_time_keyboard: true
      }
    });

    bot.once("message", (msg2) => {
      const level = msg2.text.toLowerCase();
      const category = text === "gym" ? "gym" : "technical";

      if (exercises[category][level]) {
        exercises[category][level].forEach((exercise) => {
          bot.sendMessage(
            chatId,
            `🏋️ ${exercise.name}\n${exercise.description}\n🎥 Video: ${exercise.youtube}`
          );
        });
      } else {
        bot.sendMessage(chatId, "Nivel no encontrado.");
      }
    });
  }
});
