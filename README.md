# VK playlist -> Telegram channel syncronizer

**С помощью этого скрипта можно синхронизировать плейлист ВКонтакте с группой в телеграме. Скрипт будет сам обнаруживать новые песни и перекидывать их в заданную группу.**

Установка и запуск бота:
- Создаем бота в телеграме (https://t.me/BotFather)
- Приглашаем бота в нужную группу в телеграме (это может быть и переписка с ботом. Напомню, что в телеграме можно создавать группы из одного человека)
- Клонируем или через zip загружаем проект (https://github.com/OS-M/vk_tg_playlist_sync/archive/refs/heads/main.zip)
- Заполняем поля авторизации ВК в файле settings.py (вносим логин и пароль от аккаунтна ВК, у которого есть доступ к нужному плейлисту. Это может быть: ваш аккаунт и ваш же плейлист; или ваш аккаунт и плейлист друга, если друг открыл вам доступ к аудиозаписям и тд.)
- В этом же файле заполняем поле токена токеном от BotFather (будет выглядеть как "10цифр:35букв")
- Пользователи linux пропускают этот шаг. А на windows нужно установить python3 и pip (https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe), **не забываем поставить галочку "Add python to PATH"**
- Запускаем скрипт script.sh для linux (в консоли переходим в директорию проекта и выполняем команду "sudo bash ./launch.sh") или запускаем script.bat для windows
- В группе в телеграме пишем "/add_vk_playlist _"ссылка на плейлист из адресной строки браузера"_ _"ключ"_", вместо _"ключ"_ подставляем значение из консоли: _New access key is..._ (К одной группе можно привязывать несколько плейлистов, они все будут синхронизироваться)
- Далее для обновления плейлиста его не нужно снова добавлять, просто пишем "/update_vk_playlist" после добавления новых песен в плейлист
- Наслаждаемся...

-"Сложновато" - скажите вы</br>
-"Opensource" - отвечу я

После перезапуска бота он просканирует все записи и продолжит работу, не будет повторно скидывать записи.
Пока бот работает, он не сможет принимать команды на добавление новых плейлистов. Нужно дождаться пока он закончит работу или остановить бота и добавить плейлисты вручную в файл channels.json

**Известные баги:**
- Двухфакторная авторизация ВК не всегда работает. В коде есть ее поддержка, но в библиотеке vp-api есть баг, из-за которого авторизация может не пройти. В таком случае двухфакторку придется выключить в настройках ВК
- Некоторые песни скидываются файлами очень маленького размера до 100КВ и не проигрываются. Пока что не знаю, с чем это связано, но буду искать
- Бот плохо обрабатывает некорректные команды в телеграме. Крашнуться не должен, но и сообщения об ошибке может не выдавать. Если что-то не работает, перепроверьте корректность команд, а затем если ничего не помогает внимательно переустановите бота
