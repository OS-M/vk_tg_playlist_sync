# VK playlist -> Telegram channel syncronizer

С помощью этого скрипта можно синхронизировать плейлист ВКонтакте с группой в телеграме. Скрипт будет сам обнаруживать новые песни и перекидывать их в заданную группу. 
Для начала работы требуется:
- Создать бота в телеграме (https://t.me/BotFather)
- Пригласить бота в нужную группу в телеграме.
- Клонируем или загружаем через zip проект https://github.com/OS-M/vk_tg_playlist_sync/archive/refs/heads/main.zip
- Заполнить поля авторизации в файле settings.py (вносим логин и пароль ОТ ЛЮБОГО аккаунта ВК, для которого будет доступен нужный плейлист. Это может быть: ваш аккаунт и ваш же плейлист; или ваш аккаунт и плейлист друга, если друг открыл вам доступ к аудиозаписям и тд.)
- В этом же файле заполняем поле токена токеном от BotFather (будет выглядеть как "10цифр:35букв")
- Пользователи linux пропускают этот шаг. А на windows нужно установить python3 и pip (https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe), не забываем поставить галочку "Add python to PATH"
- Запускаем скрипт script.sh для linux (в консоли переходим в директорию проекта и выполняем команду "sudo bash ./launch.sh") или запускаем script.bat для windows
- В группе в телеграме пишем "/add_vk_playlist "ссылка на плейлист из адресной строки браузера" "ключ"", вместо "ключ" подставляем значение из консоли: New access key is... (К одной группе можно привязывать несколько плейлистов, они все будут синхронизироваться)
- Для обновления плейлиста пишем "/update_vk_playlist"
- Наслаждаемся работой бота

После перезапуска бота он просканирует все записи и продолжит работу, не будет повторно скидывать записи.
Пока бот работает, он не сможет принимать команды на добавление новых плейлистов. Нужно дождаться пока он закончит работу или остановить бота и добавить плейлисты вручную в файл channels.json
