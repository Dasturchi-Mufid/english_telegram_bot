# app/utils/texts.py

LEXICON = {
    "uz": {
        # Umumiy va Menyu tugmalari
        "welcome": "👋 Xush kelibsiz, {name}!\nIngliz tili botimizga xush kelibsiz. Davom etish uchun darajangizni aniqlang yoki materiallarni ko'ring.",
        "choose_language": "Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please choose a language:",
        "main_menu": "Asosiy menyu",
        "btn_quiz": "📝 Test topshirish",
        "btn_materials": "📚 Materiallar",
        "btn_results": "📊 Mening natijalarim",
        "btn_settings": "⚙️ Sozlamalar",
        "lang_changed": "🇺🇿 Til muvaffaqiyatli o'zgartirildi!",
        "back": "⬅️ Orqaga",
        "cancel": "🚫 Amal bekor qilindi.",
        "error_occurred": "⚠️ Xatolik yuz berdi.",

        # Darajalar (Level)
        "beginner": "Boshlang`ich",
        "intermediate": "O`rta",
        "advanced": "Yuqori",

        # admin.py
        "add_category": "📂 Kategoriya qo'shish",
        "add_question": "📝 Savol qo'shish",
        "add_material": "📁 Material yuklash",
        "statistics": "📊 Statistika",
        "send_message": "📢 Xabar yuborish",
        "welcome_admin": "👨‍💻 **Admin paneliga xush kelibsiz!**\n\nBoshqaruv menyusidan kerakli bo'limni tanlang:",
        "new_category_name": "🆕 Yangi kategoriya nomini kiriting (masalan: Writing):",
        "category_added": "✅ Kategoriya muvaffaqiyatli qo'shildi.",
        "send_file": "📎 Material faylini yuboring (PDF, Audio yoki Video):",
        "choose_material_level": "📊 Ushbu material qaysi darajaga mos?",
        "send_material_name": "✅ Tanlangan daraja: {level}\n\n📝 Endi ushbu material uchun sarlavha (title) kiriting:",
        "if_not_category": "⚠️ Avval kategoriya yarating! /add_category",
        "choose_category": "📂 Kategoriyani tanlang:",
        "material_saved": "✅ Material saqlandi!\n🔹 Nom: {title}\n🔹 Daraja: {level}",
        "send_question": "❓ Test savoli matnini kiriting:",
        "send_options": "📝 Variantlarni kiriting.\nFormat: Variant1, Variant2, Variant3, Variant4\n*(Aralashtirib yubormang, 4 ta variant bo'lishi shart)*",
        "wrong_options": "🚫 Xato! Iltimos, 4 ta variantni vergul bilan ajratib yuboring.",
        "correct_answer": "🎯 To'g'ri javobni belgilang:",
        "question_level": "📈 Ushbu savol qaysi darajaga mos?",
        "question_saved": "✅ Savol muvaffaqiyatli saqlandi! (Daraja: {level})",
        "show_stats": "📈 **Bot statistikasi:**\n\n👤 Foydalanuvchilar: {user_count}\n📝 Topshirilgan testlar: {quiz_count}",
        "send_broadcast_text": "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing (matn, rasm yoki video bo'lishi mumkin):",
        "quantity_sended_message": "✅ Xabar {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!\n(Adminlar ro'yxatdan chiqarildi)",

        # materials.py
        "absent_category": "😔 Hozircha hech qanday bo'lim yaratilmagan.",
        "no_materials_found": "⚠️ Bu bo'limda {level} darajasi uchun materiallar topilmadi.",
        "choose_material": "✅ Sizning darajangiz: {level}\n📖 Kerakli materialni tanlang:",
        "file_send_error": "❌ Faylni yuborishda xatolik yuz berdi. Fayl ID eskirgan bo'lishi mumkin.",
        "categories_not_found": "⚠️ Kategoriyalar topilmadi.",

        # quiz.py
        "btn_detect_level": "📊 Darajamni aniqlash",
        "quiz_not_ready": "⚠️ Kechirasiz, test tizimi hali tayyor emas (savollar yetarli emas).",
        "test_started": "🚀 Test boshlandi! Jami {count} ta savol. Omad!",
        "next_question": "❓ **Savol {index}:**\n\n{text}",
        "loading_test": "Test yakunlanmoqda...",
        "questions_not_found": "❌ Xatolik: Savollar topilmadi.",
        "test_finished": "🏁 **Test yakunlandi!**\n\n📊 Natijangiz: **{score} / {max_score}**\n📈 Foiz: **{percentage:.1f}%**\n🏆 Sizning darajangiz: **{level}**\n\n✅ Ma'lumotlaringiz saqlandi. \"Mening natijalarim\" bo'limida tarixingizni kuzatishingiz mumkin!",

        # start.py
        "start_welcome": "👋 Salom, {name}!\n\nIELTS tayyorlov botiga xush kelibsiz. Bu yerda siz o'z darajangizga mos materiallarni topishingiz va bilimingizni sinab ko'rishingiz mumkin.",
        "else_welcome": "😊 Sizni yana ko'rganimizdan xursandmiz, {name}!",
        "my_profile": "👤 Mening profilim",
        "no_quiz_yet": "Hali test topshirilmagan",
        "profile_text": "👤 **Sizning profilingiz:**\n\n📝 **Ism:** {name}\n📊 **Daraja:** {level}\n🆔 **ID:** `{tg_id}`\n📅 **Ro'yxatdan o'tgan sana:** {date}\n\n🔄 Darajangizni yangilash uchun \"📊 Darajamni aniqlash\" tugmasini bosing.",
        "profile_not_found": "⚠️ Ma'lumotlaringiz topilmadi. Iltimos, /start buyrug'ini bosing.",
        "no_results_yet": "📭 Siz hali test topshirmagansiz. Test yordamida darajangizni aniqlang!",
        "your_results": "📊 **Sizning oxirgi natijalaringiz:**\n\n",
        "result_item": "📅 {date} | 🎯 {score}/{total} ({percentage}%) | 🏆 {level}\n",

        # middlewares.py
        "only_admins": "⛔️ Bu bo'lim faqat adminlar uchun!"
    },
    "ru": {
        # Общие и кнопки меню
        "welcome": "👋 Добро пожаловать, {name}!\nДобро пожаловать в наш бот для изучения английского языка. Определите свой уровень или просмотрите материалы.",
        "choose_language": "Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please choose a language:",
        "main_menu": "Главное меню",
        "btn_quiz": "📝 Пройти тест",
        "btn_materials": "📚 Материалы",
        "btn_results": "📊 Мои результаты",
        "btn_settings": "⚙️ Настройки",
        "lang_changed": "🇷🇺 Язык успешно изменен!",
        "back": "⬅️ Назад",
        "cancel": "🚫 Действие отменено.",
        "error_occurred": "⚠️ Произошла ошибка.",

        # Уровни
        "beginner": "Начальный (Beginner)",
        "intermediate": "Средний (Intermediate)",
        "advanced": "Продвинутый (Advanced)",

        # admin.py
        "add_category": "📂 Добавить категорию",
        "add_question": "📝 Добавить вопрос",
        "add_material": "📁 Загрузить материал",
        "statistics": "📊 Статистика",
        "send_message": "📢 Рассылка",
        "welcome_admin": "👨‍💻 **Добро пожаловать в админ-панель!**\n\nВыберите нужный раздел из меню управления:",
        "new_category_name": "🆕 Введите название новой категории (например: Writing):",
        "category_added": "✅ Категория успешно добавлена.",
        "send_file": "📎 Отправьте файл материала (PDF, Аудио или Видео):",
        "choose_material_level": "📊 Для какого уровня этот материал?",
        "send_material_name": "✅ Выбранный уровень: {level}\n\n📝 Теперь введите заголовок (title) для этого материала:",
        "if_not_category": "⚠️ Сначала создайте категорию! /add_category",
        "choose_category": "📂 Выберите категорию:",
        "material_saved": "✅ Материал сохранен!\n🔹 Название: {title}\n🔹 Уровень: {level}",
        "send_question": "❓ Введите текст вопроса:",
        "send_options": "📝 Введите варианты ответов.\nФормат: Вариант1, Вариант2, Вариант3, Вариант4\n*(Обязательно должно быть 4 варианта через запятую)*",
        "wrong_options": "🚫 Ошибка! Пожалуйста, отправьте 4 варианта ответов, разделенных запятой.",
        "correct_answer": "🎯 Выберите правильный ответ:",
        "question_level": "📈 Для какого уровня этот вопрос?",
        "question_saved": "✅ Вопрос успешно сохранен! (Уровень: {level})",
        "show_stats": "📈 **Статистика бота:**\n\n👤 Пользователи: {user_count}\n📝 Пройденные тесты: {quiz_count}",
        "send_broadcast_text": "Введите сообщение для рассылки всем пользователям (текст, фото или видео):",
        "quantity_sended_message": "✅ Сообщение успешно отправлено {count} пользователям!\n(Администраторы исключены)",

        # materials.py
        "absent_category": "😔 Разделы пока не созданы.",
        "no_materials_found": "⚠️ В этом разделе не найдены материалы для уровня {level}.",
        "choose_material": "✅ Ваш уровень: {level}\n📖 Выберите необходимый материал:",
        "file_send_error": "❌ Ошибка при отправке файла. Возможно, File ID устарел.",
        "categories_not_found": "⚠️ Категории не найдены.",

        # quiz.py
        "btn_detect_level": "📊 Определить мой уровень",
        "quiz_not_ready": "⚠️ К сожалению, система тестирования еще не готова (недостаточно вопросов).",
        "test_started": "🚀 Тест начался! Всего {count} вопросов. Удачи!",
        "next_question": "❓ **Вопрос {index}:**\n\n{text}",
        "loading_test": "Тест завершается...",
        "questions_not_found": "❌ Ошибка: Вопросы не найдены.",
        "test_finished": "🏁 **Тест завершен!**\n\n📊 Ваш результат: **{score} / {max_score}**\n📈 Процент: **{percentage:.1f}%**\n🏆 Ваш уровень: **{level}**\n\n✅ Данные сохранены. Вы можете отслеживать свою историю в разделе \"Мои результаты\"!",

        # start.py
        "start_welcome": "👋 Привет, {name}!\n\nДобро пожаловать в бот подготовки к IELTS. Здесь вы можете найти материалы, соответствующие вашему уровню, и проверить свои знания.",
        "else_welcome": "😊 Рады видеть вас снова, {name}!",
        "my_profile": "👤 Мой профиль",
        "no_quiz_yet": "Тесты еще не пройдены",
        "profile_text": "👤 **Ваш профиль:**\n\n📝 **Имя:** {name}\n📊 **Уровень:** {level}\n🆔 **ID:** `{tg_id}`\n📅 **Дата регистрации:** {date}\n\n🔄 Чтобы обновить уровень, нажмите кнопку \"📊 Определить мой уровень\".",
        "profile_not_found": "⚠️ Ваши данные не найдены. Пожалуйста, нажмите команду /start.",
        "no_results_yet": "📭 Вы еще не проходили тесты. Определите свой уровень с помощью теста!",
        "your_results": "📊 **Ваши последние результаты:**\n\n",
        "result_item": "📅 {date} | 🎯 {score}/{total} ({percentage}%) | 🏆 {level}\n",

        # middlewares.py
        "only_admins": "⛔️ Этот раздел только для администраторов!"
    },
    "en": {
        # General & Menu Buttons
        "welcome": "👋 Welcome, {name}!\nWelcome to our English learning bot. Test your level or browse materials to get started.",
        "choose_language": "Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please choose a language:",
        "main_menu": "Main menu",
        "btn_quiz": "📝 Take a Quiz",
        "btn_materials": "📚 Materials",
        "btn_results": "📊 My Results",
        "btn_settings": "⚙️ Settings",
        "lang_changed": "🇬🇧 Language successfully changed!",
        "back": "⬅️ Back",
        "cancel": "🚫 Action canceled.",
        "error_occurred": "⚠️ An error occurred.",

        # Levels
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",

        # admin.py
        "add_category": "📂 Add Category",
        "add_question": "📝 Add Question",
        "add_material": "📁 Upload Material",
        "statistics": "📊 Statistics",
        "send_message": "📢 Broadcast",
        "welcome_admin": "👨‍💻 **Welcome to the admin panel!**\n\nSelect the required section from the control menu:",
        "new_category_name": "🆕 Enter the name of the new category (e.g., Writing):",
        "category_added": "✅ Category successfully added.",
        "send_file": "📎 Send the material file (PDF, Audio, or Video):",
        "choose_material_level": "📊 Which level is this material suitable for?",
        "send_material_name": "✅ Selected level: {level}\n\n📝 Now enter a title for this material:",
        "if_not_category": "⚠️ Create a category first! /add_category",
        "choose_category": "📂 Select a category:",
        "material_saved": "✅ Material saved!\n🔹 Title: {title}\n🔹 Level: {level}",
        "send_question": "❓ Enter the question text:",
        "send_options": "📝 Enter options.\nFormat: Option1, Option2, Option3, Option4\n*(Must be exactly 4 options separated by commas)*",
        "wrong_options": "🚫 Error! Please send 4 options separated by commas.",
        "correct_answer": "🎯 Select the correct answer:",
        "question_level": "📈 Which level is this question for?",
        "question_saved": "✅ Question successfully saved! (Level: {level})",
        "show_stats": "📈 **Bot Statistics:**\n\n👤 Users: {user_count}\n📝 Quizzes Taken: {quiz_count}",
        "send_broadcast_text": "Enter the message to broadcast to all users (text, photo, or video):",
        "quantity_sended_message": "✅ Message successfully sent to {count} users!\n(Administrators excluded)",

        # materials.py
        "absent_category": "😔 No categories created yet.",
        "no_materials_found": "⚠️ No materials found for {level} level in this section.",
        "choose_material": "✅ Your level: {level}\n📖 Select the required material:",
        "file_send_error": "❌ Error sending file. File ID might be expired.",
        "categories_not_found": "⚠️ Categories not found.",

        # quiz.py
        "btn_detect_level": "📊 Determine my level",
        "quiz_not_ready": "⚠️ Sorry, the quiz system is not ready yet (not enough questions).",
        "test_started": "🚀 Quiz started! Total of {count} questions. Good luck!",
        "next_question": "❓ **Question {index}:**\n\n{text}",
        "loading_test": "Finishing quiz...",
        "questions_not_found": "❌ Error: Questions not found.",
        "test_finished": "🏁 **Quiz finished!**\n\n📊 Your score: **{score} / {max_score}**\n📈 Percentage: **{percentage:.1f}%**\n🏆 Your level: **{level}**\n\n✅ Data saved. You can track your history in \"My Results\" section!",

        # start.py
        "start_welcome": "👋 Hello, {name}!\n\nWelcome to the IELTS preparation bot. Here you can find materials suitable for your level and test your knowledge.",
        "else_welcome": "😊 Glad to see you again, {name}!",
        "my_profile": "👤 My profile",
        "no_quiz_yet": "No quizzes taken yet",
        "profile_text": "👤 **Your Profile:**\n\n📝 **Name:** {name}\n📊 **Level:** {level}\n🆔 **ID:** `{tg_id}`\n📅 **Registration Date:** {date}\n\n🔄 To update your level, click \"📊 Determine my level\" button.",
        "profile_not_found": "⚠️ Your data not found. Please click the /start command.",
        "no_results_yet": "📭 You haven't taken any quizzes yet. Determine your level with a quiz!",
        "your_results": "📊 **Your latest results:**\n\n",
        "result_item": "📅 {date} | 🎯 {score}/{total} ({percentage}%) | 🏆 {level}\n",

        # middlewares.py
        "only_admins": "⛔️ This section is for admins only!"
    }
}