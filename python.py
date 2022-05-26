import telebot


bot = telebot.TeleBot('5319883177:AAHLc5bJ9420HUAA7uSvHP07QNkfAeYizdE')

conn = sqlite3.connect('D:\YoptaBot\db\yopt.db', check_same_thread=False)

cursor = conn.cursor()

def db_table_val(user_id: int, subscribe: int):

cursor.execute('INSERT or REPLACE INTO users (user_id, subscribe) VALUES (?, ?)', (user_id, subscribe))

conn.commit()

def subscriber_exists(user_id):

with conn:

result = cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()

return bool(len(result))

def subscriber_is_active(user_id):

with conn:

result = cursor.execute('SELECT * FROM users WHERE user_id = ? AND subscribe = ?', (user_id, 1)).fetchall()

return bool(len(result))

def show_anecdote(text):

with conn:

return cursor.execute("SELECT text FROM `anecdotes` WHERE `id` = ?", (text,))

@bot.message_handler(content_types=['text'])

def welcome(message):

if message.text == "/start":

user_id = message.from_user.id

if subscriber_exists(user_id):

bot.send_message(message.chat.id, "И снова привет")

else:

bot.send_message(message.chat.id, "Привет! Подпишись командой /subscribe")

db_table_val(user_id, 0)

if message.text == "/subscribe":

user_id = message.from_user.id

if subscriber_is_active(user_id):

bot.send_message(message.chat.id, "Ты уже подписан!")

else:

bot.send_message(message.chat.id, "Поздравляю! Теперь ты подписчик")

db_table_val(user_id, 1)

if message.text == "/unsubscribe":

user_id = message.from_user.id

if subscriber_is_active(user_id):

bot.send_message(message.chat.id, "Ты отписан! Для возвращения, используй команду /subscribe")

db_table_val(user_id, 0)

else:

bot.send_message(message.chat.id, "Ты уже отписан! Для возвращения, используй команду /subscribe")

if message.text == "/anecdote":

user_id = message.from_user.id

if subscriber_is_active(user_id):

bot.send_message(message.chat.id, show_anecdote)

else:

bot.send_message(message.chat.id, "Анекдоты доступны только подписчикам. Используй /subscribe")

bot.polling(none_stop=True, interval=0)
