#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hello Plugin — مثال تعريفي لنظام إضافات Ultimate Toolbox Pro v4.2.

يوضّح: التسجيل، البطاقات، الحقول، الأزرار، التوست، النسخ، التنقل بين
الأدوات، والترجمة وقت التشغيل عبر add_translations().
"""
from toolbox_api import (register_tool, card, buttons, field, statuslabel,
                         toast, copy_text, open_tool, t, add_translations,
                         row)
import customtkinter as ctk

# ترجمات هذه الإضافة — تُدمج فور التحميل قبل أول عرض
add_translations({
    "ar": {"Hello Plugin": "إضافة ترحيب", "Your name": "اسمك",
           "Greet": "تحية", "Copy greeting": "نسخ التحية",
           "Open Calculator": "افتح الآلة الحاسبة",
           "Hello from the plugin system": "تحية من نظام الإضافات",
           "Hello, {name}! 👋": "أهلًا {name}! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "اكتب اسمك ثم اضغط تحية — الإضافة مجرد بايثون 😊"},
    "zh": {"Hello Plugin": "问候插件", "Your name": "你的名字",
           "Greet": "打招呼", "Copy greeting": "复制问候语",
           "Open Calculator": "打开计算器",
           "Hello from the plugin system": "来自插件系统的问候",
           "Hello, {name}! 👋": "你好，{name}！👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "输入名字后点打招呼——插件就是普通 Python 😊"},
    "es": {"Hello Plugin": "Complemento de saludo", "Your name": "Tu nombre",
           "Greet": "Saludar", "Copy greeting": "Copiar saludo",
           "Open Calculator": "Abrir calculadora",
           "Hello from the plugin system": "Saludo del sistema de complementos",
           "Hello, {name}! 👋": "¡Hola, {name}! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "Escribe tu nombre y pulsa Saludar — un complemento es Python 😊"},
    "fr": {"Hello Plugin": "Extension de salutation", "Your name": "Votre nom",
           "Greet": "Saluer", "Copy greeting": "Copier le message",
           "Open Calculator": "Ouvrir la calculatrice",
           "Hello from the plugin system": "Bonjour depuis le système d'extensions",
           "Hello, {name}! 👋": "Bonjour, {name} ! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "Écrivez votre nom puis Saluer — une extension, c'est du Python 😊"},
    "ru": {"Hello Plugin": "Плагин приветствия", "Your name": "Ваше имя",
           "Greet": "Приветствовать", "Copy greeting": "Копировать приветствие",
           "Open Calculator": "Открыть калькулятор",
           "Hello from the plugin system": "Привет от системы плагинов",
           "Hello, {name}! 👋": "Привет, {name}! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "Введите имя и нажмите «Приветствовать» — плагин это просто Python 😊"},
    "pt": {"Hello Plugin": "Plugin de saudação", "Your name": "Seu nome",
           "Greet": "Cumprimentar", "Copy greeting": "Copiar saudação",
           "Open Calculator": "Abrir calculadora",
           "Hello from the plugin system": "Olá do sistema de plugins",
           "Hello, {name}! 👋": "Olá, {name}! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "Escreva seu nome e clique Cumprimentar — plugin é só Python 😊"},
    "hi": {"Hello Plugin": "नमस्ते प्लगइन", "Your name": "आपका नाम",
           "Greet": "नमस्ते कहें", "Copy greeting": "शुभकामना कॉपी करें",
           "Open Calculator": "कैलकुलेटर खोलें",
           "Hello from the plugin system": "प्लगइन सिस्टम से नमस्ते",
           "Hello, {name}! 👋": "नमस्ते, {name}! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "नाम लिखें और नमस्ते दबाएँ — प्लगइन सिर्फ Python है 😊"},
    "bn": {"Hello Plugin": "হ্যালো প্লাগইন", "Your name": "আপনার নাম",
           "Greet": "শুভেচ্ছা জানান", "Copy greeting": "শুভেচ্ছা কপি করুন",
           "Open Calculator": "ক্যালকুলেটর খুলুন",
           "Hello from the plugin system": "প্লাগইন সিস্টেম থেকে শুভেচ্ছা",
           "Hello, {name}! 👋": "হ্যালো, {name}! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "নাম লিখে শুভেচ্ছা চাপুন — প্লাগইন মানেই সাধারণ Python 😊"},
    "ur": {"Hello Plugin": "خوش آمدید پلگ ان", "Your name": "آپ کا نام",
           "Greet": "سلام کریں", "Copy greeting": "سلام کاپی کریں",
           "Open Calculator": "کیلکولیٹر کھولیں",
           "Hello from the plugin system": "پلگ ان سسٹم کی طرف سے سلام",
           "Hello, {name}! 👋": "خوش آمدید، {name}! 👋",
           "Write your name, then press Greet — a plugin is just Python 😊":
               "اپنا نام لکھیں اور سلام دبائیں — پلگ ان صرف Python ہے 😊"},
})


@register_tool(tid="hello_world", title="Hello Plugin", section="Plugins",
               icon="👋", keywords="demo hello example greeting welcome test")
def build(api, parent):
    """صفحة الإضافة — تُبنى عند فتح الأداة تمامًا كصفحات التطبيق."""
    card(parent, t("Hello from the plugin system"))

    name = field(parent, t("Your name"), width=280)

    def greet():
        who = (name.get() or "").strip() or "…"
        toast(t("Hello, {name}! 👋").format(name=who), "ok")

    def copy_greeting():
        who = (name.get() or "").strip() or "friend"
        copy_text(t("Hello, {name}! 👋").format(name=who))

    buttons(parent, [(t("Greet"), greet),
                     (t("Copy greeting"), copy_greeting),
                     (t("Open Calculator"), lambda: open_tool("calc"))])

    # إمكانية الخلط مع عناصر customtkinter مباشرة عند الحاجة
    r = row(parent)
    ctk.CTkLabel(r, text="🔌 v4.2 • API 1.0",
                 font=ctk.CTkFont(size=12), text_color="#9a9aa8").pack(
        anchor="e" if api.is_rtl() else "w")

    statuslabel(parent).configure(
        text=t("Write your name, then press Greet — a plugin is just Python 😊"))
