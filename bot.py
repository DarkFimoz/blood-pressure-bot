import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния разговора
HEIGHT, WEIGHT, AGE, GENDER, PREGNANT, SMOKING, ACTIVITY, STRESS, MEDICATION, BP1_SYS, BP1_DIA, BP2_SYS, BP2_DIA = range(13)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало работы с ботом"""
    await update.message.reply_text(
        "Привет! Я помогу проанализировать ваше артериальное давление.\n\n"
        "Введите ваш рост в см (например: 175):"
    )
    return HEIGHT

async def height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение роста"""
    try:
        height = int(update.message.text)
        if height < 50 or height > 250:
            await update.message.reply_text("Рост должен быть от 50 до 250 см. Введите корректный рост:")
            return HEIGHT
        context.user_data['height'] = height
        await update.message.reply_text("Введите ваш вес в кг (например: 70):")
        return WEIGHT
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число. Ваш рост в см:")
        return HEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение веса"""
    try:
        weight = int(update.message.text)
        if weight < 20 or weight > 300:
            await update.message.reply_text("Вес должен быть от 20 до 300 кг. Введите корректный вес:")
            return WEIGHT
        context.user_data['weight'] = weight
        await update.message.reply_text("Введите ваш возраст (например: 30):")
        return AGE
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число. Ваш вес в кг:")
        return WEIGHT

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение возраста"""
    try:
        age = int(update.message.text)
        if age < 1 or age > 120:
            await update.message.reply_text("Возраст должен быть от 1 до 120 лет. Введите корректный возраст:")
            return AGE
        context.user_data['age'] = age
        keyboard = [['Мужской', 'Женский']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Выберите ваш пол:", reply_markup=reply_markup)
        return GENDER
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число. Ваш возраст:")
        return AGE

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение пола"""
    gender = update.message.text
    context.user_data['gender'] = gender
    
    if gender == 'Женский' and 15 <= context.user_data['age'] <= 55:
        keyboard = [['Да', 'Нет']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Вы беременны?", reply_markup=reply_markup)
        return PREGNANT
    else:
        context.user_data['pregnant'] = 'Нет'
        keyboard = [['Да', 'Нет']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Вы курите?", reply_markup=reply_markup)
        return SMOKING

async def pregnant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о беременности"""
    context.user_data['pregnant'] = update.message.text
    keyboard = [['Да', 'Нет']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Вы курите?", reply_markup=reply_markup)
    return SMOKING

async def smoking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о курении"""
    context.user_data['smoking'] = update.message.text
    keyboard = [['Высокая', 'Средняя', 'Низкая']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Какой у вас уровень физической активности?",
        reply_markup=reply_markup
    )
    return ACTIVITY

async def activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о физической активности"""
    context.user_data['activity'] = update.message.text
    keyboard = [['Высокий', 'Средний', 'Низкий']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Какой у вас уровень стресса в последнее время?",
        reply_markup=reply_markup
    )
    return STRESS

async def stress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о стрессе"""
    context.user_data['stress'] = update.message.text
    keyboard = [['Да', 'Нет']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Принимаете ли вы лекарства, влияющие на давление?",
        reply_markup=reply_markup
    )
    return MEDICATION

async def medication(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о лекарствах"""
    context.user_data['medication'] = update.message.text
    await update.message.reply_text(
        "Теперь измерьте давление первый раз.\n"
        "Введите систолическое давление (верхнее число, например: 120):",
        reply_markup=ReplyKeyboardRemove()
    )
    return BP1_SYS

async def bp1_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Первое измерение - систолическое"""
    try:
        bp = int(update.message.text)
        if bp < 50 or bp > 250:
            await update.message.reply_text("Систолическое давление должно быть от 50 до 250. Введите корректное значение:")
            return BP1_SYS
        context.user_data['bp1_sys'] = bp
        await update.message.reply_text("Введите диастолическое давление (нижнее число, например: 80):")
        return BP1_DIA
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число. Систолическое давление:")
        return BP1_SYS

async def bp1_dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Первое измерение - диастолическое"""
    try:
        bp = int(update.message.text)
        if bp < 30 or bp > 150:
            await update.message.reply_text("Диастолическое давление должно быть от 30 до 150. Введите корректное значение:")
            return BP1_DIA
        context.user_data['bp1_dia'] = bp
        await update.message.reply_text(
            "Отдохните 2-3 минуты и измерьте давление второй раз.\n"
            "Введите систолическое давление (верхнее число):"
        )
        return BP2_SYS
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число. Диастолическое давление:")
        return BP1_DIA

async def bp2_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Второе измерение - систолическое"""
    try:
        bp = int(update.message.text)
        if bp < 50 or bp > 250:
            await update.message.reply_text("Систолическое давление должно быть от 50 до 250. Введите корректное значение:")
            return BP2_SYS
        context.user_data['bp2_sys'] = bp
        await update.message.reply_text("Введите диастолическое давление (нижнее число):")
        return BP2_DIA
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число. Систолическое давление:")
        return BP2_SYS

async def bp2_dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Второе измерение - диастолическое и анализ"""
    try:
        bp = int(update.message.text)
        if bp < 30 or bp > 150:
            await update.message.reply_text("Диастолическое давление должно быть от 30 до 150. Введите корректное значение:")
            return BP2_DIA
        context.user_data['bp2_dia'] = bp
        
        # Вычисляем среднее давление
        avg_sys = (context.user_data['bp1_sys'] + context.user_data['bp2_sys']) / 2
        avg_dia = (context.user_data['bp1_dia'] + context.user_data['bp2_dia']) / 2
        
        # Анализ давления
        result = analyze_blood_pressure(
            avg_sys, avg_dia,
            context.user_data
        )
        
        response = f"📊 Результаты анализа:\n\n"
        response += f"Ваши данные:\n"
        response += f"• Рост: {context.user_data['height']} см\n"
        response += f"• Вес: {context.user_data['weight']} кг\n"
        response += f"• Возраст: {context.user_data['age']} лет\n"
        response += f"• Пол: {context.user_data['gender']}\n"
        if context.user_data['gender'] == 'Женский' and context.user_data.get('pregnant') == 'Да':
            response += f"• Беременность: Да\n"
        response += f"• Курение: {context.user_data['smoking']}\n"
        response += f"• Физическая активность: {context.user_data['activity']}\n"
        response += f"• Уровень стресса: {context.user_data['stress']}\n"
        response += f"• Прием лекарств: {context.user_data['medication']}\n\n"
        response += f"Измерения давления:\n"
        response += f"• Первое: {context.user_data['bp1_sys']}/{context.user_data['bp1_dia']}\n"
        response += f"• Второе: {context.user_data['bp2_sys']}/{context.user_data['bp2_dia']}\n"
        response += f"• Среднее: {avg_sys:.0f}/{avg_dia:.0f}\n\n"
        response += f"{result}\n\n"
        response += "Для нового измерения используйте /start"
        
        await update.message.reply_text(response)
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число. Диастолическое давление:")
        return BP2_DIA

def analyze_blood_pressure(sys, dia, user_data):
    """Анализ артериального давления"""
    
    age = user_data['age']
    gender = user_data['gender']
    pregnant = user_data.get('pregnant', 'Нет')
    smoking = user_data['smoking']
    activity = user_data['activity']
    stress = user_data['stress']
    medication = user_data['medication']
    
    # Нормы давления по возрасту
    if age < 20:
        normal_sys_range = (100, 120)
        normal_dia_range = (70, 80)
    elif age < 40:
        normal_sys_range = (110, 130)
        normal_dia_range = (70, 85)
    elif age < 60:
        normal_sys_range = (120, 135)
        normal_dia_range = (75, 85)
    else:
        normal_sys_range = (120, 140)
        normal_dia_range = (80, 90)
    
    # Определение категории давления
    if sys < 90 or dia < 60:
        category = "❗ Гипотония (пониженное давление)"
        recommendation = "Ваше давление ниже нормы. Рекомендуется консультация врача."
    elif sys < normal_sys_range[0] or dia < normal_dia_range[0]:
        category = "⚠️ Немного пониженное давление"
        recommendation = "Давление чуть ниже нормы для вашего возраста. Следите за самочувствием."
    elif sys <= normal_sys_range[1] and dia <= normal_dia_range[1]:
        category = "✅ Нормальное давление"
        recommendation = "Ваше давление в пределах нормы! Продолжайте вести здоровый образ жизни."
    elif sys <= 139 and dia <= 89:
        category = "⚠️ Предгипертония (повышенное нормальное)"
        recommendation = "Давление немного повышено. Рекомендуется контролировать его регулярно."
    elif sys <= 159 and dia <= 99:
        category = "❗ Гипертония 1 степени"
        recommendation = "Повышенное давление. Необходима консультация врача и контроль давления."
    elif sys <= 179 and dia <= 109:
        category = "❗❗ Гипертония 2 степени"
        recommendation = "Значительно повышенное давление. Обязательно обратитесь к врачу!"
    else:
        category = "🚨 Гипертония 3 степени (критическое)"
        recommendation = "КРИТИЧЕСКИ высокое давление! Срочно обратитесь к врачу!"
    
    result = f"Категория: {category}\n\n"
    result += f"Норма для вашего возраста ({age} лет):\n"
    result += f"• Систолическое: {normal_sys_range[0]}-{normal_sys_range[1]}\n"
    result += f"• Диастолическое: {normal_dia_range[0]}-{normal_dia_range[1]}\n\n"
    result += f"💡 {recommendation}\n\n"
    
    # Анализ факторов риска
    risk_factors = []
    positive_factors = []
    
    if pregnant == 'Да':
        risk_factors.append("⚠️ Беременность требует особого контроля давления")
    
    if smoking == 'Да':
        risk_factors.append("⚠️ Курение повышает риск гипертонии и сердечно-сосудистых заболеваний")
    
    if activity == 'Низкая':
        risk_factors.append("⚠️ Низкая физическая активность может способствовать повышению давления")
    elif activity == 'Высокая':
        positive_factors.append("✅ Высокая физическая активность помогает поддерживать нормальное давление")
    
    if stress == 'Высокий':
        risk_factors.append("⚠️ Высокий уровень стресса может временно повышать давление")
    
    if medication == 'Да':
        risk_factors.append("ℹ️ Учитывайте, что лекарства могут влиять на показатели давления")
    
    # Расчет ИМТ
    height_m = user_data['height'] / 100
    bmi = user_data['weight'] / (height_m ** 2)
    
    if bmi < 18.5:
        risk_factors.append(f"⚠️ Недостаточный вес (ИМТ: {bmi:.1f}) может быть связан с гипотонией")
    elif bmi >= 25 and bmi < 30:
        risk_factors.append(f"⚠️ Избыточный вес (ИМТ: {bmi:.1f}) повышает риск гипертонии")
    elif bmi >= 30:
        risk_factors.append(f"⚠️ Ожирение (ИМТ: {bmi:.1f}) значительно повышает риск гипертонии")
    else:
        positive_factors.append(f"✅ Нормальный вес (ИМТ: {bmi:.1f})")
    
    if risk_factors:
        result += "⚠️ Факторы риска:\n"
        for factor in risk_factors:
            result += f"{factor}\n"
        result += "\n"
    
    if positive_factors:
        result += "✅ Положительные факторы:\n"
        for factor in positive_factors:
            result += f"{factor}\n"
        result += "\n"
    
    # Общие рекомендации
    result += "📋 Рекомендации:\n"
    if smoking == 'Да':
        result += "• Откажитесь от курения\n"
    if activity == 'Низкая':
        result += "• Увеличьте физическую активность (30 мин в день)\n"
    if stress == 'Высокий':
        result += "• Практикуйте методы снижения стресса\n"
    if bmi >= 25:
        result += "• Нормализуйте вес\n"
    result += "• Ограничьте соль в рационе\n"
    result += "• Регулярно измеряйте давление\n"
    if sys > 140 or dia > 90:
        result += "• Обязательно проконсультируйтесь с врачом!"
    
    return result

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена разговора"""
    await update.message.reply_text(
        "Операция отменена. Для начала используйте /start",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    """Запуск бота"""
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не установлен!")
        return
    
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, height)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            PREGNANT: [MessageHandler(filters.TEXT & ~filters.COMMAND, pregnant)],
            SMOKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, smoking)],
            ACTIVITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, activity)],
            STRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, stress)],
            MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, medication)],
            BP1_SYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, bp1_sys)],
            BP1_DIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, bp1_dia)],
            BP2_SYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, bp2_sys)],
            BP2_DIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, bp2_dia)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(conv_handler)
    
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
