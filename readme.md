download ngrok или другое приложение(необходим туннель для авторизации через telegram)

./ngrok http 8000, копируем адрес.

open telegram , пишем боту "BotFather" создаем бота, инструкция(https://zen.yandex.ru/media/id/5f781897d3b1a36bf3a139c6/sozdanie-chat-bota-telegram-5f806da9109c65627e22e0d4)

копируем ключ бота в settings/SOCIAL_AUTH_TELEGRAM_BOT_TOKEN

вводим /setdomain , выбираем бота, и вставляем ему скопированный адрес.

Переходим в login.html (templates/service/login.html), ищем тег <script> , меняем в поле data-telegram-login="ваш ник бота" , data-auth-url - до "/auth" вставляем ваш адрес, который мы ранее копировали, /auth/complete/telegram - эта часть должна остаться.