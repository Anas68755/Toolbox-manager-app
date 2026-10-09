#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate Toolbox Pro v4.5
=========================
صندوق أدوات متكامل لسطح المكتب — Windows / Linux / macOS
Python 3.9+ · customtkinter (6.x) · offline-first

التشغيل:  python toolbox.py
الاعتمادات الأساسية:   customtkinter, psutil
الاعتمادات الاختيارية: requests, qrcode, Pillow, llama-cpp-python (للـ LLM المحلي)،
                      cryptography (لخزائن AES/Fernet — اختياري، له بديل مدمج)

سجل تحسينات v4.5 — التفكير العميق + موديلات أكبر + خزائن Vault:
- مفتاح 🧠 "التفكير العميق" في المحادثة: تشغيل/إيقاف بضغطة (للأجهزة الضعيفة)
  · الإيقاف يحجب ‎<think>…</think>‎ وreasoning_content من البث فورًا ويعرض الجواب فقط
  · مع خادم llama.cpp يُرسل chat_template_kwargs enable_thinking=false فلا تُولَّد
    رموز التفكير أصلًا (توفير حقيقي في الوقت والذاكرة على الأجهزة الضعيفة)
  · الحالة تُحفظ مع إعدادات LLM ويُشار لعدد الرموز المحجوبة بعد كل جواب
- قائمة الموديلات أصبحت 25 موديلًا موثّقًا بالحجم الحقيقي: قائمتان — صغيرة (حتى 3B)
  وكبيرة (7B حتى 70B): Qwen2.5/Qwen3، Llama 3.1/3.3، Mistral، gemma-2، phi-4،
  DeepSeek-R1-Distill وQwQ وQwen3-30B-A3B (MoE) — كل الروابط فُحصت حيًّا (HTTP 200)
- أداة جديدة 🛡️ Vault في قسم Security: خزائن مشفّرة بكلمة سر رئيسية
  · تشفير AES-128 عبر Fernet إن توفّرت cryptography، وإلا شيفرة مدمجة
    PBKDF2-HMAC-SHA256 (200k) + keystream HMAC-SHA256-CTR + MAC (encrypt-then-MAC)
  · خزائن متعددة (.uvault)، إدخالات: عنوان/مستخدم/كلمة سر/رابط/ملاحظات
  · نسخ كلمة السر بمسح تلقائي من الحافظة بعد 30 ثانية، بحث فوري، توليد كلمات سر
  · قفل تلقائي بعد 5 دقائق خمول + قفل يدوي + تغيير الكلمة الرئيسية + حذف الخزنة

سجل تحسينات v4.1 — Local LLM (GGUF):
- أداة جديدة 🦙 Local LLM في قسم Developer: تشغيل نماذج GGUF محليًا بالكامل دون إنترنت
- المحرك: llama.cpp عبر llama-cpp-python (اختياري — غيابه لا يؤثر على أي أداة أخرى)
- تحميل/إخراج الموديل (Unload يحرر الذاكرة)، والموديل يبقى محمّلًا عند التنقل بين الأدوات
- محادثة متعددة الأدوار مع بث حي للرموز (streaming) عبر قناة _ui الآمنة للخيوط
- زر إيقاف فوري للتوليد + إحصاءات بعد كل إجابة (عدد الرموز والسرعة tok/s)
- قارئ رؤوس GGUF مكتوب من الصفر عبر struct: الاسم، البنية، التكميم، طول السياق، الطبقات، المفردات — يعمل حتى بدون llama-cpp-python وبلا قراءة كاملة للملف
- تقدير الذاكرة المطلوبة قبل التحميل + قائمة أحدث 6 موديلات محفوظة في الإعدادات
- تذكّر آخر إعدادات الضبط (السياق، GPU layers، الحرارة، Top-P، البرومبت النظامي…) واستعادتها تلقائيًا
- مغادرة صفحة الأداة أو إغلاق التطبيق يوقف التوليد ويحرر الذاكرة بأمان
- صفر استدعاءات Tcl من خيوط العامل في أداة LLM: قيم الواجهة تُقرأ في الخيط الرئيسي وتُمرَّر كوسائط بايثون سادة (أكثر أمانًا على macOS خاصة)
- كل النصوص الجديدة مترجمة في 10 لغات

سجل تحسينات v4.0 — Phase 1 (القائمة الجانبية القابلة للتمرير + UX):
- الشريط الجانبي أصبح CTkScrollableFrame قابلًا للتمرير: كل الأدوات تظهر حتى في النوافذ القصيرة (500px)
- شريط تمرير رفيع 6px بألوان الثيم (border/primary) مع إخفاء تلقائي عندما لا تكون هناك حاجة له
- عجلة الفأرة تعمل فوق الأزرار والعناوين (مدمجة في customtkinter 6.x + ربط صريح للأمان)
- Shift+Wheel للتمرير الأفقي (مدعوم أصلًا من CTkScrollableFrame)
- البحث يمرّر القائمة لأعلى تلقائيًا + debounce (180ms) لسلاسة الكتابة مع 60+ أداة
- توسيع/طي الأقسام يحافظ على موضع التمرير (لا قفز مزعج للأعلى)
- تلميح "اسحب للأسفل ↓" عند أول تشغيل فقط إذا كان المحتوى أطول من القائمة (يُحفظ في الإعدادات)
- بحث ضبابي (fuzzy) عبر difflib عند عدم التطابق الحرفي (يتحمّل الأخطاء المطبعية البسيطة)
- عدّاد نتائج البحث في شريط الحالة + Escape يمسح البحث
- خطوط القائمة مخزّنة مؤقتًا (أسرع بـ ~70 إنشاء خط لكل إعادة بناء)
- اختصارات جديدة: F1 حول، Ctrl+, إعدادات، Ctrl+D تبديل الوضع
- سجل تحسينات v3.2 (Changelog):
- إصلاح عرض المؤقّت/بومودورو للمدد > 59 دقيقة (كانت تلتفّ إلى 00:00)
- إصلاح حساب "الميلاد القادم" لتواريخ 29 فبراير (كان ينهار)
- فحص المنافذ أصبح متوازيًا (أسرع ~50×) مع مؤشر تقدّم مباشر ونطاق أوسع
- قناة آمنة لتحديث الواجهة من الخيوط (queue بدل after() من threads)
- زر ⭐ لم يعد يمسح مدخلات الأداة الحالية عند التفضيل
- لوحة الأوامر: تنقّل بـ ↑/↓ + Enter، وتظليل للعنصر المحدد
- HTTP Client: PUT/DELETE/HEAD + ترويسات مخصصة + عرض حالة الاستجابة
- المساعد الذكي: محادثة متعددة الأدوار + system prompt + محادثة جديدة
- Regex: استبدال. Bulk Rename: دعم regex + حماية من الكتابة فوق الملفات
- كاشف المكرّرات: حذف آمن مع تأكيد. Checksum: خوارزميات sha3/blake2
- الملاحظات: حفظ تلقائي كل 30 ثانية
- منع وميض نافذة الكونسول على Windows عند استدعاء أوامر خارجية
- فحص رموز حالة HTTP في طبقة الشبكة + معالجة أخطاء أدق
- ترجمة كل الرسائل المدمجة في الواجهة (لا عربية ثابتة في اللغات الأخرى)
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────
# 【1】 الاستيرادات والحمايات
# ─────────────────────────────────────────────────────────────
import ast
import base64
import binascii
import csv
import ctypes
import datetime as _dt
import difflib
import gc
import hashlib
import hmac
import html
import io
import json
import math
import os
import platform
import queue
import random
import re
import secrets
import shutil
import socket
import string
import struct
import subprocess
import sys
import tarfile
import threading
import time
import traceback
import urllib.parse
import urllib.request
import uuid
import webbrowser
import zipfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

# tkinter (يأتي مع بايثون) — نحتاج Canvas و filedialog
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except Exception:  # pragma: no cover
    print("[!] tkinter غير مثبت. على Linux: sudo apt install python3-tk")
    sys.exit(1)

# zoneinfo (Python 3.9+)
try:
    from zoneinfo import ZoneInfo, available_timezones
    HAS_ZONEINFO = True
except Exception:
    ZoneInfo = None  # type: ignore
    available_timezones = lambda: set()  # type: ignore
    HAS_ZONEINFO = False

# ── اعتماد أساسي: customtkinter
try:
    import customtkinter as ctk
except Exception:
    print("[!] customtkinter غير مثبت.\n    ثبّته عبر:  pip install customtkinter")
    sys.exit(1)

# ── اعتماد أساسي: psutil
try:
    import psutil
    HAS_PSUTIL = True
except Exception:
    psutil = None  # type: ignore
    HAS_PSUTIL = False

# ── اعتمادات اختيارية (لا تُسقط التطبيق أبدًا)
try:
    import requests
    HAS_REQUESTS = True
except Exception:
    requests = None  # type: ignore
    HAS_REQUESTS = False

try:
    import qrcode
    HAS_QRCODE = True
except Exception:
    qrcode = None  # type: ignore
    HAS_QRCODE = False

try:
    from PIL import Image, ImageTk, ImageOps
    HAS_PIL = True
except Exception:
    Image = ImageTk = ImageOps = None  # type: ignore
    HAS_PIL = False

MISSING_HINTS = {
    "psutil":   "pip install psutil",
    "requests": "pip install requests",
    "qrcode":   "pip install qrcode[pil]",
    "Pillow":   "pip install Pillow",
    "llama-cpp-python": "pip install llama-cpp-python",
}

# ─────────────────────────────────────────────────────────────
# 【2】 الثوابت والمسارات
# ─────────────────────────────────────────────────────────────
APP_NAME = "Ultimate Toolbox Pro"
APP_VERSION = "4.7.0"
APP_DIR = os.path.dirname(os.path.abspath(__file__))

F_SETTINGS = os.path.join(APP_DIR, "ultimate_toolbox_settings.json")
F_TASKS    = os.path.join(APP_DIR, "ultimate_toolbox_tasks.json")
F_NOTES    = os.path.join(APP_DIR, "ultimate_toolbox_notes.txt")
F_THEME    = os.path.join(APP_DIR, "ultimate_toolbox_theme.json")
F_HISTORY  = os.path.join(APP_DIR, "polybuild_history.json")

SUBPROCESS_TIMEOUT = 30          # لا subprocess بدون timeout
NET_TIMEOUT = 12
MAX_HISTORY = 100

# ✦ v4.2: واجهة الإضافات — يجب أن تجاور toolbox.py؛ غيابها لا يُسقط التطبيق
try:
    import toolbox_api
except Exception:                      # تشغيل من sandbox بلا toolbox_api
    toolbox_api = None

# لوحة الألوان: أسود/أحمر
PALETTE = {
    "dark": {
        "bg":        "#0b0b0d",
        "surface":   "#131317",
        "surface2":  "#1b1b21",
        "border":    "#2a2a33",
        "text":      "#f2f2f5",
        "muted":     "#9a9aa8",
        "primary":   "#e01b24",
        "primary_h": "#ff2d38",
        "ok":        "#2ecc71",
        "warn":      "#f0a020",
        "err":       "#ff4d4d",
    },
    "light": {
        "bg":        "#f4f4f6",
        "surface":   "#ffffff",
        "surface2":  "#ececf0",
        "border":    "#d3d3da",
        "text":      "#15151a",
        "muted":     "#61616e",
        "primary":   "#c00d16",
        "primary_h": "#e01b24",
        "ok":        "#199e4f",
        "warn":      "#b97400",
        "err":       "#c62828",
    },
}


def C(key: str, mode: Optional[str] = None) -> str:
    """إرجاع لون من اللوحة حسب الوضع الحالي."""
    m = mode or ctk.get_appearance_mode().lower()
    return PALETTE["light" if m == "light" else "dark"][key]


def CC(key: str) -> Tuple[str, str]:
    """زوج (فاتح، داكن) لاستخدامه مباشرة في widgets customtkinter."""
    return (PALETTE["light"][key], PALETTE["dark"][key])


# ─────────────────────────────────────────────────────────────
# 【3】 توليد ملف الثيم JSON حقيقي
# ─────────────────────────────────────────────────────────────
def _base_theme_dict() -> Dict[str, Any]:
    """نقرأ ثيم customtkinter المدمج كأساس لضمان وجود كل المفاتيح."""
    try:
        base_dir = os.path.join(os.path.dirname(ctk.__file__), "assets", "themes")
        for name in ("blue.json", "dark-blue.json", "green.json"):
            p = os.path.join(base_dir, name)
            if os.path.isfile(p):
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
    except Exception:
        pass
    return {}


def build_theme_file(font_family: str = "Roboto") -> str:
    """توليد ultimate_toolbox_theme.json بلوحة أسود/أحمر — يتبعه كل widget."""
    th = _base_theme_dict()
    L, D = PALETTE["light"], PALETTE["dark"]
    pair = lambda k: [L[k], D[k]]

    def setk(widget: str, **kw):
        th.setdefault(widget, {})
        th[widget].update(kw)

    setk("CTk", fg_color=pair("bg"))
    setk("CTkToplevel", fg_color=pair("bg"))
    setk("CTkFrame",
         fg_color=pair("surface"), top_fg_color=pair("surface2"),
         border_color=pair("border"))
    setk("CTkButton",
         fg_color=pair("primary"), hover_color=pair("primary_h"),
         border_color=pair("border"), text_color=["#ffffff", "#ffffff"],
         text_color_disabled=pair("muted"))
    setk("CTkLabel", fg_color="transparent", text_color=pair("text"))
    setk("CTkEntry",
         fg_color=pair("surface2"), border_color=pair("border"),
         text_color=pair("text"), placeholder_text_color=pair("muted"))
    setk("CTkCheckBox",
         fg_color=pair("primary"), border_color=pair("border"),
         hover_color=pair("primary_h"), checkmark_color=["#ffffff", "#ffffff"],
         text_color=pair("text"), text_color_disabled=pair("muted"))
    setk("CTkSwitch",
         fg_color=pair("border"), progress_color=pair("primary"),
         button_color=pair("text"), button_hover_color=pair("primary_h"),
         text_color=pair("text"), text_color_disabled=pair("muted"))
    setk("CTkRadioButton",
         fg_color=pair("primary"), border_color=pair("border"),
         hover_color=pair("primary_h"), text_color=pair("text"),
         text_color_disabled=pair("muted"))
    setk("CTkProgressBar",
         fg_color=pair("surface2"), progress_color=pair("primary"),
         border_color=pair("border"))
    setk("CTkSlider",
         fg_color=pair("surface2"), progress_color=pair("primary"),
         button_color=pair("primary"), button_hover_color=pair("primary_h"))
    setk("CTkOptionMenu",
         fg_color=pair("surface2"), button_color=pair("primary"),
         button_hover_color=pair("primary_h"), text_color=pair("text"),
         text_color_disabled=pair("muted"))
    setk("CTkComboBox",
         fg_color=pair("surface2"), border_color=pair("border"),
         button_color=pair("primary"), button_hover_color=pair("primary_h"),
         text_color=pair("text"), text_color_disabled=pair("muted"))
    setk("CTkScrollbar",
         fg_color="transparent", button_color=pair("border"),
         button_hover_color=pair("primary"))
    setk("CTkSegmentedButton",
         fg_color=pair("surface2"), selected_color=pair("primary"),
         selected_hover_color=pair("primary_h"),
         unselected_color=pair("surface2"),
         unselected_hover_color=pair("border"),
         text_color=pair("text"), text_color_disabled=pair("muted"))
    setk("CTkTextbox",
         fg_color=pair("surface2"), border_color=pair("border"),
         text_color=pair("text"), scrollbar_button_color=pair("border"),
         scrollbar_button_hover_color=pair("primary"))
    setk("CTkScrollableFrame", label_fg_color=pair("surface2"))
    setk("DropdownMenu",
         fg_color=pair("surface2"), hover_color=pair("primary"),
         text_color=pair("text"))

    # قيم شكلية افتراضية — تُستخدم فقط إن تعذّر قراءة ثيم customtkinter المدمج
    shapes = {
        "CTkFrame": {"corner_radius": 6, "border_width": 0},
        "CTkButton": {"corner_radius": 6, "border_width": 0},
        "CTkLabel": {"corner_radius": 0},
        "CTkEntry": {"corner_radius": 6, "border_width": 2},
        "CTkCheckBox": {"corner_radius": 6, "border_width": 3},
        "CTkSwitch": {"corner_radius": 1000, "border_width": 3,
                      "button_length": 0},
        "CTkRadioButton": {"corner_radius": 1000, "border_width_checked": 6,
                           "border_width_unchecked": 3},
        "CTkProgressBar": {"corner_radius": 1000, "border_width": 0},
        "CTkSlider": {"corner_radius": 1000, "button_corner_radius": 1000,
                      "border_width": 6, "button_length": 0},
        "CTkOptionMenu": {"corner_radius": 6},
        "CTkComboBox": {"corner_radius": 6, "border_width": 2},
        "CTkScrollbar": {"corner_radius": 1000, "border_spacing": 4},
        "CTkSegmentedButton": {"corner_radius": 6, "border_width": 2},
        "CTkTextbox": {"corner_radius": 6, "border_width": 0,
                       "scrollbar_button_color": pair("border"),
                       "scrollbar_button_hover_color": pair("primary")},
        "CTkScrollableFrame": {"label_fg_color": pair("surface2")},
        "DropdownMenu": {"corner_radius": 6, "border_width": 0},
    }
    for widget, vals in shapes.items():
        th.setdefault(widget, {})
        for k, v in vals.items():
            th[widget].setdefault(k, v)

    # الخطوط: Tajawal للعربية/الأردية، Roboto لغيرها
    th.setdefault("CTkFont", {})
    for osname, size in (("macOS", 13), ("Windows", 13), ("Linux", 13)):
        th["CTkFont"][osname] = {"family": font_family, "size": size, "weight": "normal"}

    try:
        with open(F_THEME, "w", encoding="utf-8") as f:
            json.dump(th, f, ensure_ascii=False, indent=2)
        return F_THEME
    except Exception:
        return "blue"


# ─────────────────────────────────────────────────────────────
# 【4】 النظام اللغوي i18n — المفتاح الأساسي هو الإنجليزية
# ─────────────────────────────────────────────────────────────
LANG_NAMES = {           # كل لغة تُعرض بلغتها الأصلية دائمًا
    "en": "English", "ar": "العربية", "zh": "中文", "hi": "हिन्दी",
    "es": "Español", "fr": "Français", "bn": "বাংলা", "pt": "Português",
    "ru": "Русский", "ur": "اردو",
}
RTL_LANGS = {"ar", "ur"}

_AR = {
    # الأقسام
    "General": "عام", "System": "النظام", "Files": "الملفات", "Text": "النصوص",
    "Security": "الأمن", "Media": "الوسائط", "Calc & Time": "الحساب والوقت",
    "Productivity": "الإنتاجية", "Developer": "المطوّر", "APIs": "الخدمات",
    "Data": "البيانات",
    # عناصر عامة
    "Dashboard": "لوحة التحكم", "Settings": "الإعدادات", "About": "حول",
    "Search tools…": "ابحث عن أداة…", "Favorites": "المفضلة",
    "Recent": "المستخدمة حديثًا", "Language": "اللغة", "Theme": "الثيم",
    "Dark": "داكن", "Light": "فاتح", "Run": "تشغيل", "Copy": "نسخ",
    "Clear": "مسح", "Save": "حفظ", "Load": "تحميل", "Delete": "حذف",
    "Browse": "استعراض", "Close": "إغلاق", "Add": "إضافة", "Refresh": "تحديث",
    "Start": "ابدأ", "Stop": "إيقاف", "Reset": "تصفير", "Export": "تصدير",
    "Import": "استيراد", "Generate": "توليد", "Convert": "تحويل",
    "Loading…": "جارٍ التحميل…", "Done": "تم", "Failed": "فشل",
    "Copied to clipboard": "تم النسخ إلى الحافظة",
    "Result": "النتيجة", "Input": "المدخل", "Output": "المخرج",
    "Options": "الخيارات", "Command palette": "لوحة الأوامر",
    "Not installed": "غير مثبت", "Install with": "ثبّته عبر",
    "Select folder": "اختر مجلدًا", "Select file": "اختر ملفًا",
    # الأدوات
    "System Information": "معلومات النظام", "Process Manager": "مدير العمليات",
    "Network Info": "معلومات الشبكة", "DNS Lookup": "استعلام DNS",
    "HTTP Headers": "ترويسات HTTP", "Time Zones": "المناطق الزمنية",
    "File Organizer": "منظّم الملفات", "Duplicate Finder": "كاشف المكرّر",
    "Bulk Rename": "إعادة تسمية جماعية", "Split & Merge": "تقسيم ودمج",
    "Checksum": "بصمة الملف", "ZIP Tools": "أدوات ZIP",
    "Base64 File": "ملف Base64", "CSV ⇄ JSON": "CSV ⇄ JSON",
    "Text Counter": "عدّاد النص", "Text Transform": "تحويل النص",
    "Text Diff": "مقارنة نصين", "Encode / Decode": "ترميز / فك ترميز",
    "JSON Tools": "أدوات JSON", "Regex Tester": "اختبار Regex",
    "URL Analyzer": "محلل الروابط", "Password Generator": "مولّد كلمات المرور",
    "Text Hash": "تجزئة النص", "UUID Generator": "مولّد UUID",
    "Color Converter": "محوّل الألوان", "Color Palette": "لوحة ألوان",
    "QR Code": "رمز QR", "Image Tools": "أدوات الصور",
    "Calculator": "الآلة الحاسبة", "Unit Converter": "محوّل الوحدات",
    "Date & Time": "التاريخ والوقت", "Timer": "المؤقّت",
    "Pomodoro": "بومودورو", "Todo List": "قائمة المهام", "Notes": "الملاحظات",
    "Backup": "النسخ الاحتياطي", "PolyBuild": "PolyBuild",
    "Port Scanner": "فاحص المنافذ", "HTTP Client": "عميل HTTP",
    "Weather": "الطقس", "Currency": "العملات", "Translate": "الترجمة",
    "GeoIP": "تحديد الموقع", "GitHub": "GitHub", "Crypto Prices": "أسعار العملات الرقمية",
    "News": "الأخبار", "URL Shortener": "اختصار الروابط", "Fun APIs": "خدمات ترفيهية",
    "AI Assistant": "المساعد الذكي", "Fake Data": "بيانات وهمية",
    "Random Picker": "اختيار عشوائي", "Lorem Ipsum": "نص تجريبي",
    # مفاتيح v3.2
    "Click a color to copy": "اضغط على أي لون لنسخه",
    "One item per line": "سطر واحد لكل عنصر",
    "3 stages: size → 8KB prefix → full hash": "ثلاث مراحل: الحجم ← بادئة 8KB ← التجزئة الكاملة",
    "Keys are stored locally only.": "تُحفظ المفاتيح محليًا فقط في ملف الإعدادات",
    "Safe: parsed via ast — no eval": "آمنة: تُحلَّل التعابير عبر ast — بلا eval",
    "OpenAI-compatible endpoint; keys in Settings": "متوافق مع OpenAI؛ المفاتيح تُضبط في الإعدادات",
    "polybuild.py not found — set it in Settings": "polybuild.py غير موجود — حدّده في الإعدادات",
    "Restart the app to apply everything.": "أعد تشغيل التطبيق لتطبيق كل شيء.",
    "psutil missing — limited info.": "psutil غير مثبت — التفاصيل محدودة.",
    "Time is up!": "انتهى الوقت!",
    "Break time!": "وقت الراحة!",
    "Back to work!": "عودة إلى العمل!",
    "Add OpenWeather key in Settings for more details.": "أضف مفتاح OpenWeather في الإعدادات لتفاصيل أدق.",
    "Replace": "استبدال",
    "New chat": "محادثة جديدة",
    "Terminate process?": "إنهاء العملية؟",
    "Delete duplicates?": "حذف الملفات المكرّرة؟",
    "autosave every 30s": "حفظ تلقائي كل 30 ثانية",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "اسحب للأسفل ↓",
    "{n} tools found": "تم العثور على {n} أداة",
    # مفاتيح v4.1 — Local LLM (GGUF)
    "Local LLM": "نموذج لغوي محلي",
    "Run GGUF models locally — 100% offline": "شغّل نماذج GGUF محليًا — دون اتصال 100%",
    "Model": "الموديل", "GGUF model file": "ملف GGUF",
    "Load model": "تحميل الموديل", "Unload model": "إخراج الموديل",
    "Model info": "معلومات الموديل", "Configuration": "الضبط",
    "Context size": "حجم السياق", "GPU layers (0=CPU, -1=all)": "طبقات GPU (0=معالج، -1=الكل)",
    "Threads": "الخيوط", "Temperature": "الحرارة", "Top P": "Top P",
    "Max tokens": "أقصى عدد للرموز", "Repeat penalty": "عقوبة التكرار",
    "System prompt": "تعليمات النظام", "Chat": "المحادثة", "Send": "إرسال",
    "Generating…": "جارٍ التوليد…", "Stopped.": "توقف.",
    "Model unloaded": "تم إخراج الموديل", "No model selected": "لم يُحدَّد موديل",
    "Quantization": "التكميم", "Context length": "طول السياق",
    "Architecture": "البنية", "Layers": "طبقات", "Vocabulary": "المفردات",
    "Estimated RAM": "الذاكرة التقديرية", "Save chat": "حفظ المحادثة",
    "Chat saved to": "حُفظت المحادثة في", "Recent models": "الموديلات الأخيرة",
    "You": "أنت", "Assistant": "المساعد", "Your message": "رسالتك",
    "Chat is empty": "المحادثة فارغة", "Model ready": "الموديل جاهز",
    "First load can take a minute…": "التحميل الأول قد يستغرق دقيقة…",
}

_ZH = {
    "General": "常规", "System": "系统", "Files": "文件", "Text": "文本",
    "Security": "安全", "Media": "媒体", "Calc & Time": "计算与时间",
    "Productivity": "效率", "Developer": "开发者", "APIs": "接口", "Data": "数据",
    "Dashboard": "仪表盘", "Settings": "设置", "About": "关于",
    "Search tools…": "搜索工具…", "Favorites": "收藏", "Recent": "最近使用",
    "Language": "语言", "Theme": "主题", "Dark": "深色", "Light": "浅色",
    "Run": "运行", "Copy": "复制", "Clear": "清空", "Save": "保存",
    "Load": "载入", "Delete": "删除", "Browse": "浏览", "Close": "关闭",
    "Add": "添加", "Refresh": "刷新", "Start": "开始", "Stop": "停止",
    "Reset": "重置", "Export": "导出", "Import": "导入", "Generate": "生成",
    "Convert": "转换", "Loading…": "加载中…", "Done": "完成", "Failed": "失败",
    "Copied to clipboard": "已复制到剪贴板", "Result": "结果", "Input": "输入",
    "Output": "输出", "Options": "选项", "System Information": "系统信息",
    "Process Manager": "进程管理", "Network Info": "网络信息",
    "File Organizer": "文件整理", "Duplicate Finder": "重复文件查找",
    "Bulk Rename": "批量重命名", "Checksum": "校验和", "ZIP Tools": "ZIP 工具",
    "Text Counter": "文本统计", "Text Transform": "文本转换", "Text Diff": "文本对比",
    "JSON Tools": "JSON 工具", "Regex Tester": "正则测试",
    "Password Generator": "密码生成器", "Text Hash": "文本哈希",
    "Color Converter": "颜色转换", "QR Code": "二维码", "Image Tools": "图像工具",
    "Calculator": "计算器", "Unit Converter": "单位换算", "Date & Time": "日期时间",
    "Timer": "计时器", "Todo List": "待办事项", "Notes": "笔记",
    "Backup": "备份", "Weather": "天气", "Currency": "汇率", "Translate": "翻译",
    "News": "新闻", "Fake Data": "测试数据", "Time Zones": "时区",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "向下滚动查看更多 ↓",
    "{n} tools found": "找到 {n} 个工具",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "本地大模型",
    "Run GGUF models locally — 100% offline": "本地运行 GGUF 模型 — 100% 离线",
    "Model": "模型", "GGUF model file": "GGUF 模型文件",
    "Load model": "加载模型", "Unload model": "卸载模型",
    "Model info": "模型信息", "Configuration": "参数配置",
    "Context size": "上下文大小", "GPU layers (0=CPU, -1=all)": "GPU 层数 (0=CPU, -1=全部)",
    "Threads": "线程数", "Temperature": "温度", "Top P": "Top P",
    "Max tokens": "最大 Token 数", "Repeat penalty": "重复惩罚",
    "System prompt": "系统提示词", "Chat": "对话", "Send": "发送",
    "Generating…": "正在生成…", "Stopped.": "已停止。",
    "Model unloaded": "模型已卸载", "No model selected": "未选择模型",
    "Quantization": "量化格式", "Context length": "上下文长度",
    "Architecture": "架构", "Layers": "层数", "Vocabulary": "词表大小",
    "Estimated RAM": "预估内存", "Save chat": "保存对话",
    "Chat saved to": "对话已保存到", "Recent models": "最近模型",
    "You": "你", "Assistant": "助手", "Your message": "输入消息…",
    "Chat is empty": "对话为空", "Model ready": "模型就绪",
    "First load can take a minute…": "首次加载可能需要一分钟…",
}

_ES = {
    "General": "General", "System": "Sistema", "Files": "Archivos", "Text": "Texto",
    "Security": "Seguridad", "Media": "Multimedia", "Calc & Time": "Cálculo y hora",
    "Productivity": "Productividad", "Developer": "Desarrollo", "APIs": "APIs",
    "Data": "Datos", "Dashboard": "Panel", "Settings": "Ajustes", "About": "Acerca de",
    "Search tools…": "Buscar herramientas…", "Favorites": "Favoritos",
    "Recent": "Recientes", "Language": "Idioma", "Theme": "Tema", "Dark": "Oscuro",
    "Light": "Claro", "Run": "Ejecutar", "Copy": "Copiar", "Clear": "Limpiar",
    "Save": "Guardar", "Load": "Cargar", "Delete": "Eliminar", "Browse": "Examinar",
    "Close": "Cerrar", "Add": "Añadir", "Refresh": "Actualizar", "Start": "Iniciar",
    "Stop": "Detener", "Reset": "Reiniciar", "Export": "Exportar", "Import": "Importar",
    "Generate": "Generar", "Convert": "Convertir", "Loading…": "Cargando…",
    "Done": "Listo", "Failed": "Error", "Copied to clipboard": "Copiado al portapapeles",
    "Result": "Resultado", "Input": "Entrada", "Output": "Salida", "Options": "Opciones",
    "System Information": "Información del sistema", "Process Manager": "Procesos",
    "Network Info": "Red", "File Organizer": "Organizador de archivos",
    "Duplicate Finder": "Buscar duplicados", "Bulk Rename": "Renombrado masivo",
    "Checksum": "Suma de verificación", "Text Counter": "Contador de texto",
    "Text Transform": "Transformar texto", "Text Diff": "Comparar textos",
    "Password Generator": "Generador de contraseñas", "Color Converter": "Conversor de color",
    "QR Code": "Código QR", "Image Tools": "Herramientas de imagen",
    "Calculator": "Calculadora", "Unit Converter": "Conversor de unidades",
    "Date & Time": "Fecha y hora", "Timer": "Temporizador", "Todo List": "Tareas",
    "Notes": "Notas", "Backup": "Copia de seguridad", "Weather": "Clima",
    "Currency": "Divisas", "Translate": "Traducir", "News": "Noticias",
    "Time Zones": "Zonas horarias", "Fake Data": "Datos de prueba",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "Desplázate para ver más ↓",
    "{n} tools found": "Se encontraron {n} herramientas",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "LLM local",
    "Run GGUF models locally — 100% offline": "Ejecuta modelos GGUF en local — 100% sin conexión",
    "Model": "Modelo", "GGUF model file": "Archivo GGUF",
    "Load model": "Cargar modelo", "Unload model": "Liberar modelo",
    "Model info": "Info del modelo", "Configuration": "Parámetros",
    "Context size": "Tamaño de contexto", "GPU layers (0=CPU, -1=all)": "Capas GPU (0=CPU, -1=todas)",
    "Threads": "Hilos", "Temperature": "Temperatura", "Top P": "Top P",
    "Max tokens": "Tokens máx.", "Repeat penalty": "Penalización por repetición",
    "System prompt": "Prompt del sistema", "Chat": "Chat", "Send": "Enviar",
    "Generating…": "Generando…", "Stopped.": "Detenido.",
    "Model unloaded": "Modelo liberado", "No model selected": "Sin modelo seleccionado",
    "Quantization": "Cuantización", "Context length": "Longitud de contexto",
    "Architecture": "Arquitectura", "Layers": "Capas", "Vocabulary": "Vocabulario",
    "Estimated RAM": "RAM estimada", "Save chat": "Guardar chat",
    "Chat saved to": "Chat guardado en", "Recent models": "Modelos recientes",
    "You": "Tú", "Assistant": "Asistente", "Your message": "Tu mensaje",
    "Chat is empty": "El chat está vacío", "Model ready": "Modelo listo",
    "First load can take a minute…": "La primera carga puede tardar un minuto…",
}

_FR = {
    "General": "Général", "System": "Système", "Files": "Fichiers", "Text": "Texte",
    "Security": "Sécurité", "Media": "Médias", "Calc & Time": "Calcul et heure",
    "Productivity": "Productivité", "Developer": "Développeur", "APIs": "APIs",
    "Data": "Données", "Dashboard": "Tableau de bord", "Settings": "Paramètres",
    "About": "À propos", "Search tools…": "Rechercher…", "Favorites": "Favoris",
    "Recent": "Récents", "Language": "Langue", "Theme": "Thème", "Dark": "Sombre",
    "Light": "Clair", "Run": "Exécuter", "Copy": "Copier", "Clear": "Effacer",
    "Save": "Enregistrer", "Load": "Charger", "Delete": "Supprimer",
    "Browse": "Parcourir", "Close": "Fermer", "Add": "Ajouter",
    "Refresh": "Actualiser", "Start": "Démarrer", "Stop": "Arrêter",
    "Reset": "Réinitialiser", "Export": "Exporter", "Import": "Importer",
    "Generate": "Générer", "Convert": "Convertir", "Loading…": "Chargement…",
    "Done": "Terminé", "Failed": "Échec", "Copied to clipboard": "Copié",
    "Result": "Résultat", "Input": "Entrée", "Output": "Sortie", "Options": "Options",
    "System Information": "Informations système", "Process Manager": "Processus",
    "Network Info": "Réseau", "File Organizer": "Organisateur de fichiers",
    "Duplicate Finder": "Doublons", "Bulk Rename": "Renommage en masse",
    "Checksum": "Somme de contrôle", "Text Counter": "Compteur de texte",
    "Text Diff": "Comparer deux textes", "Password Generator": "Générateur de mots de passe",
    "Color Converter": "Convertisseur de couleurs", "QR Code": "Code QR",
    "Image Tools": "Outils d'image", "Calculator": "Calculatrice",
    "Unit Converter": "Convertisseur d'unités", "Date & Time": "Date et heure",
    "Timer": "Minuteur", "Todo List": "Tâches", "Notes": "Notes",
    "Backup": "Sauvegarde", "Weather": "Météo", "Currency": "Devises",
    "Translate": "Traduire", "News": "Actualités", "Time Zones": "Fuseaux horaires",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "Faites défiler pour voir plus ↓",
    "{n} tools found": "{n} outils trouvés",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "LLM local",
    "Run GGUF models locally — 100% offline": "Exécutez des modèles GGUF en local — 100 % hors ligne",
    "Model": "Modèle", "GGUF model file": "Fichier GGUF",
    "Load model": "Charger le modèle", "Unload model": "Décharger le modèle",
    "Model info": "Infos du modèle", "Configuration": "Réglages",
    "Context size": "Taille du contexte", "GPU layers (0=CPU, -1=all)": "Couches GPU (0=CPU, -1=tout)",
    "Threads": "Threads", "Temperature": "Température", "Top P": "Top P",
    "Max tokens": "Tokens max", "Repeat penalty": "Pénalité de répétition",
    "System prompt": "Prompt système", "Chat": "Discussion", "Send": "Envoyer",
    "Generating…": "Génération…", "Stopped.": "Arrêté.",
    "Model unloaded": "Modèle déchargé", "No model selected": "Aucun modèle sélectionné",
    "Quantization": "Quantification", "Context length": "Longueur du contexte",
    "Architecture": "Architecture", "Layers": "Couches", "Vocabulary": "Vocabulaire",
    "Estimated RAM": "RAM estimée", "Save chat": "Sauver la discussion",
    "Chat saved to": "Discussion enregistrée dans", "Recent models": "Modèles récents",
    "You": "Vous", "Assistant": "Assistant", "Your message": "Votre message",
    "Chat is empty": "La discussion est vide", "Model ready": "Modèle prêt",
    "First load can take a minute…": "Le premier chargement peut prendre une minute…",
}

_RU = {
    "General": "Общее", "System": "Система", "Files": "Файлы", "Text": "Текст",
    "Security": "Безопасность", "Media": "Медиа", "Calc & Time": "Расчёты и время",
    "Productivity": "Продуктивность", "Developer": "Разработка", "APIs": "API",
    "Data": "Данные", "Dashboard": "Панель", "Settings": "Настройки",
    "About": "О программе", "Search tools…": "Поиск инструментов…",
    "Favorites": "Избранное", "Recent": "Недавние", "Language": "Язык",
    "Theme": "Тема", "Dark": "Тёмная", "Light": "Светлая", "Run": "Запустить",
    "Copy": "Копировать", "Clear": "Очистить", "Save": "Сохранить",
    "Load": "Загрузить", "Delete": "Удалить", "Browse": "Обзор", "Close": "Закрыть",
    "Add": "Добавить", "Refresh": "Обновить", "Start": "Старт", "Stop": "Стоп",
    "Reset": "Сброс", "Export": "Экспорт", "Import": "Импорт",
    "Generate": "Создать", "Convert": "Конвертировать", "Loading…": "Загрузка…",
    "Done": "Готово", "Failed": "Ошибка", "Copied to clipboard": "Скопировано",
    "Result": "Результат", "Input": "Ввод", "Output": "Вывод", "Options": "Опции",
    "System Information": "Сведения о системе", "Process Manager": "Процессы",
    "Network Info": "Сеть", "File Organizer": "Органайзер файлов",
    "Duplicate Finder": "Поиск дубликатов", "Bulk Rename": "Массовое переименование",
    "Checksum": "Контрольная сумма", "Text Counter": "Счётчик текста",
    "Password Generator": "Генератор паролей", "Color Converter": "Конвертер цветов",
    "QR Code": "QR-код", "Image Tools": "Работа с изображениями",
    "Calculator": "Калькулятор", "Unit Converter": "Конвертер единиц",
    "Date & Time": "Дата и время", "Timer": "Таймер", "Todo List": "Задачи",
    "Notes": "Заметки", "Backup": "Резервная копия", "Weather": "Погода",
    "Currency": "Валюты", "Translate": "Перевод", "News": "Новости",
    "Time Zones": "Часовые пояса",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "Прокрутите вниз, чтобы увидеть больше ↓",
    "{n} tools found": "Найдено инструментов: {n}",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "Локальная LLM",
    "Run GGUF models locally — 100% offline": "Запуск GGUF-моделей локально — 100% офлайн",
    "Model": "Модель", "GGUF model file": "GGUF-файл",
    "Load model": "Загрузить модель", "Unload model": "Выгрузить модель",
    "Model info": "О модели", "Configuration": "Параметры",
    "Context size": "Размер контекста", "GPU layers (0=CPU, -1=all)": "Слои GPU (0=CPU, -1=все)",
    "Threads": "Потоки", "Temperature": "Температура", "Top P": "Top P",
    "Max tokens": "Макс. токенов", "Repeat penalty": "Штраф за повтор",
    "System prompt": "Системный промпт", "Chat": "Чат", "Send": "Отправить",
    "Generating…": "Генерация…", "Stopped.": "Остановлено.",
    "Model unloaded": "Модель выгружена", "No model selected": "Модель не выбрана",
    "Quantization": "Квантование", "Context length": "Длина контекста",
    "Architecture": "Архитектура", "Layers": "Слои", "Vocabulary": "Словарь",
    "Estimated RAM": "Оценка ОЗУ", "Save chat": "Сохранить чат",
    "Chat saved to": "Чат сохранён в", "Recent models": "Недавние модели",
    "You": "Вы", "Assistant": "Ассистент", "Your message": "Ваше сообщение",
    "Chat is empty": "Чат пуст", "Model ready": "Модель готова",
    "First load can take a minute…": "Первая загрузка может занять минуту…",
}

_PT = {
    "General": "Geral", "System": "Sistema", "Files": "Arquivos", "Text": "Texto",
    "Security": "Segurança", "Media": "Mídia", "Calc & Time": "Cálculo e tempo",
    "Productivity": "Produtividade", "Developer": "Desenvolvedor", "APIs": "APIs",
    "Data": "Dados", "Dashboard": "Painel", "Settings": "Configurações",
    "About": "Sobre", "Search tools…": "Buscar ferramentas…", "Favorites": "Favoritos",
    "Recent": "Recentes", "Language": "Idioma", "Theme": "Tema", "Dark": "Escuro",
    "Light": "Claro", "Run": "Executar", "Copy": "Copiar", "Clear": "Limpar",
    "Save": "Salvar", "Load": "Carregar", "Delete": "Excluir", "Browse": "Procurar",
    "Close": "Fechar", "Add": "Adicionar", "Refresh": "Atualizar", "Start": "Iniciar",
    "Stop": "Parar", "Reset": "Redefinir", "Export": "Exportar", "Import": "Importar",
    "Generate": "Gerar", "Convert": "Converter", "Loading…": "Carregando…",
    "Done": "Concluído", "Failed": "Falhou", "Copied to clipboard": "Copiado",
    "Result": "Resultado", "Input": "Entrada", "Output": "Saída", "Options": "Opções",
    "System Information": "Informações do sistema", "Process Manager": "Processos",
    "Network Info": "Rede", "Calculator": "Calculadora", "Timer": "Cronômetro",
    "Todo List": "Tarefas", "Notes": "Notas", "Weather": "Clima",
    "Currency": "Moedas", "Translate": "Traduzir", "News": "Notícias",
    "Password Generator": "Gerador de senhas", "QR Code": "Código QR",
    "Time Zones": "Fusos horários", "Date & Time": "Data e hora",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "Role para ver mais ↓",
    "{n} tools found": "{n} ferramentas encontradas",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "LLM local",
    "Run GGUF models locally — 100% offline": "Executa modelos GGUF localmente — 100% offline",
    "Model": "Modelo", "GGUF model file": "Arquivo GGUF",
    "Load model": "Carregar modelo", "Unload model": "Liberar modelo",
    "Model info": "Info do modelo", "Configuration": "Parâmetros",
    "Context size": "Tamanho do contexto", "GPU layers (0=CPU, -1=all)": "Camadas GPU (0=CPU, -1=todas)",
    "Threads": "Threads", "Temperature": "Temperatura", "Top P": "Top P",
    "Max tokens": "Tokens máx.", "Repeat penalty": "Penalidade de repetição",
    "System prompt": "Prompt do sistema", "Chat": "Conversa", "Send": "Enviar",
    "Generating…": "Gerando…", "Stopped.": "Parado.",
    "Model unloaded": "Modelo liberado", "No model selected": "Nenhum modelo selecionado",
    "Quantization": "Quantização", "Context length": "Comprimento do contexto",
    "Architecture": "Arquitetura", "Layers": "Camadas", "Vocabulary": "Vocabulário",
    "Estimated RAM": "RAM estimada", "Save chat": "Salvar conversa",
    "Chat saved to": "Conversa salva em", "Recent models": "Modelos recentes",
    "You": "Você", "Assistant": "Assistente", "Your message": "Sua mensagem",
    "Chat is empty": "A conversa está vazia", "Model ready": "Modelo pronto",
    "First load can take a minute…": "O primeiro carregamento pode levar um minuto…",
}

_HI = {
    "General": "सामान्य", "System": "सिस्टम", "Files": "फ़ाइलें", "Text": "पाठ",
    "Security": "सुरक्षा", "Media": "मीडिया", "Calc & Time": "गणना और समय",
    "Productivity": "उत्पादकता", "Developer": "डेवलपर", "APIs": "एपीआई",
    "Data": "डेटा", "Dashboard": "डैशबोर्ड", "Settings": "सेटिंग्स",
    "About": "परिचय", "Search tools…": "उपकरण खोजें…", "Favorites": "पसंदीदा",
    "Recent": "हाल के", "Language": "भाषा", "Theme": "थीम", "Dark": "गहरा",
    "Light": "हल्का", "Run": "चलाएँ", "Copy": "कॉपी", "Clear": "साफ़ करें",
    "Save": "सहेजें", "Load": "लोड", "Delete": "हटाएँ", "Browse": "ब्राउज़",
    "Close": "बंद करें", "Add": "जोड़ें", "Refresh": "ताज़ा करें",
    "Start": "शुरू", "Stop": "रोकें", "Reset": "रीसेट", "Export": "निर्यात",
    "Import": "आयात", "Generate": "बनाएँ", "Convert": "बदलें",
    "Loading…": "लोड हो रहा है…", "Done": "हो गया", "Failed": "विफल",
    "Result": "परिणाम", "Input": "इनपुट", "Output": "आउटपुट",
    "Calculator": "कैलकुलेटर", "Timer": "टाइमर", "Notes": "नोट्स",
    "Todo List": "कार्य सूची", "Weather": "मौसम", "News": "समाचार",
    "Translate": "अनुवाद", "QR Code": "क्यूआर कोड", "Time Zones": "समय क्षेत्र",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "और देखने के लिए नीचे स्क्रॉल करें ↓",
    "{n} tools found": "{n} उपकरण मिले",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "लोकल LLM",
    "Run GGUF models locally — 100% offline": "GGUF मॉडल लोकल चलाएँ — 100% ऑफ़लाइन",
    "Model": "मॉडल", "GGUF model file": "GGUF फ़ाइल",
    "Load model": "मॉडल लोड करें", "Unload model": "मॉडल हटाएँ",
    "Model info": "मॉडल जानकारी", "Configuration": "कॉन्फ़िगरेशन",
    "Context size": "कॉन्टेक्स्ट आकार", "GPU layers (0=CPU, -1=all)": "GPU लेयर (0=CPU, -1=सभी)",
    "Threads": "थ्रेड", "Temperature": "टेम्परेचर", "Top P": "Top P",
    "Max tokens": "अधिकतम टोकन", "Repeat penalty": "रिपीट पेनल्टी",
    "System prompt": "सिस्टम प्रॉम्प्ट", "Chat": "चैट", "Send": "भेजें",
    "Generating…": "जनरेट हो रहा है…", "Stopped.": "रुक गया।",
    "Model unloaded": "मॉडल हटा दिया", "No model selected": "कोई मॉडल चयनित नहीं",
    "Quantization": "क्वांटिज़ेशन", "Context length": "कॉन्टेक्स्ट लंबाई",
    "Architecture": "आर्किटेक्चर", "Layers": "लेयर", "Vocabulary": "वोकैबुलरी",
    "Estimated RAM": "अनुमानित RAM", "Save chat": "चैट सहेजें",
    "Chat saved to": "चैट सहेजी गई:", "Recent models": "हाल के मॉडल",
    "You": "आप", "Assistant": "असिस्टेंट", "Your message": "आपका संदेश",
    "Chat is empty": "चैट खाली है", "Model ready": "मॉडल तैयार",
    "First load can take a minute…": "पहली लोड में एक मिनट लग सकता है…",
}

_BN = {
    "General": "সাধারণ", "System": "সিস্টেম", "Files": "ফাইল", "Text": "টেক্সট",
    "Security": "নিরাপত্তা", "Media": "মিডিয়া", "Calc & Time": "হিসাব ও সময়",
    "Productivity": "উৎপাদনশীলতা", "Developer": "ডেভেলপার", "APIs": "এপিআই",
    "Data": "ডেটা", "Dashboard": "ড্যাশবোর্ড", "Settings": "সেটিংস",
    "About": "সম্পর্কে", "Search tools…": "টুল খুঁজুন…", "Favorites": "প্রিয়",
    "Recent": "সাম্প্রতিক", "Language": "ভাষা", "Theme": "থিম", "Dark": "গাঢ়",
    "Light": "হালকা", "Run": "চালান", "Copy": "কপি", "Clear": "মুছুন",
    "Save": "সংরক্ষণ", "Load": "লোড", "Delete": "মুছে ফেলুন", "Browse": "ব্রাউজ",
    "Close": "বন্ধ", "Add": "যোগ", "Refresh": "রিফ্রেশ", "Start": "শুরু",
    "Stop": "থামান", "Reset": "রিসেট", "Export": "রপ্তানি", "Import": "আমদানি",
    "Generate": "তৈরি", "Convert": "রূপান্তর", "Loading…": "লোড হচ্ছে…",
    "Done": "সম্পন্ন", "Failed": "ব্যর্থ", "Result": "ফলাফল",
    "Calculator": "ক্যালকুলেটর", "Timer": "টাইমার", "Notes": "নোট",
    "Todo List": "কাজের তালিকা", "Weather": "আবহাওয়া", "News": "সংবাদ",
    "Translate": "অনুবাদ", "QR Code": "কিউআর কোড", "Time Zones": "সময় অঞ্চল",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "আরও দেখতে নিচে স্ক্রল করুন ↓",
    "{n} tools found": "{n}টি টুল পাওয়া গেছে",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "লোকাল LLM",
    "Run GGUF models locally — 100% offline": "GGUF মডেল লোকালি চালান — ১০০% অফলাইন",
    "Model": "মডেল", "GGUF model file": "GGUF ফাইল",
    "Load model": "মডেল লোড করুন", "Unload model": "মডেল সরান",
    "Model info": "মডেল তথ্য", "Configuration": "কনফিগারেশন",
    "Context size": "কনটেক্সট সাইজ", "GPU layers (0=CPU, -1=all)": "GPU লেয়ার (0=CPU, -1=সব)",
    "Threads": "থ্রেড", "Temperature": "টেম্পারেচার", "Top P": "Top P",
    "Max tokens": "সর্বোচ্চ টোকেন", "Repeat penalty": "রিপিট পেনাল্টি",
    "System prompt": "সিস্টেম প্রম্পট", "Chat": "চ্যাট", "Send": "পাঠান",
    "Generating…": "জেনারেট হচ্ছে…", "Stopped.": "থামানো হয়েছে।",
    "Model unloaded": "মডেল সরানো হয়েছে", "No model selected": "কোনো মডেল নির্বাচিত নয়",
    "Quantization": "কোয়ান্টাইজেশন", "Context length": "কনটেক্সট দৈর্ঘ্য",
    "Architecture": "আর্কিটেকচার", "Layers": "লেয়ার", "Vocabulary": "ভোকাবুলারি",
    "Estimated RAM": "আনুমানিক RAM", "Save chat": "চ্যাট সংরক্ষণ",
    "Chat saved to": "চ্যাট সংরক্ষিত:", "Recent models": "সাম্প্রতিক মডেল",
    "You": "আপনি", "Assistant": "অ্যাসিস্ট্যান্ট", "Your message": "আপনার বার্তা",
    "Chat is empty": "চ্যাট খালি", "Model ready": "মডেল প্রস্তুত",
    "First load can take a minute…": "প্রথম লোডে এক মিনিট লাগতে পারে…",
}

_UR = {
    "General": "عام", "System": "سسٹم", "Files": "فائلیں", "Text": "متن",
    "Security": "سیکیورٹی", "Media": "میڈیا", "Calc & Time": "حساب و وقت",
    "Productivity": "پیداواری", "Developer": "ڈویلپر", "APIs": "اے پی آئی",
    "Data": "ڈیٹا", "Dashboard": "ڈیش بورڈ", "Settings": "ترتیبات",
    "About": "تعارف", "Search tools…": "ٹولز تلاش کریں…", "Favorites": "پسندیدہ",
    "Recent": "حالیہ", "Language": "زبان", "Theme": "تھیم", "Dark": "گہرا",
    "Light": "ہلکا", "Run": "چلائیں", "Copy": "کاپی", "Clear": "صاف کریں",
    "Save": "محفوظ", "Load": "لوڈ", "Delete": "حذف", "Browse": "منتخب کریں",
    "Close": "بند", "Add": "شامل", "Refresh": "تازہ", "Start": "شروع",
    "Stop": "روکیں", "Reset": "ری سیٹ", "Export": "برآمد", "Import": "درآمد",
    "Generate": "بنائیں", "Convert": "تبدیل", "Loading…": "لوڈ ہو رہا ہے…",
    "Done": "مکمل", "Failed": "ناکام", "Result": "نتیجہ",
    "Calculator": "کیلکولیٹر", "Timer": "ٹائمر", "Notes": "نوٹس",
    "Todo List": "فہرست کام", "Weather": "موسم", "News": "خبریں",
    "Translate": "ترجمہ", "QR Code": "کیو آر کوڈ", "Time Zones": "ٹائم زونز",
    # مفاتيح v4.0 Phase 1
    "Scroll for more ↓": "مزید دیکھنے کے لیے نیچے اسکرول کریں ↓",
    "{n} tools found": "{n} ٹولز مل گئے",
    # v4.1 — Local LLM (GGUF)
    "Local LLM": "لوکل LLM",
    "Run GGUF models locally — 100% offline": "GGUF ماڈلز لوکل چلائیں — 100% آف لائن",
    "Model": "ماڈل", "GGUF model file": "GGUF فائل",
    "Load model": "ماڈل لوڈ کریں", "Unload model": "ماڈل ہٹائیں",
    "Model info": "ماڈل کی معلومات", "Configuration": "پیرامیٹرز",
    "Context size": "کانٹیکسٹ سائز", "GPU layers (0=CPU, -1=all)": "GPU لیئرز (0=CPU، -1=سب)",
    "Threads": "تھریڈز", "Temperature": "ٹمپریچر", "Top P": "Top P",
    "Max tokens": "زیادہ سے زیادہ ٹوکن", "Repeat penalty": "ریپیٹ پینلٹی",
    "System prompt": "سسٹم پرامپٹ", "Chat": "چیٹ", "Send": "بھیجیں",
    "Generating…": "تولید جاری ہے…", "Stopped.": "روک دیا گیا۔",
    "Model unloaded": "ماڈل ہٹا دیا گیا", "No model selected": "کوئی ماڈل منتخب نہیں",
    "Quantization": "کوانٹائزیشن", "Context length": "کانٹیکسٹ لمبائی",
    "Architecture": "آرکیٹیکچر", "Layers": "لیئرز", "Vocabulary": "وکیبولری",
    "Estimated RAM": "تخمینی RAM", "Save chat": "چیٹ محفوظ کریں",
    "Chat saved to": "چیٹ محفوظ ہوگئی:", "Recent models": "حالیہ ماڈلز",
    "You": "آپ", "Assistant": "اسسٹنٹ", "Your message": "آپ کا پیغام",
    "Chat is empty": "چیٹ خالی ہے", "Model ready": "ماڈل تیار ہے",
    "First load can take a minute…": "پہلی لوڈ میں ایک منٹ لگ سکتا ہے…",
}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {}, "ar": _AR, "zh": _ZH, "es": _ES, "fr": _FR,
    "ru": _RU, "pt": _PT, "hi": _HI, "bn": _BN, "ur": _UR,
}

# ✦ v4.2: مفاتيح نظام الإضافات — تُدمج هنا بدل تعديل كل قاموس لغة يدويًا
_PLUG_T: Dict[str, Dict[str, str]] = {
    "ar": {
        "Plugins": "الإضافات",
        "{n} plugins loaded": "تم تحميل {n} إضافة",
        "Plugin error: {name}": "خطأ في الإضافة: {name}",
        "Plugin crashed": "تعطّلت الإضافة",
    },
    "zh": {
        "Plugins": "插件",
        "{n} plugins loaded": "已加载 {n} 个插件",
        "Plugin error: {name}": "插件错误：{name}",
        "Plugin crashed": "插件已崩溃",
    },
    "es": {
        "Plugins": "Complementos",
        "{n} plugins loaded": "{n} complemento(s) cargado(s)",
        "Plugin error: {name}": "Error del complemento: {name}",
        "Plugin crashed": "El complemento falló",
    },
    "fr": {
        "Plugins": "Extensions",
        "{n} plugins loaded": "{n} extension(s) chargée(s)",
        "Plugin error: {name}": "Erreur du plugin : {name}",
        "Plugin crashed": "Le plugin a planté",
    },
    "ru": {
        "Plugins": "Плагины",
        "{n} plugins loaded": "Загружено плагинов: {n}",
        "Plugin error: {name}": "Ошибка плагина: {name}",
        "Plugin crashed": "Сбой плагина",
    },
    "pt": {
        "Plugins": "Plugins",
        "{n} plugins loaded": "{n} plugin(s) carregado(s)",
        "Plugin error: {name}": "Erro do plugin: {name}",
        "Plugin crashed": "O plugin falhou",
    },
    "hi": {
        "Plugins": "प्लगइन्स",
        "{n} plugins loaded": "{n} प्लगइन लोड हुए",
        "Plugin error: {name}": "प्लगइन त्रुटि: {name}",
        "Plugin crashed": "प्लगइन क्रैश हो गया",
    },
    "bn": {
        "Plugins": "প্লাগইন",
        "{n} plugins loaded": "{n}টি প্লাগইন লোড হয়েছে",
        "Plugin error: {name}": "প্লাগইন ত্রুটি: {name}",
        "Plugin crashed": "প্লাগইন ক্র্যাশ করেছে",
    },
    "ur": {
        "Plugins": "پلگ انز",
        "{n} plugins loaded": "{n} پلگ انز لوڈ ہوئے",
        "Plugin error: {name}": "پلگ ان میں خرابی: {name}",
        "Plugin crashed": "پلگ ان کراش ہو گیا",
    },
}
for _l, _m in _PLUG_T.items():
    TRANSLATIONS.setdefault(_l, {}).update(_m)
del _l, _m

# ✦ v4.3: مفاتيح محرّكات LLM الخلفية (خادم llama.cpp) — تُدمج بنفس أسلوب الإضافات
_LLM_T: Dict[str, Dict[str, str]] = {
    "ar": {
        "Backend": "المحرّك الخلفي",
        "In-process (llama-cpp-python)": "داخلي (llama-cpp-python)",
        "llama.cpp Server (running)": "خادم llama.cpp (يعمل حاليًا)",
        "llama.cpp Server (auto-start)": "خادم llama.cpp (تشغيل تلقائي)",
        "Server URL": "عنوان الخادم",
        "llama-server executable": "ملف llama-server التنفيذي",
        "Port": "المنفذ",
        "Server ready": "الخادم جاهز",
        "Server not responding": "الخادم لا يستجيب",
        "Failed to start llama-server": "فشل تشغيل llama-server",
        "Install help": "مساعدة التثبيت",
        "Install help copied": "نُسخت مساعدة التثبيت",
        "Connecting…": "جارٍ الاتصال…",
    },
    "zh": {
        "Backend": "后端",
        "In-process (llama-cpp-python)": "进程内 (llama-cpp-python)",
        "llama.cpp Server (running)": "llama.cpp 服务器（已运行）",
        "llama.cpp Server (auto-start)": "llama.cpp 服务器（自动启动）",
        "Server URL": "服务器地址",
        "llama-server executable": "llama-server 可执行文件",
        "Port": "端口",
        "Server ready": "服务器已就绪",
        "Server not responding": "服务器无响应",
        "Failed to start llama-server": "启动 llama-server 失败",
        "Install help": "安装帮助",
        "Install help copied": "安装帮助已复制",
        "Connecting…": "连接中…",
    },
    "es": {
        "Backend": "Motor",
        "In-process (llama-cpp-python)": "Interno (llama-cpp-python)",
        "llama.cpp Server (running)": "Servidor llama.cpp (en ejecución)",
        "llama.cpp Server (auto-start)": "Servidor llama.cpp (inicio automático)",
        "Server URL": "URL del servidor",
        "llama-server executable": "Ejecutable de llama-server",
        "Port": "Puerto",
        "Server ready": "Servidor listo",
        "Server not responding": "El servidor no responde",
        "Failed to start llama-server": "No se pudo iniciar llama-server",
        "Install help": "Ayuda de instalación",
        "Install help copied": "Ayuda de instalación copiada",
        "Connecting…": "Conectando…",
    },
    "fr": {
        "Backend": "Moteur",
        "In-process (llama-cpp-python)": "Intégré (llama-cpp-python)",
        "llama.cpp Server (running)": "Serveur llama.cpp (en cours)",
        "llama.cpp Server (auto-start)": "Serveur llama.cpp (démarrage auto)",
        "Server URL": "URL du serveur",
        "llama-server executable": "Exécutable llama-server",
        "Port": "Port",
        "Server ready": "Serveur prêt",
        "Server not responding": "Le serveur ne répond pas",
        "Failed to start llama-server": "Échec du démarrage de llama-server",
        "Install help": "Aide à l'installation",
        "Install help copied": "Aide à l'installation copiée",
        "Connecting…": "Connexion…",
    },
    "ru": {
        "Backend": "Движок",
        "In-process (llama-cpp-python)": "Встроенный (llama-cpp-python)",
        "llama.cpp Server (running)": "Сервер llama.cpp (запущен)",
        "llama.cpp Server (auto-start)": "Сервер llama.cpp (автозапуск)",
        "Server URL": "URL сервера",
        "llama-server executable": "Исполняемый файл llama-server",
        "Port": "Порт",
        "Server ready": "Сервер готов",
        "Server not responding": "Сервер не отвечает",
        "Failed to start llama-server": "Не удалось запустить llama-server",
        "Install help": "Справка по установке",
        "Install help copied": "Справка скопирована",
        "Connecting…": "Подключение…",
    },
    "pt": {
        "Backend": "Motor",
        "In-process (llama-cpp-python)": "Interno (llama-cpp-python)",
        "llama.cpp Server (running)": "Servidor llama.cpp (em execução)",
        "llama.cpp Server (auto-start)": "Servidor llama.cpp (início automático)",
        "Server URL": "URL do servidor",
        "llama-server executable": "Executável do llama-server",
        "Port": "Porta",
        "Server ready": "Servidor pronto",
        "Server not responding": "O servidor não responde",
        "Failed to start llama-server": "Falha ao iniciar o llama-server",
        "Install help": "Ajuda de instalação",
        "Install help copied": "Ajuda de instalação copiada",
        "Connecting…": "Conectando…",
    },
    "hi": {
        "Backend": "बैकएंड",
        "In-process (llama-cpp-python)": "इन-प्रोसेस (llama-cpp-python)",
        "llama.cpp Server (running)": "llama.cpp सर्वर (चल रहा है)",
        "llama.cpp Server (auto-start)": "llama.cpp सर्वर (ऑटो-स्टार्ट)",
        "Server URL": "सर्वर URL",
        "llama-server executable": "llama-server एक्ज़ीक्यूटेबल",
        "Port": "पोर्ट",
        "Server ready": "सर्वर तैयार है",
        "Server not responding": "सर्वर प्रतिक्रिया नहीं दे रहा",
        "Failed to start llama-server": "llama-server शुरू करने में विफल",
        "Install help": "इंस्टॉल सहायता",
        "Install help copied": "इंस्टॉल सहायता कॉपी हो गई",
        "Connecting…": "कनेक्ट हो रहा है…",
    },
    "bn": {
        "Backend": "ব্যাকএন্ড",
        "In-process (llama-cpp-python)": "ইন-প্রসেস (llama-cpp-python)",
        "llama.cpp Server (running)": "llama.cpp সার্ভার (চলছে)",
        "llama.cpp Server (auto-start)": "llama.cpp সার্ভার (অটো-স্টার্ট)",
        "Server URL": "সার্ভার URL",
        "llama-server executable": "llama-server এক্সিকিউটেবল",
        "Port": "পোর্ট",
        "Server ready": "সার্ভার প্রস্তুত",
        "Server not responding": "সার্ভার সাড়া দিচ্ছে না",
        "Failed to start llama-server": "llama-server চালু করতে ব্যর্থ",
        "Install help": "ইনস্টল সহায়তা",
        "Install help copied": "ইনস্টল সহায়তা কপি হয়েছে",
        "Connecting…": "সংযোগ করা হচ্ছে…",
    },
    "ur": {
        "Backend": "بیک اینڈ",
        "In-process (llama-cpp-python)": "ان پروسس (llama-cpp-python)",
        "llama.cpp Server (running)": "llama.cpp سرور (چل رہا ہے)",
        "llama.cpp Server (auto-start)": "llama.cpp سرور (خودکار آغاز)",
        "Server URL": "سرور URL",
        "llama-server executable": "llama-server ایگزیکیوٹبل",
        "Port": "پورٹ",
        "Server ready": "سرور تیار ہے",
        "Server not responding": "سرور جواب نہیں دے رہا",
        "Failed to start llama-server": "llama-server شروع کرنے میں ناکامی",
        "Install help": "انسٹالیشن مدد",
        "Install help copied": "انسٹالیشن مدد کاپی ہوگئی",
        "Connecting…": "جڑ رہا ہے…",
    },
}
for _l, _m in _LLM_T.items():
    TRANSLATIONS.setdefault(_l, {}).update(_m)
del _l, _m

# ✦ v4.4: مفاتيح التنزيل التلقائي (llama-server + موديلات GGUF) — بنفس أسلوب _LLM_T
_LLMDL_T: Dict[str, Dict[str, str]] = {
    "ar": {
        "Build": "النسخة",
        "Auto (recommended)": "تلقائي (موصى به)",
        "CPU build": "نسخة CPU",
        "CUDA build (NVIDIA)": "نسخة CUDA (NVIDIA)",
        "Vulkan build": "نسخة Vulkan",
        "Download llama-server": "تنزيل llama-server",
        "Download model": "تنزيل موديل",
        "Model": "الموديل",
        "Fetching release info…": "جلب معلومات الإصدار…",
        "Extracting…": "جارٍ الاستخراج…",
        "Starting download…": "جارٍ بدء التنزيل…",
        "Download complete": "اكتمل التنزيل",
        "Download failed": "فشل التنزيل",
        "Canceled": "أُلغي",
        "Saved to": "حُفظ في",
        "Model downloaded": "تم تنزيل الموديل",
    },
    "zh": {
        "Build": "构建版本",
        "Auto (recommended)": "自动（推荐）",
        "CPU build": "CPU 构建",
        "CUDA build (NVIDIA)": "CUDA 构建（NVIDIA）",
        "Vulkan build": "Vulkan 构建",
        "Download llama-server": "下载 llama-server",
        "Download model": "下载模型",
        "Model": "模型",
        "Fetching release info…": "获取发布信息…",
        "Extracting…": "解压中…",
        "Starting download…": "开始下载…",
        "Download complete": "下载完成",
        "Download failed": "下载失败",
        "Canceled": "已取消",
        "Saved to": "已保存到",
        "Model downloaded": "模型已下载",
    },
    "es": {
        "Build": "Versión",
        "Auto (recommended)": "Automático (recomendado)",
        "CPU build": "Versión CPU",
        "CUDA build (NVIDIA)": "Versión CUDA (NVIDIA)",
        "Vulkan build": "Versión Vulkan",
        "Download llama-server": "Descargar llama-server",
        "Download model": "Descargar modelo",
        "Model": "Modelo",
        "Fetching release info…": "Obteniendo información de la versión…",
        "Extracting…": "Extrayendo…",
        "Starting download…": "Iniciando descarga…",
        "Download complete": "Descarga completa",
        "Download failed": "Descarga fallida",
        "Canceled": "Cancelado",
        "Saved to": "Guardado en",
        "Model downloaded": "Modelo descargado",
    },
    "fr": {
        "Build": "Version",
        "Auto (recommended)": "Auto (recommandé)",
        "CPU build": "Version CPU",
        "CUDA build (NVIDIA)": "Version CUDA (NVIDIA)",
        "Vulkan build": "Version Vulkan",
        "Download llama-server": "Télécharger llama-server",
        "Download model": "Télécharger un modèle",
        "Model": "Modèle",
        "Fetching release info…": "Récupération des infos de version…",
        "Extracting…": "Extraction…",
        "Starting download…": "Démarrage du téléchargement…",
        "Download complete": "Téléchargement terminé",
        "Download failed": "Échec du téléchargement",
        "Canceled": "Annulé",
        "Saved to": "Enregistré sous",
        "Model downloaded": "Modèle téléchargé",
    },
    "ru": {
        "Build": "Версия",
        "Auto (recommended)": "Авто (рекомендуется)",
        "CPU build": "Версия CPU",
        "CUDA build (NVIDIA)": "Версия CUDA (NVIDIA)",
        "Vulkan build": "Версия Vulkan",
        "Download llama-server": "Скачать llama-server",
        "Download model": "Скачать модель",
        "Model": "Модель",
        "Fetching release info…": "Получение данных о релизе…",
        "Extracting…": "Распаковка…",
        "Starting download…": "Начало загрузки…",
        "Download complete": "Загрузка завершена",
        "Download failed": "Ошибка загрузки",
        "Canceled": "Отменено",
        "Saved to": "Сохранено в",
        "Model downloaded": "Модель загружена",
    },
    "pt": {
        "Build": "Versão",
        "Auto (recommended)": "Automático (recomendado)",
        "CPU build": "Versão CPU",
        "CUDA build (NVIDIA)": "Versão CUDA (NVIDIA)",
        "Vulkan build": "Versão Vulkan",
        "Download llama-server": "Baixar llama-server",
        "Download model": "Baixar modelo",
        "Model": "Modelo",
        "Fetching release info…": "Obtendo informações da versão…",
        "Extracting…": "Extraindo…",
        "Starting download…": "Iniciando download…",
        "Download complete": "Download concluído",
        "Download failed": "Falha no download",
        "Canceled": "Cancelado",
        "Saved to": "Salvo em",
        "Model downloaded": "Modelo baixado",
    },
    "hi": {
        "Build": "बिल्ड",
        "Auto (recommended)": "ऑटो (अनुशंसित)",
        "CPU build": "CPU बिल्ड",
        "CUDA build (NVIDIA)": "CUDA बिल्ड (NVIDIA)",
        "Vulkan build": "Vulkan बिल्ड",
        "Download llama-server": "llama-server डाउनलोड करें",
        "Download model": "मॉडल डाउनलोड करें",
        "Model": "मॉडल",
        "Fetching release info…": "रिलीज़ जानकारी प्राप्त कर रहे हैं…",
        "Extracting…": "निकाल रहे हैं…",
        "Starting download…": "डाउनलोड शुरू हो रहा है…",
        "Download complete": "डाउनलोड पूरा",
        "Download failed": "डाउनलोड विफल",
        "Canceled": "रद्द",
        "Saved to": "सहेजा गया",
        "Model downloaded": "मॉडल डाउनलोड हुआ",
    },
    "bn": {
        "Build": "বিল্ড",
        "Auto (recommended)": "অটো (সুপারিশকৃত)",
        "CPU build": "CPU বিল্ড",
        "CUDA build (NVIDIA)": "CUDA বিল্ড (NVIDIA)",
        "Vulkan build": "Vulkan বিল্ড",
        "Download llama-server": "llama-server ডাউনলোড করুন",
        "Download model": "মডেল ডাউনলোড করুন",
        "Model": "মডেল",
        "Fetching release info…": "রিলিজ তথ্য আনা হচ্ছে…",
        "Extracting…": "বের করা হচ্ছে…",
        "Starting download…": "ডাউনলোড শুরু হচ্ছে…",
        "Download complete": "ডাউনলোড সম্পূর্ণ",
        "Download failed": "ডাউনলোড ব্যর্থ",
        "Canceled": "বাতিল",
        "Saved to": "সংরক্ষিত হয়েছে",
        "Model downloaded": "মডেল ডাউনলোড হয়েছে",
    },
    "ur": {
        "Build": "بلڈ",
        "Auto (recommended)": "خودکار (تجویز کردہ)",
        "CPU build": "CPU بلڈ",
        "CUDA build (NVIDIA)": "CUDA بلڈ (NVIDIA)",
        "Vulkan build": "Vulkan بلڈ",
        "Download llama-server": "llama-server ڈاؤن لوڈ کریں",
        "Download model": "ماڈل ڈاؤن لوڈ کریں",
        "Model": "ماڈل",
        "Fetching release info…": "ریلیز کی معلومات حاصل کی جا رہی ہیں…",
        "Extracting…": "نکالا جا رہا ہے…",
        "Starting download…": "ڈاؤن لوڈ شروع ہو رہا ہے…",
        "Download complete": "ڈاؤن لوڈ مکمل",
        "Download failed": "ڈاؤن لوڈ ناکام",
        "Canceled": "منسوخ",
        "Saved to": "محفوظ کیا گیا",
        "Model downloaded": "ماڈل ڈاؤن لوڈ ہو گیا",
    },
}
for _l, _m in _LLMDL_T.items():
    TRANSLATIONS.setdefault(_l, {}).update(_m)
del _l, _m

# ✦ v4.5: مفاتيح التفكير العميق + الخزائن المشفّرة — بنفس أسلوب _LLMDL_T
# (URL/Notes/Generate موجودة مسبقًا في TRANSLATIONS وتُعاد استخدامها)
_V45_T: Dict[str, Dict[str, str]] = {
    "ar": {
        "Deep thinking": "التفكير العميق",
        "Thinking hidden": "التفكير مخفي",
        "Download large model": "تنزيل موديل كبير",
        "Vault": "الخزنة",
        "Encrypted vault — master password + PBKDF2":
            "خزنة مشفّرة — كلمة سر رئيسية + PBKDF2",
        "Vault file": "ملف الخزنة",
        "Vault name": "اسم الخزنة",
        "Vault name exists": "اسم الخزنة موجود مسبقًا",
        "Master password": "الكلمة السر الرئيسية",
        "Unlock": "فتح",
        "Lock": "قفل",
        "New vault": "خزنة جديدة",
        "Delete vault": "حذف الخزنة",
        "Change password": "تغيير الكلمة السر",
        "New password": "كلمة سر جديدة",
        "Confirm password": "تأكيد الكلمة السر",
        "Vault locked": "أُقفلت الخزنة",
        "Vault auto-locked (idle)": "أُقفلت الخزنة تلقائيًا (خمول)",
        "Wrong master password": "كلمة السر الرئيسية خاطئة",
        "Vault corrupted": "ملف الخزنة تالف",
        "Invalid vault name": "اسم خزنة غير صالح",
        "Vault created": "أُنشئت الخزنة",
        "Vault deleted": "حُذفت الخزنة",
        "Master passwords do not match": "الكلمتان السرّيتان غير متطابقتين",
        "Password too short (min 4)": "الكلمة السر قصيرة (4 أحرف على الأقل)",
        "Entries": "الإدخالات",
        "Add entry": "إضافة إدخال",
        "Edit entry": "تعديل إدخال",
        "Title": "العنوان",
        "Username": "اسم المستخدم",
        "Password": "كلمة السر",
        "Save entry": "حفظ الإدخال",
        "Entry saved": "حُفظ الإدخال",
        "Delete entry": "حذف الإدخال",
        "Search…": "بحث…",
        "copied (clears in 30s)": "نُسخ (يُمسح من الحافظة بعد 30 ثانية)",
        "Clear form": "تفريغ النموذج",
    },
    "zh": {
        "Deep thinking": "深度思考",
        "Thinking hidden": "已隐藏思考",
        "Download large model": "下载大型模型",
        "Vault": "密码金库",
        "Encrypted vault — master password + PBKDF2": "加密金库 — 主密码 + PBKDF2",
        "Vault file": "金库文件",
        "Vault name": "金库名称",
        "Vault name exists": "金库名称已存在",
        "Master password": "主密码",
        "Unlock": "解锁",
        "Lock": "锁定",
        "New vault": "新建金库",
        "Delete vault": "删除金库",
        "Change password": "更改主密码",
        "New password": "新密码",
        "Confirm password": "确认密码",
        "Vault locked": "金库已锁定",
        "Vault auto-locked (idle)": "金库已自动锁定（空闲）",
        "Wrong master password": "主密码错误",
        "Vault corrupted": "金库文件损坏",
        "Invalid vault name": "金库名称无效",
        "Vault created": "金库已创建",
        "Vault deleted": "金库已删除",
        "Master passwords do not match": "两次输入的密码不一致",
        "Password too short (min 4)": "密码太短（至少 4 位）",
        "Entries": "条目",
        "Add entry": "添加条目",
        "Edit entry": "编辑条目",
        "Title": "标题",
        "Username": "用户名",
        "Password": "密码",
        "Save entry": "保存条目",
        "Entry saved": "条目已保存",
        "Delete entry": "删除条目",
        "Search…": "搜索…",
        "copied (clears in 30s)": "已复制（30 秒后自动清除）",
        "Clear form": "清空表单",
    },
    "es": {
        "Deep thinking": "Razonamiento profundo",
        "Thinking hidden": "Razonamiento oculto",
        "Download large model": "Descargar modelo grande",
        "Vault": "Bóveda",
        "Encrypted vault — master password + PBKDF2":
            "Bóveda cifrada — contraseña maestra + PBKDF2",
        "Vault file": "Archivo de bóveda",
        "Vault name": "Nombre de la bóveda",
        "Vault name exists": "El nombre de la bóveda ya existe",
        "Master password": "Contraseña maestra",
        "Unlock": "Desbloquear",
        "Lock": "Bloquear",
        "New vault": "Nueva bóveda",
        "Delete vault": "Eliminar bóveda",
        "Change password": "Cambiar contraseña",
        "New password": "Nueva contraseña",
        "Confirm password": "Confirmar contraseña",
        "Vault locked": "Bóveda bloqueada",
        "Vault auto-locked (idle)": "Bóveda bloqueada automáticamente (inactividad)",
        "Wrong master password": "Contraseña maestra incorrecta",
        "Vault corrupted": "Archivo de bóveda dañado",
        "Invalid vault name": "Nombre de bóveda no válido",
        "Vault created": "Bóveda creada",
        "Vault deleted": "Bóveda eliminada",
        "Master passwords do not match": "Las contraseñas no coinciden",
        "Password too short (min 4)": "Contraseña demasiado corta (mín. 4)",
        "Entries": "Entradas",
        "Add entry": "Añadir entrada",
        "Edit entry": "Editar entrada",
        "Title": "Título",
        "Username": "Usuario",
        "Password": "Contraseña",
        "Save entry": "Guardar entrada",
        "Entry saved": "Entrada guardada",
        "Delete entry": "Eliminar entrada",
        "Search…": "Buscar…",
        "copied (clears in 30s)": "copiado (se borra en 30 s)",
        "Clear form": "Limpiar formulario",
    },
    "fr": {
        "Deep thinking": "Raisonnement approfondi",
        "Thinking hidden": "Raisonnement masqué",
        "Download large model": "Télécharger un grand modèle",
        "Vault": "Coffre-fort",
        "Encrypted vault — master password + PBKDF2":
            "Coffre chiffré — mot de passe maître + PBKDF2",
        "Vault file": "Fichier du coffre",
        "Vault name": "Nom du coffre",
        "Vault name exists": "Ce nom de coffre existe déjà",
        "Master password": "Mot de passe maître",
        "Unlock": "Déverrouiller",
        "Lock": "Verrouiller",
        "New vault": "Nouveau coffre",
        "Delete vault": "Supprimer le coffre",
        "Change password": "Changer le mot de passe",
        "New password": "Nouveau mot de passe",
        "Confirm password": "Confirmer le mot de passe",
        "Vault locked": "Coffre verrouillé",
        "Vault auto-locked (idle)": "Coffre verrouillé automatiquement (inactivité)",
        "Wrong master password": "Mot de passe maître incorrect",
        "Vault corrupted": "Fichier de coffre corrompu",
        "Invalid vault name": "Nom de coffre non valide",
        "Vault created": "Coffre créé",
        "Vault deleted": "Coffre supprimé",
        "Master passwords do not match": "Les mots de passe ne correspondent pas",
        "Password too short (min 4)": "Mot de passe trop court (min. 4)",
        "Entries": "Entrées",
        "Add entry": "Ajouter une entrée",
        "Edit entry": "Modifier l'entrée",
        "Title": "Titre",
        "Username": "Nom d'utilisateur",
        "Password": "Mot de passe",
        "Save entry": "Enregistrer l'entrée",
        "Entry saved": "Entrée enregistrée",
        "Delete entry": "Supprimer l'entrée",
        "Search…": "Rechercher…",
        "copied (clears in 30s)": "copié (effacé dans 30 s)",
        "Clear form": "Vider le formulaire",
    },
    "ru": {
        "Deep thinking": "Глубокое размышление",
        "Thinking hidden": "Размышления скрыты",
        "Download large model": "Скачать большую модель",
        "Vault": "Хранилище",
        "Encrypted vault — master password + PBKDF2":
            "Зашифрованное хранилище — мастер-пароль + PBKDF2",
        "Vault file": "Файл хранилища",
        "Vault name": "Имя хранилища",
        "Vault name exists": "Такое имя хранилища уже существует",
        "Master password": "Мастер-пароль",
        "Unlock": "Разблокировать",
        "Lock": "Заблокировать",
        "New vault": "Новое хранилище",
        "Delete vault": "Удалить хранилище",
        "Change password": "Сменить пароль",
        "New password": "Новый пароль",
        "Confirm password": "Подтвердите пароль",
        "Vault locked": "Хранилище заблокировано",
        "Vault auto-locked (idle)": "Хранилище заблокировано (простой)",
        "Wrong master password": "Неверный мастер-пароль",
        "Vault corrupted": "Файл хранилища повреждён",
        "Invalid vault name": "Недопустимое имя хранилища",
        "Vault created": "Хранилище создано",
        "Vault deleted": "Хранилище удалено",
        "Master passwords do not match": "Пароли не совпадают",
        "Password too short (min 4)": "Пароль слишком короткий (мин. 4)",
        "Entries": "Записи",
        "Add entry": "Добавить запись",
        "Edit entry": "Изменить запись",
        "Title": "Название",
        "Username": "Имя пользователя",
        "Password": "Пароль",
        "Save entry": "Сохранить запись",
        "Entry saved": "Запись сохранена",
        "Delete entry": "Удалить запись",
        "Search…": "Поиск…",
        "copied (clears in 30s)": "скопировано (очистка через 30 с)",
        "Clear form": "Очистить форму",
    },
    "pt": {
        "Deep thinking": "Raciocínio profundo",
        "Thinking hidden": "Raciocínio oculto",
        "Download large model": "Baixar modelo grande",
        "Vault": "Cofre",
        "Encrypted vault — master password + PBKDF2":
            "Cofre criptografado — senha mestra + PBKDF2",
        "Vault file": "Arquivo do cofre",
        "Vault name": "Nome do cofre",
        "Vault name exists": "Nome do cofre já existe",
        "Master password": "Senha mestra",
        "Unlock": "Desbloquear",
        "Lock": "Bloquear",
        "New vault": "Novo cofre",
        "Delete vault": "Excluir cofre",
        "Change password": "Alterar senha",
        "New password": "Nova senha",
        "Confirm password": "Confirmar senha",
        "Vault locked": "Cofre bloqueado",
        "Vault auto-locked (idle)": "Cofre bloqueado automaticamente (inatividade)",
        "Wrong master password": "Senha mestra incorreta",
        "Vault corrupted": "Arquivo do cofre corrompido",
        "Invalid vault name": "Nome de cofre inválido",
        "Vault created": "Cofre criado",
        "Vault deleted": "Cofre excluído",
        "Master passwords do not match": "As senhas não coincidem",
        "Password too short (min 4)": "Senha muito curta (mín. 4)",
        "Entries": "Entradas",
        "Add entry": "Adicionar entrada",
        "Edit entry": "Editar entrada",
        "Title": "Título",
        "Username": "Usuário",
        "Password": "Senha",
        "Save entry": "Salvar entrada",
        "Entry saved": "Entrada salva",
        "Delete entry": "Excluir entrada",
        "Search…": "Pesquisar…",
        "copied (clears in 30s)": "copiado (limpa em 30 s)",
        "Clear form": "Limpar formulário",
    },
    "hi": {
        "Deep thinking": "गहन चिंतन",
        "Thinking hidden": "चिंतन छिपाया गया",
        "Download large model": "बड़ा मॉडल डाउनलोड करें",
        "Vault": "वॉल्ट",
        "Encrypted vault — master password + PBKDF2":
            "एन्क्रिप्टेड वॉल्ट — मास्टर पासवर्ड + PBKDF2",
        "Vault file": "वॉल्ट फ़ाइल",
        "Vault name": "वॉल्ट नाम",
        "Vault name exists": "वॉल्ट नाम पहले से मौजूद है",
        "Master password": "मास्टर पासवर्ड",
        "Unlock": "अनलॉक",
        "Lock": "लॉक",
        "New vault": "नया वॉल्ट",
        "Delete vault": "वॉल्ट हटाएँ",
        "Change password": "पासवर्ड बदलें",
        "New password": "नया पासवर्ड",
        "Confirm password": "पासवर्ड की पुष्टि करें",
        "Vault locked": "वॉल्ट लॉक हो गया",
        "Vault auto-locked (idle)": "वॉल्ट स्वतः लॉक हुआ (निष्क्रिय)",
        "Wrong master password": "गलत मास्टर पासवर्ड",
        "Vault corrupted": "वॉल्ट फ़ाइल दूषित",
        "Invalid vault name": "अवैध वॉल्ट नाम",
        "Vault created": "वॉल्ट बनाया गया",
        "Vault deleted": "वॉल्ट हटाया गया",
        "Master passwords do not match": "पासवर्ड मेल नहीं खाते",
        "Password too short (min 4)": "पासवर्ड बहुत छोटा है (न्यूनतम 4)",
        "Entries": "प्रविष्टियाँ",
        "Add entry": "प्रविष्टि जोड़ें",
        "Edit entry": "प्रविष्टि संपादित करें",
        "Title": "शीर्षक",
        "Username": "उपयोगकर्ता नाम",
        "Password": "पासवर्ड",
        "Save entry": "प्रविष्टि सहेजें",
        "Entry saved": "प्रविष्टि सहेजी गई",
        "Delete entry": "प्रविष्टि हटाएँ",
        "Search…": "खोजें…",
        "copied (clears in 30s)": "कॉपी हुआ (30 सेकंड में साफ़)",
        "Clear form": "फ़ॉर्म खाली करें",
    },
    "bn": {
        "Deep thinking": "গভীর চিন্তা",
        "Thinking hidden": "চিন্তা লুকানো হয়েছে",
        "Download large model": "বড় মডেল ডাউনলোড করুন",
        "Vault": "ভল্ট",
        "Encrypted vault — master password + PBKDF2":
            "এনক্রিপ্টেড ভল্ট — মাস্টার পাসওয়ার্ড + PBKDF2",
        "Vault file": "ভল্ট ফাইল",
        "Vault name": "ভল্টের নাম",
        "Vault name exists": "ভল্টের নাম আগেই আছে",
        "Master password": "মাস্টার পাসওয়ার্ড",
        "Unlock": "আনলক",
        "Lock": "লক",
        "New vault": "নতুন ভল্ট",
        "Delete vault": "ভল্ট মুছুন",
        "Change password": "পাসওয়ার্ড পরিবর্তন",
        "New password": "নতুন পাসওয়ার্ড",
        "Confirm password": "পাসওয়ার্ড নিশ্চিত করুন",
        "Vault locked": "ভল্ট লক হয়েছে",
        "Vault auto-locked (idle)": "ভল্ট স্বয়ংক্রিয়ভাবে লক হয়েছে (নিষ্ক্রিয়)",
        "Wrong master password": "ভুল মাস্টার পাসওয়ার্ড",
        "Vault corrupted": "ভল্ট ফাইল ক্ষতিগ্রস্ত",
        "Invalid vault name": "অবৈধ ভল্টের নাম",
        "Vault created": "ভল্ট তৈরি হয়েছে",
        "Vault deleted": "ভল্ট মুছে ফেলা হয়েছে",
        "Master passwords do not match": "পাসওয়ার্ড মিলছে না",
        "Password too short (min 4)": "পাসওয়ার্ড খুব ছোট (সর্বনিম্ন ৪)",
        "Entries": "এন্ট্রি",
        "Add entry": "এন্ট্রি যোগ করুন",
        "Edit entry": "এন্ট্রি সম্পাদনা",
        "Title": "শিরোনাম",
        "Username": "ব্যবহারকারীর নাম",
        "Password": "পাসওয়ার্ড",
        "Save entry": "এন্ট্রি সংরক্ষণ",
        "Entry saved": "এন্ট্রি সংরক্ষিত",
        "Delete entry": "এন্ট্রি মুছুন",
        "Search…": "অনুসন্ধান…",
        "copied (clears in 30s)": "কপি হয়েছে (৩০ সেকেন্ডে মুছবে)",
        "Clear form": "ফর্ম খালি করুন",
    },
    "ur": {
        "Deep thinking": "گہری سوچ",
        "Thinking hidden": "سوچ چھپا دی گئی",
        "Download large model": "بڑا ماڈل ڈاؤن لوڈ کریں",
        "Vault": "خزانہ",
        "Encrypted vault — master password + PBKDF2":
            "مرموز خزانہ — ماسٹر پاس ورڈ + PBKDF2",
        "Vault file": "خزانے کی فائل",
        "Vault name": "خزانے کا نام",
        "Vault name exists": "خزانے کا نام پہلے سے موجود ہے",
        "Master password": "ماسٹر پاس ورڈ",
        "Unlock": "کھولیں",
        "Lock": "بند کریں",
        "New vault": "نیا خزانہ",
        "Delete vault": "خزانہ حذف کریں",
        "Change password": "پاس ورڈ تبدیل کریں",
        "New password": "نیا پاس ورڈ",
        "Confirm password": "پاس ورڈ کی تصدیق",
        "Vault locked": "خزانہ بند ہو گیا",
        "Vault auto-locked (idle)": "خزانہ خودکار بند ہو گیا (بے کار)",
        "Wrong master password": "ماسٹر پاس ورڈ غلط ہے",
        "Vault corrupted": "خزانے کی فائل خراب ہے",
        "Invalid vault name": "غلط خزانے کا نام",
        "Vault created": "خزانہ بنا دیا گیا",
        "Vault deleted": "خزانہ حذف کر دیا گیا",
        "Master passwords do not match": "پاس ورڈ مماثل نہیں",
        "Password too short (min 4)": "پاس ورڈ بہت مختصر ہے (کم از کم 4)",
        "Entries": "اندراجات",
        "Add entry": "اندراج شامل کریں",
        "Edit entry": "اندراج ترمیم کریں",
        "Title": "عنوان",
        "Username": "صارف نام",
        "Password": "پاس ورڈ",
        "Save entry": "اندراج محفوظ کریں",
        "Entry saved": "اندراج محفوظ ہو گیا",
        "Delete entry": "اندراج حذف کریں",
        "Search…": "تلاش…",
        "copied (clears in 30s)": "کاپی ہو گیا (30 سیکنڈ میں صاف)",
        "Clear form": "فارم خالی کریں",
    },
}
for _l, _m in _V45_T.items():
    TRANSLATIONS.setdefault(_l, {}).update(_m)
del _l, _m

# ✦ v4.6: مفاتيح وضع الرام المنخفضة + موديل المسودة — بنفس أسلوب _V45_T
# (Estimated RAM/Browse/Model موجودة مسبقًا وتُعاد استخدامها؛
#  MoE اختصار تقني يُترك كما هو في كل اللغات)
_V46_T: Dict[str, Dict[str, str]] = {
    "ar": {
        "Low RAM (<8 GB)": "الرام المنخفضة (<8 GB)",
        "KV cache": "ذاكرة KV",
        "Auto": "تلقائي",
        "Draft model": "موديل مسودة",
        "Draft model (.gguf)": "ملف المسودة (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "تسريع: التحقق من دفعات المسودة دفعةً واحدة — الدقة نفسها",
        "Low-RAM: experts stream from SSD · native accuracy":
            "الرام المنخفضة: الخبراء تُقرأ من القرص · الدقة الأصلية كاملة",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "الرام المنخفضة: الموديل يُقرأ من القرص · رام أقل وأبطأ",
        "Suggested: enable Low RAM for this model":
            "مقترح: فعّل «الرام المنخفضة» لهذا الموديل",
        "Draft model not found — ignored":
            "ملف المسودة غير موجود — سيُتجاهل",
        "Server backend recommended for MoE + Low RAM":
            "يُنصح بمحرّك الخادم لموديلات MoE مع الرام المنخفضة",
        "experts": "خبيرًا",
        "active/token": "نشط/رمز",
    },
    "zh": {
        "Low RAM (<8 GB)": "低内存模式 (<8 GB)",
        "KV cache": "KV 缓存",
        "Auto": "自动",
        "Draft model": "草稿模型",
        "Draft model (.gguf)": "草稿模型 (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "加速：批量验证草稿 — 精度不变",
        "Low-RAM: experts stream from SSD · native accuracy":
            "低内存：专家权重从 SSD 流式读取 · 精度不变",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "低内存：模型从 SSD 流式读取 · 省内存但较慢",
        "Suggested: enable Low RAM for this model":
            "建议：为该模型开启低内存模式",
        "Draft model not found — ignored": "未找到草稿模型 — 已忽略",
        "Server backend recommended for MoE + Low RAM":
            "MoE + 低内存模式建议使用服务器后端",
        "experts": "个专家",
        "active/token": "激活/词元",
    },
    "es": {
        "Low RAM (<8 GB)": "RAM baja (<8 GB)",
        "KV cache": "caché KV",
        "Auto": "Auto",
        "Draft model": "modelo borrador",
        "Draft model (.gguf)": "modelo borrador (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "Rapidez: verifica lotes del borrador — misma precisión",
        "Low-RAM: experts stream from SSD · native accuracy":
            "RAM baja: los expertos se leen del SSD · precisión nativa",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "RAM baja: el modelo se lee del SSD · menos RAM, más lento",
        "Suggested: enable Low RAM for this model":
            "Sugerencia: activa RAM baja para este modelo",
        "Draft model not found — ignored":
            "modelo borrador no encontrado — se ignora",
        "Server backend recommended for MoE + Low RAM":
            "se recomienda el backend servidor para MoE + RAM baja",
        "experts": "expertos",
        "active/token": "activos/token",
    },
    "fr": {
        "Low RAM (<8 GB)": "RAM faible (<8 Go)",
        "KV cache": "cache KV",
        "Auto": "Auto",
        "Draft model": "modèle brouillon",
        "Draft model (.gguf)": "modèle brouillon (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "Vitesse : vérifie les lots du brouillon — précision identique",
        "Low-RAM: experts stream from SSD · native accuracy":
            "RAM faible : les experts sont lus depuis le SSD · précision native",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "RAM faible : le modèle est lu depuis le SSD · peu de RAM, plus lent",
        "Suggested: enable Low RAM for this model":
            "Suggestion : activez RAM faible pour ce modèle",
        "Draft model not found — ignored":
            "modèle brouillon introuvable — ignoré",
        "Server backend recommended for MoE + Low RAM":
            "backend serveur recommandé pour MoE + RAM faible",
        "experts": "experts",
        "active/token": "actifs/token",
    },
    "ru": {
        "Low RAM (<8 GB)": "Мало ОЗУ (<8 ГБ)",
        "KV cache": "кэш KV",
        "Auto": "Авто",
        "Draft model": "черновая модель",
        "Draft model (.gguf)": "черновая модель (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "Скорость: черновик проверяется пачками — точность та же",
        "Low-RAM: experts stream from SSD · native accuracy":
            "Мало ОЗУ: эксперты читаются с SSD · точность не меняется",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "Мало ОЗУ: модель читается с SSD · экономия ОЗУ, медленнее",
        "Suggested: enable Low RAM for this model":
            "Совет: включите «Мало ОЗУ» для этой модели",
        "Draft model not found — ignored":
            "черновая модель не найдена — игнорируется",
        "Server backend recommended for MoE + Low RAM":
            "для MoE + мало ОЗУ рекомендуется серверный движок",
        "experts": "экспертов",
        "active/token": "активных/токен",
    },
    "pt": {
        "Low RAM (<8 GB)": "RAM baixa (<8 GB)",
        "KV cache": "cache KV",
        "Auto": "Auto",
        "Draft model": "modelo rascunho",
        "Draft model (.gguf)": "modelo rascunho (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "Velocidade: verifica lotes do rascunho — mesma precisão",
        "Low-RAM: experts stream from SSD · native accuracy":
            "RAM baixa: especialistas lidos do SSD · precisão nativa",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "RAM baixa: modelo lido do SSD · menos RAM, mais lento",
        "Suggested: enable Low RAM for this model":
            "Sugestão: ative RAM baixa para este modelo",
        "Draft model not found — ignored":
            "modelo rascunho não encontrado — ignorado",
        "Server backend recommended for MoE + Low RAM":
            "backend servidor recomendado para MoE + RAM baixa",
        "experts": "especialistas",
        "active/token": "ativos/token",
    },
    "hi": {
        "Low RAM (<8 GB)": "कम RAM (<8 GB)",
        "KV cache": "KV कैश",
        "Auto": "स्वतः",
        "Draft model": "ड्राफ़्ट मॉडल",
        "Draft model (.gguf)": "ड्राफ़्ट मॉडल (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "गति: ड्राफ़्ट बैच एक साथ सत्यापित — वही सटीकता",
        "Low-RAM: experts stream from SSD · native accuracy":
            "कम RAM: विशेषज्ञ SSD से पढ़े जाते हैं · मूल सटीकता",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "कम RAM: मॉडल SSD से पढ़ा जाता है · कम RAM, धीमा",
        "Suggested: enable Low RAM for this model":
            "सुझाव: इस मॉडल के लिए कम RAM चालू करें",
        "Draft model not found — ignored": "ड्राफ़्ट मॉडल नहीं मिला — अनदेखा",
        "Server backend recommended for MoE + Low RAM":
            "MoE + कम RAM हेतु सर्वर बैकएंड बेहतर",
        "experts": "विशेषज्ञ",
        "active/token": "सक्रिय/टोकन",
    },
    "bn": {
        "Low RAM (<8 GB)": "কম RAM (<8 GB)",
        "KV cache": "KV ক্যাশ",
        "Auto": "স্বয়ংক্রিয়",
        "Draft model": "ড্রাফ্ট মডেল",
        "Draft model (.gguf)": "ড্রাফ্ট মডেল (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "গতি: ড্রাফ্ট ব্যাচ একসাথে যাচাই — নির্ভুলতা এক",
        "Low-RAM: experts stream from SSD · native accuracy":
            "কম RAM: এক্সপার্ট SSD থেকে পড়া হয় · আসল নির্ভুলতা",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "কম RAM: মডেল SSD থেকে পড়া হয় · কম RAM, ধীর",
        "Suggested: enable Low RAM for this model":
            "পরামর্শ: এই মডেলের জন্য কম RAM চালু করুন",
        "Draft model not found — ignored": "ড্রাফ্ট মডেল পাওয়া যায়নি — উপেক্ষিত",
        "Server backend recommended for MoE + Low RAM":
            "MoE + কম RAM-এর জন্য সার্ভার ব্যাকএন্ড ভালো",
        "experts": "এক্সপার্ট",
        "active/token": "সক্রিয়/টোকেন",
    },
    "ur": {
        "Low RAM (<8 GB)": "کم RAM (<8 GB)",
        "KV cache": "KV کیش",
        "Auto": "خودکار",
        "Draft model": "ڈرافٹ ماڈل",
        "Draft model (.gguf)": "ڈرافٹ ماڈل (.gguf)",
        "Speed: verifies draft batches — same accuracy":
            "رفتار: ڈرافٹ بیچ بیک ساتھ تصدیق — وہی درستگی",
        "Low-RAM: experts stream from SSD · native accuracy":
            "کم RAM: ماہرین SSD سے پڑھے جاتے ہیں · اصل درستگی",
        "Low-RAM: model streams from SSD · low RAM, slower":
            "کم RAM: ماڈل SSD سے پڑھا جاتا ہے · کم RAM، سست",
        "Suggested: enable Low RAM for this model":
            "تجویز: اس ماڈل کے لیے کم RAM آن کریں",
        "Draft model not found — ignored": "ڈرافٹ ماڈل نہیں ملا — نظر انداز",
        "Server backend recommended for MoE + Low RAM":
            "MoE + کم RAM کے لیے سرور بیک اینڈ بہتر",
        "experts": "ماہرین",
        "active/token": "فعال/ٹوکن",
    },
}
for _l, _m in _V46_T.items():
    TRANSLATIONS.setdefault(_l, {}).update(_m)
del _l, _m

# ✦ v4.7: مفاتيح الموديلات غير المحجوبة — بنفس أسلوب _V45_T/_V46_T
# (Model/Canceled/Download failed... موجودة مسبقًا وتُعاد استخدامها)
_V47_T: Dict[str, Dict[str, str]] = {
    "ar": {
        "Download uncensored model": "تنزيل موديل غير محجوب",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "موديلات غير محجوبة: نسخ معدّلة من المجتمع (Dolphin · Abliterated "
            "· Lexi · Stheno) أُزيل منها سلوك الرفض — استخدمها بمسؤولية "
            "ووفق قوانين بلدك.",
    },
    "zh": {
        "Download uncensored model": "下载无审查模型",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "无审查模型：社区微调版（Dolphin · Abliterated · Lexi · Stheno），"
            "移除了拒绝行为 — 请负责任地并按当地法律使用。",
    },
    "es": {
        "Download uncensored model": "Descargar modelo sin censura",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "Modelos sin censura: versiones de la comunidad (Dolphin · "
            "Abliterated · Lexi · Stheno) sin rechazos — úsalos con "
            "responsabilidad y según tus leyes locales.",
    },
    "fr": {
        "Download uncensored model": "Télécharger un modèle non censuré",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "Modèles non censurés : versions communautaires (Dolphin · "
            "Abliterated · Lexi · Stheno) sans refus — à utiliser de manière "
            "responsable et selon vos lois locales.",
    },
    "ru": {
        "Download uncensored model": "Скачать модель без цензуры",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "Модели без цензуры: версии от сообщества (Dolphin · Abliterated "
            "· Lexi · Stheno) без отказов — используйте ответственно и "
            "согласно местным законам.",
    },
    "pt": {
        "Download uncensored model": "Baixar modelo sem censura",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "Modelos sem censura: versões da comunidade (Dolphin · "
            "Abliterated · Lexi · Stheno) sem recusas — use com "
            "responsabilidade e conforme as leis locais.",
    },
    "hi": {
        "Download uncensored model": "असेंसर्ड मॉडल डाउनलोड करें",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "असेंसर्ड मॉडल: कम्युनिटी संस्करण (Dolphin · Abliterated · Lexi · "
            "Stheno) जिनसे इनकार व्यवहार हटाया गया — ज़िम्मेदारी से और "
            "स्थानीय कानूनों के अनुसार उपयोग करें।",
    },
    "bn": {
        "Download uncensored model": "আনসেনসর্ড মডেল ডাউনলোড",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "আনসেনসর্ড মডেল: কমিউনিটি সংস্করণ (Dolphin · Abliterated · Lexi · "
            "Stheno), অস্বীকৃতি আচরণ সরানো হয়েছে — দায়িত্বের সাথে ও "
            "স্থানীয় আইন অনুযায়ী ব্যবহার করুন।",
    },
    "ur": {
        "Download uncensored model": "غیر چیک شدہ ماڈل ڈاؤن لوڈ کریں",
        "Uncensored models are community fine-tunes (Dolphin · Abliterated "
        "· Lexi · Stheno) with refusal behavior removed — use responsibly "
        "and per your local laws.":
            "غیر چیک شدہ ماڈل: کمیونٹی ورژن (Dolphin · Abliterated · Lexi · "
            "Stheno) جن سے انکار کا رویہ ہٹایا گیا — ذمہ داری اور مقامی "
            "قوانین کے مطابق استعمال کریں۔",
    },
}
for _l, _m in _V47_T.items():
    TRANSLATIONS.setdefault(_l, {}).update(_m)
del _l, _m

_T_CACHE: Dict[Tuple[str, str], str] = {}


def translate(key: str, lang: str = "en") -> str:
    """ترجمة نص — الإنجليزية هي الحالة المطابقة (identity)، مع cache."""
    ck = (lang, key)
    if ck in _T_CACHE:
        return _T_CACHE[ck]
    val = TRANSLATIONS.get(lang, {}).get(key, key)
    _T_CACHE[ck] = val
    return val


# ─────────────────────────────────────────────────────────────
# 【5】 الأدوات المساعدة (Helpers)
# ─────────────────────────────────────────────────────────────
def jload(path: str, default: Any) -> Any:
    """قراءة JSON بأمان مع قيمة افتراضية."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def jsave(path: str, data: Any) -> bool:
    """كتابة JSON بأمان (داخل مجلد التطبيق فقط)."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def human_size(n: float) -> str:
    """تحويل البايتات إلى صيغة مقروءة."""
    for u in ("B", "KB", "MB", "GB", "TB", "PB"):
        if abs(n) < 1024:
            return f"{n:.1f} {u}" if u != "B" else f"{int(n)} B"
        n /= 1024
    return f"{n:.1f} EB"


def human_time(sec: float) -> str:
    """تحويل الثواني إلى d/h/m/s."""
    sec = int(sec)
    d, sec = divmod(sec, 86400)
    h, sec = divmod(sec, 3600)
    m, s = divmod(sec, 60)
    parts = []
    if d:
        parts.append(f"{d}d")
    if h or d:
        parts.append(f"{h}h")
    if m or h or d:
        parts.append(f"{m}m")
    parts.append(f"{s}s")
    return " ".join(parts)


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def fmt_mmss(sec: float) -> str:
    """تنسيق مدة كـ mm:ss أو h:mm:ss عند تجاوز الساعة (إصلاح الالتفاف عند 60 دقيقة)."""
    sec = max(0, int(round(sec)))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def next_birthday_days(a: _dt.date, years: int) -> int:
    """أيام حتى المناسبة القادمة — آمنة لسنة 29 فبراير في سنوات غير كبيسة."""
    try:
        nb = a.replace(year=a.year + years + 1)
    except ValueError:                      # 29 فبراير في سنة غير كبيسة
        nb = a.replace(year=a.year + years + 1, day=28)
    return (nb - _dt.date.today()).days


# ── حاسبة آمنة بدون eval — تعتمد ast
_ALLOWED_FUNCS = {
    "sqrt": math.sqrt, "abs": abs, "round": round, "sin": math.sin,
    "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos,
    "atan": math.atan, "log": math.log, "log10": math.log10, "log2": math.log2,
    "exp": math.exp, "floor": math.floor, "ceil": math.ceil, "pow": math.pow,
    "factorial": math.factorial, "degrees": math.degrees, "radians": math.radians,
    "min": min, "max": max, "hypot": math.hypot,
}
_ALLOWED_NAMES = {"pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf}

_BIN_OPS = {
    ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b, ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b, ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
}


def safe_eval(expr: str) -> float:
    """تقييم تعبير رياضي عبر ast — ممنوع eval تمامًا."""
    expr = expr.replace("^", "**").replace("×", "*").replace("÷", "/").strip()
    if not expr:
        raise ValueError("empty expression")
    if len(expr) > 500:
        raise ValueError("expression too long")
    node = ast.parse(expr, mode="eval").body

    def ev(n: ast.AST) -> Any:
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("unsupported constant")
        if isinstance(n, ast.BinOp):
            op = _BIN_OPS.get(type(n.op))
            if op is None:
                raise ValueError("unsupported operator")
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Pow) and (abs(b) > 1000 or abs(a) > 1e12):
                raise ValueError("exponent too large")
            return op(a, b)
        if isinstance(n, ast.UnaryOp):
            if isinstance(n.op, ast.UAdd):
                return +ev(n.operand)
            if isinstance(n.op, ast.USub):
                return -ev(n.operand)
            raise ValueError("unsupported unary operator")
        if isinstance(n, ast.Name):
            if n.id in _ALLOWED_NAMES:
                return _ALLOWED_NAMES[n.id]
            raise ValueError(f"unknown name: {n.id}")
        if isinstance(n, ast.Call):
            if not isinstance(n.func, ast.Name) or n.func.id not in _ALLOWED_FUNCS:
                raise ValueError("function not allowed")
            if n.keywords:
                raise ValueError("keyword args not allowed")
            return _ALLOWED_FUNCS[n.func.id](*[ev(a) for a in n.args])
        raise ValueError("unsupported expression")

    return ev(node)


# ── مورس
MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.", ".": ".-.-.-", ",": "--..--", "?": "..--..",
    "!": "-.-.--", "/": "-..-.", "-": "-....-", "(": "-.--.", ")": "-.--.-",
    " ": "/",
}
MORSE_REV = {v: k for k, v in MORSE.items()}


def to_morse(s: str) -> str:
    return " ".join(MORSE.get(ch.upper(), "?") for ch in s)


def from_morse(s: str) -> str:
    return "".join(MORSE_REV.get(tok, "?") for tok in s.split())


# ── ألوان
def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError("bad hex")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02X}{:02X}{:02X}".format(int(clamp(r, 0, 255)),
                                        int(clamp(g, 0, 255)),
                                        int(clamp(b, 0, 255)))


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    r_, g_, b_ = r / 255, g / 255, b / 255
    mx, mn = max(r_, g_, b_), min(r_, g_, b_)
    l = (mx + mn) / 2
    if mx == mn:
        return (0.0, 0.0, round(l * 100, 1))
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r_:
        h = ((g_ - b_) / d) % 6
    elif mx == g_:
        h = (b_ - r_) / d + 2
    else:
        h = (r_ - g_) / d + 4
    return (round(h * 60, 1), round(s * 100, 1), round(l * 100, 1))


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    h, s, l = h % 360, clamp(s, 0, 100) / 100, clamp(l, 0, 100) / 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    seg = int(h // 60)
    rgb = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][seg]
    return tuple(int(round((v + m) * 255)) for v in rgb)  # type: ignore


# ── شبكة: طبقة HTTP بسيطة تعمل بـ requests أو urllib
def http_get(url: str, headers: Optional[dict] = None,
             timeout: int = NET_TIMEOUT) -> Tuple[int, str]:
    """GET بسيط — يستخدم requests إن وُجد، وإلا urllib."""
    headers = dict(headers or {})
    headers.setdefault("User-Agent", f"{APP_NAME}/{APP_VERSION}")
    if HAS_REQUESTS:
        r = requests.get(url, headers=headers, timeout=timeout)
        return r.status_code, r.text
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def http_json(url: str, headers: Optional[dict] = None) -> Any:
    code, body = http_get(url, headers)
    if code >= 400:
        raise RuntimeError(f"HTTP {code}")
    return json.loads(body)


def http_request(method: str, url: str, headers: Optional[dict] = None,
                 data: Optional[str] = None,
                 timeout: int = NET_TIMEOUT) -> Tuple[int, str, Dict[str, str]]:
    """طلب HTTP عام (GET/POST/PUT/DELETE/HEAD) — يعيد (الحالة، النص، الترويسات)."""
    hdrs = dict(headers or {})
    hdrs.setdefault("User-Agent", f"{APP_NAME}/{APP_VERSION}")
    body = data.encode("utf-8") if isinstance(data, str) else data
    if HAS_REQUESTS:
        r = requests.request(method, url, headers=hdrs, data=body, timeout=timeout)
        return r.status_code, r.text, dict(r.headers)
    send_body = None if method.upper() in ("GET", "HEAD") else body
    req = urllib.request.Request(url, data=send_body, headers=hdrs, method=method.upper())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8", "replace"), dict(resp.headers)


def http_post_json(url: str, payload: dict,
                   headers: Optional[dict] = None) -> Any:
    """POST JSON — للمساعد الذكي وغيره."""
    headers = dict(headers or {})
    headers.setdefault("Content-Type", "application/json")
    headers.setdefault("User-Agent", f"{APP_NAME}/{APP_VERSION}")
    data = json.dumps(payload).encode("utf-8")
    if HAS_REQUESTS:
        r = requests.post(url, data=data, headers=headers, timeout=NET_TIMEOUT)
        if r.status_code >= 400:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        return r.json()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=NET_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def _no_window_flags() -> int:
    """منع وميض نافذة الكونسول عند استدعاء أوامر خارجية على Windows."""
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def run_cmd(args: List[str], timeout: int = SUBPROCESS_TIMEOUT) -> Tuple[int, str]:
    """تنفيذ أمر خارجي — دائمًا بـ timeout."""
    try:
        p = subprocess.run(args, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace",
                           creationflags=_no_window_flags())
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, f"[timeout > {timeout}s]"
    except FileNotFoundError:
        return -2, f"[not found: {args[0]}]"
    except Exception as e:
        return -3, f"[error: {e}]"


def file_hash(path: str, algo: str = "sha256", chunk: int = 1 << 20,
              limit: Optional[int] = None) -> str:
    """تجزئة ملف على دفعات (limit = اقرأ أول N بايت فقط)."""
    h = hashlib.new(algo)
    read = 0
    with open(path, "rb") as f:
        while True:
            want = chunk if limit is None else min(chunk, limit - read)
            if want <= 0:
                break
            b = f.read(want)
            if not b:
                break
            h.update(b)
            read += len(b)
    return h.hexdigest()


def entropy_bits(pw: str) -> float:
    """حساب Entropy تقريبي لكلمة المرور."""
    pool = 0
    if any(c.islower() for c in pw):
        pool += 26
    if any(c.isupper() for c in pw):
        pool += 26
    if any(c.isdigit() for c in pw):
        pool += 10
    if any(c in string.punctuation for c in pw):
        pool += len(string.punctuation)
    if any(ord(c) > 127 for c in pw):
        pool += 100
    return round(len(pw) * math.log2(pool), 1) if pool else 0.0


# ── بيانات وهمية
FAKE_FIRST = ["Omar", "Lina", "Yusuf", "Sara", "Adam", "Nour", "Ali", "Maya",
              "Karim", "Huda", "Tariq", "Rana", "Zaid", "Layla", "Sami", "Dina"]
FAKE_LAST = ["Haddad", "Nasser", "Khalil", "Aziz", "Farouk", "Mansour", "Saleh",
             "Rahman", "Barakat", "Younes", "Darwish", "Qasim", "Shakir"]
FAKE_DOMAINS = ["example.com", "mail.test", "demo.org", "sample.net"]
FAKE_CITIES = ["Istanbul", "Cairo", "Amman", "Dubai", "Tunis", "Rabat",
               "Beirut", "Doha", "Riyadh", "Kuwait City"]

LOREM_WORDS = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do "
               "eiusmod tempor incididunt ut labore et dolore magna aliqua enim "
               "ad minim veniam quis nostrud exercitation ullamco laboris nisi "
               "aliquip ex ea commodo consequat duis aute irure in reprehenderit "
               "voluptate velit esse cillum eu fugiat nulla pariatur").split()


def fake_person() -> Dict[str, str]:
    """توليد شخص وهمي للاختبار."""
    fn, ln = random.choice(FAKE_FIRST), random.choice(FAKE_LAST)
    return {
        "name": f"{fn} {ln}",
        "email": f"{fn.lower()}.{ln.lower()}{random.randint(1, 99)}@{random.choice(FAKE_DOMAINS)}",
        "phone": f"+90 5{random.randint(10, 59)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
        "city": random.choice(FAKE_CITIES),
        "uuid": str(uuid.uuid4()),
        "birth": (_dt.date(1970, 1, 1) + _dt.timedelta(days=random.randint(0, 16000))).isoformat(),
    }


# ── وحدات التحويل (المعامل بالنسبة للوحدة الأساسية)
UNITS: Dict[str, Dict[str, float]] = {
    "Length": {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000, "inch": 0.0254,
               "ft": 0.3048, "yd": 0.9144, "mile": 1609.344, "nmi": 1852},
    "Weight": {"mg": 1e-6, "g": 0.001, "kg": 1, "ton": 1000, "oz": 0.0283495,
               "lb": 0.453592, "stone": 6.35029},
    "Data":   {"bit": 0.125, "B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3,
               "TB": 1024**4, "PB": 1024**5},
    "Speed":  {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knot": 0.514444,
               "ft/s": 0.3048},
    "Time":   {"ms": 0.001, "s": 1, "min": 60, "h": 3600, "day": 86400,
               "week": 604800, "year": 31557600},
    "Area":   {"mm²": 1e-6, "cm²": 1e-4, "m²": 1, "km²": 1e6, "ft²": 0.092903,
               "acre": 4046.86, "hectare": 10000},
    "Volume": {"ml": 0.001, "l": 1, "m³": 1000, "cup": 0.236588,
               "gal(US)": 3.78541, "pint": 0.473176},
}
TEMP_UNITS = ["°C", "°F", "K"]


def convert_temp(v: float, src: str, dst: str) -> float:
    """تحويل درجات الحرارة (حالة خاصة لأنها ليست خطية بمعامل)."""
    c = v if src == "°C" else (v - 32) * 5 / 9 if src == "°F" else v - 273.15
    return c if dst == "°C" else c * 9 / 5 + 32 if dst == "°F" else c + 273.15


# ─────────────────────────────────────────────────────────────
# 【5.5】 LLM المحلي (GGUF) — v4.1
# ─────────────────────────────────────────────────────────────
_LAMACPP: Dict[str, Any] = {"tried": False, "mod": None}


def _get_llama_cpp():
    """استيراد llama-cpp-python بشكل كسول (محاولة واحدة فقط) — اختياري تمامًا.

    الاستيراد المبكر يبطئ إقلاع التطبيق (يحمّل مكتبة llama.cpp المشتركة)،
    لذلك نؤجّله حتى أول استخدام فعلي لأداة Local LLM.
    """
    if not _LAMACPP["tried"]:
        _LAMACPP["tried"] = True
        try:
            import llama_cpp  # noqa: استيراد كسول
            _LAMACPP["mod"] = llama_cpp
        except Exception:
            _LAMACPP["mod"] = None
    return _LAMACPP["mod"]


_GGUF_FILE_TYPE = {
    0: "F32", 1: "F16", 2: "Q4_0", 3: "Q4_1", 4: "Q4_1_SOME_F16",
    7: "Q8_0", 8: "Q5_0", 9: "Q5_1", 10: "Q2_K", 11: "Q3_K_S",
    12: "Q3_K_M", 13: "Q3_K_L", 14: "Q4_K_S", 15: "Q4_K_M",
    16: "Q5_K_S", 17: "Q5_K_M", 18: "Q6_K", 19: "IQ2_XXS", 20: "IQ2_XS",
    21: "Q2_K_S", 22: "IQ3_XS", 23: "IQ3_XXS", 24: "IQ1_S", 25: "IQ4_NL",
    26: "IQ3_S", 27: "IQ2_S", 28: "IQ4_XS", 29: "IQ1_M", 30: "BF16",
    36: "TQ1_0", 37: "TQ2_0",
}

# أنواع القيم في رأس GGUF: (صيغة struct، حجم بالبايت) — str/arr يُعالجان يدويًا
_GGUF_VT = {0: ("<B", 1), 1: ("<b", 1), 2: ("<H", 2), 3: ("<h", 2),
            4: ("<I", 4), 5: ("<i", 4), 6: ("<f", 4), 7: ("<?", 1),
            8: ("str", 0), 9: ("arr", 0), 10: ("<Q", 8), 11: ("<q", 8),
            12: ("<d", 8)}


def gguf_metadata(path: str) -> Dict[str, Any]:
    """قراءة رأس ملف GGUF دون تحميل الموديل — عبر struct فقط، بلا اعتمادات.

    يستخرج: الاسم، البنية (arch)، التكميم (quant)، طول السياق، عدد الطبقات،
    بُعد التضمين، حجم المفردات. يتوقف مبكرًا عند اكتمال المعلومات المفيدة أو
    عند الوصول إلى مفاتيح tokenizer (مصفوفات ضخمة)، ويتحمّل الملفات التالفة
    بإرجاع ما استُخرج فقط.
    """
    out: Dict[str, Any] = {}
    try:
        with open(path, "rb") as f:
            head = f.read(24)
            if len(head) < 24 or head[:4] != b"GGUF":
                return out
            _version, _tensors, kv_count = struct.unpack("<IQQ", head[4:24])

            def rstr() -> str:
                n = struct.unpack("<Q", f.read(8))[0]
                if n > 8 * 1024 * 1024:                 # قيمة شاذة — ملف تالف
                    raise ValueError("gguf: string too long")
                return f.read(n).decode("utf-8", "replace")

            def rval(vt: int, budget: List[int]) -> Any:
                if vt == 8:
                    return rstr()
                if vt == 9:                             # مصفوفة
                    et = struct.unpack("<I", f.read(4))[0]
                    cnt = struct.unpack("<Q", f.read(8))[0]
                    spec = _GGUF_VT.get(et)
                    if spec and spec[0] not in ("str", "arr"):
                        f.seek(cnt * spec[1], 1)        # تخطّي كامل — عناصر ثابتة الحجم
                        return f"array[{cnt}]"
                    items = []
                    for _ in range(min(cnt, 4)):        # نصوص: نقرأ عينة صغيرة فقط
                        if budget[0] <= 0:
                            raise ValueError("gguf: budget exhausted")
                        budget[0] -= 1
                        items.append(rval(et, budget))
                    if cnt > 4:
                        raise ValueError("gguf: big string array")
                    return items
                spec = _GGUF_VT.get(vt)
                if not spec or spec[0] in ("str", "arr"):
                    raise ValueError("gguf: bad value type")
                return struct.unpack(spec[0], f.read(spec[1]))[0]

            budget = [4096]
            scanned = 0
            while scanned < 64 and scanned < kv_count:
                key = rstr()
                vt = struct.unpack("<I", f.read(4))[0]
                scanned += 1
                if key == "general.name":
                    out["name"] = str(rval(vt, budget))
                elif key == "general.architecture":
                    out["arch"] = str(rval(vt, budget))
                elif key == "general.file_type":
                    out["quant"] = _GGUF_FILE_TYPE.get(
                        int(rval(vt, budget)), "?")
                elif key == "general.size_label":
                    out["size_label"] = str(rval(vt, budget))
                elif key == "general.parameter_count":
                    out["params"] = rval(vt, budget)
                elif key.endswith(".context_length"):
                    out["ctx"] = int(rval(vt, budget))
                elif key.endswith(".block_count"):
                    out["layers"] = int(rval(vt, budget))
                elif key.endswith(".embedding_length"):
                    out["embed"] = int(rval(vt, budget))
                elif key.endswith(".vocab_size"):
                    out["vocab"] = int(rval(vt, budget))
                else:
                    rval(vt, budget)                    # قراءة لتخطّي القيمة
                if key.startswith("tokenizer."):
                    break                               # ما بعدها مفردات ضخمة — لا فائدة
    except Exception:
        pass                                            # رأس تالف → نُبقي ما استُخرج
    return out


# ─────────────────────────────────────────────────────────────
# 【5.5b】 v4.6: فحص موترات GGUF (كشف MoE) + مقدّر الرام المنخفضة
# ─────────────────────────────────────────────────────────────

# حجم كتلة/عنصر لأنواع تكميم GGML: type → (block_size, bytes_per_block)
_GGML_TSIZE = {
    0: (1, 4), 1: (1, 2), 2: (32, 18), 3: (32, 20), 6: (32, 22),
    7: (32, 24), 8: (32, 34), 9: (32, 36), 10: (256, 84), 11: (256, 110),
    12: (256, 144), 13: (256, 176), 14: (256, 210), 15: (256, 292),
    16: (256, 66), 17: (256, 74), 18: (256, 93), 19: (256, 50),
    20: (32, 20), 21: (256, 109), 22: (256, 97), 23: (256, 72),
    24: (256, 56), 25: (1, 2), 28: (32, 17),
}

# ذاكرة الفحص — المسار+mtime+الحجم مفتاح؛ نُبقي 8 نتائج كحد أقصى
_GGUF_SCAN_CACHE: Dict[str, Dict[str, Any]] = {}


def _gguf_tensor_scan(path: str) -> Dict[str, Any]:
    """✦ v4.6: مسح قسم معلومات الموترات في GGUF — كشف موديلات MoE وقياسها.

    يمشي كامل قسم البيانات الوصفية (بلا توقف مبكر عند tokenizer) ثم يقرأ
    إدخالات الموترات ويحسب الأحجام النظرية من (numel × dtype)، فيجمع:
    tensor_bytes (مجموع كل الأوزان)، expert_bytes (موترات الخبراء ثلاثية
    الأبعاد ذات ‎.ffn_‎ — التسمية الموحدة في Mixtral/Qwen3-MoE/DeepSeek/GLM)،
    experts/experts_used (من مفاتيح المعمارية)، kv_width (رؤوس KV × طول
    المفتاح — لتقدير ذاكرة السياق بدقة GQA). النتيجة تُخزَّن مؤقتًا حسب
    المسار+mtime لأن الرأس يُقرأ عدة مرات. أي ملف تالف/نوع مجهول → {}.
    """
    try:
        st = os.stat(path)
        ck = f"{path}:{st.st_mtime_ns}:{st.st_size}"
        hit = _GGUF_SCAN_CACHE.get(ck)
        if hit is not None:
            return hit
        out: Dict[str, Any] = {}
        with open(path, "rb") as f:
            head = f.read(24)
            if len(head) < 24 or head[:4] != b"GGUF":
                return {}
            ver, n_tensors, kv_count = struct.unpack("<IQQ", head[4:24])
            if ver < 2 or kv_count > 4096 or n_tensors > 20000:
                return {}                               # إصدار قديم/شاذ

            def rstr() -> str:
                n = struct.unpack("<Q", f.read(8))[0]
                if n > 8 * 1024 * 1024:
                    raise ValueError("bad string")
                return f.read(n).decode("utf-8", "replace")

            def skip_val(vt: int) -> Any:
                if vt == 8:
                    rstr()
                    return None
                if vt == 9:                             # مصفوفة
                    et = struct.unpack("<I", f.read(4))[0]
                    cnt = struct.unpack("<Q", f.read(8))[0]
                    spec = _GGUF_VT.get(et)
                    if spec and spec[0] not in ("str", "arr"):
                        f.seek(cnt * spec[1], 1)
                        return None
                    if cnt > 2_000_000:
                        raise ValueError("huge array")
                    for _ in range(cnt):
                        skip_val(et)
                    return None
                spec = _GGUF_VT.get(vt)
                if not spec or spec[0] in ("str", "arr"):
                    raise ValueError("bad type")
                return struct.unpack(spec[0], f.read(spec[1]))[0]

            arch = ""
            for _ in range(kv_count):
                key = rstr()
                vt = struct.unpack("<I", f.read(4))[0]
                if key == "general.architecture":
                    # ⚠ skip_val يعيد None للنصوص — نقرأ القيمة هنا يدويًا
                    arch = rstr() if vt == 8 else str(skip_val(vt) or "")
                elif arch and key == f"{arch}.expert_count":
                    out["experts"] = int(skip_val(vt) or 0)
                elif arch and key == f"{arch}.expert_used_count":
                    out["experts_used"] = int(skip_val(vt) or 0)
                elif key.endswith(".attention.head_count_kv"):
                    v = skip_val(vt)
                    if isinstance(v, (int, float)):
                        out["kv_heads"] = int(v)
                elif key.endswith(".attention.key_length"):
                    v = skip_val(vt)
                    if isinstance(v, (int, float)):
                        out["key_length"] = int(v)
                else:
                    skip_val(vt)
            if out.get("kv_heads") and out.get("key_length"):
                out["kv_width"] = out["kv_heads"] * out["key_length"]

            total = 0
            expert = 0
            for _ in range(n_tensors):
                # ترتيب المواصفة: الاسم أولاً ثم n_dims ثم dims ثم type/offset
                name = rstr()
                n_dims = struct.unpack("<I", f.read(4))[0]
                dims = struct.unpack(f"<{n_dims}Q",
                                     f.read(8 * n_dims)) if n_dims else ()
                ttype = struct.unpack("<I", f.read(4))[0]
                struct.unpack("<Q", f.read(8))          # offset — لا نحتاجه
                spec = _GGML_TSIZE.get(ttype)
                if spec is None:
                    raise ValueError("unknown tensor type")
                numel = 1
                for d in dims:
                    numel *= d
                nb = ((numel + spec[0] - 1) // spec[0]) * spec[1]
                total += nb
                if n_dims == 3 and ".ffn_" in name:
                    expert += nb                        # موتر خبراء
            out["tensor_bytes"] = total
            out["expert_bytes"] = expert
        _GGUF_SCAN_CACHE[ck] = out
        if len(_GGUF_SCAN_CACHE) > 8:                   # نظافة الذاكرة
            _GGUF_SCAN_CACHE.pop(next(iter(_GGUF_SCAN_CACHE)))
        return out
    except Exception:
        return {}


def _llm_estimate_ram(meta: Dict[str, Any], file_size: int, *,
                      lowram: bool = False, kv_q: str = "f16"
                      ) -> Dict[str, Any]:
    """✦ v4.6: مقدّر ذاكرة وحدوي — يقود سطور «Estimated RAM» في الواجهة.

    المدخلات من gguf_metadata + _gguf_tensor_scan — بلا وصول لملفات.
    يعيد: moe / experts / experts_used / kv (تقدير ذاكرة السياق حسب kv_q)
    / resident (الرام المقيمة مع وضع lowram: الأوزان غير الخبيرة + السياق +
    مخازن) / full (الرام اللازمة للسرعة الكاملة) / tok_bytes (قراءة القرص
    لكل توكن عند البث) / tok_lo..tok_hi (مدى tok/s على NVMe 2500–6000MB/s).
    """
    experts = int(meta.get("experts") or 0)
    used = int(meta.get("experts_used") or 0)
    moe = experts > 0
    layers = int(meta.get("layers") or 0)
    ctx = int(meta.get("ctx") or 4096)
    kv_w = int(meta.get("kv_width") or 0)
    if kv_w <= 0:
        kv_w = max(1, int(meta.get("embed") or 0) // 4)  # GQA تقريبي
    elem = {"q8_0": 1.0, "q4_0": 0.5}.get(kv_q, 2.0)
    kv = int(2 * layers * ctx * kv_w * elem) if layers else 0
    out: Dict[str, Any] = {"moe": moe, "experts": experts,
                           "experts_used": used, "kv": kv}
    total = int(meta.get("tensor_bytes") or file_size)
    expert = int(meta.get("expert_bytes") or 0)
    if moe:
        # الأوزان غير الخبيرة هي ما يقيم فعليًا مع exps=CPU (والبقية mmap)
        rest = max(0, total - expert) if expert > 0 else int(total * 0.2)
        # القراءة من القرص لكل توكن = الخبراء النشطون فقط (used/experts)
        act = expert * (used / experts) if (expert and used) else \
            expert * 0.1
        out["resident"] = int(rest * 1.12 + kv + 0.4 * (1 << 30))
        out["tok_bytes"] = int(act + kv / max(1, ctx))
    else:
        out["resident"] = int(file_size * 1.12 + kv)
        out["tok_bytes"] = int(file_size)
    out["full"] = int(file_size * 1.12 + kv)
    mb = max(1.0, out["tok_bytes"] / (1 << 20))
    out["tok_lo"] = round(2500 / mb, 1)                 # SSD متواضع
    out["tok_hi"] = round(6000 / mb, 1)                 # NVMe سريع
    return out


# مفاتيح llama-server الاختيارية — قد ترفضها إصدارات أقدم فتُحذف في إعادة المحاولة
_LLM_OPT_FLAGS = ("-fa", "--cache-type-k", "--cache-type-v",
                  "--override-tensor", "-md", "--draft-max", "--draft-min",
                  "--draft-p-min")


def _llm_strip_optional(args: List[str]) -> List[str]:
    """حذف المفاتيح الاختيارية (ووسائطها) من سطر أوامر llama-server."""
    out: List[str] = []
    skip = False
    for a in args:
        if skip:
            skip = False
            continue
        if a in _LLM_OPT_FLAGS:
            skip = a != "-fa"                           # -fa بلا وسيط قيمة
            continue
        out.append(a)
    return out


def _llm_lowram_flags(lowram: bool, kv_q: str, moe: bool,
                      draft: str = "") -> List[str]:
    """✦ v4.6: وسائط llama-server لوضع الرام المنخفضة + موديل المسودة.

    - lowram: بلا تثبيت صفحات (--no-mlock) وبلا تسخين (--no-warmup يمنع
      قفزة الرام عند الإقلاع) + دفعات حساب صغيرة ‎-b/-ub 128‎ تقلّص مخازن
      الحساب + تكميم ذاكرة KV (q8_0 أثره على الدقة شبه معدوم، q4_0 أكبر
      توفير) — يُفعَّل FlashAttention لأن تكميم V يتطلبه.
    - moe: ‎--override-tensor "exps=CPU"‎ يُبقي موترات الخبراء (~80-90٪ من
      الموديل) على القرص عبر mmap وتُقرأ التجزئة النشطة لكل توكن فقط —
      موديل 30B يعمل بأقل من 8GB رام وبالدقة الأصلية الكاملة (بلا تكميم
      إضافي). مع -ngl تبقى طبقات الانتباه على GPU فترتفع السرعة.
    - draft: فك تشفير تخميني — الموديل الصغير يقترح حتى 16 رمزًا والكبير
      يتحقق منها دفعةً واحدة، فتُقرأ الأوزان مرة واحدة لعدة رموز: تسريع
      حقيقي دون أي تغيير في الدقة (قبول الرموز يضمن نفس التوزيع).
    """
    flags: List[str] = []
    if draft and os.path.isfile(draft):
        flags += ["-md", draft, "--draft-max", "16", "--draft-min", "3"]
    if lowram:
        flags += ["--no-mlock", "--no-warmup", "-b", "128", "-ub", "128"]
        if kv_q in ("q8_0", "q4_0"):
            flags += ["-fa", "--cache-type-k", kv_q, "--cache-type-v", kv_q]
        if moe:
            flags += ["--override-tensor", "exps=CPU"]
    return flags


# ─────────────────────────────────────────────────────────────
# 【5.6】 خادم llama.cpp عبر HTTP — v4.3 (بلا llama-cpp-python وبلا مترجم)
# ─────────────────────────────────────────────────────────────
_LLM_INSTALL_HELP = """\
llama-cpp-python — install help
===============================
Python 3.13 on Windows has NO prebuilt wheel for llama-cpp-python,
so pip falls back to compiling it and fails without MSVC
("nmake: no such file or directory").

OPTION 1 - llama.cpp server  (RECOMMENDED - no compiler, v4.4 auto-download)
  1) In this tool:  Build = "Auto (recommended)"
     ->  click "Download llama-server" — the toolbox picks the
     right prebuilt binary (CPU/CUDA) from GitHub automatically.
     Manual alternative: https://github.com/ggml-org/llama.cpp/releases
  2) Click "Download model" to fetch a ready GGUF from Hugging Face,
     or extract/browse your own .gguf file.
  3) Backend = "llama.cpp Server (auto-start)"  ->  Load model.
     The toolbox starts the server and streams over HTTP.

OPTION 2 - compile in-process  (needs ~7 GB disk + 20-60 minutes)
  winget install Microsoft.VisualStudio.2022.BuildTools --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
  pip install llama-cpp-python --no-cache-dir

OPTION 3 - older Python (3.12 or earlier has community wheels)
  pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

Server mode (option 1) needs NO llama-cpp-python at all.
"""


def _llm_server_ready(base_url: str, timeout: float = 3.0) -> Tuple[bool, str]:
    """فحص جهوزية خادم llama.cpp عبر ‎/health — يرجع (جاهز؟، سبب الفشل)."""
    url = base_url.rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return True, ""
    except Exception as e:
        code = getattr(e, "code", None)
        if code == 503:
            return False, "loading"                     # النموذج ما زال يُحمَّل
        if code:
            return False, f"HTTP {code}"
        return False, (str(e) or e.__class__.__name__)


def _llm_chat_body(messages: List[Dict[str, str]], *, max_tokens: int,
                   temperature: float, top_p: float,
                   repeat_penalty: Optional[float] = None,
                   disable_thinking: bool = False) -> Dict[str, Any]:
    """جسم طلب /v1/chat/completions — مُفصَل ليُختبر وحدويًا.

    ✦ v4.5: disable_thinking=True يُرسل chat_template_kwargs enable_thinking=false
    (مدعوم في llama.cpp الحديثة لموديلات Qwen3 وغيرها) — فيستغني عن توليد رموز
    التفكير أصلًا بدل إخفائها بعد توليدها. الخوادم الأقدم تتجاهل الحقل بهدوء.
    """
    body: Dict[str, Any] = {"messages": messages, "stream": True,
                            "max_tokens": int(max_tokens),
                            "temperature": float(temperature),
                            "top_p": float(top_p)}
    if repeat_penalty and repeat_penalty > 1.0:
        body["repeat_penalty"] = float(repeat_penalty)
    if disable_thinking:
        body["chat_template_kwargs"] = {"enable_thinking": False}
    return body


def _llm_http_stream(base_url: str, messages: List[Dict[str, str]], *,
                     max_tokens: int, temperature: float, top_p: float,
                     repeat_penalty: Optional[float] = None,
                     disable_thinking: bool = False,
                     stop_ev: Optional[threading.Event] = None):
    """بث محادثة من خادم متوافق مع OpenAI عبر urllib — مولّد مقاطع نصية.

    ينتج قواميس بنفس شكل llama-cpp-python
    ({"choices": [{"delta": {"content": ...}}]}) لتبقى حلقة الاستهلاك واحدة.
    ✦ v4.5: قد يُنتج أيضًا delta["reasoning_content"] (خوادم llama.cpp الحديثة
    تفصل رموز التفكير عن الجواب) — المستهلك يقرر عرضه أو حجبه حسب المفتاح.
    """
    url = base_url.rstrip("/") + "/v1/chat/completions"
    body = _llm_chat_body(messages, max_tokens=max_tokens,
                          temperature=temperature, top_p=top_p,
                          repeat_penalty=repeat_penalty,
                          disable_thinking=disable_thinking)
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Accept": "text/event-stream"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        for raw in resp:
            if stop_ev is not None and stop_ev.is_set():
                break
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue                                # SSE: تعليقات/أسطر فارغة
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            try:
                obj = json.loads(payload)
                delta = obj["choices"][0].get("delta") or {}
                piece = delta.get("content") or ""
                rc = delta.get("reasoning_content") or ""
            except Exception:
                piece, rc = "", ""
            if piece or rc:
                yield {"choices": [{"delta": {"content": piece,
                                              "reasoning_content": rc}}]}


class _ThinkFilter:
    """✦ v4.5: مرشّح بثّي يحجب كتل التفكير ‎<think>…</think>‎ (وبدائلها).

    يُغذّى بمقاطع قد تتقطّع في أي حرف ويرجع النص الظاهر فقط.
    يعمل مع موديلات DeepSeek-R1/QwQ/Qwen3-thinking وأي موديل يضع التفكير
    بين وسوم. يتتبّع: suppressed_chars (عدد الأحرف المحجوبة)،
    suppressing (هل نحن داخل كتلة تفكير الآن؟).
    """

    OPEN = ("<think>", "<thinking>", "<reasoning>")
    CLOSE = ("</think>", "</thinking>", "</reasoning>")

    def __init__(self):
        self._buf = ""
        self._inside = False
        self.suppressed_chars = 0

    @property
    def suppressing(self) -> bool:
        return self._inside

    @staticmethod
    def _earliest(buf: str, tags: Tuple[str, ...]) -> Tuple[int, int]:
        """(أول موقع، طول الوسم) — أو (-1، 0) إن لم يوجد."""
        best, blen = -1, 0
        for tg in tags:
            i = buf.find(tg)
            if i != -1 and (best == -1 or i < best):
                best, blen = i, len(tg)
        return best, blen

    def feed(self, chunk: str) -> str:
        out: List[str] = []
        buf = self._buf + chunk
        maxlen = max(len(t) for t in self.OPEN + self.CLOSE)
        while buf:
            if self._inside:
                i, ln = self._earliest(buf, self.CLOSE)
                if i == -1:
                    break          # كله يبقى مؤقتًا — قد يحمل وسم إغلاق مبتور
                self.suppressed_chars += i + ln
                buf = buf[i + ln:]
                self._inside = False
            else:
                i, ln = self._earliest(buf, self.OPEN)
                if i == -1:
                    keep = max(0, len(buf) - (maxlen - 1))
                    out.append(buf[:keep])
                    buf = buf[keep:]
                    break
                out.append(buf[:i])
                buf = buf[i + ln:]
                self._inside = True
                self.suppressed_chars += ln       # وسم الفتح نفسه محجوب
        self._buf = buf
        text = "".join(out)
        return text

    def flush(self) -> str:
        """ما تبقّى في النهاية: نص ظاهر إن كنا خارج كتلة، ولا شيء داخلها."""
        buf, self._buf = self._buf, ""
        if self._inside:
            self.suppressed_chars += len(buf)
            return ""
        return buf


def _llm_start_server(exe: str, model: str, ctx: int, gpu: int, thr: int,
                      port: int,
                      stop_ev: Optional[threading.Event] = None,
                      extra: Optional[List[str]] = None
                      ) -> Tuple[Any, str]:
    """تشغيل llama-server كعملية خلفية وانتظار جهوزيته — يرجع (proc, url).

    يعمل مع أي ثنائي llama-server (Windows/Linux/macOS) بلا مترجم وبلا
    llama-cpp-python. يُنهي العملية بنفسه عند المهلة أو الإيقاف.
    ✦ v4.6: ‎extra‎ = وسائط إضافية (وضع الرام المنخفضة/المسودة من
    _llm_lowram_flags). إن خرج الخادم مبكرًا مع المفاتيح الاختيارية
    (cache-type/override-tensor/draft…) تُعاد المحاولة مرة واحدة بدونها —
    لإصدارات llama.cpp الأقدم التي لا تعرفها.
    """
    base = [exe, "-m", model, "-c", str(max(256, ctx)),
            "--host", "127.0.0.1", "--port", str(port)]
    if gpu:
        base += ["-ngl", str(gpu)]
    if thr and thr > 0:
        base += ["-t", str(thr)]
    attempts = [base + list(extra or [])]
    if extra:
        reduced = base + _llm_strip_optional(list(extra))
        if reduced != attempts[0]:
            attempts.append(reduced)                    # محاولة مخفَّضة احتياطية
    last_err = "llama-server exited early"
    for ai, args in enumerate(attempts):
        is_last = ai == len(attempts) - 1
        try:
            proc = subprocess.Popen(args, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.STDOUT,
                                    creationflags=_no_window_flags())
        except FileNotFoundError as e:
            raise RuntimeError(f"llama-server not found: {exe} ({e})") from e
        url = f"http://127.0.0.1:{port}"
        deadline = time.time() + 120                    # الموديلات الكبيرة تحتاج وقتًا
        early_exit = False
        try:
            while time.time() < deadline:
                if stop_ev is not None and stop_ev.is_set():
                    raise RuntimeError("stopped")
                if proc.poll() is not None:
                    early_exit = True                   # مفاتيح غير مدعومة؟
                    break
                ok, _ = _llm_server_ready(url, timeout=1.0)
                if ok:
                    return proc, url
                time.sleep(0.5)
        except Exception:
            if proc.poll() is None:
                try:
                    proc.terminate()
                except Exception:
                    pass
            raise
        if not early_exit:
            raise RuntimeError("health timeout after 120s")
        last_err = f"llama-server exited early (code {proc.returncode})"
        if is_last:
            raise RuntimeError(last_err)
        # نسخة أقدم من llama.cpp — نجرّب بلا المفاتيح الاختيارية


# ─────────────────────────────────────────────────────────────
# 【5.7】 التنزيل التلقائي — v4.4: llama-server من GitHub + موديلات GGUF من Hugging Face
# ─────────────────────────────────────────────────────────────
_LLM_UA = "UltimateToolbox/" + APP_VERSION
_LLM_GH_API = "https://api.github.com/repos/ggml-org/llama.cpp/releases/latest"

# موديلات GGUF موصى بها — روابط مباشرة مجانية بلا تسجيل (Apache/Llama مفتوحة)
# ✦ v4.5: 25 موديلًا بقسمان — v4.6: عائلة MoE — v4.7: قسم unc غير المحجوب
#   (Dolphin/Abliterated/Lexi/Stheno) — كل الروابط فُحصت حيًّا (HTTP 200)
#   والأحجام من Content-Length الفعلي
_LLM_MODELS: List[Dict[str, str]] = [
    # ── صغيرة (tier=small): تصلح لأي جهاز ──
    {"tier": "small", "name": "SmolLM2 360M Instruct · Q8_0", "size": "≈0.4 GB",
     "url": "https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct-GGUF/resolve/main/"
            "smollm2-360m-instruct-q8_0.gguf"},
    {"tier": "small", "name": "Qwen2.5 0.5B Instruct · Q4_K_M", "size": "≈0.4 GB",
     "url": "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/"
            "qwen2.5-0.5b-instruct-q4_k_m.gguf"},
    {"tier": "small", "name": "TinyLlama 1.1B Chat · Q4_K_M", "size": "≈0.7 GB",
     "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/"
            "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"},
    {"tier": "small", "name": "Llama 3.2 1B Instruct · Q4_K_M", "size": "≈0.8 GB",
     "url": "https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/"
            "Llama-3.2-1B-Instruct-Q4_K_M.gguf"},
    {"tier": "small", "name": "Qwen2.5 1.5B Instruct · Q4_K_M", "size": "≈1.0 GB",
     "url": "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/"
            "qwen2.5-1.5b-instruct-q4_k_m.gguf"},
    {"tier": "small", "name": "Qwen2.5 3B Instruct · Q4_K_M", "size": "≈1.9 GB",
     "url": "https://huggingface.co/bartowski/Qwen2.5-3B-Instruct-GGUF/resolve/main/"
            "Qwen2.5-3B-Instruct-Q4_K_M.gguf"},
    {"tier": "small", "name": "Llama 3.2 3B Instruct · Q4_K_M", "size": "≈2.0 GB",
     "url": "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/"
            "Llama-3.2-3B-Instruct-Q4_K_M.gguf"},
    {"tier": "small", "name": "Phi-3-mini 4k Instruct · Q4_K_M", "size": "≈2.4 GB",
     "url": "https://huggingface.co/bartowski/Phi-3-mini-4k-instruct-GGUF/resolve/main/"
            "Phi-3-mini-4k-instruct-Q4_K_M.gguf"},
    # ── كبيرة (tier=large): 7B حتى 70B — تحتاج RAM/VRAM أكبر ──
    {"tier": "large", "name": "Mistral 7B Instruct v0.3 · Q4_K_M", "size": "≈4.4 GB",
     "url": "https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/"
            "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"},
    {"tier": "large", "name": "Qwen2.5 7B Instruct · Q4_K_M", "size": "≈4.7 GB",
     "url": "https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/"
            "Qwen2.5-7B-Instruct-Q4_K_M.gguf"},
    {"tier": "large", "name": "DeepSeek-R1-Distill-Qwen-7B · Q4_K_M", "size": "≈4.7 GB",
     "url": "https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/"
            "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"},
    {"tier": "large", "name": "Meta-Llama 3.1 8B Instruct · Q4_K_M", "size": "≈4.9 GB",
     "url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/"
            "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"},
    {"tier": "large", "name": "Qwen3 8B · Q4_K_M", "size": "≈5.0 GB",
     "url": "https://huggingface.co/Qwen/Qwen3-8B-GGUF/resolve/main/"
            "Qwen3-8B-Q4_K_M.gguf"},
    {"tier": "large", "name": "gemma-2 9B it · Q4_K_M", "size": "≈5.8 GB",
     "url": "https://huggingface.co/bartowski/gemma-2-9b-it-GGUF/resolve/main/"
            "gemma-2-9b-it-Q4_K_M.gguf"},
    {"tier": "large", "name": "Qwen2.5 14B Instruct · Q4_K_M", "size": "≈9.0 GB",
     "url": "https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/"
            "Qwen2.5-14B-Instruct-Q4_K_M.gguf"},
    {"tier": "large", "name": "DeepSeek-R1-Distill-Qwen-14B · Q4_K_M", "size": "≈9.0 GB",
     "url": "https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-14B-GGUF/resolve/main/"
            "DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf"},
    {"tier": "large", "name": "phi-4 14B · Q4_K_M", "size": "≈9.1 GB",
     "url": "https://huggingface.co/bartowski/phi-4-GGUF/resolve/main/"
            "phi-4-Q4_K_M.gguf"},
    {"tier": "large", "name": "Mistral-Small 24B Instruct 2501 · Q4_K_M", "size": "≈14.3 GB",
     "url": "https://huggingface.co/bartowski/Mistral-Small-24B-Instruct-2501-GGUF/resolve/main/"
            "Mistral-Small-24B-Instruct-2501-Q4_K_M.gguf"},
    {"tier": "large", "name": "gemma-2 27B it · Q4_K_M", "size": "≈16.6 GB",
     "url": "https://huggingface.co/bartowski/gemma-2-27b-it-GGUF/resolve/main/"
            "gemma-2-27b-it-Q4_K_M.gguf"},
    {"tier": "large", "name": "Qwen3 30B-A3B (MoE) · Q4_K_M", "size": "≈18.6 GB",
     "url": "https://huggingface.co/Qwen/Qwen3-30B-A3B-GGUF/resolve/main/"
            "Qwen3-30B-A3B-Q4_K_M.gguf"},
    # ✦ v4.6: عائلة 30B-A3B MoE — تعمل بأقل من 8GB رام مع وضع Low RAM
    #   (الخبراء تُقرأ من القرص) — مرايا unsloth (الرسمية gated) فُحصت 200
    {"tier": "large", "name": "Qwen3 30B-A3B Instruct 2507 (MoE) · Q4_K_M",
     "size": "≈18.6 GB",
     "url": "https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF/"
            "resolve/main/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf"},
    {"tier": "large", "name": "Qwen3 30B-A3B Thinking 2507 (MoE) · Q4_K_M",
     "size": "≈18.6 GB",
     "url": "https://huggingface.co/unsloth/Qwen3-30B-A3B-Thinking-2507-GGUF/"
            "resolve/main/Qwen3-30B-A3B-Thinking-2507-Q4_K_M.gguf"},
    {"tier": "large", "name": "Qwen3 Coder 30B-A3B (MoE) · Q4_K_M",
     "size": "≈18.6 GB",
     "url": "https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF/"
            "resolve/main/Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf"},
    {"tier": "large", "name": "Qwen3 32B · Q4_K_M", "size": "≈19.8 GB",
     "url": "https://huggingface.co/Qwen/Qwen3-32B-GGUF/resolve/main/"
            "Qwen3-32B-Q4_K_M.gguf"},
    {"tier": "large", "name": "QwQ 32B · Q4_K_M", "size": "≈19.9 GB",
     "url": "https://huggingface.co/Qwen/QwQ-32B-GGUF/resolve/main/"
            "qwq-32b-q4_k_m.gguf"},
    {"tier": "large", "name": "Qwen2.5 32B Instruct · Q4_K_M", "size": "≈19.9 GB",
     "url": "https://huggingface.co/bartowski/Qwen2.5-32B-Instruct-GGUF/resolve/main/"
            "Qwen2.5-32B-Instruct-Q4_K_M.gguf"},
    {"tier": "large", "name": "Llama 3.3 70B Instruct · Q4_K_M", "size": "≈42.5 GB",
     "url": "https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF/resolve/main/"
            "Llama-3.3-70B-Instruct-Q4_K_M.gguf"},
    {"tier": "large", "name": "DeepSeek-R1-Distill-Llama-70B · Q4_K_M", "size": "≈42.5 GB",
     "url": "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Llama-70B-GGUF/resolve/main/"
            "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf"},
    # ── غير محجوبة (tier=unc) — v4.7: نسخ معدّلة من المجتمع أُزيل منها سلوك
    #    الرفض (Dolphin/Abliterated/Lexi/Stheno) — روابط فُحصت 200 بأحجام حقيقية
    {"tier": "unc", "name": "Dolphin 2.6 Mistral 7B DPO · Q4_K_M", "size": "≈4.4 GB",
     "url": "https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-dpo-GGUF/resolve/main/"
            "dolphin-2.6-mistral-7b-dpo.Q4_K_M.gguf"},
    {"tier": "unc", "name": "Dolphin 2.9 Llama-3 8B · Q4_K_M", "size": "≈4.9 GB",
     "url": "https://huggingface.co/bartowski/dolphin-2.9-llama3-8b-GGUF/resolve/main/"
            "dolphin-2.9-llama3-8b-Q4_K_M.gguf"},
    {"tier": "unc", "name": "Llama-3.1 8B Lexi Uncensored · Q4_K_M", "size": "≈4.9 GB",
     "url": "https://huggingface.co/bartowski/Llama-3.1-8B-Lexi-Uncensored-GGUF/resolve/main/"
            "Llama-3.1-8B-Lexi-Uncensored-Q4_K_M.gguf"},
    {"tier": "unc", "name": "Llama-3.1 8B Instruct Abliterated · Q4_K_M", "size": "≈4.9 GB",
     "url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-abliterated-GGUF/resolve/main/"
            "Meta-Llama-3.1-8B-Instruct-abliterated-Q4_K_M.gguf"},
    {"tier": "unc", "name": "L3-8B-Stheno v3.2 · Q4_K_M", "size": "≈4.9 GB",
     "url": "https://huggingface.co/bartowski/L3-8B-Stheno-v3.2-GGUF/resolve/main/"
            "L3-8B-Stheno-v3.2-Q4_K_M.gguf"},
    {"tier": "unc", "name": "Dolphin 2.7 Mixtral 8x7B · Q4_K_M", "size": "≈26.4 GB",
     "url": "https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF/resolve/main/"
            "dolphin-2.7-mixtral-8x7b.Q4_K_M.gguf"},
]


def _llm_dl_dir(kind: str) -> str:
    """مجلد التنزيلات (bin/models) — يجرّب الكتابة بجانب toolbox.py ثم المنزل."""
    if getattr(_llm_dl_dir, "_root", None) is None:
        root = None
        for base in (os.path.join(APP_DIR, "toolbox_data"),
                     os.path.join(os.path.expanduser("~"), ".ultimate_toolbox")):
            try:
                os.makedirs(base, exist_ok=True)
                probe = os.path.join(base, ".probe")
                with open(probe, "w") as f:
                    f.write("x")
                os.remove(probe)
                root = base
                break
            except Exception:
                continue
        _llm_dl_dir._root = root or os.getcwd()
    d = os.path.join(_llm_dl_dir._root, kind)
    os.makedirs(d, exist_ok=True)
    return d


def _llm_fetch_json(url: str, timeout: float = 25.0) -> dict:
    """GET JSON مع User-Agent واضح (GitHub API يرفض الطلبات بلا UA)."""
    req = urllib.request.Request(url, headers={
        "User-Agent": _LLM_UA, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def _llm_platform() -> str:
    return {"win32": "win", "darwin": "macos"}.get(sys.platform, "linux")


def _llm_arch() -> str:
    return "arm64" if platform.machine().lower() in ("arm64", "aarch64") else "x64"


def _llm_has_cuda() -> bool:
    """كشف تعريف NVIDIA عبر تحميل مكتبة CUDA مباشرة — بلا مكتبات خارجية."""
    try:
        if os.name == "nt":
            ctypes.CDLL("nvcuda.dll")
            return True
        ctypes.CDLL("libcuda.so.1")
        return True
    except Exception:
        return False


def _llm_choose_asset(assets: List[Dict[str, Any]], build: str = "auto") -> Dict[str, Any]:
    """اختيار أصل llama.cpp المناسب للمنصّة والنسخة المطلوبة."""
    plat, arch = _llm_platform(), _llm_arch()

    def pick(*subs: str) -> Optional[Dict[str, Any]]:
        for a in assets:
            n = str(a.get("name", "")).lower()
            if all(s in n for s in subs) and n.endswith((".zip", ".tar.gz")):
                return a
        return None

    if plat == "win":
        if build == "auto":
            a = pick("bin-win-cuda", "-x64") if _llm_has_cuda() else None
            return (a or pick("bin-win-cpu", "-x64")
                    or pick("bin-win-vulkan", "-x64"))
        return pick({"cpu": "bin-win-cpu", "cuda": "bin-win-cuda",
                     "vulkan": "bin-win-vulkan"}.get(build, "bin-win-cpu"),
                    "-x64")
    if plat == "linux":
        return pick("bin-ubuntu-x64")
    return pick("bin-macos-arm64") if arch == "arm64" else pick("bin-macos-x64")


def _llm_download(url: str, dest: str,
                  progress: Optional[Callable[[float, float, float], None]] = None,
                  stop_ev: Optional[threading.Event] = None,
                  timeout: float = 90.0) -> Optional[str]:
    """تنزيل ملف إلى dest عبر .part ثم إعادة تسمية — يرجع None عند الإلغاء.

    progress(done_bytes, total_bytes, speed_bps) يُستدعى بحد أقصى ~3 مرات/ثانية.
    urllib يتبع التحويلات تلقائيًا (روابط Hugging Face resolve تُحوَّل إلى CDN).
    """
    part = dest + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": _LLM_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r, \
                open(part, "wb") as f:
            total = int(r.headers.get("Content-Length") or 0)
            done, t0, last = 0, time.time(), 0.0
            while True:
                if stop_ev is not None and stop_ev.is_set():
                    f.close()
                    try:
                        os.remove(part)
                    except Exception:
                        pass
                    return None
                b = r.read(1 << 18)
                if not b:
                    break
                f.write(b)
                done += len(b)
                now = time.time()
                if progress is not None and (now - last) >= 0.3:
                    last = now
                    progress(float(done), float(total),
                             done / max(1e-9, now - t0))
            if progress is not None:
                progress(float(done), float(total or done),
                         done / max(1e-9, time.time() - t0))
        os.replace(part, dest)
        return dest
    except Exception:
        try:
            if os.path.isfile(part):
                os.remove(part)
        except Exception:
            pass
        raise


_LLM_KEEP = re.compile(
    r"(^|[/\\])(llama-server(\.exe)?|[\w.\-]+\.(dll|so([.\d]*)?|dylib))$", re.I)


def _llm_extract_server(archive: str, target_dir: str) -> str:
    """استخراج llama-server + المكتبات من zip/tar.gz (تسطيح + منع zip-slip).

    يرجع المسار الكامل للملف التنفيذي llama-server.
    """
    os.makedirs(target_dir, exist_ok=True)
    found = {"win": False, "posix": False}
    if archive.lower().endswith(".zip"):
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                base = os.path.basename(info.filename.replace("\\", "/"))
                if not base or not _LLM_KEEP.search(base):
                    continue
                with z.open(info) as src, \
                        open(os.path.join(target_dir, base), "wb") as dst:
                    shutil.copyfileobj(src, dst)
                if base.lower().endswith(".exe"):
                    found["win"] = True
                else:
                    found["posix"] = True
    else:                                                   # .tar.gz
        with tarfile.open(archive, "r:*") as t:
            for m in t.getmembers():
                if not m.isfile():
                    continue
                base = os.path.basename(m.name.replace("\\", "/"))
                if not base or not _LLM_KEEP.search(base):
                    continue
                with t.extractfile(m) as src, \
                        open(os.path.join(target_dir, base), "wb") as dst:
                    shutil.copyfileobj(src, dst)
                found["win" if base.lower().endswith(".exe") else "posix"] = True
    if not (found["win"] or found["posix"]):
        raise RuntimeError("llama-server binary not found in archive")
    # نفضّل ثنائي منصّتنا الحالية، ونقبل الآخر إن كان هو الموجود في الأرشيف
    pref = "llama-server.exe" if os.name == "nt" else "llama-server"
    alt = "llama-server" if os.name == "nt" else "llama-server.exe"
    exe = os.path.join(target_dir,
                       pref if os.path.isfile(os.path.join(target_dir, pref))
                       else alt)
    if os.name != "nt":                                     # بت التشغيل على Linux/macOS
        for n in os.listdir(target_dir):
            if _LLM_KEEP.search(n):
                try:
                    os.chmod(os.path.join(target_dir, n), 0o755)
                except Exception:
                    pass
    if not os.path.isfile(exe):
        raise RuntimeError(f"llama-server missing after extract: {exe}")
    return exe


def _llm_fetch_release(build: str = "auto",
                       progress: Optional[Callable[[float, float, float], None]] = None,
                       stop_ev: Optional[threading.Event] = None,
                       phase: Optional[Callable[[str], None]] = None
                       ) -> Optional[Tuple[str, str]]:
    """تنزيل أحدث llama.cpp جاهز من GitHub واستخراج llama-server — (مساره، رقم الإصدار).

    يرجع None عند الإلغاء عبر stop_ev. phase("info"/"download"/"extract") للتغذية الراجعة.
    """
    if phase:
        phase("info")
    info = _llm_fetch_json(_LLM_GH_API)
    assets = info.get("assets") or []
    if not assets:
        raise RuntimeError("no assets in latest llama.cpp release")
    asset = _llm_choose_asset(assets, build)
    if not asset:
        raise RuntimeError(
            f"no matching llama.cpp asset for {_llm_platform()}/{_llm_arch()}"
            f" build={build}")
    name = os.path.basename(str(asset.get("name") or "llama.zip"))
    url = asset.get("browser_download_url") or ""
    if not url:
        raise RuntimeError(f"asset has no download url: {name}")
    ddir = _llm_dl_dir("llama")
    dest = os.path.join(ddir, name)
    if phase:
        phase("download")
    r = _llm_download(url, dest, progress, stop_ev)
    if r is None:
        return None
    if phase:
        phase("extract")
    exe = _llm_extract_server(dest, ddir)
    try:
        os.remove(dest)                                     # الأرشيف لم يعد لازمًا
    except Exception:
        pass
    return exe, str(info.get("tag_name") or "?")


# ─────────────────────────────────────────────────────────────
# 【5.8】 خزائن مشفّرة (Vault) — v4.5: PBKDF2 + AES/Fernet أو HMAC-CTR مدمج
# ─────────────────────────────────────────────────────────────
_VLT_EXT = ".uvault"
_VLT_MAGIC_F = b"UVLT1F"          # صيغة Fernet (AES-128-CBC + HMAC) — إن توفّرت cryptography
_VLT_MAGIC_H = b"UVLT1H"          # الصيغة المدمجة: keystream HMAC-SHA256-CTR + MAC
_VLT_ITERS = 200_000              # تكرارات PBKDF2-HMAC-SHA256
_VLT_ITERS_H = 300_000            # الصيغة المدمجة: تكرارات أعلى لتعويض خفة HMAC عن KDFs المخصّصة
_VAULT_LOCK_SECS = 300            # قفل تلقائي بعد 5 دقائق خمول

# cryptography اختيارية تمامًا — غيابها يُسقط تلقائيًا إلى الصيغة المدمجة
try:
    from cryptography.fernet import Fernet as _Fernet
    _HAS_FERNET = True
except Exception:
    _Fernet = None                 # type: ignore
    _HAS_FERNET = False


def _vault_dir() -> str:
    """مجلد الخزائن — يعيد استخدام منطق الجذر القابل للكتابة في _llm_dl_dir."""
    return _llm_dl_dir("vaults")


def _vault_keystream(key: bytes, iv: bytes, n: int) -> bytes:
    """تدفّق مفاتيح HMAC-SHA256 بوضع العدّاد (CTR) — بديل مدمج بلا اعتمادات.

    keystream_i = HMAC-SHA256(key, iv || counter_i) — آمن عمليًا ما دام HMAC-SHA256
    دالةً شبه عشوائية، ويُدمج مع MAC (encrypt-then-MAC) أدناه.
    """
    out = bytearray()
    counter = 0
    while len(out) < n:
        out += hmac.new(key, iv + counter.to_bytes(8, "big"),
                        hashlib.sha256).digest()
        counter += 1
    return bytes(out[:n])


def _vault_xor(data: bytes, ks: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, ks))


def vault_encrypt(data: bytes, password: str,
                  iters: Optional[int] = None) -> bytes:
    """تشفير bytes بكلمة السر — يرجع blob: magic + iters + salt (+iv) + tag + body.

    يستخدم Fernet (AES) إن توفّرت cryptography وإلا الشيفرة المدمجة.
    كل نص مشفّر مستقل (salt وiv عشوائيان في كل مرة).
    """
    if not password:
        raise ValueError("empty password")
    if _HAS_FERNET:
        iters = int(iters or _VLT_ITERS)
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                  salt, iters, dklen=32)
        token = _Fernet(base64.urlsafe_b64encode(key)).encrypt(data)
        return (_VLT_MAGIC_F + iters.to_bytes(4, "big") + salt
                + len(token).to_bytes(4, "big") + token)
    iters = int(iters or _VLT_ITERS_H)
    salt, iv = os.urandom(16), os.urandom(16)
    km = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                             salt, iters, dklen=64)
    k_enc, k_mac = km[:32], km[32:]
    ks = _vault_keystream(k_enc, iv, len(data))
    body = _vault_xor(data, ks)
    tag = hmac.new(k_mac, salt + iv + body, hashlib.sha256).digest()
    return _VLT_MAGIC_H + iters.to_bytes(4, "big") + salt + iv + tag + body


def vault_decrypt(blob: bytes, password: str) -> bytes:
    """فك تشفير blob — يرفع ValueError عند كلمة سر خاطئة أو تلف البيانات."""
    if not password:
        raise ValueError("empty password")
    try:
        if blob.startswith(_VLT_MAGIC_F):
            off = len(_VLT_MAGIC_F)
            iters = int.from_bytes(blob[off:off + 4], "big")
            salt = blob[off + 4:off + 20]
            tlen = int.from_bytes(blob[off + 20:off + 24], "big")
            token = blob[off + 24:off + 24 + tlen]
            if tlen <= 0 or len(token) != tlen:
                raise ValueError("corrupted vault file")
            key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                      salt, iters, dklen=32)
            try:
                return _Fernet(base64.urlsafe_b64encode(key)).decrypt(token)
            except Exception as e:
                raise ValueError("wrong master password") from e
        if blob.startswith(_VLT_MAGIC_H):
            off = len(_VLT_MAGIC_H)
            iters = int.from_bytes(blob[off:off + 4], "big")
            salt = blob[off + 4:off + 20]
            iv = blob[off + 20:off + 36]
            tag = blob[off + 36:off + 68]
            body = blob[off + 68:]
            km = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                     salt, iters, dklen=64)
            k_enc, k_mac = km[:32], km[32:]
            good = hmac.new(k_mac, salt + iv + body, hashlib.sha256).digest()
            if not hmac.compare_digest(good, tag):
                raise ValueError("wrong master password")
            return _vault_xor(body, _vault_keystream(k_enc, iv, len(body)))
        raise ValueError("not a vault file")
    except ValueError:
        raise
    except Exception as e:
        raise ValueError("corrupted vault file") from e


def _vault_genpw(length: int = 16) -> str:
    """توليد كلمة سر قوية بضمان حرف من كل فئة — عبر secrets (آمن تشفيريًا)."""
    pools = [string.ascii_lowercase, string.ascii_uppercase,
             string.digits, "!@#$%^&*()-_=+"]
    length = max(8, min(64, length))
    rnd = secrets.SystemRandom()
    chars = [rnd.choice(p) for p in pools]
    allp = "".join(pools)
    chars += [rnd.choice(allp) for _ in range(length - len(chars))]
    rnd.shuffle(chars)
    return "".join(chars)


# ─────────────────────────────────────────────────────────────
# 【6】 سجل الأدوات — 11 قسمًا
# ─────────────────────────────────────────────────────────────
@dataclass
class Tool:
    tid: str
    title: str          # المفتاح الإنجليزي
    section: str
    icon: str = "•"
    keywords: str = ""


TOOLS: List[Tool] = [
    # General
    Tool("dashboard", "Dashboard", "General", "📊", "cpu ram monitor"),
    Tool("settings", "Settings", "General", "⚙️", "language theme config"),
    Tool("about", "About", "General", "ℹ️", "version help"),
    # System
    Tool("sysinfo", "System Information", "System", "🖥️", "cpu memory disk battery"),
    Tool("procs", "Process Manager", "System", "🧩", "kill task pid"),
    Tool("network", "Network Info", "System", "🌐", "ip ping local public"),
    Tool("dns", "DNS Lookup", "System", "🔎", "domain resolve host"),
    Tool("headers", "HTTP Headers", "System", "📨", "inspect response"),
    Tool("tz", "Time Zones", "System", "🕓", "timezone utc convert"),
    # Files
    Tool("organizer", "File Organizer", "Files", "🗂️", "sort extension usb"),
    Tool("dupes", "Duplicate Finder", "Files", "👯", "duplicate hash"),
    Tool("rename", "Bulk Rename", "Files", "✏️", "batch prefix suffix"),
    Tool("splitmerge", "Split & Merge", "Files", "✂️", "chunk join parts"),
    Tool("checksum", "Checksum", "Files", "🔐", "md5 sha256 verify"),
    Tool("zip", "ZIP Tools", "Files", "🗜️", "compress extract archive"),
    Tool("b64file", "Base64 File", "Files", "📦", "encode decode binary"),
    Tool("csvjson", "CSV ⇄ JSON", "Files", "🔁", "convert table"),
    # Text
    Tool("counter", "Text Counter", "Text", "🔢", "words chars reading time"),
    Tool("transform", "Text Transform", "Text", "🔤", "upper lower sort unique"),
    Tool("diff", "Text Diff", "Text", "📑", "compare changes"),
    Tool("encode", "Encode / Decode", "Text", "🧬", "base64 url hex binary morse"),
    Tool("jsontools", "JSON Tools", "Text", "{}", "format minify validate"),
    Tool("regex", "Regex Tester", "Text", "🪄", "pattern match groups"),
    Tool("urlan", "URL Analyzer", "Text", "🔗", "query params parse"),
    # Security
    Tool("vault", "Vault", "Security", "🛡️",
         "password manager encrypted secrets safe store keeper"),
    Tool("password", "Password Generator", "Security", "🔑", "entropy strong random"),
    Tool("hash", "Text Hash", "Security", "#️⃣", "md5 sha"),
    Tool("uuidgen", "UUID Generator", "Security", "🆔", "guid v4 v1"),
    # Media
    Tool("color", "Color Converter", "Media", "🎨", "hex rgb hsl"),
    Tool("palette", "Color Palette", "Media", "🖌️", "harmony scheme"),
    Tool("qr", "QR Code", "Media", "🔳", "barcode generate"),
    Tool("image", "Image Tools", "Media", "🖼️", "resize rotate grayscale convert"),
    # Calc & Time
    Tool("calc", "Calculator", "Calc & Time", "🧮", "math ast safe"),
    Tool("units", "Unit Converter", "Calc & Time", "📏", "length weight temperature"),
    Tool("datetime", "Date & Time", "Calc & Time", "📅", "age difference timestamp"),
    Tool("timer", "Timer", "Calc & Time", "⏱️", "stopwatch countdown"),
    Tool("pomodoro", "Pomodoro", "Calc & Time", "🍅", "focus 25 5"),
    # Productivity
    Tool("todo", "Todo List", "Productivity", "✅", "tasks checklist"),
    Tool("notes", "Notes", "Productivity", "📝", "scratchpad memo"),
    Tool("backup", "Backup", "Productivity", "💾", "export import settings"),
    # Developer
    Tool("polybuild", "PolyBuild", "Developer", "🏗️", "build compile package exe apk"),
    Tool("ports", "Port Scanner", "Developer", "📡", "scan tcp open"),
    Tool("httpclient", "HTTP Client", "Developer", "🛰️", "request get post api"),
    Tool("llm", "Local LLM", "Developer", "🦙", "gguf llama local ai chat offline model chatbot"),
    # APIs
    Tool("weather", "Weather", "APIs", "⛅", "forecast temperature"),
    Tool("currency", "Currency", "APIs", "💱", "exchange rate fx"),
    Tool("translate", "Translate", "APIs", "🌍", "mymemory language"),
    Tool("geoip", "GeoIP", "APIs", "📍", "ip location"),
    Tool("github", "GitHub", "APIs", "🐙", "user repo"),
    Tool("crypto", "Crypto Prices", "APIs", "₿", "bitcoin coingecko"),
    Tool("news", "News", "APIs", "📰", "headlines newsapi"),
    Tool("shorten", "URL Shortener", "APIs", "🔗", "is.gd tiny"),
    Tool("fun", "Fun APIs", "APIs", "🎲", "joke advice cat activity"),
    Tool("ai", "AI Assistant", "APIs", "🤖", "openai chat llm"),
    # Data
    Tool("fake", "Fake Data", "Data", "🧪", "mock names emails"),
    Tool("picker", "Random Picker", "Data", "🎯", "choose shuffle lottery"),
    Tool("lorem", "Lorem Ipsum", "Data", "📄", "placeholder text"),
]

SECTIONS = ["General", "System", "Files", "Text", "Security", "Media",
            "Calc & Time", "Productivity", "Developer", "APIs", "Data"]
TOOL_BY_ID = {t.tid: t for t in TOOLS}

DEFAULT_SETTINGS = {
    "lang": "en",
    "appearance": "Dark",
    "favorites": [],
    "recent": [],
    "collapsed": [],
    "hint_scroll_shown": False,   # ✦ v4.0: هل عُرض تلميح "اسحب للأسفل" من قبل؟
    "polybuild_path": "",
    "llm_recent": [],             # ✦ v4.1: أحدث نماذج GGUF المستخدمة
    "llm_params": {},             # ✦ v4.1: آخر إعدادات ضبط الـ LLM المحلي
    "api_keys": {"openweather": "", "newsapi": "", "ipinfo": "",
                 "github": "", "openai": "", "openai_base": "https://api.openai.com/v1"},
    "presets": {},
}


# ─────────────────────────────────────────────────────────────
# 【7】 الـ class الرئيسي
# ─────────────────────────────────────────────────────────────
class ToolboxApp(ctk.CTk):
    """التطبيق الرئيسي: شريط جانبي + منطقة محتوى + توستات + لوحة أوامر."""

    # ── الإقلاع ────────────────────────────────────────────
    def __init__(self):
        super().__init__()
        self.settings: Dict[str, Any] = {**DEFAULT_SETTINGS, **jload(F_SETTINGS, {})}
        for k, v in DEFAULT_SETTINGS.items():          # دمج المفاتيح الناقصة
            if isinstance(v, dict):
                self.settings[k] = {**v, **(self.settings.get(k) or {})}
        self.lang: str = self.settings.get("lang", "en")
        self.current: str = "dashboard"
        self.section_frames: Dict[str, ctk.CTkFrame] = {}
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        self._toasts: List[ctk.CTkFrame] = []
        self._stop_flags: Dict[str, threading.Event] = {}
        self._timers: Dict[str, Any] = {}
        self.cpu_hist: List[float] = [0.0] * 60
        self.ram_hist: List[float] = [0.0] * 60
        self._palette_win: Optional[ctk.CTkToplevel] = None
        self._pb_proc: Optional[subprocess.Popen] = None
        self._ui_q: queue.Queue = queue.Queue()
        self._fav_btn: Optional[ctk.CTkButton] = None
        # ✦ v4.0: حالة القائمة الجانبية القابلة للتمرير
        self._search_after = None          # مؤقّت debounce للبحث
        self._nav_hint = None              # تلميح "اسحب للأسفل ↓" (أول تشغيل)
        self.nav_canvas = None             # الكانفاس الداخلي للقائمة
        self.nav_scrollbar = None          # شريط التمرير الداخلي
        self._ctk_wheel_native = True      # هل يدير CTk 6.x العجلة أصلًا؟
        self._nav_font_header = None       # خطوط مخزّنة لأداء أسرع
        self._nav_font_item = None
        # ✦ v4.1: حالة الـ LLM المحلي — الموديل يبقى محمّلًا عند التنقل بين الأدوات
        # ✦ v4.3: backend=local/server، url وproc لخادم llama.cpp المُشغَّل تلقائيًا
        self._llm: Dict[str, Any] = {"model": None, "path": "", "stop": None,
                                     "busy": False, "hist": [],
                                     "backend": "local", "url": "",
                                     "proc": None}
        # ✦ v4.2: نظام الإضافات — tid → دالة بناء الصفحة من plugins/
        self._plugin_pages: Dict[str, Callable] = {}
        # ✦ v4.5: حالة الخزائن المشفّرة — تُمسح كلمة السر من الذاكرة عند القفل
        self._vault: Dict[str, Any] = {"name": None, "pw": "", "entries": [],
                                       "unlocked": False, "last_touch": 0.0,
                                       "edit_idx": None}

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1280x800")
        self.minsize(1000, 640)
        ctk.set_appearance_mode(self.settings.get("appearance", "Dark"))

        self._build_layout()
        self._bind_keys()
        self.show_tool(self.current)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(1200, self._tick_monitor)
        self.after(40, self._pump_ui)
        # ✦ v4.2: ربط واجهة الإضافات ثم تحميل plugins/ ثم تحديث القائمة
        try:
            toolbox_api._bind(self, TRANSLATIONS, _T_CACHE)
            self._load_plugins()
            self._rebuild_nav()
        except Exception:
            traceback.print_exc()

    # ── ترجمة مختصرة
    def t(self, key: str) -> str:
        return translate(key, self.lang)

    @property
    def rtl(self) -> bool:
        return self.lang in RTL_LANGS

    # ── التخطيط العام
    def _build_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # الشريط العلوي
        top = ctk.CTkFrame(self, height=52, corner_radius=0,
                           fg_color=CC("surface2"))
        top.grid(row=0, column=0, columnspan=2, sticky="ew")
        top.grid_propagate(False)
        top.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(top, text=f"  ⬢  {APP_NAME}  v{APP_VERSION}",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=CC("primary")).grid(row=0, column=0, padx=(12, 0), pady=10)

        self.title_label = ctk.CTkLabel(top, text="", font=ctk.CTkFont(size=14))
        self.title_label.grid(row=0, column=1, sticky="e" if self.rtl else "w", padx=16)

        right = ctk.CTkFrame(top, fg_color="transparent")
        right.grid(row=0, column=2, padx=10)
        ctk.CTkButton(right, text="⌘ Ctrl+K", width=90, height=30,
                      fg_color=CC("surface"), hover_color=CC("border"),
                      text_color=CC("muted"),
                      command=self.open_palette).pack(side="left", padx=4)
        self.lang_menu = ctk.CTkOptionMenu(
            right, width=120, height=30,
            values=[LANG_NAMES[c] for c in LANG_NAMES],
            command=self._on_lang_change)
        self.lang_menu.set(LANG_NAMES.get(self.lang, "English"))
        self.lang_menu.pack(side="left", padx=4)
        self.mode_switch = ctk.CTkSwitch(right, text="☾", width=48,
                                         command=self._toggle_mode)
        if ctk.get_appearance_mode().lower() == "dark":
            self.mode_switch.select()
        self.mode_switch.pack(side="left", padx=4)

        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0,
                                    fg_color=CC("surface"))
        self.sidebar.grid(row=1, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.search_entry = ctk.CTkEntry(self.sidebar,
                                         placeholder_text=self.t("Search tools…"),
                                         height=34)
        self.search_entry.pack(fill="x", padx=8, pady=(6, 8))
        # ✦ v4.0: debounce للبحث + Escape يمسح البحث
        self.search_entry.bind("<KeyRelease>", self._on_search_key)
        self.search_entry.bind("<Escape>", self._clear_search)

        # ✦ v4.0: قائمة جانبية قابلة للتمرير — كل الأدوات متاحة حتى في النوافذ القصيرة
        self.nav_holder = ctk.CTkScrollableFrame(
            self.sidebar, fg_color="transparent",
            scrollbar_button_color=CC("border"),
            scrollbar_button_hover_color=CC("primary"))
        self.nav_holder.pack(fill="both", expand=True)
        self._setup_nav_scroll()

        # منطقة المحتوى
        self.content_wrap = ctk.CTkFrame(self, fg_color=CC("bg"), corner_radius=0)
        self.content_wrap.grid(row=1, column=1, sticky="nsew")
        self.content_wrap.grid_rowconfigure(0, weight=1)
        self.content_wrap.grid_columnconfigure(0, weight=1)

        # شريط الحالة
        self.status = ctk.CTkLabel(self, text="", height=24,
                                   text_color=CC("muted"),
                                   font=ctk.CTkFont(size=11))
        self.status.grid(row=2, column=0, columnspan=2,
                         sticky="e" if self.rtl else "w", padx=12)

        self._rebuild_nav()
        # ✦ v4.0: فحص overflow وعرض تلميح "اسحب للأسفل ↓" عند أول تشغيل فقط
        self.after(900, self._maybe_show_nav_hint)

    # ── بناء الشريط الجانبي (مع الطي والبحث والمفضلة والحديثة)
    def _rebuild_nav(self, scroll_to_top: bool = False):
        # ✦ v4.0: حفظ موضع التمرير قبل الإعادة — لا قفز مزعج عند الطي/التوسيع
        frac = 0.0
        if not scroll_to_top and self.nav_canvas is not None:
            try:
                frac = self.nav_canvas.yview()[0]
            except Exception:
                frac = 0.0
        for w in self.nav_holder.winfo_children():
            w.destroy()
        self.nav_buttons.clear()
        q = (self.search_entry.get() or "").strip().lower() if hasattr(self, "search_entry") else ""

        def match(tool: Tool) -> bool:
            if not q:
                return True
            hay = f"{tool.title} {self.t(tool.title)} {tool.keywords} {tool.tid}".lower()
            if q in hay:
                return True
            # ✦ v4.0: بحث ضبابي عبر difflib — مطابقة كلمة-بكلمة ليتحمّل
            #   الأخطاء المطبعية في استعلامات كلمة واحدة أو متعددة
            tokens = set(hay.split())
            for qw in q.split():
                if len(qw) >= 3 and difflib.get_close_matches(qw, tokens, n=1, cutoff=0.75):
                    return True
            return False

        favs = [f for f in self.settings.get("favorites", []) if f in TOOL_BY_ID]
        if favs and not q:
            self._nav_header(f"⭐ {self.t('Favorites')}")
            for tid in favs:
                self._nav_button(TOOL_BY_ID[tid])

        recents = [r for r in self.settings.get("recent", []) if r in TOOL_BY_ID][:5]
        if recents and not q:
            self._nav_header(f"🕘 {self.t('Recent')}")
            for tid in recents:
                self._nav_button(TOOL_BY_ID[tid])

        collapsed = set(self.settings.get("collapsed", []))
        visible_count = 0
        for sec in SECTIONS:
            items = [t for t in TOOLS if t.section == sec and match(t)]
            if not items:
                continue
            visible_count += len(items)
            is_open = q != "" or sec not in collapsed
            self._nav_header(f"{'▾' if is_open else '▸'} {self.t(sec)}",
                             cmd=lambda s=sec: self._toggle_section(s))
            if is_open:
                for tool in items:
                    self._nav_button(tool)

        # ✦ v4.0: عدّاد نتائج البحث في شريط الحالة
        if q:
            self.set_status(self.t("{n} tools found").format(n=visible_count))

        # ✦ v4.0: موضع التمرير — للأعلى عند البحث، أو الحفاظ عند الطي/التوسيع
        if scroll_to_top:
            self._nav_scroll_top()
        elif frac > 0:
            self._nav_scroll_restore(frac)
        # ✦ v4.0: تحديث الإخفاء التلقائي لشريط التمرير بعد إعادة البناء
        self.after(70, self._update_nav_scrollbar)

    # ── v4.0: إدارة تمرير القائمة الجانبية ─────────────────────
    def _setup_nav_scroll(self):
        """تهيئة القائمة القابلة للتمرير: سماكة 6px + إخفاء تلقائي + خطوط مخزّنة."""
        try:
            self.nav_canvas = getattr(self.nav_holder, "_parent_canvas", None)
            self.nav_scrollbar = getattr(self.nav_holder, "_scrollbar", None)
            self._ctk_wheel_native = hasattr(self.nav_holder, "_mouse_wheel_all")
            # خطوط مخزّنة: توفير ~70 إنشاء خط في كل إعادة بناء
            self._nav_font_header = ctk.CTkFont(size=12, weight="bold")
            self._nav_font_item = ctk.CTkFont(size=13)
            try:
                if self.nav_scrollbar is not None:
                    self.nav_scrollbar.configure(width=6)      # شريط رفيع 6px
            except Exception:
                pass
            if self.nav_canvas is not None:
                # فحص الإخفاء التلقائي عند تغيّر حجم النافذة أو المحتوى
                self.nav_canvas.bind("<Configure>",
                                     lambda e: self.after(60, self._update_nav_scrollbar),
                                     add="+")
            # ربط احتياطي للعجلة (customtkinter < 6) — CTk 6.x يديرها أصلًا حتى فوق الأزرار
            if not self._ctk_wheel_native:
                self._bind_nav_wheel(self.nav_holder)
                if self.nav_canvas is not None:
                    self._bind_nav_wheel(self.nav_canvas)
        except Exception:
            pass

    def _bind_nav_wheel(self, widget):
        """ربط احتياطي لعجلة الفأرة (لإصدارات customtkinter الأقدم من 6)."""
        if getattr(self, "_ctk_wheel_native", False):
            return
        try:
            if os.name == "posix" and sys.platform != "darwin":
                widget.bind("<Button-4>", self._nav_wheel_scroll, add="+")
                widget.bind("<Button-5>", self._nav_wheel_scroll, add="+")
            else:
                widget.bind("<MouseWheel>", self._nav_wheel_scroll, add="+")
        except Exception:
            pass

    def _nav_wheel_scroll(self, event):
        """تمرير القائمة بعجلة الفأرة (نفس معادلات CTk 6) — يعمل فوق الأزرار."""
        try:
            canvas = self.nav_canvas
            if canvas is None:
                return
            if sys.platform.startswith("win"):
                canvas.yview("scroll", -int(event.delta / 6), "units")
            elif sys.platform == "darwin":
                canvas.yview("scroll", -event.delta, "units")
            else:
                canvas.yview_scroll(-1 if getattr(event, "num", 0) == 4 else 1, "units")
            self._hide_nav_hint()
            return "break"
        except Exception:
            return None

    def _update_nav_scrollbar(self):
        """إخفاء شريط التمرير تلقائيًا عندما لا تكون هناك حاجة له."""
        try:
            canvas = self.nav_canvas
            sb = self.nav_scrollbar
            if canvas is None or sb is None:
                return
            if canvas.yview() == (0.0, 1.0):
                if sb.winfo_manager():
                    sb.grid_remove()
            else:
                if not sb.winfo_manager():
                    sb.grid()
        except Exception:
            pass

    def _nav_scroll_top(self):
        """تمرير القائمة إلى الأعلى (يُستدعى عند البحث)."""
        try:
            if self.nav_canvas is not None:
                self.nav_canvas.yview_moveto(0.0)
        except Exception:
            pass

    def _nav_scroll_restore(self, frac: float):
        """استعادة موضع التمرير بعد إعادة البناء (مع انتظار اكتمال التخطيط)."""
        try:
            canvas = self.nav_canvas
            if canvas is None:
                return

            def _apply():
                try:
                    canvas.update_idletasks()
                    canvas.yview_moveto(max(0.0, min(1.0, frac)))
                except Exception:
                    pass

            self.after(10, _apply)
        except Exception:
            pass

    def _on_search_key(self, event=None):
        """debounce للبحث (180ms) — سلاسة الكتابة مع 60+ أداة."""
        if getattr(event, "keysym", "") in ("Up", "Down", "Left", "Right", "Return", "Escape"):
            return
        if self._search_after is not None:
            try:
                self.after_cancel(self._search_after)
            except Exception:
                pass
        self._search_after = self.after(180, self._search_fire)

    def _search_fire(self):
        self._search_after = None
        # ✦ البحث يمرّر القائمة لأعلى تلقائيًا
        self._rebuild_nav(scroll_to_top=True)

    def _clear_search(self, event=None):
        """Escape في خانة البحث يمسحها ويعيد القائمة كاملة."""
        self.search_entry.delete(0, "end")
        self._rebuild_nav(scroll_to_top=True)

    def _maybe_show_nav_hint(self):
        """تلميح "اسحب للأسفل ↓" عند أول تشغيل فقط إذا وُجد overflow."""
        try:
            if self.settings.get("hint_scroll_shown"):
                return
            canvas = self.nav_canvas
            if canvas is None or not canvas.winfo_ismapped():
                self.after(600, self._maybe_show_nav_hint)      # التخطيط لم يكتمل بعد
                return
            bbox = canvas.bbox("all")
            if not bbox:
                return
            if bbox[3] - bbox[1] <= canvas.winfo_height() + 4:
                # لا overflow أبدًا (شاشة كبيرة) — لا داعي للتلميح مستقبلًا
                self.settings["hint_scroll_shown"] = True
                self.save_settings()
                return
            self._nav_hint = ctk.CTkLabel(
                self.sidebar, text=self.t("Scroll for more ↓"),
                height=28, corner_radius=8,
                fg_color=CC("primary"), text_color="#ffffff",
                font=ctk.CTkFont(size=12, weight="bold"))
            self._nav_hint.place(relx=0.5, rely=0.96, anchor="s", relwidth=0.72)
            self.settings["hint_scroll_shown"] = True
            self.save_settings()
            self.after(5200, self._hide_nav_hint)
            # يختفي عند أول تمرير أيضًا
            for seq in (("<MouseWheel>",) if os.name != "posix" or sys.platform == "darwin"
                        else ("<Button-4>", "<Button-5>")):
                self.bind_all(seq, lambda e: self._hide_nav_hint(), add="+")
        except Exception:
            pass

    def _hide_nav_hint(self):
        try:
            if self._nav_hint is not None:
                self._nav_hint.place_forget()
                self._nav_hint.destroy()
                self._nav_hint = None
        except Exception:
            pass

    def _nav_header(self, text: str, cmd: Optional[Callable] = None):
        b = ctk.CTkButton(self.nav_holder, text=text, anchor="e" if self.rtl else "w",
                          height=28, fg_color="transparent",
                          hover_color=CC("surface2"), text_color=CC("muted"),
                          font=self._nav_font_header,
                          command=cmd or (lambda: None))
        b.pack(fill="x", padx=6, pady=(8, 2))
        self._bind_nav_wheel(b)

    def _nav_button(self, tool: Tool):
        active = tool.tid == self.current
        b = ctk.CTkButton(
            self.nav_holder, text=f"  {tool.icon}  {self.t(tool.title)}",
            anchor="e" if self.rtl else "w", height=32,
            fg_color=CC("primary") if active else "transparent",
            hover_color=CC("primary_h") if active else CC("surface2"),
            text_color=("#ffffff" if active else C("text")),
            font=self._nav_font_item,
            command=lambda tid=tool.tid: self.show_tool(tid))
        b.pack(fill="x", padx=6, pady=1)
        self.nav_buttons[tool.tid] = b
        self._bind_nav_wheel(b)

    def _toggle_section(self, sec: str):
        col = set(self.settings.get("collapsed", []))
        col.symmetric_difference_update({sec})
        self.settings["collapsed"] = sorted(col)
        self.save_settings()
        self._rebuild_nav()

    # ── الاختصارات
    def _bind_keys(self):
        self.bind("<Control-k>", lambda e: self.open_palette())
        self.bind("<Control-K>", lambda e: self.open_palette())
        self.bind("<Control-s>", lambda e: (self.save_settings(),
                                            self.toast(self.t("Done"), "ok")))
        self.bind("<Escape>", lambda e: self._close_palette())
        self.bind("<Control-f>", lambda e: self.search_entry.focus_set())
        # ✦ v4.0: اختصارات إضافية
        self.bind("<F1>", lambda e: self.show_tool("about"))
        self.bind("<Control-comma>", lambda e: self.show_tool("settings"))
        self.bind("<Control-d>", self._kbd_toggle_mode)
        self.bind("<Control-D>", self._kbd_toggle_mode)

    def _kbd_toggle_mode(self, event=None):
        """Ctrl+D: تبديل الوضع الداكن/الفاتح."""
        try:
            self.mode_switch.toggle()
        except Exception:
            pass
        self._toggle_mode()

    # ── تبديل الوضع واللغة
    def _toggle_mode(self):
        mode = "Dark" if self.mode_switch.get() else "Light"
        ctk.set_appearance_mode(mode)
        self.settings["appearance"] = mode
        self.save_settings()
        self.show_tool(self.current)

    def _on_lang_change(self, display_name: str):
        code = next((c for c, n in LANG_NAMES.items() if n == display_name), "en")
        self.lang = code
        self.settings["lang"] = code
        self.save_settings()
        self.search_entry.configure(placeholder_text=self.t("Search tools…"))
        self._rebuild_nav(scroll_to_top=True)
        self.show_tool(self.current)          # تبديل فوري بلا إعادة تشغيل
        self.toast(f"{LANG_NAMES[code]} ✓", "ok")

    # ── الحفظ والإغلاق
    def save_settings(self):
        jsave(F_SETTINGS, self.settings)

    def on_close(self):
        for flag in self._stop_flags.values():
            flag.set()
        try:                                   # ✦ v4.1: إيقاف التوليد وتحرير موديل LLM
            if self._llm.get("stop") is not None:
                self._llm["stop"].set()
            self._llm["model"] = None
            _pr = self._llm.get("proc")        # ✦ v4.3: إيقاف llama-server المُشغَّل تلقائيًا
            if _pr is not None and _pr.poll() is None:
                _pr.terminate()
                self._llm["proc"] = None
        except Exception:
            pass
        gc.collect()
        self._cancel_timers()
        self.save_settings()
        try:
            if self._pb_proc and self._pb_proc.poll() is None:
                self._pb_proc.terminate()
        except Exception:
            pass
        self.destroy()

    # ── قناة آمنة لتحديث الواجهة من الخيوط ─────────────────
    def _ui(self, fn: Callable, *args, **kwargs):
        """جدولة استدعاء في الخيط الرئيسي — آمنة الاستدعاء من أي thread."""
        self._ui_q.put((fn, args, kwargs))

    def _pump_ui(self):
        """تنفيذ استدعاءات الواجهة المؤجلة كل 40ms — يغني عن after(0) من الخيوط."""
        try:
            while True:
                fn, args, kwargs = self._ui_q.get_nowait()
                try:
                    fn(*args, **kwargs)
                except Exception:
                    pass
        except queue.Empty:
            pass
        self.after(40, self._pump_ui)

    # ── التوستات والنوافذ الموحّدة ─────────────────────────
    def toast(self, msg: str, kind: str = "info", ms: int = 2600):
        """إشعار سريع أسفل النافذة."""
        colors = {"ok": CC("ok"), "err": CC("err"), "warn": CC("warn"),
                  "info": CC("surface2")}
        f = ctk.CTkFrame(self, fg_color=colors.get(kind, CC("surface2")),
                         corner_radius=8, border_width=1, border_color=CC("border"))
        ctk.CTkLabel(f, text=msg, text_color=("#111111", "#ffffff") if kind != "info" else CC("text"),
                     font=ctk.CTkFont(size=12)).pack(padx=14, pady=8)
        idx = len(self._toasts)
        f.place(relx=0.99, rely=0.96 - idx * 0.07, anchor="se")
        self._toasts.append(f)

        def kill():
            try:
                f.destroy()
                self._toasts.remove(f)
            except Exception:
                pass
        self.after(ms, kill)

    def popup(self, title: str, message: str):
        """نافذة تنبيه موحّدة."""
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("460x240")
        win.transient(self)
        ctk.CTkLabel(win, text=title, font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=CC("primary")).pack(pady=(16, 6))
        box = ctk.CTkTextbox(win, height=120)
        box.pack(fill="both", expand=True, padx=16, pady=6)
        box.insert("1.0", message)
        box.configure(state="disabled")
        ctk.CTkButton(win, text=self.t("Close"), command=win.destroy).pack(pady=10)
        win.after(120, win.lift)

    def set_status(self, text: str):
        try:
            self.status.configure(text=text)
        except Exception:
            pass

    def copy_text(self, text: str):
        """نسخ إلى الحافظة."""
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.toast(self.t("Copied to clipboard"), "ok")
        except Exception as e:
            self.toast(f"{self.t('Failed')}: {e}", "err")

    # ── تشغيل غير متزامن مع مؤشر تحميل ────────────────────
    def run_async(self, work: Callable[[], Any],
                  done: Optional[Callable[[Any], None]] = None,
                  label: Optional[ctk.CTkLabel] = None,
                  busy_text: Optional[str] = None):
        """تشغيل عملية طويلة في thread مع حالة نجاح/فشل."""
        busy = busy_text or self.t("Loading…")
        if label is not None:
            try:
                label.configure(text=f"⏳ {busy}", text_color=CC("warn"))
            except Exception:
                pass
        self.set_status(f"⏳ {busy}")

        def runner():
            try:
                res = work()
                self._ui(self._async_ok, res, done, label)
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                self._ui(self._async_err, err, label)

        threading.Thread(target=runner, daemon=True).start()

    def _async_ok(self, res, done, label):
        if label is not None:
            try:
                label.configure(text=f"✓ {self.t('Done')}", text_color=CC("ok"))
            except Exception:
                pass
        self.set_status(f"✓ {self.t('Done')}")
        if done:
            try:
                done(res)
            except Exception as e:
                self.toast(f"{self.t('Failed')}: {e}", "err")

    def _async_err(self, err: str, label):
        if label is not None:
            try:
                label.configure(text=f"✗ {err}", text_color=CC("err"))
            except Exception:
                pass
        self.set_status(f"✗ {err}")
        self.toast(err[:120], "err")

    # ── لوحة الأوامر Ctrl+K ───────────────────────────────
    def open_palette(self):
        if self._palette_win is not None and self._palette_win.winfo_exists():
            self._palette_win.lift()
            return
        win = ctk.CTkToplevel(self)
        self._palette_win = win
        win.title(self.t("Command palette"))
        win.geometry("560x420")
        win.transient(self)
        entry = ctk.CTkEntry(win, placeholder_text=self.t("Search tools…"), height=40,
                             font=ctk.CTkFont(size=15))
        entry.pack(fill="x", padx=12, pady=12)
        listf = ctk.CTkScrollableFrame(win, fg_color="transparent")
        listf.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        pal: Dict[str, Any] = {"tids": [], "btns": [], "sel": 0}

        def highlight():
            for i, b in enumerate(pal["btns"]):
                active = i == pal["sel"]
                b.configure(fg_color=CC("primary") if active else "transparent",
                            text_color=("#ffffff" if active else CC("text")))

        def refresh(*_):
            for w in listf.winfo_children():
                w.destroy()
            q = entry.get().strip().lower()
            hits = [t for t in TOOLS
                    if not q or q in f"{t.title} {self.t(t.title)} {t.keywords}".lower()][:30]
            pal["tids"], pal["btns"], pal["sel"] = [], [], 0
            for tool in hits:
                pal["tids"].append(tool.tid)
                b = ctk.CTkButton(
                    listf, text=f"{tool.icon}  {self.t(tool.title)}   ·   {self.t(tool.section)}",
                    anchor="e" if self.rtl else "w", height=32, fg_color="transparent",
                    hover_color=CC("primary"), text_color=CC("text"),
                    command=lambda tid=tool.tid: (self._close_palette(), self.show_tool(tid))
                )
                b.pack(fill="x", pady=1)
                pal["btns"].append(b)
            highlight()

        def move(d: int):
            if not pal["btns"]:
                return
            pal["sel"] = (pal["sel"] + d) % len(pal["btns"])
            highlight()

        def go(_=None):
            if pal["tids"]:
                self._close_palette()
                self.show_tool(pal["tids"][pal["sel"]])

        entry.bind("<KeyRelease>", refresh)
        entry.bind("<Return>", go)
        entry.bind("<Down>", lambda e: move(1))
        entry.bind("<Up>", lambda e: move(-1))
        win.bind("<Escape>", lambda e: self._close_palette())
        refresh()
        win.after(120, lambda: (win.lift(), entry.focus_set()))

    def _close_palette(self):
        if self._palette_win is not None and self._palette_win.winfo_exists():
            self._palette_win.destroy()
        self._palette_win = None

    # ── التنقل بين الأدوات ────────────────────────────────
    def show_tool(self, tid: str):
        """عرض صفحة الأداة وتحديث السجل والشريط الجانبي."""
        if tid not in TOOL_BY_ID:
            return
        if self.current == "llm" and self._llm.get("stop") is not None:
            try:
                self._llm["stop"].set()        # ✦ v4.1: مغادرة الصفحة توقف التوليد
            except Exception:
                pass
        self._cancel_timers()
        self.current = tid
        tool = TOOL_BY_ID[tid]

        rec = [r for r in self.settings.get("recent", []) if r != tid]
        rec.insert(0, tid)
        self.settings["recent"] = rec[:10]
        self.save_settings()

        for w in self.content_wrap.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self.content_wrap, fg_color="transparent")
        header.grid(row=0, column=0, sticky="new", padx=18, pady=(14, 0))
        self.content_wrap.grid_rowconfigure(0, weight=0)
        self.content_wrap.grid_rowconfigure(1, weight=1)
        side = "right" if self.rtl else "left"
        ctk.CTkLabel(header, text=f"{tool.icon}  {self.t(tool.title)}",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(side=side)
        fav = tid in self.settings.get("favorites", [])
        self._fav_btn = ctk.CTkButton(header, text="⭐" if fav else "☆", width=40,
                                      height=30, fg_color="transparent",
                                      hover_color=CC("surface2"),
                                      text_color=CC("warn") if fav else CC("muted"),
                                      command=lambda: self.toggle_fav(tid))
        self._fav_btn.pack(side=side, padx=8)

        self.page = ctk.CTkScrollableFrame(self.content_wrap, fg_color="transparent")
        self.page.grid(row=1, column=0, sticky="nsew", padx=10, pady=8)

        builder = getattr(self, f"page_{tid}", None)
        if builder is None and tid in self._plugin_pages:   # ✦ v4.2: صفحة إضافة
            builder = self._make_plugin_builder(tid)
        try:
            if builder:
                builder(self.page)
            else:
                ctk.CTkLabel(self.page, text="…").pack()
        except Exception:
            ctk.CTkLabel(self.page, text=traceback.format_exc(),
                         justify="left", text_color=CC("err")).pack(anchor="w")
        self._rebuild_nav()
        self.title_label.configure(text=f"{self.t(tool.section)}  ›  {self.t(tool.title)}")
        self.set_status("")

    # ═════════════════════════════════════════════════════
    # 【7.4】 v4.2: نظام الإضافات (plugins/)
    # ═════════════════════════════════════════════════════
    def _load_plugins(self):
        """فحص مجلد plugins/ وتحميل كل *.py بأمان — خطأ أي إضافة معزول.

        كل ملف يستورد toolbox_api ويسجّل أدواته عبر @register_tool؛
        بعد التحميل تُدمج الأدوات في TOOLS/TOOL_BY_ID وتُنشأ الأقسام
        الجديدة تلقائيًا فتظهر في القائمة والبحث ولوحة الأوامر والمفضلة.
        """
        if toolbox_api is None:
            return
        pdir = os.path.join(APP_DIR, "plugins")
        if not os.path.isdir(pdir):
            return
        import importlib.util
        for fname in sorted(os.listdir(pdir)):
            if (not fname.endswith(".py")
                    or fname.startswith(("_", "."))
                    or fname == "toolbox_api.py"):
                continue
            path = os.path.join(pdir, fname)
            try:
                modname = ("toolbox_plugin_"
                           + fname[:-3].replace("-", "_").replace(".", "_"))
                spec = importlib.util.spec_from_file_location(modname, path)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[modname] = mod
                spec.loader.exec_module(mod)
            except Exception:
                print(f"[plugins] {fname}: import failed\n{traceback.format_exc()}")
                self.toast(self.t("Plugin error: {name}").format(name=fname),
                           "err", 4200)
                continue
        # دمج الأدوات المسجّلة (رفض المكرر بأمان)
        known = set(TOOL_BY_ID) | set(self._plugin_pages)
        new: List[Tool] = []
        for reg in toolbox_api.get_registry():
            if reg["tid"] in known:
                print(f"[plugins] duplicate tid skipped: {reg['tid']}")
                continue
            known.add(reg["tid"])
            new.append(Tool(reg["tid"], reg["title"], reg["section"],
                            reg["icon"], reg["description"]))
            self._plugin_pages[reg["tid"]] = reg["builder"]
        if new:
            TOOLS.extend(new)
            TOOL_BY_ID.update({t.tid: t for t in new})
            for t in new:
                if t.section not in SECTIONS:
                    SECTIONS.append(t.section)   # قسم جديد يُنشأ تلقائيًا
            self.set_status(self.t("{n} plugins loaded").format(n=len(new)))
            print(f"[plugins] loaded {len(new)} tool(s)")

    def _make_plugin_builder(self, tid: str) -> Callable:
        """غلاف آمن حول دالة بناء صفحة الإضافة — الخطأ يُعرض داخل الصفحة."""
        pb = self._plugin_pages[tid]

        def _build(parent):
            try:
                pb(toolbox_api, parent)
            except Exception:
                traceback.print_exc()
                c = self.card(parent, f"⚠ {self.t('Plugin crashed')}")
                ctk.CTkLabel(c, text=traceback.format_exc()[-1600:],
                             justify="left", text_color=CC("err"),
                             font=ctk.CTkFont(family="Courier", size=11),
                             wraplength=760).pack(anchor="w", padx=14,
                                                  pady=(0, 12))
        return _build

    def toggle_fav(self, tid: str):
        favs = list(self.settings.get("favorites", []))
        if tid in favs:
            favs.remove(tid)
        else:
            favs.append(tid)
        self.settings["favorites"] = favs
        self.save_settings()
        # تحديث زر النجمة مباشرة بدل إعادة بناء الصفحة — حماية لمدخلات المستخدم
        try:
            if self._fav_btn is not None and self._fav_btn.winfo_exists():
                is_fav = tid in favs
                self._fav_btn.configure(text="⭐" if is_fav else "☆",
                                        text_color=CC("warn") if is_fav else CC("muted"))
        except Exception:
            pass
        self._rebuild_nav()

    def _cancel_timers(self):
        for key, job in list(self._timers.items()):
            try:
                self.after_cancel(job)
            except Exception:
                pass
        self._timers.clear()

    # ── لبنات واجهة موحّدة ────────────────────────────────
    def card(self, parent, title: str = "") -> ctk.CTkFrame:
        """بطاقة موحّدة لتجميع عناصر الأداة."""
        f = ctk.CTkFrame(parent, fg_color=CC("surface"), corner_radius=12,
                         border_width=1, border_color=CC("border"))
        f.pack(fill="x", padx=8, pady=8)
        if title:
            ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=CC("primary")).pack(
                anchor="e" if self.rtl else "w", padx=14, pady=(12, 0))
        return f

    def row(self, parent) -> ctk.CTkFrame:
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=12, pady=6)
        return f

    def field(self, parent, label: str, default: str = "", width: int = 300,
              show: Optional[str] = None) -> ctk.CTkEntry:
        r = self.row(parent)
        side = "right" if self.rtl else "left"
        ctk.CTkLabel(r, text=label, width=150,
                     anchor="e" if self.rtl else "w").pack(side=side)
        e = ctk.CTkEntry(r, width=width, show=show)
        e.pack(side=side, padx=8)
        if default:
            e.insert(0, default)
        return e

    def option(self, parent, label: str, values: List[str],
               default: Optional[str] = None, width: int = 220,
               command: Optional[Callable] = None) -> ctk.CTkOptionMenu:
        r = self.row(parent)
        side = "right" if self.rtl else "left"
        ctk.CTkLabel(r, text=label, width=150,
                     anchor="e" if self.rtl else "w").pack(side=side)
        m = ctk.CTkOptionMenu(r, values=values or ["-"], width=width, command=command)
        m.set(default or (values[0] if values else "-"))
        m.pack(side=side, padx=8)
        return m

    def textbox(self, parent, height: int = 160, text: str = "") -> ctk.CTkTextbox:
        tb = ctk.CTkTextbox(parent, height=height, font=ctk.CTkFont(family="Courier", size=12))
        tb.pack(fill="both", expand=True, padx=12, pady=8)
        if text:
            tb.insert("1.0", text)
        return tb

    def buttons(self, parent, items: List[Tuple[str, Callable]]) -> ctk.CTkFrame:
        r = self.row(parent)
        side = "right" if self.rtl else "left"
        for text, cmd in items:
            ctk.CTkButton(r, text=text, command=cmd, height=32,
                          width=max(90, 10 * len(text))).pack(side=side, padx=4)
        return r

    def statuslabel(self, parent) -> ctk.CTkLabel:
        l = ctk.CTkLabel(parent, text="", text_color=CC("muted"),
                         font=ctk.CTkFont(size=12), justify="left")
        l.pack(anchor="e" if self.rtl else "w", padx=14, pady=(0, 10))
        return l

    def set_box(self, box: ctk.CTkTextbox, text: str):
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)

    def need(self, parent, name: str) -> bool:
        """عرض رسالة واضحة بدل الانهيار عند غياب مكتبة اختيارية."""
        have = {"psutil": HAS_PSUTIL, "requests": HAS_REQUESTS,
                "qrcode": HAS_QRCODE, "Pillow": HAS_PIL}.get(name, True)
        if have:
            return True
        c = self.card(parent, f"⚠ {name} — {self.t('Not installed')}")
        ctk.CTkLabel(c, text=f"{self.t('Install with')}:  {MISSING_HINTS.get(name, '')}",
                     text_color=CC("warn")).pack(anchor="w", padx=14, pady=(0, 14))
        return False

    # ═════════════════════════════════════════════════════
    # 【8】 صفحات القسم: General
    # ═════════════════════════════════════════════════════
    def _tick_monitor(self):
        """جمع قراءات CPU/RAM كل ~1.2 ثانية حتى خارج لوحة التحكم."""
        try:
            if HAS_PSUTIL:
                self.cpu_hist.append(psutil.cpu_percent())
                self.ram_hist.append(psutil.virtual_memory().percent)
                self.cpu_hist = self.cpu_hist[-60:]
                self.ram_hist = self.ram_hist[-60:]
        except Exception:
            pass
        # ✦ v4.5: قفل تلقائي للخزنة بعد خمول _VAULT_LOCK_SECS
        try:
            v = self._vault
            if (v.get("unlocked")
                    and time.time() - v.get("last_touch", 0.0) > _VAULT_LOCK_SECS):
                self._vault_lock_now(auto=True)
                if self.current == "vault":
                    self.show_tool("vault")            # إعادة رسم الصفحة مقفولة
        except Exception:
            pass
        self.after(1200, self._tick_monitor)

    def _vault_lock_now(self, auto: bool = False):
        """قفل الخزنة الحالية ومسح كلمة السر والإدخالات من الذاكرة."""
        v = self._vault
        had = v.get("unlocked")
        v["pw"] = ""
        v["entries"] = []
        v["unlocked"] = False
        v["last_touch"] = 0.0
        v["edit_idx"] = None
        if had:
            msg = (self.t("Vault auto-locked (idle)") if auto
                   else self.t("Vault locked"))
            self.toast("🔒 " + msg, "warn")

    def page_dashboard(self, p):
        if not self.need(p, "psutil"):
            return
        top = ctk.CTkFrame(p, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=6)

        self._gauges = {}
        for key, icon in (("CPU", "🧠"), ("RAM", "💾"), ("Disk", "🗄️"), ("Uptime", "⏳")):
            c = ctk.CTkFrame(top, fg_color=CC("surface"), corner_radius=12,
                             border_width=1, border_color=CC("border"))
            c.pack(side="right" if self.rtl else "left", fill="both",
                   expand=True, padx=6)
            ctk.CTkLabel(c, text=f"{icon}  {key}", text_color=CC("muted"),
                         font=ctk.CTkFont(size=12)).pack(pady=(12, 2))
            val = ctk.CTkLabel(c, text="—", font=ctk.CTkFont(size=26, weight="bold"),
                               text_color=CC("primary"))
            val.pack()
            bar = ctk.CTkProgressBar(c, height=8)
            bar.set(0)
            bar.pack(fill="x", padx=16, pady=(6, 14))
            self._gauges[key] = (val, bar)

        card = self.card(p, "📈 CPU / RAM (60s)")
        self._chart = tk.Canvas(card, height=220, highlightthickness=0,
                                bg=C("surface2"))
        self._chart.pack(fill="x", padx=14, pady=(8, 14))

        legend = self.row(card)
        for name, col in (("CPU", C("primary")), ("RAM", C("ok"))):
            ctk.CTkLabel(legend, text=f"■ {name}", text_color=col).pack(
                side="right" if self.rtl else "left", padx=8)

        info = self.card(p, "🖥️ " + self.t("System Information"))
        self._dash_info = ctk.CTkLabel(info, text="", justify="left",
                                       font=ctk.CTkFont(family="Courier", size=12))
        self._dash_info.pack(anchor="e" if self.rtl else "w", padx=16, pady=(4, 14))

        self._refresh_dashboard()

    def _refresh_dashboard(self):
        """تحديث حي للوحة التحكم (يتوقف تلقائيًا عند مغادرة الصفحة)."""
        if self.current != "dashboard" or not HAS_PSUTIL:
            return
        try:
            cpu = self.cpu_hist[-1] if self.cpu_hist else 0
            vm = psutil.virtual_memory()
            du = psutil.disk_usage(os.path.abspath(os.sep))
            up = time.time() - psutil.boot_time()
            vals = {"CPU": (f"{cpu:.0f}%", cpu / 100),
                    "RAM": (f"{vm.percent:.0f}%", vm.percent / 100),
                    "Disk": (f"{du.percent:.0f}%", du.percent / 100),
                    "Uptime": (human_time(up), min(1.0, up / 604800))}
            for k, (txt, frac) in vals.items():
                lbl, bar = self._gauges[k]
                lbl.configure(text=txt)
                bar.set(frac)
                bar.configure(progress_color=(C("err") if frac > 0.9
                                              else C("warn") if frac > 0.7
                                              else C("primary")))
            self._draw_chart()
            self._dash_info.configure(text=(
                f"{platform.system()} {platform.release()}  ·  {platform.machine()}\n"
                f"Python {platform.python_version()}  ·  {os.cpu_count()} cores\n"
                f"RAM  {human_size(vm.used)} / {human_size(vm.total)}\n"
                f"Disk {human_size(du.used)} / {human_size(du.total)}\n"
                f"Host {socket.gethostname()}"))
        except Exception:
            pass
        self._timers["dash"] = self.after(1200, self._refresh_dashboard)

    def _draw_chart(self):
        """رسم خطي حي للـ CPU/RAM على Canvas."""
        cv = self._chart
        cv.delete("all")
        cv.configure(bg=C("surface2"))
        w = max(cv.winfo_width(), 400)
        h = 220
        for i in range(0, 5):
            y = 10 + i * (h - 30) / 4
            cv.create_line(0, y, w, y, fill=C("border"))
            cv.create_text(24, y - 8, text=f"{100 - i * 25}%",
                           fill=C("muted"), font=("TkDefaultFont", 8))

        def plot(data, color):
            if len(data) < 2:
                return
            step = w / max(1, len(data) - 1)
            pts = []
            for i, v in enumerate(data):
                pts += [i * step, 10 + (100 - v) * (h - 30) / 100]
            cv.create_line(*pts, fill=color, width=2, smooth=True)

        plot(self.cpu_hist, C("primary"))
        plot(self.ram_hist, C("ok"))

    def page_settings(self, p):
        c = self.card(p, "🌐 " + self.t("Language") + " / " + self.t("Theme"))
        self.option(c, self.t("Language"),
                    [LANG_NAMES[k] for k in LANG_NAMES],
                    LANG_NAMES.get(self.lang, "English"),
                    command=self._on_lang_change)
        self.option(c, self.t("Theme"), ["Dark", "Light", "System"],
                    self.settings.get("appearance", "Dark"),
                    command=self._set_mode)

        k = self.card(p, "🔑 API Keys")
        ctk.CTkLabel(k, text="🔒 " + self.t("Keys are stored locally only."),
                     text_color=CC("muted")).pack(anchor="w", padx=14)
        keys = self.settings["api_keys"]
        entries = {}
        for name in ("openweather", "newsapi", "ipinfo", "github", "openai", "openai_base"):
            entries[name] = self.field(k, name, keys.get(name, ""), width=380,
                                       show=None if name.endswith("base") else "•")

        def save_keys():
            for n, e in entries.items():
                self.settings["api_keys"][n] = e.get().strip()
            self.save_settings()
            self.toast(self.t("Done"), "ok")

        pb = self.card(p, "🏗️ PolyBuild")
        pb_e = self.field(pb, "polybuild.py", self.settings.get("polybuild_path", ""),
                          width=420)

        def pick_pb():
            path = filedialog.askopenfilename(title="polybuild.py",
                                              filetypes=[("Python", "*.py"), ("All", "*.*")])
            if path:
                pb_e.delete(0, "end")
                pb_e.insert(0, path)

        def save_pb():
            self.settings["polybuild_path"] = pb_e.get().strip()
            self.save_settings()
            self.toast(self.t("Done"), "ok")

        self.buttons(pb, [(self.t("Browse"), pick_pb), (self.t("Save"), save_pb)])
        self.buttons(k, [(self.t("Save"), save_keys)])

        d = self.card(p, "📁 " + self.t("Data"))
        ctk.CTkLabel(d, text=APP_DIR, text_color=CC("muted"),
                     font=ctk.CTkFont(family="Courier", size=11)).pack(anchor="w", padx=14, pady=(0, 10))
        self.buttons(d, [("📂 " + self.t("Browse"),
                          lambda: webbrowser.open("file://" + APP_DIR))])

    def _set_mode(self, mode: str):
        ctk.set_appearance_mode(mode)
        self.settings["appearance"] = mode
        self.save_settings()
        self.show_tool(self.current)

    def page_about(self, p):
        c = self.card(p, f"⬢ {APP_NAME} v{APP_VERSION}")
        deps = "\n".join([
            f"  customtkinter   ✓  {getattr(ctk, '__version__', '?')}",
            f"  psutil          {'✓' if HAS_PSUTIL else '✗  ' + MISSING_HINTS['psutil']}",
            f"  requests        {'✓' if HAS_REQUESTS else '✗  ' + MISSING_HINTS['requests']}",
            f"  qrcode          {'✓' if HAS_QRCODE else '✗  ' + MISSING_HINTS['qrcode']}",
            f"  Pillow          {'✓' if HAS_PIL else '✗  ' + MISSING_HINTS['Pillow']}",
            f"  zoneinfo        {'✓' if HAS_ZONEINFO else '✗'}",
        ])
        ctk.CTkLabel(c, justify="left", font=ctk.CTkFont(family="Courier", size=12),
                     text=(f"{len(TOOLS)} tools · {len(SECTIONS)} sections · "
                           f"{len(LANG_NAMES)} languages\n"
                           f"Python {platform.python_version()} on "
                           f"{platform.system()} {platform.release()}\n\n"
                           f"Dependencies:\n{deps}\n\n"
                           "🔒 لا تتبّع · لا تحليلات · لا تخزين سحابي\n"
                           "   الاتصال بالشبكة يحدث فقط عند استخدام أدوات APIs صراحةً."
                           )).pack(anchor="w", padx=16, pady=(4, 12))
        s = self.card(p, "⌨️ Shortcuts")
        ctk.CTkLabel(s, justify="left", font=ctk.CTkFont(family="Courier", size=12),
                     text=("  Ctrl+K   Command palette\n"
                           "  ↑ / ↓    Navigate palette results\n"
                           "  Ctrl+F   Focus search\n"
                           "  Ctrl+S   Save settings\n"
                           "  Esc      Close palette\n"
                           "  Enter    Run in most tools")).pack(anchor="w", padx=16, pady=(4, 14))

    # ═════════════════════════════════════════════════════
    # 【9】 صفحات القسم: System
    # ═════════════════════════════════════════════════════
    def page_sysinfo(self, p):
        c = self.card(p, "🖥️ " + self.t("System Information"))
        out = self.textbox(c, 420)
        st = self.statuslabel(c)

        def collect() -> str:
            L = [f"{'='*52}", " SYSTEM", f"{'='*52}",
                 f" OS         : {platform.system()} {platform.release()} ({platform.version()[:40]})",
                 f" Machine    : {platform.machine()}  |  {platform.processor() or 'n/a'}",
                 f" Hostname   : {socket.gethostname()}",
                 f" Python     : {platform.python_version()} ({sys.executable})",
                 f" App dir    : {APP_DIR}"]
            if HAS_PSUTIL:
                vm, sw = psutil.virtual_memory(), psutil.swap_memory()
                L += ["", f"{'='*52}", " CPU", f"{'='*52}",
                      f" Cores      : {psutil.cpu_count(logical=False)} physical / {psutil.cpu_count()} logical",
                      f" Usage      : {psutil.cpu_percent(interval=0.4)}%"]
                try:
                    fr = psutil.cpu_freq()
                    if fr:
                        L.append(f" Frequency  : {fr.current:.0f} MHz (max {fr.max:.0f})")
                except Exception:
                    pass
                L += ["", f"{'='*52}", " MEMORY", f"{'='*52}",
                      f" RAM        : {human_size(vm.used)} / {human_size(vm.total)} ({vm.percent}%)",
                      f" Available  : {human_size(vm.available)}",
                      f" Swap       : {human_size(sw.used)} / {human_size(sw.total)}",
                      "", f"{'='*52}", " DISKS", f"{'='*52}"]
                for part in psutil.disk_partitions(all=False):
                    try:
                        u = psutil.disk_usage(part.mountpoint)
                        L.append(f" {part.device:<16} {part.fstype:<8} "
                                 f"{human_size(u.used)}/{human_size(u.total)} ({u.percent}%)  → {part.mountpoint}")
                    except Exception:
                        continue
                try:
                    bat = psutil.sensors_battery()
                    if bat:
                        L += ["", f"{'='*52}", " BATTERY", f"{'='*52}",
                              f" Charge     : {bat.percent:.0f}%  "
                              f"{'(plugged in)' if bat.power_plugged else ''}",
                              f" Left       : {human_time(bat.secsleft) if bat.secsleft and bat.secsleft > 0 else 'n/a'}"]
                except Exception:
                    pass
                L += ["", f" Boot time  : {_dt.datetime.fromtimestamp(psutil.boot_time()):%Y-%m-%d %H:%M}",
                      f" Uptime     : {human_time(time.time() - psutil.boot_time())}"]
            else:
                L.append("\n [!] " + self.t("psutil missing — limited info.") +
                         "  pip install psutil")
            return "\n".join(L)

        self.run_async(collect, lambda r: self.set_box(out, r), st)
        self.buttons(c, [(self.t("Refresh"),
                          lambda: self.run_async(collect, lambda r: self.set_box(out, r), st)),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_procs(self, p):
        if not self.need(p, "psutil"):
            return
        c = self.card(p, "🧩 " + self.t("Process Manager"))
        r = self.row(c)
        side = "right" if self.rtl else "left"
        flt = ctk.CTkEntry(r, placeholder_text="filter by name / pid", width=260)
        flt.pack(side=side, padx=4)
        sort_by = ctk.CTkOptionMenu(r, values=["cpu", "memory", "name", "pid"], width=120)
        sort_by.pack(side=side, padx=4)
        pid_e = ctk.CTkEntry(r, placeholder_text="PID", width=90)
        pid_e.pack(side=side, padx=4)

        out = self.textbox(c, 420)
        st = self.statuslabel(c)

        def load() -> str:
            q = flt.get().strip().lower()
            key = sort_by.get()
            rows = []
            for pr in psutil.process_iter(["pid", "name", "username",
                                           "cpu_percent", "memory_info"]):
                try:
                    i = pr.info
                    if q and q not in str(i.get("name", "")).lower() and q != str(i["pid"]):
                        continue
                    mem = i["memory_info"].rss if i.get("memory_info") else 0
                    rows.append((i["pid"], (i.get("name") or "?")[:28],
                                 (i.get("username") or "?")[:16],
                                 i.get("cpu_percent") or 0.0, mem))
                except Exception:
                    continue
            idx = {"pid": 0, "name": 1, "cpu": 3, "memory": 4}[key]
            rows.sort(key=lambda x: x[idx], reverse=key in ("cpu", "memory"))
            head = f"{'PID':>7}  {'NAME':<28} {'USER':<16} {'CPU%':>6}  {'MEM':>10}"
            body = "\n".join(f"{a:>7}  {b:<28} {c_:<16} {d:>6.1f}  {human_size(e):>10}"
                             for a, b, c_, d, e in rows[:300])
            return f"{head}\n{'-' * len(head)}\n{body}\n\n{len(rows)} processes"

        def kill():
            try:
                pid = int(pid_e.get().strip())
            except Exception:
                self.toast("invalid PID", "err")
                return
            if not messagebox.askyesno(self.t("Process Manager"),
                                       f"{self.t('Terminate process?')}  (PID {pid})"):
                return
            try:
                pr = psutil.Process(pid)
                pr.terminate()
                try:
                    pr.wait(timeout=3)
                except psutil.TimeoutExpired:
                    pr.kill()                    # تصعيد إلى kill إذا لم يستجب
                    pr.wait(timeout=3)
                self.toast(f"terminated {pid}", "ok")
                self.run_async(load, lambda r_: self.set_box(out, r_), st)
            except Exception as e:
                self.toast(f"{self.t('Failed')}: {e}", "err")

        self.buttons(c, [(self.t("Refresh"),
                          lambda: self.run_async(load, lambda r_: self.set_box(out, r_), st)),
                         ("⛔ Kill PID", kill)])
        self.run_async(load, lambda r_: self.set_box(out, r_), st)

    def page_network(self, p):
        c = self.card(p, "🌐 " + self.t("Network Info"))
        out = self.textbox(c, 260)
        st = self.statuslabel(c)

        def local_info() -> str:
            L = [f" Hostname   : {socket.gethostname()}"]
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1.0)
                s.connect(("8.8.8.8", 80))
                L.append(f" Local IP   : {s.getsockname()[0]}")
                s.close()
            except Exception:
                L.append(" Local IP   : n/a")
            if HAS_PSUTIL:
                try:
                    for name, addrs in psutil.net_if_addrs().items():
                        ips = [a.address for a in addrs if a.family == socket.AF_INET]
                        if ips:
                            L.append(f" {name:<10} : {', '.join(ips)}")
                    io_ = psutil.net_io_counters()
                    L.append(f" Traffic    : ↑ {human_size(io_.bytes_sent)}  ↓ {human_size(io_.bytes_recv)}")
                except Exception:
                    pass
            return "\n".join(L)

        self.run_async(local_info, lambda r_: self.set_box(out, r_), st)

        def public_ip():
            def work():
                base = local_info()
                ip = json.loads(http_get("https://api.ipify.org?format=json")[1]).get("ip", "?")
                return base + f"\n Public IP  : {ip}"
            self.run_async(work, lambda r_: self.set_box(out, r_), st)

        self.buttons(c, [(self.t("Refresh"),
                          lambda: self.run_async(local_info,
                                                 lambda r_: self.set_box(out, r_), st)),
                         ("🌍 Public IP", public_ip)])

        pc = self.card(p, "📶 Ping")
        host = self.field(pc, "host", "1.1.1.1", 240)
        pout = self.textbox(pc, 180)
        pst = self.statuslabel(pc)

        def ping():
            h = host.get().strip()
            cnt = "-n" if platform.system() == "Windows" else "-c"
            self.run_async(lambda: run_cmd(["ping", cnt, "4", h], 20)[1],
                           lambda r_: self.set_box(pout, r_), pst)

        self.buttons(pc, [("📶 Ping", ping)])

    def page_ports(self, p):
        c = self.card(p, "📡 " + self.t("Port Scanner"))
        host = self.field(c, "host", "127.0.0.1", 240)
        rng = self.field(c, "ports", "1-1024", 200)
        out = self.textbox(c, 300)
        st = self.statuslabel(c)
        stop = threading.Event()
        self._stop_flags["ports"] = stop

        common = {20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
                  53: "dns", 67: "dhcp", 80: "http", 110: "pop3", 123: "ntp",
                  135: "msrpc", 139: "netbios", 143: "imap", 161: "snmp",
                  389: "ldap", 443: "https", 445: "smb", 465: "smtps",
                  587: "submission", 993: "imaps", 995: "pop3s", 1433: "mssql",
                  1521: "oracle", 2049: "nfs", 3306: "mysql", 3389: "rdp",
                  5432: "postgres", 5555: "adb", 6379: "redis", 8080: "http-alt",
                  8443: "https-alt", 9200: "elasticsearch", 27017: "mongodb"}

        def scan() -> str:
            stop.clear()
            h = host.get().strip()
            if not h:
                raise ValueError("host required")
            a, _, b = rng.get().strip().partition("-")
            lo, hi = int(a or 0), int(b or a or 0)
            lo, hi = max(1, lo), min(hi, 65535)
            if lo > hi:
                raise ValueError("invalid range")
            if hi - lo + 1 > 20000:
                raise ValueError("range too wide (max 20000 ports)")
            total = hi - lo + 1
            found: List[str] = []
            done = [0]
            lock = threading.Lock()

            def probe(port: int):
                if stop.is_set():
                    return
                s = socket.socket()
                s.settimeout(0.5)
                try:
                    if s.connect_ex((h, port)) == 0:
                        with lock:
                            found.append(f"  {port:>6}  OPEN   {common.get(port, '')}")
                finally:
                    s.close()
                    with lock:
                        done[0] += 1
                        if done[0] % 200 == 0 or done[0] == total:
                            self._ui(st.configure, text=f"⏳ {done[0]}/{total} …",
                                     text_color=CC("warn"))

            workers = min(300, max(32, total // 4))
            with ThreadPoolExecutor(max_workers=workers) as ex:
                list(ex.map(probe, range(lo, hi + 1)))
            found.sort()
            if stop.is_set():
                return "\n".join(found) + f"\n\n⏹ stopped at {done[0]}/{total}"
            return ("\n".join(found) or "no open ports found") + \
                f"\n\n✓ scanned {total} ports in parallel"

        self.buttons(c, [("▶ " + self.t("Start"),
                          lambda: self.run_async(scan, lambda r_: self.set_box(out, r_), st)),
                         ("⏹ " + self.t("Stop"), lambda: stop.set())])

    def page_dns(self, p):
        c = self.card(p, "🔎 " + self.t("DNS Lookup"))
        host = self.field(c, "domain / ip", "github.com", 300)
        out = self.textbox(c, 260)
        st = self.statuslabel(c)

        def lookup() -> str:
            h = host.get().strip()
            L = []
            try:
                name, aliases, ips = socket.gethostbyname_ex(h)
                L += [f" Canonical : {name}",
                      f" Aliases   : {', '.join(aliases) or '-'}",
                      f" IPv4      : {', '.join(ips)}"]
            except Exception as e:
                L.append(f" A lookup failed: {e}")
            try:
                infos = socket.getaddrinfo(h, None)
                v6 = sorted({i[4][0] for i in infos if i[0] == socket.AF_INET6})
                if v6:
                    L.append(f" IPv6      : {', '.join(v6)}")
            except Exception:
                pass
            try:
                L.append(f" Reverse   : {socket.gethostbyaddr(h)[0]}")
            except Exception:
                pass
            return "\n".join(L)

        self.buttons(c, [("🔎 " + self.t("Run"),
                          lambda: self.run_async(lookup, lambda r_: self.set_box(out, r_), st))])

    def page_headers(self, p):
        c = self.card(p, "📨 " + self.t("HTTP Headers"))
        url = self.field(c, "URL", "https://example.com", 420)
        out = self.textbox(c, 320)
        st = self.statuslabel(c)

        def inspect() -> str:
            u = url.get().strip()
            if not u.startswith("http"):
                u = "https://" + u
            req = urllib.request.Request(u, headers={"User-Agent": f"{APP_NAME}/{APP_VERSION}"},
                                         method="GET")
            with urllib.request.urlopen(req, timeout=NET_TIMEOUT) as resp:
                L = [f" Status : {resp.status} {resp.reason}",
                     f" URL    : {resp.url}", ""]
                for k, v in resp.headers.items():
                    L.append(f" {k:<28}: {v}")
                return "\n".join(L)

        self.buttons(c, [("📨 " + self.t("Run"),
                          lambda: self.run_async(inspect, lambda r_: self.set_box(out, r_), st))])

    def page_httpclient(self, p):
        c = self.card(p, "🛰️ " + self.t("HTTP Client"))
        method = self.option(c, "method", ["GET", "POST", "PUT", "DELETE", "HEAD"],
                             "GET", 140)
        url = self.field(c, "URL", "https://api.github.com", 440)
        hdrs_e = self.field(c, "headers (Key: value per line)", "", 440)
        ctk.CTkLabel(c, text="body (JSON / raw)", text_color=CC("muted")).pack(
            anchor="e" if self.rtl else "w", padx=14)
        body = self.textbox(c, 110)
        out = self.textbox(c, 300)
        st = self.statuslabel(c)

        def send() -> str:
            u = url.get().strip()
            if not u:
                raise ValueError("URL required")
            hmap: Dict[str, str] = {}
            for ln in hdrs_e.get().splitlines():
                if ":" in ln:
                    k2, v2 = ln.split(":", 1)
                    if k2.strip():
                        hmap[k2.strip()] = v2.strip()
            m = method.get()
            payload = body.get("1.0", "end").strip()
            data = payload if (payload and m not in ("GET", "HEAD")) else None
            code, text, rhdrs = http_request(m, u, hmap, data=data)
            try:
                text = json.dumps(json.loads(text), ensure_ascii=False, indent=2)
            except Exception:
                pass
            interesting = [k for k in ("Content-Type", "Content-Length", "Date",
                                       "Server", "Cache-Control", "Location")
                           if k in rhdrs]
            L = [f"HTTP {code}"] + [f"{k}: {rhdrs[k]}" for k in interesting] + [""]
            return "\n".join(L) if m == "HEAD" else "\n".join(L) + text[:200000]

        self.buttons(c, [("▶ " + self.t("Run"),
                          lambda: self.run_async(send, lambda r_: self.set_box(out, r_), st)),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_tz(self, p):
        c = self.card(p, "🕓 " + self.t("Time Zones"))
        zones = sorted(available_timezones()) if HAS_ZONEINFO else []
        common = ["UTC", "Europe/Istanbul", "Europe/London", "Africa/Cairo",
                  "Asia/Dubai", "Asia/Riyadh", "Asia/Tokyo", "America/New_York",
                  "America/Los_Angeles", "Australia/Sydney"]
        pool = common + [z for z in zones if z not in common]
        src = self.option(c, "from", pool[:400], "UTC", 260)
        dst = self.option(c, "to", pool[:400], "Europe/Istanbul", 260)
        when = self.field(c, "datetime", _dt.datetime.now().strftime("%Y-%m-%d %H:%M"), 220)
        out = self.textbox(c, 220)

        def convert():
            try:
                if not HAS_ZONEINFO:
                    raise RuntimeError("zoneinfo unavailable (Python 3.9+ required)")
                naive = _dt.datetime.strptime(when.get().strip(), "%Y-%m-%d %H:%M")
                a = naive.replace(tzinfo=ZoneInfo(src.get()))
                b = a.astimezone(ZoneInfo(dst.get()))
                lines = [f" {src.get():<26} {a:%Y-%m-%d %H:%M %Z (UTC%z)}",
                         f" {dst.get():<26} {b:%Y-%m-%d %H:%M %Z (UTC%z)}",
                         f" Difference {'':<15} {(b.utcoffset() - a.utcoffset()).total_seconds() / 3600:+.1f} h",
                         "", " World clock:"]
                for z in common:
                    try:
                        lines.append(f"   {z:<24} {a.astimezone(ZoneInfo(z)):%H:%M  %a %d %b}")
                    except Exception:
                        continue
                self.set_box(out, "\n".join(lines))
            except Exception as e:
                self.set_box(out, f"✗ {e}")

        self.buttons(c, [(self.t("Convert"), convert)])
        convert()

    # ═════════════════════════════════════════════════════
    # 【10】 صفحات القسم: Files
    # ═════════════════════════════════════════════════════
    def _folder_picker(self, parent, label: str = "folder") -> ctk.CTkEntry:
        r = self.row(parent)
        side = "right" if self.rtl else "left"
        ctk.CTkLabel(r, text=label, width=90,
                     anchor="e" if self.rtl else "w").pack(side=side)
        e = ctk.CTkEntry(r, width=420)
        e.pack(side=side, padx=6)

        def pick():
            d = filedialog.askdirectory(title=self.t("Select folder"))
            if d:
                e.delete(0, "end")
                e.insert(0, d)
        ctk.CTkButton(r, text="📂", width=44, command=pick).pack(side=side)
        return e

    def _file_picker(self, parent, label: str = "file", save: bool = False) -> ctk.CTkEntry:
        r = self.row(parent)
        side = "right" if self.rtl else "left"
        ctk.CTkLabel(r, text=label, width=90,
                     anchor="e" if self.rtl else "w").pack(side=side)
        e = ctk.CTkEntry(r, width=420)
        e.pack(side=side, padx=6)

        def pick():
            f = (filedialog.asksaveasfilename() if save
                 else filedialog.askopenfilename(title=self.t("Select file")))
            if f:
                e.delete(0, "end")
                e.insert(0, f)
        ctk.CTkButton(r, text="📄", width=44, command=pick).pack(side=side)
        return e

    ORGANIZER_MAP = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff", ".heic"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md", ".xls",
                      ".xlsx", ".ppt", ".pptx", ".csv"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
        "Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rs",
                 ".rb", ".php", ".html", ".css", ".json", ".xml", ".sh", ".kt"],
        "Executables": [".exe", ".msi", ".apk", ".deb", ".rpm", ".dmg", ".appimage"],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    }

    def page_organizer(self, p):
        c = self.card(p, "🗂️ " + self.t("File Organizer"))
        folder = self._folder_picker(c)
        dry = ctk.CTkCheckBox(c, text="Dry run (preview only)")
        dry.select()
        dry.pack(anchor="e" if self.rtl else "w", padx=14, pady=4)
        out = self.textbox(c, 300)
        st = self.statuslabel(c)

        def organize() -> str:
            d = folder.get().strip()
            if not os.path.isdir(d):
                raise ValueError("folder not found")
            preview = bool(dry.get())
            moved, L = 0, []
            for name in sorted(os.listdir(d)):
                src = os.path.join(d, name)
                if not os.path.isfile(src) or name.startswith("."):
                    continue
                ext = os.path.splitext(name)[1].lower()
                cat = next((k for k, v in self.ORGANIZER_MAP.items() if ext in v), "Other")
                dstdir = os.path.join(d, cat)
                dst = os.path.join(dstdir, name)
                L.append(f"  {name}  →  {cat}/")
                if not preview:
                    os.makedirs(dstdir, exist_ok=True)
                    if os.path.exists(dst):
                        base, e2 = os.path.splitext(name)
                        dst = os.path.join(dstdir, f"{base}_{int(time.time())}{e2}")
                    shutil.move(src, dst)
                moved += 1
            head = ("PREVIEW — nothing moved\n" if preview else "MOVED\n")
            return f"{head}{moved} file(s)\n\n" + "\n".join(L[:500])

        self.buttons(c, [("▶ " + self.t("Run"),
                          lambda: self.run_async(organize, lambda r_: self.set_box(out, r_), st))])

        u = self.card(p, "🔌 USB / Removable drives")
        uout = self.textbox(u, 140)

        def detect():
            if not HAS_PSUTIL:
                self.set_box(uout, "psutil " + self.t("Not installed"))
                return
            L = []
            for part in psutil.disk_partitions(all=False):
                opts = part.opts.lower()
                removable = ("removable" in opts or "/media" in part.mountpoint
                             or "/run/media" in part.mountpoint
                             or "/Volumes" in part.mountpoint)
                if removable:
                    try:
                        us = psutil.disk_usage(part.mountpoint)
                        L.append(f"  🔌 {part.device}  {part.mountpoint}  "
                                 f"{human_size(us.free)} free / {human_size(us.total)}")
                    except Exception:
                        L.append(f"  🔌 {part.device}  {part.mountpoint}")
            self.set_box(uout, "\n".join(L) or "no removable drives detected")

        self.buttons(u, [(self.t("Refresh"), detect)])
        detect()

    def page_dupes(self, p):
        c = self.card(p, "👯 " + self.t("Duplicate Finder"))
        ctk.CTkLabel(c, text="🧬 " + self.t("3 stages: size → 8KB prefix → full hash"),
                     text_color=CC("muted")).pack(anchor="e" if self.rtl else "w", padx=14)
        folder = self._folder_picker(c)
        out = self.textbox(c, 340)
        st = self.statuslabel(c)
        last: Dict[str, Any] = {"groups": []}

        def find() -> str:
            d = folder.get().strip()
            if not os.path.isdir(d):
                raise ValueError("folder not found")
            by_size: Dict[int, List[str]] = {}
            for root, _, files in os.walk(d):
                for fn in files:
                    fp = os.path.join(root, fn)
                    try:
                        sz = os.path.getsize(fp)
                    except OSError:
                        continue
                    if sz > 0:
                        by_size.setdefault(sz, []).append(fp)
            stage1 = {s: v for s, v in by_size.items() if len(v) > 1}
            by_prefix: Dict[Tuple[int, str], List[str]] = {}
            for s, paths in stage1.items():
                for fp in paths:
                    try:
                        by_prefix.setdefault((s, file_hash(fp, "md5", limit=8192)), []).append(fp)
                    except OSError:
                        continue
            groups: Dict[str, List[str]] = {}
            for key, paths in by_prefix.items():
                if len(paths) < 2:
                    continue
                for fp in paths:
                    try:
                        groups.setdefault(file_hash(fp, "sha256"), []).append(fp)
                    except OSError:
                        continue
            dupes = {k: v for k, v in groups.items() if len(v) > 1}
            wasted = sum(os.path.getsize(v[0]) * (len(v) - 1) for v in dupes.values())
            last["groups"] = list(dupes.values())
            L = [f"scanned groups: {len(by_size)}  ·  duplicate groups: {len(dupes)}",
                 f"reclaimable: {human_size(wasted)}", "",
                 "ℹ the FIRST path in each group is the one kept by “Delete”", ""]
            for h, paths in list(dupes.items())[:200]:
                L.append(f"■ {h[:16]}…  ({human_size(os.path.getsize(paths[0]))})")
                for fp in paths:
                    L.append(f"    {fp}")
                L.append("")
            return "\n".join(L)

        def del_dupes():
            groups = last.get("groups") or []
            if not groups:
                self.toast("run the scan first", "warn")
                return
            victims = [fp for grp in groups for fp in grp[1:]]
            if not victims:
                self.toast("nothing to delete", "info")
                return
            try:
                freed = sum(os.path.getsize(v) for v in victims)
            except OSError:
                freed = 0
            if not messagebox.askyesno(
                    self.t("Duplicate Finder"),
                    f"{self.t('Delete duplicates?')}\n"
                    f"{len(victims)} file(s) · {human_size(freed)}"):
                return
            n = 0
            for fp in victims:
                try:
                    os.remove(fp)
                    n += 1
                except OSError:
                    continue
            self.toast(f"deleted {n} file(s)", "ok")
            self.run_async(find, lambda r_: self.set_box(out, r_), st)

        self.buttons(c, [("🔍 " + self.t("Run"),
                          lambda: self.run_async(find, lambda r_: self.set_box(out, r_), st)),
                         ("🗑 " + self.t("Delete"), del_dupes),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_rename(self, p):
        c = self.card(p, "✏️ " + self.t("Bulk Rename"))
        folder = self._folder_picker(c)
        find_e = self.field(c, "find", "", 200)
        repl_e = self.field(c, "replace", "", 200)
        pre_e = self.field(c, "prefix", "", 200)
        suf_e = self.field(c, "suffix", "", 200)
        case_m = self.option(c, "case", ["keep", "lower", "UPPER", "Title"], "keep", 160)
        use_rx = ctk.CTkCheckBox(c, text="find is regex")
        use_rx.pack(anchor="e" if self.rtl else "w", padx=14, pady=2)
        dry = ctk.CTkCheckBox(c, text="Dry run (preview only)")
        dry.select()
        dry.pack(anchor="e" if self.rtl else "w", padx=14, pady=2)
        out = self.textbox(c, 280)
        st = self.statuslabel(c)

        def do() -> str:
            d = folder.get().strip()
            if not os.path.isdir(d):
                raise ValueError("folder not found")
            preview = bool(dry.get())
            L, n, skipped = [], 0, 0
            for name in sorted(os.listdir(d)):
                src = os.path.join(d, name)
                if not os.path.isfile(src):
                    continue
                base, ext = os.path.splitext(name)
                try:
                    if find_e.get():
                        if use_rx.get():
                            base = re.sub(find_e.get(), repl_e.get(), base)
                        else:
                            base = base.replace(find_e.get(), repl_e.get())
                except re.error as e:
                    raise ValueError(f"bad regex: {e}")
                cm = case_m.get()
                base = (base.lower() if cm == "lower" else base.upper() if cm == "UPPER"
                        else base.title() if cm == "Title" else base)
                new = f"{pre_e.get()}{base}{suf_e.get()}{ext}"
                if new == name:
                    continue
                if not preview and os.path.exists(os.path.join(d, new)):
                    L.append(f"  {name}  ⚠ skipped — target exists: {new}")
                    skipped += 1
                    continue
                L.append(f"  {name}  →  {new}")
                n += 1
                if not preview:
                    os.rename(src, os.path.join(d, new))
            head = "PREVIEW — nothing renamed\n" if preview else "RENAMED\n"
            tail = f"\n\n⚠ {skipped} skipped (target exists)" if skipped else ""
            return f"{head}{n} file(s){tail}\n\n" + "\n".join(L[:500])

        self.buttons(c, [("▶ " + self.t("Run"),
                          lambda: self.run_async(do, lambda r_: self.set_box(out, r_), st))])

    def page_splitmerge(self, p):
        c = self.card(p, "✂️ Split")
        src = self._file_picker(c, "file")
        size_e = self.field(c, "chunk (MB)", "10", 120)
        sout = self.textbox(c, 120)
        sst = self.statuslabel(c)

        def split() -> str:
            f = src.get().strip()
            chunk = int(float(size_e.get()) * 1024 * 1024)
            if chunk < 1024:
                raise ValueError("chunk too small")
            n = 0
            with open(f, "rb") as fh:
                while True:
                    b = fh.read(chunk)
                    if not b:
                        break
                    n += 1
                    with open(f"{f}.part{n:03d}", "wb") as o:
                        o.write(b)
            return f"created {n} part(s) next to the source file"

        self.buttons(c, [("✂️ Split",
                          lambda: self.run_async(split, lambda r_: self.set_box(sout, r_), sst))])

        m = self.card(p, "🧷 Merge")
        first = self._file_picker(m, ".part001")
        mout = self.textbox(m, 120)
        mst = self.statuslabel(m)

        def merge() -> str:
            f = first.get().strip()
            base = re.sub(r"\.part\d+$", "", f)
            folder = os.path.dirname(base) or "."
            stem = os.path.basename(base)
            parts = sorted(g for g in os.listdir(folder)
                           if re.fullmatch(re.escape(stem) + r"\.part\d+", g))
            if not parts:
                raise ValueError("no .partNNN files found")
            dst = base + ".merged"
            with open(dst, "wb") as o:
                for pt in parts:
                    with open(os.path.join(folder, pt), "rb") as fh:
                        shutil.copyfileobj(fh, o)
            return f"merged {len(parts)} parts → {dst}"

        self.buttons(m, [("🧷 Merge",
                          lambda: self.run_async(merge, lambda r_: self.set_box(mout, r_), mst))])

    def page_checksum(self, p):
        c = self.card(p, "🔐 " + self.t("Checksum"))
        f = self._file_picker(c, "file")
        expect = self.field(c, "expected", "", 420)
        out = self.textbox(c, 200)
        st = self.statuslabel(c)

        def calc() -> str:
            path = f.get().strip()
            if not os.path.isfile(path):
                raise ValueError("file not found")
            L = [f" size   : {human_size(os.path.getsize(path))}"]
            hashes: List[str] = []
            for a in ("md5", "sha1", "sha256", "sha512", "sha3_256", "blake2b"):
                try:
                    v = file_hash(path, a)
                    hashes.append(v)
                    L.append(f" {a:<9}: {v}")
                except Exception:          # بعض الإصدارات لا تدعم sha3
                    continue
            exp = expect.get().strip().lower()
            if exp:
                ok = exp in hashes
                L.append("")
                L.append(" ✓ MATCH" if ok else " ✗ MISMATCH")
            return "\n".join(L)

        self.buttons(c, [("🔐 " + self.t("Run"),
                          lambda: self.run_async(calc, lambda r_: self.set_box(out, r_), st)),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_zip(self, p):
        c = self.card(p, "🗜️ Compress")
        folder = self._folder_picker(c)
        zout = self.textbox(c, 120)
        zst = self.statuslabel(c)

        def compress() -> str:
            d = folder.get().strip()
            if not os.path.isdir(d):
                raise ValueError("folder not found")
            dst = d.rstrip(os.sep) + ".zip"
            n = 0
            with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
                for root, _, files in os.walk(d):
                    for fn in files:
                        fp = os.path.join(root, fn)
                        z.write(fp, os.path.relpath(fp, d))
                        n += 1
            return f"{n} files → {dst}\n{human_size(os.path.getsize(dst))}"

        self.buttons(c, [("🗜️ " + self.t("Run"),
                          lambda: self.run_async(compress, lambda r_: self.set_box(zout, r_), zst))])

        e = self.card(p, "📤 Extract")
        zf = self._file_picker(e, "zip")
        target = self._folder_picker(e, "to")
        eout = self.textbox(e, 140)
        est = self.statuslabel(e)

        def extract() -> str:
            src = zf.get().strip()
            dst = target.get().strip() or os.path.splitext(src)[0]
            os.makedirs(dst, exist_ok=True)
            with zipfile.ZipFile(src) as z:
                names = z.namelist()
                for nm in names:                       # حماية من Zip-Slip
                    full = os.path.realpath(os.path.join(dst, nm))
                    if not full.startswith(os.path.realpath(dst)):
                        raise ValueError(f"unsafe path in archive: {nm}")
                z.extractall(dst)
            return f"extracted {len(names)} entries → {dst}"

        self.buttons(e, [("📤 " + self.t("Run"),
                          lambda: self.run_async(extract, lambda r_: self.set_box(eout, r_), est))])

    def page_b64file(self, p):
        c = self.card(p, "📦 " + self.t("Base64 File"))
        f = self._file_picker(c, "file")
        out = self.textbox(c, 200)
        st = self.statuslabel(c)

        def enc() -> str:
            path = f.get().strip()
            with open(path, "rb") as fh:
                data = base64.b64encode(fh.read()).decode()
            dst = path + ".b64"
            with open(dst, "w", encoding="utf-8") as o:
                o.write(data)
            return f"encoded → {dst}\n{human_size(len(data))}\n\n{data[:2000]}…"

        def dec() -> str:
            path = f.get().strip()
            with open(path, "r", encoding="utf-8") as fh:
                raw = base64.b64decode(fh.read())
            dst = path[:-4] if path.endswith(".b64") else path + ".bin"
            with open(dst, "wb") as o:
                o.write(raw)
            return f"decoded → {dst}\n{human_size(len(raw))}"

        self.buttons(c, [("→ Base64",
                          lambda: self.run_async(enc, lambda r_: self.set_box(out, r_), st)),
                         ("← Binary",
                          lambda: self.run_async(dec, lambda r_: self.set_box(out, r_), st))])

    def page_csvjson(self, p):
        c = self.card(p, "🔁 " + self.t("CSV ⇄ JSON"))
        f = self._file_picker(c, "file")
        out = self.textbox(c, 300)
        st = self.statuslabel(c)

        def c2j() -> str:
            path = f.get().strip()
            with open(path, "r", encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.DictReader(fh))
            dst = os.path.splitext(path)[0] + ".json"
            jsave(dst, rows)
            return f"{len(rows)} rows → {dst}\n\n" + json.dumps(rows[:20], ensure_ascii=False, indent=2)

        def j2c() -> str:
            path = f.get().strip()
            data = jload(path, None)
            if not isinstance(data, list) or not data:
                raise ValueError("JSON must be a non-empty array of objects")
            cols: List[str] = []
            for rowd in data:
                for k in rowd:
                    if k not in cols:
                        cols.append(k)
            dst = os.path.splitext(path)[0] + ".csv"
            with open(dst, "w", encoding="utf-8", newline="") as o:
                w = csv.DictWriter(o, fieldnames=cols)
                w.writeheader()
                for rowd in data:
                    flat = {k: (json.dumps(v, ensure_ascii=False)
                                if isinstance(v, (dict, list)) else v)
                            for k, v in rowd.items()}
                    w.writerow(flat)
            return f"{len(data)} rows → {dst}\ncolumns: {', '.join(cols)}"

        self.buttons(c, [("CSV → JSON",
                          lambda: self.run_async(c2j, lambda r_: self.set_box(out, r_), st)),
                         ("JSON → CSV",
                          lambda: self.run_async(j2c, lambda r_: self.set_box(out, r_), st))])

    # ═════════════════════════════════════════════════════
    # 【11】 صفحات القسم: Text
    # ═════════════════════════════════════════════════════
    def page_counter(self, p):
        c = self.card(p, "🔢 " + self.t("Text Counter"))
        box = self.textbox(c, 240)
        res = ctk.CTkLabel(c, text="", justify="left",
                           font=ctk.CTkFont(family="Courier", size=13))
        res.pack(anchor="e" if self.rtl else "w", padx=16, pady=(0, 12))

        def count(*_):
            s = box.get("1.0", "end").rstrip("\n")
            words = re.findall(r"\S+", s)
            sentences = [x for x in re.split(r"[.!?؟]+", s) if x.strip()]
            paras = [x for x in s.split("\n\n") if x.strip()]
            freq: Dict[str, int] = {}
            for w in words:
                k = re.sub(r"[^\w\u0600-\u06FF]", "", w.lower())
                if len(k) > 3:
                    freq[k] = freq.get(k, 0) + 1
            top = sorted(freq.items(), key=lambda x: -x[1])[:5]
            res.configure(text=(
                f" characters      : {len(s)}\n"
                f" without spaces  : {len(s.replace(' ', '').replace(chr(10), ''))}\n"
                f" words           : {len(words)}\n"
                f" unique words    : {len(set(w.lower() for w in words))}\n"
                f" lines           : {s.count(chr(10)) + 1 if s else 0}\n"
                f" sentences       : {len(sentences)}\n"
                f" paragraphs      : {len(paras)}\n"
                f" reading time    : {max(1, round(len(words) / 200))} min\n"
                f" speaking time   : {max(1, round(len(words) / 130))} min\n"
                f" top words       : {', '.join(f'{k}({v})' for k, v in top) or '-'}"))

        box.bind("<KeyRelease>", count)
        self.buttons(c, [(self.t("Run"), count),
                         (self.t("Clear"), lambda: (box.delete("1.0", "end"), count()))])
        count()

    def page_transform(self, p):
        c = self.card(p, "🔤 " + self.t("Text Transform"))
        box = self.textbox(c, 200)
        out = self.textbox(c, 200)

        def apply(fn: Callable[[str], str]):
            self.set_box(out, fn(box.get("1.0", "end").rstrip("\n")))

        ops: List[Tuple[str, Callable[[str], str]]] = [
            ("UPPER", str.upper), ("lower", str.lower), ("Title", str.title),
            ("Reverse", lambda s: s[::-1]),
            ("Sort", lambda s: "\n".join(sorted(s.splitlines()))),
            ("Unique", lambda s: "\n".join(dict.fromkeys(s.splitlines()))),
            ("Trim", lambda s: "\n".join(x.strip() for x in s.splitlines())),
            ("No blanks", lambda s: "\n".join(x for x in s.splitlines() if x.strip())),
            ("snake_case", lambda s: re.sub(r"[\s\-]+", "_", s.strip()).lower()),
            ("kebab-case", lambda s: re.sub(r"[\s_]+", "-", s.strip()).lower()),
            ("camelCase", lambda s: re.sub(r"[\s_\-]+(\w)", lambda m: m.group(1).upper(), s.strip())),
            ("Slugify", lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")),
        ]
        grid = ctk.CTkFrame(c, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=6)
        for i, (name, fn) in enumerate(ops):
            ctk.CTkButton(grid, text=name, width=110, height=30,
                          command=lambda f=fn: apply(f)).grid(
                row=i // 6, column=i % 6, padx=3, pady=3)
        self.buttons(c, [(self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_diff(self, p):
        c = self.card(p, "📑 " + self.t("Text Diff"))
        r = ctk.CTkFrame(c, fg_color="transparent")
        r.pack(fill="both", expand=True, padx=12, pady=6)
        a = ctk.CTkTextbox(r, height=180, font=ctk.CTkFont(family="Courier", size=12))
        b = ctk.CTkTextbox(r, height=180, font=ctk.CTkFont(family="Courier", size=12))
        a.pack(side="right" if self.rtl else "left", fill="both", expand=True, padx=4)
        b.pack(side="right" if self.rtl else "left", fill="both", expand=True, padx=4)
        out = self.textbox(c, 260)

        def compare():
            x = a.get("1.0", "end").splitlines()
            y = b.get("1.0", "end").splitlines()
            ratio = difflib.SequenceMatcher(None, "\n".join(x), "\n".join(y)).ratio()
            diff = list(difflib.unified_diff(x, y, "A", "B", lineterm="", n=2))
            self.set_box(out, f"similarity: {ratio * 100:.1f}%\n" + "-" * 40 + "\n" +
                         ("\n".join(diff) if diff else "identical ✓"))

        self.buttons(c, [("⇄ " + self.t("Run"), compare),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_encode(self, p):
        c = self.card(p, "🧬 " + self.t("Encode / Decode"))
        mode = self.option(c, "format",
                           ["Base64", "URL", "HTML", "Hex", "Binary", "Morse", "ROT13"],
                           "Base64", 180)
        box = self.textbox(c, 170)
        out = self.textbox(c, 170)

        def enc():
            s = box.get("1.0", "end").rstrip("\n")
            m = mode.get()
            try:
                if m == "Base64":
                    v = base64.b64encode(s.encode()).decode()
                elif m == "URL":
                    v = urllib.parse.quote(s, safe="")
                elif m == "HTML":
                    v = html.escape(s)
                elif m == "Hex":
                    v = s.encode().hex()
                elif m == "Binary":
                    v = " ".join(format(x, "08b") for x in s.encode())
                elif m == "Morse":
                    v = to_morse(s)
                else:
                    v = s.translate(str.maketrans(
                        string.ascii_letters,
                        string.ascii_lowercase[13:] + string.ascii_lowercase[:13] +
                        string.ascii_uppercase[13:] + string.ascii_uppercase[:13]))
                self.set_box(out, v)
            except Exception as e:
                self.set_box(out, f"✗ {e}")

        def dec():
            s = box.get("1.0", "end").strip()
            m = mode.get()
            try:
                if m == "Base64":
                    v = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8", "replace")
                elif m == "URL":
                    v = urllib.parse.unquote(s)
                elif m == "HTML":
                    v = html.unescape(s)
                elif m == "Hex":
                    v = bytes.fromhex(re.sub(r"\s", "", s)).decode("utf-8", "replace")
                elif m == "Binary":
                    v = bytes(int(x, 2) for x in s.split()).decode("utf-8", "replace")
                elif m == "Morse":
                    v = from_morse(s)
                else:
                    v = s.translate(str.maketrans(
                        string.ascii_letters,
                        string.ascii_lowercase[13:] + string.ascii_lowercase[:13] +
                        string.ascii_uppercase[13:] + string.ascii_uppercase[:13]))
                self.set_box(out, v)
            except (binascii.Error, ValueError, UnicodeDecodeError) as e:
                self.set_box(out, f"✗ {e}")

        self.buttons(c, [("→ Encode", enc), ("← Decode", dec),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_jsontools(self, p):
        c = self.card(p, "{} " + self.t("JSON Tools"))
        box = self.textbox(c, 220, '{"hello": "world", "n": [1, 2, 3]}')
        out = self.textbox(c, 240)

        def act(kind: str):
            try:
                data = json.loads(box.get("1.0", "end"))
                if kind == "format":
                    v = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)
                elif kind == "minify":
                    v = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                elif kind == "sort":
                    v = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
                else:
                    def walk(o, d=0):
                        if isinstance(o, dict):
                            return 1 + sum(walk(v_, d + 1) for v_ in o.values())
                        if isinstance(o, list):
                            return 1 + sum(walk(v_, d + 1) for v_ in o)
                        return 1
                    v = (f"✓ valid JSON\ntype   : {type(data).__name__}\n"
                         f"nodes  : {walk(data)}\n"
                         f"top keys: {', '.join(map(str, data))[:300]}"
                         if isinstance(data, dict) else f"✓ valid JSON\ntype: {type(data).__name__}")
                self.set_box(out, v)
            except json.JSONDecodeError as e:
                self.set_box(out, f"✗ invalid JSON\nline {e.lineno}, col {e.colno}: {e.msg}")

        self.buttons(c, [("Format", lambda: act("format")), ("Minify", lambda: act("minify")),
                         ("Sort keys", lambda: act("sort")), ("Validate", lambda: act("validate")),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_regex(self, p):
        c = self.card(p, "🪄 " + self.t("Regex Tester"))
        pat = self.field(c, "pattern", r"\b\w+@\w+\.\w+\b", 420)
        r = self.row(c)
        side = "right" if self.rtl else "left"
        flags = {}
        for name in ("IGNORECASE", "MULTILINE", "DOTALL", "UNICODE"):
            cb = ctk.CTkCheckBox(r, text=name.lower(), width=110)
            cb.pack(side=side, padx=4)
            flags[name] = cb
        box = self.textbox(c, 170, "contact: omar@test.com, lina@demo.org")
        repl = self.field(c, "replace with", "", 420)
        out = self.textbox(c, 220)

        def replace_all():
            try:
                rx = re.compile(pat.get())
                s = box.get("1.0", "end").rstrip("\n")
                new, cnt = rx.subn(repl.get(), s)
                self.set_box(out, f"✓ {cnt} replacement(ies)\n" + "-" * 40 + "\n" + new)
            except re.error as e:
                self.set_box(out, f"✗ invalid pattern: {e}")

        def test(*_):
            f = 0
            for name, cb in flags.items():
                if cb.get():
                    f |= getattr(re, name)
            try:
                rx = re.compile(pat.get(), f)
                s = box.get("1.0", "end").rstrip("\n")
                ms = list(rx.finditer(s))
                L = [f"✓ {len(ms)} match(es)", "-" * 40]
                for i, m in enumerate(ms[:100], 1):
                    L.append(f"{i:>3}. [{m.start()}:{m.end()}]  {m.group(0)!r}")
                    if m.groups():
                        L.append(f"      groups: {m.groups()}")
                    if m.groupdict():
                        L.append(f"      named : {m.groupdict()}")
                self.set_box(out, "\n".join(L))
            except re.error as e:
                self.set_box(out, f"✗ invalid pattern: {e}")

        box.bind("<KeyRelease>", test)
        pat.bind("<KeyRelease>", test)
        self.buttons(c, [(self.t("Run"), test),
                         ("⇄ " + self.t("Replace"), replace_all),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])
        test()

    def page_urlan(self, p):
        c = self.card(p, "🔗 " + self.t("URL Analyzer"))
        url = self.field(c, "URL", "https://user:pw@example.com:8443/a/b?x=1&y=2#top", 480)
        out = self.textbox(c, 260)

        def analyze():
            u = urllib.parse.urlparse(url.get().strip())
            qs = urllib.parse.parse_qs(u.query)
            L = [f" scheme   : {u.scheme}", f" host     : {u.hostname}",
                 f" port     : {u.port or '(default)'}", f" user     : {u.username or '-'}",
                 f" path     : {u.path or '/'}", f" fragment : {u.fragment or '-'}",
                 "", " query parameters:"]
            L += [f"   {k:<16} = {', '.join(v)}" for k, v in qs.items()] or ["   (none)"]
            L += ["", f" decoded path : {urllib.parse.unquote(u.path)}"]
            self.set_box(out, "\n".join(L))

        self.buttons(c, [(self.t("Run"), analyze)])
        analyze()

    # ═════════════════════════════════════════════════════
    # 【12】 صفحات القسم: Security
    # ═════════════════════════════════════════════════════
    def page_password(self, p):
        c = self.card(p, "🔑 " + self.t("Password Generator"))
        length = ctk.CTkSlider(c, from_=6, to=64, number_of_steps=58)
        length.set(20)
        lab = ctk.CTkLabel(c, text="length: 20")
        lab.pack(anchor="e" if self.rtl else "w", padx=16)
        length.pack(fill="x", padx=16, pady=(0, 8))
        length.configure(command=lambda v: lab.configure(text=f"length: {int(v)}"))

        r = self.row(c)
        side = "right" if self.rtl else "left"
        opts = {}
        for name, default in (("a-z", True), ("A-Z", True), ("0-9", True),
                              ("!@#", True), ("no ambiguous", False)):
            cb = ctk.CTkCheckBox(r, text=name, width=120)
            if default:
                cb.select()
            cb.pack(side=side, padx=4)
            opts[name] = cb

        out = self.textbox(c, 170)
        meter = ctk.CTkProgressBar(c, height=10)
        meter.set(0)
        meter.pack(fill="x", padx=16, pady=6)
        info = self.statuslabel(c)

        def gen():
            pool = ""
            if opts["a-z"].get():
                pool += string.ascii_lowercase
            if opts["A-Z"].get():
                pool += string.ascii_uppercase
            if opts["0-9"].get():
                pool += string.digits
            if opts["!@#"].get():
                pool += "!@#$%^&*()-_=+[]{};:,.?/"
            if opts["no ambiguous"].get():
                pool = "".join(ch for ch in pool if ch not in "l1IO0o|`'\"")
            if not pool:
                self.toast("select at least one set", "warn")
                return
            rnd = random.SystemRandom()
            n = int(length.get())
            pws = ["".join(rnd.choice(pool) for _ in range(n)) for _ in range(8)]
            self.set_box(out, "\n".join(pws))
            bits = entropy_bits(pws[0])
            level = ("very weak" if bits < 40 else "weak" if bits < 60 else
                     "good" if bits < 80 else "strong" if bits < 110 else "excellent")
            meter.set(min(1.0, bits / 128))
            meter.configure(progress_color=(C("err") if bits < 60 else
                                            C("warn") if bits < 80 else C("ok")))
            info.configure(text=f"entropy ≈ {bits} bits  ·  {level}  ·  pool {len(pool)} chars",
                           text_color=CC("muted"))

        self.buttons(c, [("🎲 " + self.t("Generate"), gen),
                         (self.t("Copy"),
                          lambda: self.copy_text(out.get("1.0", "end").split("\n")[0]))])
        gen()

    def page_hash(self, p):
        c = self.card(p, "#️⃣ " + self.t("Text Hash"))
        box = self.textbox(c, 150, "hello")
        out = self.textbox(c, 220)

        def calc(*_):
            data = box.get("1.0", "end").rstrip("\n").encode()
            L = [f" {a:<8}: {hashlib.new(a, data).hexdigest()}"
                 for a in ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")]
            L.append(f" {'crc-ish':<8}: {binascii.crc32(data) & 0xFFFFFFFF:08x}")
            self.set_box(out, "\n".join(L))

        box.bind("<KeyRelease>", calc)
        self.buttons(c, [(self.t("Run"), calc),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])
        calc()

    def page_uuidgen(self, p):
        c = self.card(p, "🆔 " + self.t("UUID Generator"))
        kind = self.option(c, "version", ["uuid4 (random)", "uuid1 (time)",
                                          "uuid5 (name)", "ULID-like"], width=200)
        name = self.field(c, "name (v5)", "example.com", 300)
        count = self.field(c, "count", "10", 100)
        out = self.textbox(c, 260)

        def gen():
            n = max(1, min(500, int(count.get() or 10)))
            k = kind.get()
            res = []
            for _ in range(n):
                if k.startswith("uuid4"):
                    res.append(str(uuid.uuid4()))
                elif k.startswith("uuid1"):
                    res.append(str(uuid.uuid1()))
                elif k.startswith("uuid5"):
                    res.append(str(uuid.uuid5(uuid.NAMESPACE_DNS, name.get() or "x")))
                else:
                    ts = format(int(time.time() * 1000), "012x")
                    res.append((ts + uuid.uuid4().hex[:14]).upper())
            self.set_box(out, "\n".join(res))

        self.buttons(c, [("🎲 " + self.t("Generate"), gen),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])
        gen()

    # ═════════════════════════════════════════════════════
    # 【13】 صفحات القسم: Media
    # ═════════════════════════════════════════════════════
    def page_color(self, p):
        c = self.card(p, "🎨 " + self.t("Color Converter"))
        hexv = self.field(c, "HEX", "#E01B24", 180)
        rgbv = self.field(c, "RGB", "224, 27, 36", 180)
        hslv = self.field(c, "HSL", "", 180)
        swatch = tk.Canvas(c, height=70, highlightthickness=1, bg="#E01B24")
        swatch.pack(fill="x", padx=16, pady=8)
        info = self.statuslabel(c)

        def from_hex(*_):
            try:
                r, g, b = hex_to_rgb(hexv.get())
                update(r, g, b, skip="hex")
            except Exception:
                pass

        def from_rgb(*_):
            try:
                parts = [int(x) for x in re.findall(r"\d+", rgbv.get())][:3]
                if len(parts) == 3:
                    update(*parts, skip="rgb")
            except Exception:
                pass

        def from_hsl(*_):
            try:
                parts = [float(x) for x in re.findall(r"[\d.]+", hslv.get())][:3]
                if len(parts) == 3:
                    update(*hsl_to_rgb(*parts), skip="hsl")
            except Exception:
                pass

        def update(r, g, b, skip=""):
            hx = rgb_to_hex(r, g, b)
            h, s, l = rgb_to_hsl(r, g, b)
            if skip != "hex":
                hexv.delete(0, "end"); hexv.insert(0, hx)
            if skip != "rgb":
                rgbv.delete(0, "end"); rgbv.insert(0, f"{r}, {g}, {b}")
            if skip != "hsl":
                hslv.delete(0, "end"); hslv.insert(0, f"{h}, {s}%, {l}%")
            swatch.configure(bg=hx)
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            info.configure(text=(f"rgba({r},{g},{b},1)   ·   luminance {lum:.2f}   ·   "
                                 f"contrast-safe text: {'black' if lum > 0.55 else 'white'}   ·   "
                                 f"CMYK-ish {100 - int(r/2.55)},{100 - int(g/2.55)},{100 - int(b/2.55)}"))

        hexv.bind("<KeyRelease>", from_hex)
        rgbv.bind("<KeyRelease>", from_rgb)
        hslv.bind("<KeyRelease>", from_hsl)
        from_hex()
        self.buttons(c, [(self.t("Copy"), lambda: self.copy_text(hexv.get()))])

    def page_palette(self, p):
        c = self.card(p, "🖌️ " + self.t("Color Palette"))
        base = self.field(c, "base HEX", "#E01B24", 180)
        scheme = self.option(c, "scheme", ["Complementary", "Analogous", "Triadic",
                                           "Tetradic", "Monochromatic", "Shades"], width=200)
        holder = ctk.CTkFrame(c, fg_color="transparent")
        holder.pack(fill="x", padx=12, pady=8)
        codes = self.statuslabel(c)

        def gen():
            for w in holder.winfo_children():
                w.destroy()
            try:
                r, g, b = hex_to_rgb(base.get())
            except Exception:
                self.toast("bad hex", "err")
                return
            h, s, l = rgb_to_hsl(r, g, b)
            sc = scheme.get()
            if sc == "Complementary":
                specs = [(h, s, l), (h + 180, s, l), (h, s * 0.6, l * 1.2), (h + 180, s * 0.6, l * 0.8)]
            elif sc == "Analogous":
                specs = [(h - 60, s, l), (h - 30, s, l), (h, s, l), (h + 30, s, l), (h + 60, s, l)]
            elif sc == "Triadic":
                specs = [(h, s, l), (h + 120, s, l), (h + 240, s, l)]
            elif sc == "Tetradic":
                specs = [(h, s, l), (h + 90, s, l), (h + 180, s, l), (h + 270, s, l)]
            elif sc == "Monochromatic":
                specs = [(h, s, x) for x in (20, 35, 50, 65, 80)]
            else:
                specs = [(h, s, x) for x in (10, 25, 40, 55, 70, 85)]
            hexes = []
            for hh, ss, ll in specs:
                col = rgb_to_hex(*hsl_to_rgb(hh, clamp(ss, 0, 100), clamp(ll, 0, 100)))
                hexes.append(col)
                cell = tk.Canvas(holder, height=90, width=110, bg=col, highlightthickness=0)
                cell.pack(side="right" if self.rtl else "left", padx=4)
                cell.bind("<Button-1>", lambda e, cc=col: self.copy_text(cc))
            codes.configure(text="   ".join(hexes) + "   (" + self.t("Click a color to copy") + ")")

        self.buttons(c, [(self.t("Generate"), gen),
                         ("🎲 Random", lambda: (base.delete(0, "end"),
                                                base.insert(0, rgb_to_hex(
                                                    random.randint(0, 255),
                                                    random.randint(0, 255),
                                                    random.randint(0, 255))),
                                                gen()))])
        gen()

    def page_qr(self, p):
        if not self.need(p, "qrcode") or not self.need(p, "Pillow"):
            return
        c = self.card(p, "🔳 " + self.t("QR Code"))
        data = self.field(c, "text / URL", "https://example.com", 420)
        size = self.option(c, "box size", ["4", "6", "8", "10", "12"], "8", 120)
        holder = ctk.CTkFrame(c, fg_color="transparent")
        holder.pack(pady=10)
        self._qr_img = None
        st = self.statuslabel(c)

        def gen():
            for w in holder.winfo_children():
                w.destroy()
            try:
                qr = qrcode.QRCode(box_size=int(size.get()), border=2,
                                   error_correction=qrcode.constants.ERROR_CORRECT_M)
                qr.add_data(data.get().strip() or " ")
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
                self._qr_img = ctk.CTkImage(light_image=img, dark_image=img,
                                            size=(min(360, img.size[0]), min(360, img.size[1])))
                ctk.CTkLabel(holder, image=self._qr_img, text="").pack()
                self._qr_pil = img
                st.configure(text=f"{img.size[0]}×{img.size[1]} px", text_color=CC("muted"))
            except Exception as e:
                st.configure(text=f"✗ {e}", text_color=CC("err"))

        def save():
            path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG", "*.png")])
            if path and getattr(self, "_qr_pil", None):
                self._qr_pil.save(path)
                self.toast(f"{self.t('Done')}: {os.path.basename(path)}", "ok")

        self.buttons(c, [(self.t("Generate"), gen), ("💾 " + self.t("Save"), save)])
        gen()

    def page_image(self, p):
        if not self.need(p, "Pillow"):
            return
        c = self.card(p, "🖼️ " + self.t("Image Tools"))
        src = self._file_picker(c, "image")
        op = self.option(c, "operation",
                         ["Resize", "Rotate 90", "Rotate 180", "Grayscale",
                          "Flip horizontal", "Flip vertical", "Convert format",
                          "Thumbnail 256", "Auto contrast"], width=220)
        w_e = self.field(c, "width", "800", 120)
        h_e = self.field(c, "height", "0 (auto)", 120)
        fmt = self.option(c, "format", ["PNG", "JPEG", "WEBP", "BMP"], "PNG", 120)
        out = self.textbox(c, 160)
        st = self.statuslabel(c)

        def process() -> str:
            path = src.get().strip()
            img = Image.open(path)
            o = op.get()
            if o == "Resize":
                w = int(re.findall(r"\d+", w_e.get())[0])
                hh = re.findall(r"\d+", h_e.get())
                h = int(hh[0]) if hh and int(hh[0]) > 0 else int(img.height * w / img.width)
                img = img.resize((w, h), Image.LANCZOS)
            elif o == "Rotate 90":
                img = img.rotate(-90, expand=True)
            elif o == "Rotate 180":
                img = img.rotate(180, expand=True)
            elif o == "Grayscale":
                img = img.convert("L")
            elif o == "Flip horizontal":
                img = ImageOps.mirror(img)
            elif o == "Flip vertical":
                img = ImageOps.flip(img)
            elif o == "Thumbnail 256":
                img.thumbnail((256, 256))
            elif o == "Auto contrast":
                img = ImageOps.autocontrast(img.convert("RGB"))
            ext = fmt.get().lower().replace("jpeg", "jpg")
            dst = f"{os.path.splitext(path)[0]}_{o.split()[0].lower()}.{ext}"
            if fmt.get() == "JPEG":
                img = img.convert("RGB")
            img.save(dst, fmt.get())
            return (f"✓ {o}\n source : {path}\n output : {dst}\n"
                    f" size   : {img.size[0]}×{img.size[1]}  ·  {human_size(os.path.getsize(dst))}")

        self.buttons(c, [("▶ " + self.t("Run"),
                          lambda: self.run_async(process, lambda r_: self.set_box(out, r_), st))])

    # ═════════════════════════════════════════════════════
    # 【14】 صفحات القسم: Calc & Time
    # ═════════════════════════════════════════════════════
    def page_calc(self, p):
        c = self.card(p, "🧮 " + self.t("Calculator"))
        ctk.CTkLabel(c, text=self.t("Safe: parsed via ast — no eval"),
                     text_color=CC("muted")).pack(anchor="e" if self.rtl else "w", padx=14)
        expr = ctk.CTkEntry(c, height=48, font=ctk.CTkFont(size=20))
        expr.pack(fill="x", padx=16, pady=8)
        result = ctk.CTkLabel(c, text="0", font=ctk.CTkFont(size=30, weight="bold"),
                              text_color=CC("primary"))
        result.pack(anchor="e" if self.rtl else "w", padx=18)
        hist = self.textbox(c, 150)

        def compute(*_):
            s = expr.get().strip()
            if not s:
                result.configure(text="0", text_color=CC("primary"))
                return
            try:
                v = safe_eval(s)
                txt = f"{v:,.10g}" if isinstance(v, float) else f"{v:,}"
                result.configure(text=txt, text_color=CC("ok"))
            except Exception as e:
                result.configure(text=f"✗ {e}", text_color=CC("err"))

        def push(*_):
            s = expr.get().strip()
            try:
                v = safe_eval(s)
                hist.insert("1.0", f"{s} = {v}\n")
                compute()
            except Exception:
                pass

        expr.bind("<KeyRelease>", compute)
        expr.bind("<Return>", push)

        keys = ["7", "8", "9", "/", "(", ")", "4", "5", "6", "*", "sqrt(", "^",
                "1", "2", "3", "-", "pi", "e", "0", ".", "%", "+", "log(", "C"]
        grid = ctk.CTkFrame(c, fg_color="transparent")
        grid.pack(padx=16, pady=8)

        def tap(k: str):
            if k == "C":
                expr.delete(0, "end")
            else:
                expr.insert("end", k)
            compute()

        for i, k in enumerate(keys):
            ctk.CTkButton(grid, text=k, width=70, height=38,
                          fg_color=CC("primary") if k in "+-*/^" else CC("surface2"),
                          text_color=CC("text") if k not in "+-*/^" else "#ffffff",
                          hover_color=CC("primary_h"),
                          command=lambda kk=k: tap(kk)).grid(row=i // 6, column=i % 6,
                                                             padx=3, pady=3)
        self.buttons(c, [("= " + self.t("Run"), push),
                         (self.t("Clear"), lambda: hist.delete("1.0", "end"))])

    def page_units(self, p):
        c = self.card(p, "📏 " + self.t("Unit Converter"))
        cats = list(UNITS.keys()) + ["Temperature"]
        cat = self.option(c, "category", cats, "Length", 200)
        val = self.field(c, "value", "1", 180)
        frm = self.option(c, "from", list(UNITS["Length"]), "m", 180)
        to = self.option(c, "to", list(UNITS["Length"]), "km", 180)
        out = self.textbox(c, 220)

        def on_cat(_=None):
            names = TEMP_UNITS if cat.get() == "Temperature" else list(UNITS[cat.get()])
            frm.configure(values=names)
            to.configure(values=names)
            frm.set(names[0])
            to.set(names[1] if len(names) > 1 else names[0])
            convert()

        def convert(*_):
            try:
                v = float(val.get())
                if cat.get() == "Temperature":
                    res = convert_temp(v, frm.get(), to.get())
                    lines = [f" {v:g} {frm.get()}  =  {res:.4f} {to.get()}", ""]
                    for u in TEMP_UNITS:
                        lines.append(f"   {convert_temp(v, frm.get(), u):>12.4f} {u}")
                else:
                    table = UNITS[cat.get()]
                    base = v * table[frm.get()]
                    lines = [f" {v:g} {frm.get()}  =  {base / table[to.get()]:.8g} {to.get()}", ""]
                    for u, k in table.items():
                        lines.append(f"   {base / k:>18.8g} {u}")
                self.set_box(out, "\n".join(lines))
            except Exception as e:
                self.set_box(out, f"✗ {e}")

        cat.configure(command=lambda _: on_cat())
        frm.configure(command=lambda _: convert())
        to.configure(command=lambda _: convert())
        val.bind("<KeyRelease>", convert)
        convert()

    def page_datetime(self, p):
        c = self.card(p, "📅 Date difference / Age")
        d1 = self.field(c, "date 1", "1990-01-01", 180)
        d2 = self.field(c, "date 2", _dt.date.today().isoformat(), 180)
        out = self.textbox(c, 200)

        def diff():
            try:
                a = _dt.date.fromisoformat(d1.get().strip())
                b = _dt.date.fromisoformat(d2.get().strip())
                if a > b:
                    a, b = b, a
                days = (b - a).days
                years = b.year - a.year - ((b.month, b.day) < (a.month, a.day))
                months = (b.year - a.year) * 12 + b.month - a.month - (b.day < a.day)
                self.set_box(out, "\n".join([
                    f" days     : {days:,}",
                    f" weeks    : {days // 7:,} ({days % 7} days)",
                    f" months   : {months:,}",
                    f" years    : {years}",
                    f" hours    : {days * 24:,}",
                    f" minutes  : {days * 1440:,}",
                    "",
                    f" age today       : {years} years",
                    f" next milestone  : {next_birthday_days(a, years)} days",
                    f" weekday of d1   : {a:%A}",
                    f" weekday of d2   : {b:%A}",
                    f" ISO week d2     : {b.isocalendar()[1]}",
                ]))
            except Exception as e:
                self.set_box(out, f"✗ {e}")

        self.buttons(c, [(self.t("Run"), diff)])
        diff()

        ts = self.card(p, "⏲️ Timestamp ⇄ Date")
        tsin = self.field(ts, "timestamp", str(int(time.time())), 200)
        tsout = self.textbox(ts, 160)

        def conv_ts():
            try:
                v = float(tsin.get().strip())
                if v > 1e11:
                    v /= 1000
                dt = _dt.datetime.fromtimestamp(v)
                utc = _dt.datetime.utcfromtimestamp(v)
                self.set_box(tsout, "\n".join([
                    f" local : {dt:%Y-%m-%d %H:%M:%S}",
                    f" UTC   : {utc:%Y-%m-%d %H:%M:%S}",
                    f" ISO   : {dt.isoformat()}",
                    f" RFC   : {dt:%a, %d %b %Y %H:%M:%S}",
                    f" ago   : {human_time(abs(time.time() - v))}",
                ]))
            except Exception as e:
                self.set_box(tsout, f"✗ {e}")

        self.buttons(ts, [(self.t("Convert"), conv_ts),
                          ("⏱ now", lambda: (tsin.delete(0, "end"),
                                             tsin.insert(0, str(int(time.time()))), conv_ts()))])
        conv_ts()

    def page_timer(self, p):
        c = self.card(p, "⏱️ Stopwatch")
        disp = ctk.CTkLabel(c, text="00:00:00.0", font=ctk.CTkFont(size=44, weight="bold"),
                            text_color=CC("primary"))
        disp.pack(pady=10)
        state = {"t0": 0.0, "acc": 0.0, "run": False}
        laps = self.textbox(c, 130)

        def tick():
            if state["run"]:
                el = state["acc"] + (time.time() - state["t0"])
                disp.configure(text=time.strftime("%H:%M:%S", time.gmtime(el)) + f".{int(el*10)%10}")
            self._timers["sw"] = self.after(100, tick)

        def toggle():
            if state["run"]:
                state["acc"] += time.time() - state["t0"]
                state["run"] = False
            else:
                state["t0"] = time.time()
                state["run"] = True

        def reset():
            state.update(t0=0.0, acc=0.0, run=False)
            disp.configure(text="00:00:00.0")

        def lap():
            laps.insert("1.0", disp.cget("text") + "\n")

        self.buttons(c, [("▶/⏸", toggle), ("⏺ Lap", lap), ("⟲ " + self.t("Reset"), reset)])
        tick()

        cd = self.card(p, "⏳ Countdown")
        mins = self.field(cd, "minutes", "5", 120)
        cdisp = ctk.CTkLabel(cd, text="05:00", font=ctk.CTkFont(size=40, weight="bold"))
        cdisp.pack(pady=8)
        cstate = {"end": 0.0, "run": False}

        def ctick():
            if cstate["run"]:
                left = cstate["end"] - time.time()
                if left <= 0:
                    cstate["run"] = False
                    cdisp.configure(text="00:00", text_color=CC("err"))
                    self.toast("⏰ " + self.t("Time is up!"), "ok", 6000)
                    self.bell()
                else:
                    cdisp.configure(text=fmt_mmss(left), text_color=CC("text"))
            self._timers["cd"] = self.after(250, ctick)

        def cstart():
            try:
                cstate["end"] = time.time() + float(mins.get()) * 60
                cstate["run"] = True
            except Exception:
                self.toast("bad value", "err")

        self.buttons(cd, [("▶ " + self.t("Start"), cstart),
                          ("⏹ " + self.t("Stop"), lambda: cstate.update(run=False))])
        ctick()

    def page_pomodoro(self, p):
        c = self.card(p, "🍅 " + self.t("Pomodoro"))
        work = self.field(c, "work (min)", "25", 100)
        rest = self.field(c, "break (min)", "5", 100)
        phase = ctk.CTkLabel(c, text="READY", font=ctk.CTkFont(size=16, weight="bold"),
                             text_color=CC("muted"))
        phase.pack()
        disp = ctk.CTkLabel(c, text="25:00", font=ctk.CTkFont(size=56, weight="bold"),
                            text_color=CC("primary"))
        disp.pack(pady=6)
        bar = ctk.CTkProgressBar(c, height=10)
        bar.set(0)
        bar.pack(fill="x", padx=20, pady=8)
        stats = self.statuslabel(c)
        st = {"run": False, "work": True, "end": 0.0, "total": 1, "cycles": 0}

        def start():
            try:
                mins = float(work.get() if st["work"] else rest.get())
            except Exception:
                mins = 25
            st["total"] = mins * 60
            st["end"] = time.time() + st["total"]
            st["run"] = True
            phase.configure(text="FOCUS" if st["work"] else "BREAK",
                            text_color=CC("primary") if st["work"] else CC("ok"))

        def tick():
            if st["run"]:
                left = st["end"] - time.time()
                if left <= 0:
                    self.bell()
                    self.toast("🍅 " + (self.t("Break time!") if st["work"]
                                        else self.t("Back to work!")), "ok", 5000)
                    if st["work"]:
                        st["cycles"] += 1
                    st["work"] = not st["work"]
                    start()
                else:
                    disp.configure(text=fmt_mmss(left))
                    bar.set(1 - left / st["total"])
            stats.configure(text=f"completed pomodoros: {st['cycles']}")
            self._timers["pomo"] = self.after(250, tick)

        self.buttons(c, [("▶ " + self.t("Start"), start),
                         ("⏸ " + self.t("Stop"), lambda: st.update(run=False)),
                         ("⟲ " + self.t("Reset"),
                          lambda: (st.update(run=False, work=True, cycles=0),
                                   disp.configure(text="25:00"), bar.set(0),
                                   phase.configure(text="READY", text_color=CC("muted"))))])
        tick()

    # ═════════════════════════════════════════════════════
    # 【15】 صفحات القسم: Productivity
    # ═════════════════════════════════════════════════════
    def page_todo(self, p):
        c = self.card(p, "✅ " + self.t("Todo List"))
        tasks: List[Dict[str, Any]] = jload(F_TASKS, [])
        r = self.row(c)
        side = "right" if self.rtl else "left"
        entry = ctk.CTkEntry(r, placeholder_text="new task…", width=360)
        entry.pack(side=side, padx=4)
        prio = ctk.CTkOptionMenu(r, values=["low", "normal", "high"], width=110)
        prio.set("normal")
        prio.pack(side=side, padx=4)
        listf = ctk.CTkFrame(c, fg_color="transparent")
        listf.pack(fill="both", expand=True, padx=12, pady=8)
        counter = self.statuslabel(c)

        def persist():
            jsave(F_TASKS, tasks)

        def render():
            for w in listf.winfo_children():
                w.destroy()
            for i, tsk in enumerate(tasks):
                row = ctk.CTkFrame(listf, fg_color=CC("surface2"), corner_radius=8)
                row.pack(fill="x", pady=2)
                cb = ctk.CTkCheckBox(row, text="", width=28,
                                     command=lambda idx=i: toggle(idx))
                if tsk.get("done"):
                    cb.select()
                cb.pack(side=side, padx=6, pady=6)
                col = {"high": C("err"), "normal": C("text"), "low": C("muted")}.get(
                    tsk.get("priority", "normal"), C("text"))
                ctk.CTkLabel(row, text=("✔ " if tsk.get("done") else "") + tsk["text"],
                             text_color=C("muted") if tsk.get("done") else col,
                             anchor="e" if self.rtl else "w").pack(
                    side=side, fill="x", expand=True, padx=6)
                ctk.CTkLabel(row, text=tsk.get("created", "")[:10],
                             text_color=CC("muted"), font=ctk.CTkFont(size=10)).pack(side=side, padx=6)
                ctk.CTkButton(row, text="✕", width=32, fg_color="transparent",
                              hover_color=CC("err"), text_color=CC("muted"),
                              command=lambda idx=i: remove(idx)).pack(side=side, padx=4)
            done = sum(1 for x in tasks if x.get("done"))
            counter.configure(text=f"{done}/{len(tasks)} " + self.t("Done").lower())

        def add(*_):
            txt = entry.get().strip()
            if not txt:
                return
            tasks.append({"text": txt, "done": False, "priority": prio.get(),
                          "created": _dt.datetime.now().isoformat(timespec="seconds")})
            entry.delete(0, "end")
            persist()
            render()

        def toggle(i: int):
            tasks[i]["done"] = not tasks[i].get("done")
            persist()
            render()

        def remove(i: int):
            tasks.pop(i)
            persist()
            render()

        entry.bind("<Return>", add)
        ctk.CTkButton(r, text="➕ " + self.t("Add"), width=100, command=add).pack(side=side, padx=4)
        self.buttons(c, [("🧹 Clear done",
                          lambda: (tasks.__setitem__(slice(None),
                                                     [x for x in tasks if not x.get("done")]),
                                   persist(), render()))])
        render()

    def page_notes(self, p):
        c = self.card(p, "📝 " + self.t("Notes"))
        box = self.textbox(c, 420)
        try:
            with open(F_NOTES, "r", encoding="utf-8") as f:
                box.insert("1.0", f.read())
        except Exception:
            pass
        st = self.statuslabel(c)

        def save():
            try:
                with open(F_NOTES, "w", encoding="utf-8") as f:
                    f.write(box.get("1.0", "end").rstrip("\n"))
                st.configure(text=f"✓ {self.t('Save')} {_dt.datetime.now():%H:%M:%S}",
                             text_color=CC("ok"))
            except Exception as e:
                st.configure(text=f"✗ {e}", text_color=CC("err"))

        def export():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(box.get("1.0", "end"))
                self.toast(self.t("Done"), "ok")

        def load():
            path = filedialog.askopenfilename(filetypes=[("Text", "*.txt *.md"), ("All", "*.*")])
            if path:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    self.set_box(box, f.read())

        self.buttons(c, [("💾 " + self.t("Save"), save),
                         ("📂 " + self.t("Load"), load),
                         ("📤 " + self.t("Export"), export)])
        st.configure(text="💾 " + self.t("autosave every 30s"), text_color=CC("muted"))

        def autosave():
            save()
            self._timers["notes_auto"] = self.after(30000, autosave)

        self._timers["notes_auto"] = self.after(30000, autosave)

    def page_backup(self, p):
        c = self.card(p, "💾 " + self.t("Backup"))
        out = self.textbox(c, 220)
        st = self.statuslabel(c)

        def export_all() -> str:
            path = filedialog.asksaveasfilename(defaultextension=".json",
                                                initialfile="toolbox_backup.json")
            if not path:
                return "cancelled"
            bundle = {
                "app": APP_NAME, "version": APP_VERSION,
                "exported": _dt.datetime.now().isoformat(timespec="seconds"),
                "settings": self.settings,
                "tasks": jload(F_TASKS, []),
                "notes": open(F_NOTES, encoding="utf-8").read() if os.path.exists(F_NOTES) else "",
                "history": jload(F_HISTORY, []),
            }
            jsave(path, bundle)
            return f"✓ exported → {path}\n{human_size(os.path.getsize(path))}"

        def import_all() -> str:
            path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
            if not path:
                return "cancelled"
            b = jload(path, {})
            if "settings" not in b:
                raise ValueError("not a Toolbox backup")
            self.settings.update(b["settings"])
            self.save_settings()
            jsave(F_TASKS, b.get("tasks", []))
            with open(F_NOTES, "w", encoding="utf-8") as f:
                f.write(b.get("notes", ""))
            jsave(F_HISTORY, b.get("history", []))
            return f"✓ imported from {path}\n" + self.t("Restart the app to apply everything.")

        self.buttons(c, [("📤 " + self.t("Export"),
                          lambda: self.run_async(export_all, lambda r_: self.set_box(out, r_), st)),
                         ("📥 " + self.t("Import"),
                          lambda: self.run_async(import_all, lambda r_: self.set_box(out, r_), st))])

        f = self.card(p, "📁 Local files")
        rows = []
        for path in (F_SETTINGS, F_TASKS, F_NOTES, F_THEME, F_HISTORY):
            ex = os.path.exists(path)
            rows.append(f" {'✓' if ex else '·'}  {os.path.basename(path):<34} "
                        f"{human_size(os.path.getsize(path)) if ex else '-'}")
        ctk.CTkLabel(f, text="\n".join(rows), justify="left",
                     font=ctk.CTkFont(family="Courier", size=12)).pack(
            anchor="e" if self.rtl else "w", padx=16, pady=(4, 14))

    # ═════════════════════════════════════════════════════
    # 【16】 صفحات القسم: Data
    # ═════════════════════════════════════════════════════
    def page_fake(self, p):
        c = self.card(p, "🧪 " + self.t("Fake Data"))
        count = self.field(c, "count", "20", 100)
        fmt = self.option(c, "format", ["Table", "JSON", "CSV", "SQL INSERT"], "Table", 180)
        out = self.textbox(c, 340)

        def gen():
            n = max(1, min(1000, int(re.findall(r"\d+", count.get() or "20")[0])))
            people = [fake_person() for _ in range(n)]
            f = fmt.get()
            if f == "JSON":
                v = json.dumps(people, ensure_ascii=False, indent=2)
            elif f == "CSV":
                buf = io.StringIO()
                w = csv.DictWriter(buf, fieldnames=list(people[0]))
                w.writeheader()
                w.writerows(people)
                v = buf.getvalue()
            elif f == "SQL INSERT":
                cols = ", ".join(people[0])
                v = "\n".join(
                    "INSERT INTO users ({}) VALUES ({});".format(
                        cols, ", ".join("'" + str(x).replace("'", "''") + "'" for x in pr.values()))
                    for pr in people)
            else:
                v = (f"{'NAME':<22}{'EMAIL':<36}{'PHONE':<20}{'CITY'}\n" + "-" * 96 + "\n" +
                     "\n".join(f"{x['name']:<22}{x['email']:<36}{x['phone']:<20}{x['city']}"
                               for x in people))
            self.set_box(out, v)

        self.buttons(c, [("🎲 " + self.t("Generate"), gen),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])
        gen()

    def page_picker(self, p):
        c = self.card(p, "🎯 " + self.t("Random Picker"))
        ctk.CTkLabel(c, text=self.t("One item per line"), text_color=CC("muted")).pack(
            anchor="e" if self.rtl else "w", padx=14)
        box = self.textbox(c, 200, "Alice\nBob\nCarol\nDave")
        n = self.field(c, "pick", "1", 100)
        out = self.textbox(c, 150)

        def pick():
            items = [x.strip() for x in box.get("1.0", "end").splitlines() if x.strip()]
            if not items:
                return
            k = max(1, min(len(items), int(re.findall(r"\d+", n.get() or "1")[0])))
            rnd = random.SystemRandom()
            self.set_box(out, "🎯 " + "\n🎯 ".join(rnd.sample(items, k)))

        def shuffle():
            items = [x.strip() for x in box.get("1.0", "end").splitlines() if x.strip()]
            random.SystemRandom().shuffle(items)
            self.set_box(out, "\n".join(f"{i}. {x}" for i, x in enumerate(items, 1)))

        self.buttons(c, [("🎯 Pick", pick), ("🔀 Shuffle", shuffle),
                         ("🎲 Dice", lambda: self.set_box(
                             out, f"🎲 {random.SystemRandom().randint(1, 6)}")),
                         ("🪙 Coin", lambda: self.set_box(
                             out, random.SystemRandom().choice(["🪙 Heads", "🪙 Tails"])))])

    def page_lorem(self, p):
        c = self.card(p, "📄 " + self.t("Lorem Ipsum"))
        kind = self.option(c, "unit", ["Paragraphs", "Sentences", "Words"], "Paragraphs", 180)
        n = self.field(c, "count", "3", 100)
        out = self.textbox(c, 320)

        def sentence() -> str:
            words = [random.choice(LOREM_WORDS) for _ in range(random.randint(6, 16))]
            return " ".join(words).capitalize() + "."

        def gen():
            k = max(1, min(200, int(re.findall(r"\d+", n.get() or "3")[0])))
            if kind.get() == "Words":
                v = " ".join(random.choice(LOREM_WORDS) for _ in range(k)).capitalize() + "."
            elif kind.get() == "Sentences":
                v = " ".join(sentence() for _ in range(k))
            else:
                v = "\n\n".join(" ".join(sentence() for _ in range(random.randint(3, 6)))
                                for _ in range(k))
            self.set_box(out, v)

        self.buttons(c, [(self.t("Generate"), gen),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])
        gen()

    # ═════════════════════════════════════════════════════
    # 【17】 صفحات القسم: APIs — تعمل فقط عند الطلب الصريح
    # ═════════════════════════════════════════════════════
    def _key(self, name: str) -> str:
        return (self.settings.get("api_keys", {}).get(name) or "").strip()

    def page_weather(self, p):
        c = self.card(p, "⛅ " + self.t("Weather"))
        city = self.field(c, "city", "Istanbul", 260)
        out = self.textbox(c, 300)
        st = self.statuslabel(c)

        def fetch() -> str:
            q = city.get().strip() or "Istanbul"
            key = self._key("openweather")
            if key:
                d = http_json("https://api.openweathermap.org/data/2.5/weather?"
                              + urllib.parse.urlencode({"q": q, "appid": key,
                                                        "units": "metric", "lang": self.lang}))
                m, w = d["main"], d["weather"][0]
                return "\n".join([
                    f" 📍 {d['name']}, {d.get('sys', {}).get('country', '')}",
                    f" 🌡  {m['temp']:.1f}°C   (feels {m['feels_like']:.1f}°C)",
                    f" 📝 {w['description']}",
                    f" 💧 humidity {m['humidity']}%   ·  press {m['pressure']} hPa",
                    f" 💨 wind {d.get('wind', {}).get('speed', 0)} m/s",
                    f" 👁  visibility {d.get('visibility', 0) / 1000:.1f} km",
                    f" 🌅 {_dt.datetime.fromtimestamp(d['sys']['sunrise']):%H:%M}"
                    f"   🌇 {_dt.datetime.fromtimestamp(d['sys']['sunset']):%H:%M}",
                    "", " source: OpenWeather"])
            # fallback بدون مفتاح
            code, text = http_get(f"https://wttr.in/{urllib.parse.quote(q)}?format=j1")
            if code >= 400:
                raise RuntimeError(f"HTTP {code}")
            d = json.loads(text)
            cur = d["current_condition"][0]
            L = [f" 📍 {q}  (wttr.in — no API key needed)",
                 f" 🌡  {cur['temp_C']}°C  (feels {cur['FeelsLikeC']}°C)",
                 f" 📝 {cur['weatherDesc'][0]['value']}",
                 f" 💧 humidity {cur['humidity']}%   ·  💨 {cur['windspeedKmph']} km/h",
                 "", " forecast:"]
            for day in d["weather"][:3]:
                L.append(f"   {day['date']}   {day['mintempC']}°…{day['maxtempC']}°C")
            L += ["", " 💡 " + self.t("Add OpenWeather key in Settings for more details.")]
            return "\n".join(L)

        self.buttons(c, [("🔄 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st))])

    def page_currency(self, p):
        c = self.card(p, "💱 " + self.t("Currency"))
        amount = self.field(c, "amount", "100", 140)
        frm = self.field(c, "from", "USD", 120)
        to = self.field(c, "to", "TRY", 120)
        out = self.textbox(c, 300)
        st = self.statuslabel(c)

        def fetch() -> str:
            a = float(amount.get() or 1)
            f_, t_ = frm.get().strip().upper(), to.get().strip().upper()
            d = http_json(f"https://open.er-api.com/v6/latest/{f_}")
            if d.get("result") != "success":
                raise RuntimeError(d.get("error-type", "api error"))
            rates = d["rates"]
            if t_ not in rates:
                raise ValueError(f"unknown currency: {t_}")
            L = [f" {a:,.2f} {f_}  =  {a * rates[t_]:,.2f} {t_}",
                 f" rate: 1 {f_} = {rates[t_]:.6g} {t_}",
                 f" updated: {d.get('time_last_update_utc', '')}", "", " popular:"]
            for cur in ("USD", "EUR", "GBP", "TRY", "SAR", "AED", "EGP", "JPY", "CNY"):
                if cur in rates:
                    L.append(f"   {a:,.2f} {f_} → {a * rates[cur]:>14,.2f} {cur}")
            return "\n".join(L)

        self.buttons(c, [("💱 " + self.t("Convert"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st))])

    def page_translate(self, p):
        c = self.card(p, "🌍 " + self.t("Translate"))
        r = self.row(c)
        side = "right" if self.rtl else "left"
        src = ctk.CTkOptionMenu(r, values=list(LANG_NAMES), width=110)
        src.set("en")
        src.pack(side=side, padx=4)
        dst = ctk.CTkOptionMenu(r, values=list(LANG_NAMES), width=110)
        dst.set("ar")
        dst.pack(side=side, padx=4)
        box = self.textbox(c, 150, "Hello, how are you?")
        out = self.textbox(c, 170)
        st = self.statuslabel(c)

        def fetch() -> str:
            text = box.get("1.0", "end").strip()[:480]
            if not text:
                raise ValueError("empty text")
            url = ("https://api.mymemory.translated.net/get?" +
                   urllib.parse.urlencode({"q": text,
                                           "langpair": f"{src.get()}|{dst.get()}"}))
            d = http_json(url)
            best = d["responseData"]["translatedText"]
            alts = [m["translation"] for m in (d.get("matches") or [])[:3]]
            return best + ("\n\n— alternatives —\n" + "\n".join(f"· {a}" for a in alts) if alts else "")

        self.buttons(c, [("🌍 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st)),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_geoip(self, p):
        c = self.card(p, "📍 " + self.t("GeoIP"))
        ip = self.field(c, "IP (blank = me)", "", 240)
        out = self.textbox(c, 280)
        st = self.statuslabel(c)

        def fetch() -> str:
            target = ip.get().strip()
            token = self._key("ipinfo")
            if token:
                url = f"https://ipinfo.io/{target or ''}?token={token}"
            else:
                url = f"https://ipapi.co/{target + '/' if target else ''}json/"
            d = http_json(url)
            keys = ["ip", "city", "region", "country", "country_name", "org",
                    "asn", "loc", "latitude", "longitude", "timezone", "postal"]
            L = [f" {k:<14}: {d[k]}" for k in keys if k in d and d[k]]
            return "\n".join(L) or json.dumps(d, indent=2)

        self.buttons(c, [("📍 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st))])

    def page_github(self, p):
        c = self.card(p, "🐙 GitHub")
        user = self.field(c, "user / repo", "torvalds", 260)
        out = self.textbox(c, 340)
        st = self.statuslabel(c)

        def headers() -> dict:
            k = self._key("github")
            return {"Authorization": f"Bearer {k}"} if k else {}

        def fetch() -> str:
            q = user.get().strip()
            if "/" in q:
                d = http_json(f"https://api.github.com/repos/{q}", headers())
                return "\n".join([
                    f" 📦 {d['full_name']}",
                    f" {d.get('description') or ''}",
                    f" ⭐ {d['stargazers_count']:,}   🍴 {d['forks_count']:,}   "
                    f"👁 {d.get('watchers_count', 0):,}   🐛 {d['open_issues_count']}",
                    f" language : {d.get('language')}",
                    f" license  : {(d.get('license') or {}).get('name', '-')}",
                    f" created  : {d['created_at'][:10]}   updated: {d['updated_at'][:10]}",
                    f" size     : {human_size(d['size'] * 1024)}",
                    f" url      : {d['html_url']}"])
            d = http_json(f"https://api.github.com/users/{q}", headers())
            repos = http_json(f"https://api.github.com/users/{q}/repos?sort=updated&per_page=10",
                              headers())
            L = [f" 👤 {d.get('name') or d['login']}  (@{d['login']})",
                 f" {d.get('bio') or ''}",
                 f" 📍 {d.get('location') or '-'}   🏢 {d.get('company') or '-'}",
                 f" repos {d['public_repos']}   followers {d['followers']:,}   "
                 f"following {d['following']:,}",
                 f" joined {d['created_at'][:10]}", "", " recent repos:"]
            for rp in repos:
                L.append(f"   ⭐{rp['stargazers_count']:<6} {rp['name']:<30} "
                         f"{(rp.get('language') or '-'):<12} {rp['updated_at'][:10]}")
            return "\n".join(L)

        self.buttons(c, [("🐙 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st))])

    def page_crypto(self, p):
        c = self.card(p, "₿ " + self.t("Crypto Prices"))
        coins = self.field(c, "coins", "bitcoin,ethereum,solana,cardano", 380)
        vs = self.field(c, "vs", "usd", 100)
        out = self.textbox(c, 280)
        st = self.statuslabel(c)

        def fetch() -> str:
            url = ("https://api.coingecko.com/api/v3/simple/price?" +
                   urllib.parse.urlencode({"ids": coins.get().strip(),
                                           "vs_currencies": vs.get().strip() or "usd",
                                           "include_24hr_change": "true",
                                           "include_market_cap": "true"}))
            d = http_json(url)
            cur = (vs.get().strip() or "usd").lower()
            L = [f"{'COIN':<16}{'PRICE':>16}{'24H':>10}{'MCAP':>18}", "-" * 60]
            for name, v in d.items():
                ch = v.get(f"{cur}_24h_change", 0)
                L.append(f"{name:<16}{v.get(cur, 0):>16,.4f}{ch:>9.2f}%"
                         f"{v.get(f'{cur}_market_cap', 0):>18,.0f}")
            L += ["", " source: CoinGecko (no key required)"]
            return "\n".join(L)

        self.buttons(c, [("🔄 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st))])

    def page_news(self, p):
        c = self.card(p, "📰 " + self.t("News"))
        topic = self.field(c, "query", "technology", 260)
        country = self.field(c, "country", "us", 100)
        out = self.textbox(c, 340)
        st = self.statuslabel(c)

        def fetch() -> str:
            key = self._key("newsapi")
            if not key:
                return ("⚠ NewsAPI key required.\n\n"
                        "أضف المفتاح في: " + self.t("Settings") + " → API Keys → newsapi\n"
                        "احصل عليه مجانًا من newsapi.org")
            url = ("https://newsapi.org/v2/top-headlines?" +
                   urllib.parse.urlencode({"q": topic.get().strip(),
                                           "country": country.get().strip() or "us",
                                           "pageSize": 20, "apiKey": key}))
            d = http_json(url)
            if d.get("status") != "ok":
                raise RuntimeError(d.get("message", "api error"))
            L = [f" {d['totalResults']} results", ""]
            for a in d["articles"]:
                L += [f" ■ {a['title']}",
                      f"   {a['source']['name']}  ·  {a['publishedAt'][:16].replace('T', ' ')}",
                      f"   {a['url']}", ""]
            return "\n".join(L)

        self.buttons(c, [("📰 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st))])

    def page_shorten(self, p):
        c = self.card(p, "🔗 " + self.t("URL Shortener"))
        url = self.field(c, "long URL", "https://example.com/very/long/path", 440)
        out = self.textbox(c, 160)
        st = self.statuslabel(c)

        last = {"short": ""}

        def fetch() -> str:
            u = url.get().strip()
            if not u.startswith("http"):
                u = "https://" + u
            code, text = http_get("https://is.gd/create.php?" +
                                  urllib.parse.urlencode({"format": "simple", "url": u}))
            if code >= 400:
                raise RuntimeError(text[:200])
            last["short"] = text.strip()
            return f" short : {text.strip()}\n long  : {u}"

        self.buttons(c, [("🔗 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st)),
                         (self.t("Copy"),
                          lambda: self.copy_text(last["short"] or
                                                 out.get("1.0", "end").strip()))])

    def page_fun(self, p):
        c = self.card(p, "🎲 " + self.t("Fun APIs"))
        out = self.textbox(c, 260)
        st = self.statuslabel(c)

        def joke() -> str:
            d = http_json("https://official-joke-api.appspot.com/random_joke")
            return f" 😄 {d['setup']}\n\n    → {d['punchline']}"

        def advice() -> str:
            d = http_json("https://api.adviceslip.com/advice")
            return f" 💡 {d['slip']['advice']}"

        def catfact() -> str:
            d = http_json("https://catfact.ninja/fact")
            return f" 🐱 {d['fact']}"

        def activity() -> str:
            d = http_json("https://bored-api.appbrewery.com/random")
            return (f" 🎯 {d.get('activity')}\n    type: {d.get('type')}  ·  "
                    f"participants: {d.get('participants')}")

        self.buttons(c, [("😄 Joke", lambda: self.run_async(joke, lambda r_: self.set_box(out, r_), st)),
                         ("💡 Advice", lambda: self.run_async(advice, lambda r_: self.set_box(out, r_), st)),
                         ("🐱 Cat fact", lambda: self.run_async(catfact, lambda r_: self.set_box(out, r_), st)),
                         ("🎯 Activity", lambda: self.run_async(activity, lambda r_: self.set_box(out, r_), st))])

    def page_ai(self, p):
        c = self.card(p, "🤖 " + self.t("AI Assistant"))
        ctk.CTkLabel(c, text=self.t("OpenAI-compatible endpoint; keys in Settings") +
                     "  (OpenAI, Ollama, LM Studio, …)",
                     text_color=CC("muted")).pack(anchor="e" if self.rtl else "w", padx=14)
        model = self.field(c, "model", "gpt-4o-mini", 240)
        sysprompt = self.field(c, "system (optional)", "", 440)
        prompt = self.textbox(c, 140, "اشرح لي فكرة الـ threading باختصار.")
        out = self.textbox(c, 300)
        st = self.statuslabel(c)
        history: List[Dict[str, str]] = []       # محادثة متعددة الأدوار

        def ask() -> str:
            key = self._key("openai")
            if not key:
                return ("⚠ API key required.\n\n" + self.t("Settings") +
                        " → API Keys → openai")
            base = self._key("openai_base") or "https://api.openai.com/v1"
            q = prompt.get("1.0", "end").strip()
            if not q:
                raise ValueError("empty prompt")
            msgs: List[Dict[str, str]] = []
            if sysprompt.get().strip():
                msgs.append({"role": "system", "content": sysprompt.get().strip()})
            msgs += history[-12:]                # آخر 6 أدوار كسياق
            msgs.append({"role": "user", "content": q})
            d = http_post_json(
                base.rstrip("/") + "/chat/completions",
                {"model": model.get().strip(), "messages": msgs, "temperature": 0.7},
                {"Authorization": f"Bearer {key}"})
            if "error" in d:
                raise RuntimeError(d["error"].get("message", "api error"))
            ans = d["choices"][0]["message"]["content"]
            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": ans})
            prompt.delete("1.0", "end")          # جاهز للسؤال التالي
            return ans + f"\n\n{'─' * 30}\n[{len(history) // 2} turn(s) in memory]"

        def new_chat():
            history.clear()
            self.set_box(out, "✓ " + self.t("New chat"))

        self.buttons(c, [("🤖 " + self.t("Run"),
                          lambda: self.run_async(ask, lambda r_: self.set_box(out, r_), st)),
                         ("🧹 " + self.t("New chat"), new_chat),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    # ═════════════════════════════════════════════════════
    # 【17.5】 Local LLM — تشغيل نماذج GGUF محليًا (llama.cpp) — v4.1
    # ═════════════════════════════════════════════════════
    def page_llm(self, p):
        llama_mod = _get_llama_cpp()          # استيراد كسول — اختياري تمامًا
        side = "right" if self.rtl else "left"
        anch = "e" if self.rtl else "w"

        def _i(s, d: int) -> int:
            try:
                return int(float(str(s).strip()))
            except Exception:
                return d

        def _f(s, d: float) -> float:
            try:
                return float(str(s).strip())
            except Exception:
                return d

        # ── بطاقة 1: اختيار الملف + معلومات الموديل (تعمل بلا llama-cpp-python)
        c1 = self.card(p, "🦙 " + self.t("Local LLM"))
        ctk.CTkLabel(c1, text=self.t("Run GGUF models locally — 100% offline"),
                     text_color=CC("muted")).pack(anchor=anch, padx=14)
        # ── v4.3: اختيار المحرّك الخلفي — داخلي أو خادم llama.cpp (بلا مترجم)
        BK_LOCAL = self.t("In-process (llama-cpp-python)")
        BK_SERVER = self.t("llama.cpp Server (running)")
        BK_AUTO = self.t("llama.cpp Server (auto-start)")
        BK_INV = {BK_LOCAL: "local", BK_SERVER: "server", BK_AUTO: "auto"}
        _pr_saved = self.settings.get("llm_params") or {}
        bk_row = self.row(c1)
        ctk.CTkLabel(bk_row, text=self.t("Backend"), width=150,
                     anchor=anch).pack(side=side)
        bk = ctk.CTkOptionMenu(bk_row, width=340,
                               values=[BK_LOCAL, BK_SERVER, BK_AUTO])
        bk.set({"local": BK_LOCAL, "server": BK_SERVER,
                "auto": BK_AUTO}.get(_pr_saved.get("backend", "local"),
                                     BK_LOCAL))
        bk.pack(side=side, padx=8)

        if llama_mod is None:
            # ✦ v4.3: لوحة مساعدة التثبيت — تشرح خيارات الحل بالتفصيل (قابلة للنسخ)
            hb = ctk.CTkTextbox(c1, height=180,
                                font=ctk.CTkFont(family="Courier", size=12))
            hb.pack(fill="x", padx=12, pady=(6, 2))
            hb.insert("1.0", _LLM_INSTALL_HELP)
            hb.configure(state="disabled")
            hw = self.row(c1)
            ctk.CTkLabel(hw, text="⚠ llama-cpp-python "
                         + self.t("Not installed"),
                         text_color=CC("warn")).pack(side=side, padx=8)
            ctk.CTkButton(hw, width=160, text="📋 " + self.t("Install help"),
                          command=lambda: (self.copy_text(_LLM_INSTALL_HELP),
                                           self.toast(self.t("Install help copied"),
                                                      "ok"))).pack(side=side,
                                                                   padx=4)

        ur = self.row(c1)
        ctk.CTkLabel(ur, text=self.t("Server URL"), width=150,
                     anchor=anch).pack(side=side)
        eurl = ctk.CTkEntry(ur, width=340,
                            placeholder_text="http://127.0.0.1:8080")
        eurl.insert(0, str(_pr_saved.get("url", "") or ""))
        eurl.pack(side=side, padx=8)

        xr = self.row(c1)
        ctk.CTkLabel(xr, text=self.t("llama-server executable"), width=150,
                     anchor=anch).pack(side=side)
        eexe = ctk.CTkEntry(xr, width=260,
                            placeholder_text="llama-server.exe")
        eexe.insert(0, str(_pr_saved.get("exe", "") or ""))
        eexe.pack(side=side, padx=(8, 0))

        def browse_exe():
            fp = filedialog.askopenfilename(
                title="llama-server",
                filetypes=[("llama-server", "llama-server*"),
                           ("Executable", "*.exe"), ("All files", "*.*")])
            if fp:
                eexe.delete(0, "end")
                eexe.insert(0, fp)

        ctk.CTkButton(xr, text="📁 " + self.t("Browse"), width=120,
                      command=browse_exe).pack(side=side, padx=4)

        # ✦ v4.4: خيار التنزيل التلقائي — llama-server من GitHub بضغطة واحدة
        bld_row = self.row(c1)
        ctk.CTkLabel(bld_row, text=self.t("Build"), width=150,
                     anchor=anch).pack(side=side)
        BLD_INV = {self.t("Auto (recommended)"): "auto",
                   self.t("CPU build"): "cpu",
                   self.t("CUDA build (NVIDIA)"): "cuda",
                   self.t("Vulkan build"): "vulkan"}
        obld = ctk.CTkOptionMenu(bld_row, width=180,
                                 values=list(BLD_INV.keys()))
        obld.set(self.t("Auto (recommended)"))
        obld.pack(side=side, padx=8)
        b_srv = ctk.CTkButton(bld_row, width=180,
                              text="⬇ " + self.t("Download llama-server"))
        b_srv.pack(side=side, padx=4)

        dl_state: Dict[str, Any] = {"busy": False, "stop": None}
        dstat = self.statuslabel(c1)            # تقدّم التنزيل المشترك + الإلغاء

        def _dl_progress(done_b: float, total_b: float, speed: float):
            def upd():
                try:
                    if total_b > 0:
                        txt = (f"⬇ {done_b / total_b * 100:5.1f}% · "
                               f"{human_size(done_b)} / {human_size(total_b)}"
                               f" · {human_size(speed)}/s")
                    else:
                        txt = f"⬇ {human_size(done_b)} · {human_size(speed)}/s"
                    dstat.configure(text=txt, text_color=CC("primary"))
                except Exception:
                    pass
            self._ui(upd)

        def _dl_phase(name: str):
            msgs = {"info": self.t("Fetching release info…"),
                    "download": self.t("Starting download…"),
                    "extract": self.t("Extracting…")}
            msg = msgs.get(name, name)
            self._ui(lambda m=msg: dstat.configure(
                text="⏳ " + m, text_color=CC("warn")))

        def work_srv(build: str, stop: threading.Event):
            try:
                res = _llm_fetch_release(build, _dl_progress, stop, _dl_phase)
                return ("ok", res) if res else ("cancel",)
            except Exception as e:
                return ("error", f"{type(e).__name__}: {e}")

        def done_srv(res):
            b_srv.configure(text="⬇ " + self.t("Download llama-server"),
                            state="normal")
            for _b in (b_mdl, b_mdl_lg, b_mdl_unc):
                _b.configure(state="normal")
            dl_state["busy"] = False
            dl_state["stop"] = None
            if res[0] == "ok":
                exe, ver = res[1]
                eexe.delete(0, "end")
                eexe.insert(0, exe)
                _save_llm_params(BK_INV.get(bk.get(), "local"), exe=exe)
                dstat.configure(
                    text="✓ " + self.t("Download complete") + f" ({ver}) — "
                         + self.t("Saved to") + f": {exe}", text_color=CC("ok"))
                self.toast("✓ llama-server " + ver, "ok")
            elif res[0] == "cancel":
                dstat.configure(text="⏹ " + self.t("Canceled"),
                                text_color=CC("muted"))
            else:
                dstat.configure(
                    text="✗ " + self.t("Download failed") + f": {res[1]}",
                    text_color=CC("err"))

        def start_srv_dl():
            if dl_state["busy"]:                # الضغط أثناء التنزيل = إلغاء
                if dl_state["stop"] is not None:
                    dl_state["stop"].set()
                return
            build = BLD_INV.get(obld.get(), "auto")
            stop = threading.Event()
            dl_state["busy"] = True
            dl_state["stop"] = stop
            b_srv.configure(text="⏹ " + self.t("Cancel"))
            for _b in (b_mdl, b_mdl_lg, b_mdl_unc):
                _b.configure(state="disabled")
            dstat.configure(text="⏳ " + self.t("Starting download…"),
                            text_color=CC("warn"))
            self.run_async(lambda: work_srv(build, stop), done_srv, None, None)

        b_srv.configure(command=start_srv_dl)

        ptr = self.row(c1)
        ctk.CTkLabel(ptr, text=self.t("Port"), width=150,
                     anchor=anch).pack(side=side)
        eport = ctk.CTkEntry(ptr, width=120)
        eport.insert(0, str(_pr_saved.get("port", "8765")))
        eport.pack(side=side, padx=8)

        r1 = self.row(c1)
        ep = ctk.CTkEntry(r1, width=470, placeholder_text=self.t("GGUF model file"))
        ep.pack(side=side, padx=(8, 0))

        # ✦ v4.4/v4.5: تنزيل موديل GGUF جاهز من Hugging Face — قائمتان صغيرة/كبيرة
        MODEL_LABELS = {f"{m['name']} · {m['size']}": m for m in _LLM_MODELS}
        SMALL_LABELS = [f"{m['name']} · {m['size']}" for m in _LLM_MODELS
                        if m.get("tier") == "small"]
        LARGE_LABELS = [f"{m['name']} · {m['size']}" for m in _LLM_MODELS
                        if m.get("tier") == "large"]
        mdr = self.row(c1)
        ctk.CTkLabel(mdr, text=self.t("Download model"), width=150,
                     anchor=anch).pack(side=side)
        omdl = ctk.CTkOptionMenu(mdr, width=330,
                                 values=SMALL_LABELS or ["-"])
        omdl.set((SMALL_LABELS or ["-"])[0])
        omdl.pack(side=side, padx=8)
        b_mdl = ctk.CTkButton(mdr, width=110, text="⬇ " + self.t("Model"))
        b_mdl.pack(side=side, padx=4)

        # ✦ v4.5: الموديلات الكبيرة (7B حتى 70B) في قائمة مستقلة
        mlr = self.row(c1)
        ctk.CTkLabel(mlr, text=self.t("Download large model"), width=150,
                     anchor=anch).pack(side=side)
        omdl_lg = ctk.CTkOptionMenu(mlr, width=330,
                                    values=LARGE_LABELS or ["-"])
        omdl_lg.set((LARGE_LABELS or ["-"])[0])
        omdl_lg.pack(side=side, padx=8)
        b_mdl_lg = ctk.CTkButton(mlr, width=110, text="⬇ " + self.t("Model"))
        b_mdl_lg.pack(side=side, padx=4)

        # ✦ v4.7: الموديلات غير المحجوبة (Dolphin/Abliterated/Lexi/Stheno) — قائمة مستقلة
        UN_LABELS = [f"{m['name']} · {m['size']}" for m in _LLM_MODELS
                     if m.get("tier") == "unc"]
        unr = self.row(c1)
        ctk.CTkLabel(unr, text=self.t("Download uncensored model"), width=150,
                     anchor=anch).pack(side=side)
        omdl_un = ctk.CTkOptionMenu(unr, width=330,
                                    values=UN_LABELS or ["-"])
        omdl_un.set((UN_LABELS or ["-"])[0])
        omdl_un.pack(side=side, padx=8)
        b_mdl_unc = ctk.CTkButton(unr, width=110, text="⬇ " + self.t("Model"))
        b_mdl_unc.pack(side=side, padx=4)
        uncnote = self.statuslabel(c1)
        uncnote.configure(
            text="ℹ " + self.t(
                "Uncensored models are community fine-tunes (Dolphin · "
                "Abliterated · Lexi · Stheno) with refusal behavior removed "
                "— use responsibly and per your local laws."),
            text_color=CC("muted"), justify="left",
            anchor=anch, wraplength=560)
        uncnote.pack(anchor=anch, padx=14, pady=(2, 6), fill="x")

        def work_mdl(mdl: Dict[str, str], stop: threading.Event):
            try:
                dest = os.path.join(_llm_dl_dir("models"),
                                    os.path.basename(mdl["url"].split("?")[0]))
                fp = _llm_download(mdl["url"], dest, _dl_progress, stop)
                return ("ok", fp) if fp else ("cancel",)
            except Exception as e:
                return ("error", f"{type(e).__name__}: {e}")

        def done_mdl(res):
            for _b in (b_mdl, b_mdl_lg, b_mdl_unc):
                _b.configure(text="⬇ " + self.t("Model"), state="normal")
            b_srv.configure(state="normal")
            dl_state["busy"] = False
            dl_state["stop"] = None
            if res[0] == "ok":
                fp = res[1]
                ep.delete(0, "end")
                ep.insert(0, fp)
                _remember_model(fp)
                refresh_info(fp)
                _save_llm_params(BK_INV.get(bk.get(), "local"), path=fp)
                dstat.configure(
                    text="✓ " + self.t("Model downloaded") + " — "
                         + self.t("Saved to") + f": {fp}", text_color=CC("ok"))
                self.toast("✓ " + os.path.basename(fp), "ok")
            elif res[0] == "cancel":
                dstat.configure(text="⏹ " + self.t("Canceled"),
                                text_color=CC("muted"))
            else:
                dstat.configure(
                    text="✗ " + self.t("Download failed") + f": {res[1]}",
                    text_color=CC("err"))

        def start_mdl_dl(menu, btn):
            if dl_state["busy"]:                # الضغط أثناء التنزيل = إلغاء
                if dl_state["stop"] is not None:
                    dl_state["stop"].set()
                return
            mdl = MODEL_LABELS.get(menu.get())
            if not mdl:
                return
            stop = threading.Event()
            dl_state["busy"] = True
            dl_state["stop"] = stop
            for _b in (b_mdl, b_mdl_lg, b_mdl_unc):
                _b.configure(state="disabled")
            btn.configure(text="⏹ " + self.t("Cancel"))
            b_srv.configure(state="disabled")
            dstat.configure(text="⏳ " + self.t("Starting download…"),
                            text_color=CC("warn"))
            self.run_async(lambda: work_mdl(mdl, stop), done_mdl, None, None)

        b_mdl.configure(command=lambda: start_mdl_dl(omdl, b_mdl))
        b_mdl_lg.configure(command=lambda: start_mdl_dl(omdl_lg, b_mdl_lg))
        b_mdl_unc.configure(command=lambda: start_mdl_dl(omdl_un, b_mdl_unc))

        # ✦ v4.6: حالة وضع الرام المنخفضة — تُقرأ في refresh_info قبل بناء بطاقة الضبط
        lr_state = {"lowram": str(_pr_saved.get("lowram", "0")) in
                    ("1", "true", "True", "1.0"),
                    "kv": str(_pr_saved.get("kv", "Auto") or "Auto")}
        info = ctk.CTkLabel(c1, text="", justify="left", anchor=anch,
                            font=ctk.CTkFont(family="Courier", size=12))
        info.pack(anchor=anch, padx=14, pady=(6, 10), fill="x")
        ramhint = ctk.CTkLabel(c1, text="", justify="left", anchor=anch,
                               text_color=CC("warn"))
        ramhint.pack(anchor=anch, padx=14, fill="x")

        def refresh_info(fp: str):
            """معلومات من رأس GGUF — بلا تحميل للموديل وبلا اعتمادات.

            ✦ v4.6: يضيف كشف MoE (فحص الموترات المخزَّن مؤقتًا) وسطر تقدير
            الرام حسب وضع Low RAM وسطر اقتراح تلقائي للموديلات الضخمة.
            """
            try:
                if not fp or not os.path.isfile(fp):
                    info.configure(text="✗ " + self.t("No model selected"))
                    ramhint.configure(text="")
                    return
                sz = os.path.getsize(fp)
                md = gguf_metadata(fp)
                md.update(_gguf_tensor_scan(fp))
                kv_eff = {"Auto": ("q8_0" if lr_state["lowram"] else "f16")}.get(
                    lr_state["kv"], lr_state["kv"])
                est = _llm_estimate_ram(md, sz, lowram=lr_state["lowram"],
                                        kv_q=kv_eff)
                lines = [f"• {os.path.basename(fp)}  —  {human_size(sz)}"]
                if md.get("name"):
                    nm = md["name"] + (f"  ({md['size_label']})" if md.get("size_label") else "")
                    lines.append("• " + self.t("Model") + ": " + nm)
                if md.get("arch"):
                    a = md["arch"]
                    if md.get("layers"):
                        a += f" · {md['layers']} " + self.t("Layers")
                    if md.get("embed"):
                        a += f" · d={md['embed']}"
                    lines.append("• " + self.t("Architecture") + ": " + a)
                if md.get("quant"):
                    lines.append("• " + self.t("Quantization") + ": " + md["quant"])
                if md.get("ctx"):
                    lines.append("• " + self.t("Context length") + f": {md['ctx']:,}")
                if md.get("vocab"):
                    lines.append("• " + self.t("Vocabulary") + f": {md['vocab']:,}")
                if est["moe"]:
                    lines.append("• MoE: " + f"{est['experts']} "
                                 + self.t("experts") + f" · "
                                 + (str(est['experts_used']) if est['experts_used']
                                    else "?") + " " + self.t("active/token"))
                if est["moe"] and lr_state["lowram"]:
                    lines.append("• " + self.t("Estimated RAM")
                                 + f": ≈ {human_size(est['resident'])} (+ctx)")
                    lines.append("  ↳ " + self.t(
                        "Low-RAM: experts stream from SSD · native accuracy")
                        + f" · ≈{est['tok_lo']}-{est['tok_hi']} tok/s")
                elif est["moe"]:
                    lines.append("• " + self.t("Estimated RAM")
                                 + f": ≈ {human_size(est['full'])} (+ctx)")
                    lines.append(f"  ↳ 🪶 " + self.t("Low RAM (<8 GB)")
                                 + f" → ≈ {human_size(est['resident'])}")
                elif lr_state["lowram"]:
                    lines.append("• " + self.t("Estimated RAM")
                                 + f": ≈ {human_size(est['full'])} (+ctx)")
                    lines.append("  ↳ " + self.t(
                        "Low-RAM: model streams from SSD · low RAM, slower")
                        + f" · ≈{est['tok_lo']}-{est['tok_hi']} tok/s")
                else:
                    lines.append("• " + self.t("Estimated RAM")
                                 + f": ≈ {human_size(est['full'])} (+ctx)")
                info.configure(text="\n".join(lines))
                # 💡 اقتراح تلقائي للموديلات الضخمة/MoE
                if (est["moe"] or sz > 6 * (1 << 30)) and not lr_state["lowram"]:
                    ramhint.configure(text="💡 " + self.t(
                        "Suggested: enable Low RAM for this model"))
                else:
                    ramhint.configure(text="")
            except Exception as e:
                info.configure(text=f"✗ {e}")

        def browse():
            fp = filedialog.askopenfilename(
                title=self.t("GGUF model file"),
                filetypes=[("GGUF model", "*.gguf"), ("All files", "*.*")])
            if fp:
                ep.delete(0, "end")
                ep.insert(0, fp)
                refresh_info(fp)

        ctk.CTkButton(r1, text="📁 " + self.t("Browse"), width=120,
                      command=browse).pack(side=side, padx=4)

        # أحدث الموديلات (من الإعدادات، مع حذف المسارات غير الموجودة)
        rec = [x for x in self.settings.get("llm_recent", []) if os.path.isfile(x)]
        rec_menu = None
        if rec:
            rr = self.row(c1)
            ctk.CTkLabel(rr, text=self.t("Recent models"), width=150,
                         anchor=anch).pack(side=side)
            rec_menu = ctk.CTkOptionMenu(rr, width=400,
                                         values=[os.path.basename(x) for x in rec])

            def pick_recent(name: str):
                for x in rec:
                    if os.path.basename(x) == name:
                        ep.delete(0, "end")
                        ep.insert(0, x)
                        refresh_info(x)
                        break
            rec_menu.configure(command=pick_recent)
            rec_menu.pack(side=side, padx=8)

        lastp = (self.settings.get("llm_params") or {}).get("path", "")
        if lastp and os.path.isfile(lastp):
            ep.insert(0, lastp)
            refresh_info(lastp)

        # ── بطاقة 2: الضبط + التحميل/الإخراج
        c2 = self.card(p, "⚙️ " + self.t("Configuration"))
        pr = {**{"n_ctx": "4096", "gpu": "0", "threads": str(os.cpu_count() or 4),
                 "temp": "0.7", "topp": "0.9", "maxtok": "512", "rp": "1.1",
                 "sys": ""},
              **(self.settings.get("llm_params") or {})}

        gf = ctk.CTkFrame(c2, fg_color="transparent")
        gf.pack(fill="x", padx=8, pady=(4, 2))

        def gmenu(row, col, label, values, val, w=120):
            ctk.CTkLabel(gf, text=label).grid(row=row, column=col * 2,
                                              sticky="w", padx=(12, 4), pady=3)
            m = ctk.CTkOptionMenu(gf, values=values, width=w)
            m.set(str(val))
            m.grid(row=row, column=col * 2 + 1, sticky="w", padx=4, pady=3)
            return m

        def gfield(row, col, label, val, w=110):
            ctk.CTkLabel(gf, text=label).grid(row=row, column=col * 2,
                                              sticky="w", padx=(12, 4), pady=3)
            e = ctk.CTkEntry(gf, width=w)
            e.insert(0, str(val))
            e.grid(row=row, column=col * 2 + 1, sticky="w", padx=4, pady=3)
            return e

        octx = gmenu(0, 0, self.t("Context size"),
                     ["512", "1024", "2048", "4096", "8192", "16384", "32768"],
                     pr.get("n_ctx", "4096"))
        ogpu = gmenu(0, 1, self.t("GPU layers (0=CPU, -1=all)"),
                     ["0", "8", "16", "24", "32", "48", "-1"],
                     pr.get("gpu", "0"), 90)
        fthr = gfield(0, 2, self.t("Threads"),
                      pr.get("threads", str(os.cpu_count() or 4)), 70)
        ftmp = gfield(1, 0, self.t("Temperature"), pr.get("temp", "0.7"))
        ftop = gfield(1, 1, self.t("Top P"), pr.get("topp", "0.9"))
        ftok = gfield(1, 2, self.t("Max tokens"), pr.get("maxtok", "512"))
        frp = gfield(2, 0, self.t("Repeat penalty"), pr.get("rp", "1.1"))
        # ✦ v4.6: تكميم ذاكرة KV + وضع الرام المنخفضة — صف ثالث في الشبكة
        okv = gmenu(2, 1, self.t("KV cache"),
                    ["Auto", "f16", "q8_0", "q4_0"],
                    pr.get("kv", "Auto"), 90)
        sw_low = ctk.CTkSwitch(gf, text="🪶 " + self.t("Low RAM (<8 GB)"),
                               onvalue="1", offvalue="0")
        if lr_state["lowram"]:
            sw_low.select()
        sw_low.grid(row=2, column=4, sticky="w", padx=(12, 4), pady=3)

        # ✦ v4.6: موديل مسودة — فك تشفير تخميني: تسريع بلا أي تغيير في الدقة
        dfr = self.row(c2)
        sw_draft = ctk.CTkSwitch(dfr, text="⚡ " + self.t("Draft model"),
                                 onvalue="1", offvalue="0")
        if str(pr.get("draft_on", "0")) in ("1", "true", "True", "1.0"):
            sw_draft.select()
        sw_draft.pack(side=side, padx=8)
        edraft = ctk.CTkEntry(dfr, width=210,
                              placeholder_text=self.t("Draft model (.gguf)"))
        edraft.insert(0, str(pr.get("draft", "") or ""))
        edraft.pack(side=side, padx=4)

        def browse_draft():
            fp2 = filedialog.askopenfilename(
                title="Draft GGUF",
                filetypes=[("GGUF model", "*.gguf"), ("All files", "*.*")])
            if fp2:
                edraft.delete(0, "end")
                edraft.insert(0, fp2)

        ctk.CTkButton(dfr, text="📁 " + self.t("Browse"), width=90,
                      command=browse_draft).pack(side=side, padx=4)
        ctk.CTkLabel(c2, text="⚡ " + self.t(
                         "Speed: verifies draft batches — same accuracy"),
                     text_color=CC("muted"), anchor=anch).pack(fill="x",
                                                               padx=14)

        ctk.CTkLabel(c2, text=self.t("System prompt"),
                     anchor=anch).pack(fill="x", padx=14, pady=(6, 0))
        fsys = self.textbox(c2, 56, pr.get("sys", ""))
        st2 = self.statuslabel(c2)

        def _save_llm_params(bk: str, **extra):
            """حفظ ضبط LLM — من الخيط الرئيسي فقط (يقرأ الواجهة)."""
            pr2 = {**(self.settings.get("llm_params") or {})}
            pr2.update({"n_ctx": octx.get(), "gpu": ogpu.get(),
                        "threads": fthr.get(), "temp": ftmp.get(),
                        "topp": ftop.get(), "maxtok": ftok.get(),
                        "rp": frp.get(), "sys": fsys.get("1.0", "end").strip(),
                        "backend": bk,
                        "think": str(sw_think.get()),
                        "lowram": str(sw_low.get()),
                        "kv": okv.get(),
                        "draft_on": str(sw_draft.get()),
                        "draft": edraft.get().strip()})
            pr2.update(extra)
            self.settings["llm_params"] = pr2
            self.save_settings()

        def _remember_model(fp: str):
            rec2 = [x for x in self.settings.get("llm_recent", []) if x != fp]
            rec2.insert(0, fp)
            self.settings["llm_recent"] = rec2[:6]
            self.save_settings()
            try:
                if rec_menu is not None and rec_menu.winfo_exists():
                    rec_menu.configure(
                        values=[os.path.basename(x) for x in rec2[:6]])
            except Exception:
                pass

        def _lr_changed(*_a):
            """✦ v4.6: تغيّر Low RAM/KV — حفظ + تحديث سطر التقدير فورًا."""
            lr_state["lowram"] = str(sw_low.get()) == "1"
            lr_state["kv"] = okv.get()
            _save_llm_params(BK_INV.get(bk.get(), "local"))
            fp2 = ep.get().strip()
            if fp2 and os.path.isfile(fp2):
                refresh_info(fp2)

        sw_low.configure(command=_lr_changed)
        okv.configure(command=_lr_changed)
        sw_draft.configure(command=lambda: _save_llm_params(
            BK_INV.get(bk.get(), "local")))

        def _wait_health(u: str):
            ok, why = _llm_server_ready(u, timeout=3.0)
            if not ok:
                raise RuntimeError(f"{self.t('Server not responding')} ({why})")
            return u

        def _auto_start(xe: str, md: str, ctx: int, gpu: int, thr: int,
                        port: int, extra: Optional[List[str]] = None):
            old = self._llm.get("proc")                 # إيقاف خادم سابق إن وُجد
            if old is not None and old.poll() is None:
                try:
                    old.terminate()
                except Exception:
                    pass
            try:
                return _llm_start_server(xe, md, ctx, gpu, thr, port,
                                         extra=extra)
            except Exception as e:
                raise RuntimeError(
                    self.t("Failed to start llama-server") + f": {e}") from e

        def on_server_ready(u: str):
            self._llm["backend"] = "server"
            self._llm["url"] = u
            self._llm["model"] = None
            _save_llm_params("server", url=u)
            fp = ep.get().strip()
            if fp and os.path.isfile(fp):
                _remember_model(fp)
            try:
                st2.configure(text="✓ " + self.t("Server ready") + f": {u}",
                              text_color=CC("ok"))
            except Exception:
                pass

        def on_auto_ready(val):
            proc, url = val
            self._llm["backend"] = "server"
            self._llm["url"] = url
            self._llm["proc"] = proc
            self._llm["model"] = None
            fp = ep.get().strip()
            _save_llm_params("server", url=url, exe=eexe.get().strip(),
                                  port=eport.get().strip(), path=fp)
            if fp and os.path.isfile(fp):
                _remember_model(fp)
                refresh_info(fp)
            try:
                st2.configure(text="✓ " + self.t("Server ready") + f": {url}",
                              text_color=CC("ok"))
            except Exception:
                pass

        def start_load():
            # ✦ v4.1/v4.3: كل قراءات الواجهة هنا في الخيط الرئيسي — الخيط العامل بلا Tcl
            if self._llm["busy"]:
                return
            bk_key = BK_INV.get(bk.get(), "local")
            if bk_key == "server":                      # خادم يعمل أصلًا
                u = eurl.get().strip() or "http://127.0.0.1:8080"
                self.run_async(lambda: _wait_health(u), on_server_ready, st2,
                               self.t("Connecting…"))
                return
            fp = ep.get().strip()
            if not fp or not os.path.isfile(fp):
                try:
                    st2.configure(text="✗ " + self.t("No model selected"),
                                  text_color=CC("err"))
                except Exception:
                    pass
                return
            ctx = max(256, _i(octx.get(), 4096))
            gpu = _i(ogpu.get(), 0)
            thr = max(1, _i(fthr.get(), os.cpu_count() or 4))
            if bk_key == "auto":                        # تشغيل llama-server تلقائيًا
                xe = eexe.get().strip()
                if not xe or not os.path.isfile(xe):
                    try:
                        st2.configure(text="✗ " + self.t("llama-server executable")
                                      + " — ⬇ " + self.t("Download llama-server"),
                                      text_color=CC("err"))
                    except Exception:
                        pass
                    return
                port = max(1024, _i(eport.get(), 8765))
                # ✦ v4.6: تكوين وسائط الرام المنخفضة/المسودة في الخيط الرئيسي
                low = str(sw_low.get()) == "1"
                kv_sel = okv.get()
                kv_eff = {"Auto": ("q8_0" if low else "f16")}.get(kv_sel,
                                                                  kv_sel)
                moef = False
                try:
                    moef = (_gguf_tensor_scan(fp).get("experts") or 0) > 0
                except Exception:
                    pass
                draft = ""
                if str(sw_draft.get()) == "1":
                    dd = edraft.get().strip()
                    if dd and os.path.isfile(dd):
                        draft = dd
                    else:
                        self.toast("⚡ " + self.t(
                            "Draft model not found — ignored"), "warn")
                extra = _llm_lowram_flags(low, kv_eff, moef, draft)
                self.run_async(
                    lambda: _auto_start(xe, fp, ctx, gpu, thr, port, extra),
                    on_auto_ready, st2, self.t("Connecting…"))
                return
            if llama_mod is None:                       # داخلي — يحتاج llama-cpp-python
                try:
                    st2.configure(text="✗ llama-cpp-python "
                                  + self.t("Not installed"), text_color=CC("err"))
                except Exception:
                    pass
                return
            # ✦ v4.6: المسار الداخلي — mmap/دفعات صغيرة/تكميم KV بلا خادم
            low = str(sw_low.get()) == "1"
            kv_sel = okv.get()
            kv_eff = {"Auto": ("q8_0" if low else "f16")}.get(kv_sel, kv_sel)
            self.run_async(lambda: _load_worker(fp, ctx, gpu, thr, low, kv_eff),
                           on_loaded, st2,
                           self.t("First load can take a minute…"))

        def _load_worker(fp, ctx, gpu, thr, low=False, kvq="f16"):
            # بلا أي استدعاءات Tk هنا — القيم كلها وسيطات بايثون سادة
            if self._llm["path"] == fp and self._llm["model"] is not None:
                return fp                                   # محمّل مسبقًا
            if self._llm["model"] is not None:              # تحرير القديم أولًا
                self._llm["model"] = None
                gc.collect()
            # ✦ v4.6: وضع الرام المنخفضة للمسار الداخلي — mmap بلا تثبيت
            # صفحات + دفعات صغيرة + تكميم KV. (exps=CPU والمسودة في محرّك
            # الخادم فقط.) الإصدارات الأقدم تُسقط الوسائط تدريجيًا بلا انهيار.
            kw: Dict[str, Any] = {}
            if low:
                kw.update(use_mlock=False, use_mmap=True,
                          n_batch=128, n_ubatch=128)
                if kvq == "q8_0":
                    kw.update(type_k=8, type_v=8, flash_attn=True)
                elif kvq == "q4_0":
                    kw.update(type_k=2, type_v=2, flash_attn=True)
            if kw:
                m = None
                drops = [(), ("flash_attn",),
                         ("type_k", "type_v", "flash_attn"),
                         ("n_ubatch", "type_k", "type_v", "flash_attn")]
                for drop in drops:
                    try:
                        m = llama_mod.Llama(
                            model_path=fp, n_ctx=ctx, n_gpu_layers=gpu,
                            n_threads=thr, verbose=False,
                            **{k: v for k, v in kw.items() if k not in drop})
                        break
                    except TypeError:
                        m = None
                if m is None:
                    raise RuntimeError(
                        "llama-cpp-python rejected Low-RAM load args")
            else:
                m = llama_mod.Llama(
                    model_path=fp, n_ctx=ctx, n_gpu_layers=gpu,
                    n_threads=thr, verbose=False)
            self._llm["model"] = m
            self._llm["path"] = fp
            return fp

        def on_loaded(fp):
            if not fp:
                return
            self._llm["backend"] = "local"
            self._llm["url"] = ""
            _save_llm_params("local", path=fp)
            _remember_model(fp)
            note = ""
            try:
                # ✦ v4.6: llama-cpp-python لا يدعم exps=CPU — خادم أفضل لـ MoE
                if str(sw_low.get()) == "1" and \
                        (_gguf_tensor_scan(fp).get("experts") or 0) > 0:
                    note = "  ·  ⓘ " + self.t(
                        "Server backend recommended for MoE + Low RAM")
            except Exception:
                pass
            try:
                st2.configure(text="✓ " + self.t("Model ready")
                              + f": {os.path.basename(fp)}" + note,
                              text_color=CC("ok"))
            except Exception:
                pass
            refresh_info(fp)

        def do_unload():
            had = (self._llm["model"] is not None
                   or self._llm.get("backend") == "server")
            self._llm["model"] = None
            self._llm["path"] = ""
            self._llm["url"] = ""
            self._llm["backend"] = "local"
            pr = self._llm.get("proc")     # ✦ v4.3: إيقاف الخادم المُشغَّل تلقائيًا
            self._llm["proc"] = None
            if pr is not None and pr.poll() is None:
                try:
                    pr.terminate()
                except Exception:
                    pass
            gc.collect()
            try:
                st2.configure(text="⏏ " + (self.t("Model unloaded") if had
                                           else self.t("No model selected")),
                              text_color=CC("muted"))
            except Exception:
                pass

        self.buttons(c2, [
            ("⬇️ " + self.t("Load model"), start_load),
            ("⏏️ " + self.t("Unload model"), do_unload)])

        # ── بطاقة 3: المحادثة (بث حي عبر _ui الآمنة للخيوط)
        c3 = self.card(p, "💬 " + self.t("Chat"))
        # ✦ v4.5: مفتاح التفكير العميق — الإيقاف يخفي التفكير ويوقف توليده على الخادم
        thkr = self.row(c3)
        sw_think = ctk.CTkSwitch(thkr, text="🧠 " + self.t("Deep thinking"),
                                 onvalue="1", offvalue="0")
        if str(_pr_saved.get("think", "1")) in ("1", "true", "True", "1.0"):
            sw_think.select()
        sw_think.pack(side=side, padx=8)
        sw_think.configure(command=lambda: _save_llm_params(
            BK_INV.get(bk.get(), "local"), think=str(sw_think.get())))
        trans = ctk.CTkTextbox(c3, height=300,
                               font=ctk.CTkFont(family="Courier", size=13))
        trans.pack(fill="both", expand=True, padx=12, pady=(8, 6))
        trans.configure(state="disabled")
        ctk.CTkLabel(c3, text=self.t("Your message"),
                     anchor=anch).pack(fill="x", padx=14, pady=(0, 0))
        inp = ctk.CTkTextbox(c3, height=64)
        inp.pack(fill="x", padx=12, pady=(2, 4))
        st3 = self.statuslabel(c3)

        hist: List[Tuple[str, str]] = self._llm["hist"]

        def _append(txt: str):
            try:
                trans.configure(state="normal")
                trans.insert("end", txt)
                trans.see("end")
                trans.configure(state="disabled")
            except Exception:
                pass

        def transcript_text() -> str:
            out = []
            for role, content in hist:
                who = self.t("You") if role == "user" else self.t("Assistant")
                out.append(f"🧑 {who}:\n{content}" if role == "user"
                           else f"🦙 {who}:\n{content}")
            return "\n\n".join(out)

        if hist:                                            # إعادة عرض المحادثة بعد إعادة بناء الصفحة
            _append(transcript_text())

        def _start_turn(q: str):
            _append(f"\n\n🧑 {self.t('You')}:\n{q}\n\n🦙 {self.t('Assistant')}:\n")

        def _finish_turn(ntok: int, secs: float, stopped: bool,
                         nhidden: int = 0):
            tail = f"\n\n— {ntok} tok · {(ntok / secs) if secs else 0:.1f} tok/s"
            if nhidden:
                tail += " · 🙈 " + self.t("Thinking hidden") + f" ({nhidden})"
            if stopped:
                tail += " · ⏹ " + self.t("Stopped.")
            _append(tail)

        def work_send(q: str, sp: str, ptemp: str, ptop: str,
                      pmaxtok: str, prp: str, pthink: bool = True):
            """يعمل في خيط عامل — كل الوسائط قيم بايثون سادة، صفر استدعاءات Tcl."""
            backend = self._llm.get("backend", "local")
            url = self._llm.get("url", "")
            m = self._llm["model"]
            if backend == "server":
                if not url:
                    raise ValueError(self.t("Server not responding"))
            elif m is None:
                raise ValueError(self.t("No model selected"))
            stop_ev = threading.Event()
            self._llm["stop"] = stop_ev
            self._llm["busy"] = True
            try:
                msgs: List[Dict[str, str]] = []
                if sp:
                    msgs.append({"role": "system", "content": sp})
                msgs += [{"role": r, "content": c} for r, c in hist[-12:]]
                msgs.append({"role": "user", "content": q})
                self._ui(_start_turn, q)
                t0 = time.time()
                ntok = 0
                pieces: List[str] = []      # النص المعروض
                pending: List[str] = []     # دفعة البث للواجهة
                answer: List[str] = []      # الجواب الصافي (بلا تفكير) للتاريخ
                shown_reason = False
                if backend == "server":
                    # ✦ v4.3: بث من خادم llama.cpp عبر HTTP — بلا llama-cpp-python
                    stream = _llm_http_stream(
                        url, msgs,
                        max_tokens=max(16, _i(pmaxtok, 512)),
                        temperature=max(0.0, min(2.0, _f(ptemp, 0.7))),
                        top_p=max(0.0, min(1.0, _f(ptop, 0.9))),
                        repeat_penalty=max(1.0, _f(prp, 1.1)),
                        disable_thinking=not pthink,     # ✦ v4.5: لا تولّد التفكير أصلًا
                        stop_ev=stop_ev)
                else:
                    stream = m.create_chat_completion(
                        messages=msgs,
                        max_tokens=max(16, _i(pmaxtok, 512)),
                        temperature=max(0.0, min(2.0, _f(ptemp, 0.7))),
                        top_p=max(0.0, min(1.0, _f(ptop, 0.9))),
                        repeat_penalty=max(1.0, _f(prp, 1.1)),
                        stream=True)
                # ✦ v4.5: إيقاف التفكير العميق = مرشّح بثّي + تجاهل reasoning_content
                tf = None if pthink else _ThinkFilter()
                for ch in stream:
                    if stop_ev.is_set():
                        break
                    try:
                        delta = ch["choices"][0].get("delta") or {}
                        rc = delta.get("reasoning_content") or ""
                        piece = delta.get("content") or ""
                    except Exception:
                        rc, piece = "", ""
                    if not (piece or rc):
                        continue
                    ntok += 1                           # كل الرموز المولّدة (حتى المحجوبة)
                    if pthink:                          # عرض التفكير مع تمييز بصري
                        if rc:
                            if not shown_reason:
                                pieces.append("🧠 ")
                                pending.append("🧠 ")
                                shown_reason = True
                            vis = rc
                        else:
                            if shown_reason:
                                pieces.append("\n\n")
                                pending.append("\n\n")
                                shown_reason = False
                            vis = piece
                            answer.append(piece)        # الجواب فقط يدخل التاريخ
                    else:
                        if rc:                          # تفكير منفصل — يُحجب فورًا
                            continue
                        vis = tf.feed(piece) if piece else ""
                        if vis:
                            answer.append(vis)
                    if vis:
                        pieces.append(vis)
                        pending.append(vis)
                        if len(pending) >= 3:           # بثّ مُخفَّف يحفظ سلاسة الواجهة
                            self._ui(_append, "".join(pending))
                            pending.clear()
                if tf is not None:                      # ما تبقّى من المرشّح
                    tail_txt = tf.flush()
                    if tail_txt:
                        pieces.append(tail_txt)
                        pending.append(tail_txt)
                        answer.append(tail_txt)
                if pending:
                    self._ui(_append, "".join(pending))
                secs = time.time() - t0
                hist.append(("user", q))
                hist.append(("assistant", "".join(answer)))
                self._ui(_finish_turn, ntok, secs, stop_ev.is_set(),
                         (tf.suppressed_chars if tf is not None else 0))
            finally:
                self._llm["busy"] = False
                self._llm["stop"] = None

        def do_send():
            # ✦ v4.1: القراءات كلها في الخيط الرئيسي ثم تُمرَّر كقيم للخيط العامل
            if self._llm["busy"]:
                return
            ready = (self._llm["model"] is not None
                     or (self._llm.get("backend") == "server"
                         and self._llm.get("url")))
            if not ready:
                try:
                    st3.configure(text="✗ " + self.t("No model selected")
                                  + " — " + self.t("Load model"),
                                  text_color=CC("err"))
                except Exception:
                    pass
                return
            q = inp.get("1.0", "end").strip()
            if not q:
                return
            sp = fsys.get("1.0", "end").strip()
            ptemp, ptop = ftmp.get(), ftop.get()
            pmaxtok, prp = ftok.get(), frp.get()
            pthink = str(sw_think.get()) == "1"          # ✦ v4.5: التفكير العميق؟
            inp.delete("1.0", "end")
            self.run_async(
                lambda: work_send(q, sp, ptemp, ptop, pmaxtok, prp, pthink),
                None, st3, self.t("Generating…"))

        def do_stop():
            if self._llm.get("stop") is not None:
                self._llm["stop"].set()

        def new_chat():
            hist.clear()
            try:
                trans.configure(state="normal")
                trans.delete("1.0", "end")
                trans.configure(state="disabled")
            except Exception:
                pass

        def save_chat():
            if not hist:
                try:
                    st3.configure(text="✗ " + self.t("Chat is empty"),
                                  text_color=CC("warn"))
                except Exception:
                    pass
                return
            fp = filedialog.asksaveasfilename(
                defaultextension=".md",
                filetypes=[("Markdown", "*.md"), ("Text", "*.txt")])
            if not fp:
                return
            with open(fp, "w", encoding="utf-8") as f:
                f.write(transcript_text() + "\n")
            self.toast(self.t("Chat saved to") + " " + fp, "ok")

        self.buttons(c3, [
            ("📨 " + self.t("Send"), do_send),
            ("⏹ " + self.t("Stop"), do_stop),
            ("🧹 " + self.t("New chat"), new_chat),
            ("💾 " + self.t("Save chat"), save_chat),
            ("📋 " + self.t("Copy"),
             lambda: self.copy_text(transcript_text()))])

    # ═════════════════════════════════════════════════════
    # 【17.5】 v4.5: الخزائن المشفّرة (Vault) — PBKDF2 + Fernet/HMAC-CTR
    # ═════════════════════════════════════════════════════
    def page_vault(self, p):
        side = "right" if self.rtl else "left"
        anch = "e" if self.rtl else "w"
        V = self._vault

        def _touch(*_):
            V["last_touch"] = time.time()

        def vault_path(name: str) -> str:
            return os.path.join(_vault_dir(), name + _VLT_EXT)

        def vault_names() -> List[str]:
            try:
                return sorted(fn[:-len(_VLT_EXT)]
                              for fn in os.listdir(_vault_dir())
                              if fn.endswith(_VLT_EXT))
            except Exception:
                return []

        def _copy_secret(txt: str):
            """نسخ سرّي مع مسح تلقائي من الحافظة بعد 30 ثانية."""
            _touch()
            self.copy_text(txt)
            self.toast("📋 " + self.t("copied (clears in 30s)"), "ok")

            def _wipe():
                try:
                    if self.clipboard_get() == txt:
                        self.clipboard_clear()
                except Exception:
                    pass
            self.after(30000, _wipe)

        def _save_vault():
            """إعادة تشفير وكتابة ملف الخزنة (كتابة ذرّية عبر .tmp)."""
            name = V.get("name")
            if not name:
                return
            payload = json.dumps({"entries": V["entries"]},
                                 ensure_ascii=False).encode("utf-8")
            blob = vault_encrypt(payload, V["pw"])
            fp = vault_path(name)
            tmp = fp + ".tmp"
            with open(tmp, "wb") as f:
                f.write(blob)
            os.replace(tmp, fp)

        # ── بطاقة 1: فتح / إنشاء / قفل ─────────────────────
        c1 = self.card(p, "🔐 " + self.t("Vault"))
        ctk.CTkLabel(c1,
                     text=self.t("Encrypted vault — master password + PBKDF2"),
                     text_color=CC("muted")).pack(anchor=anch, padx=14)

        vr = self.row(c1)
        ctk.CTkLabel(vr, text=self.t("Vault file"), width=140,
                     anchor=anch).pack(side=side)
        ovlt = ctk.CTkOptionMenu(vr, width=250,
                                 values=vault_names() or ["—"])
        if V.get("name") in vault_names():
            ovlt.set(V["name"])
        ovlt.pack(side=side, padx=8)
        b_del = ctk.CTkButton(vr, width=130, text="🗑 " + self.t("Delete vault"),
                              fg_color=C("err"), hover_color=C("err"))

        pr1 = self.row(c1)
        ctk.CTkLabel(pr1, text=self.t("Master password"), width=140,
                     anchor=anch).pack(side=side)
        epw = ctk.CTkEntry(pr1, width=250, show="•",
                           placeholder_text=self.t("Master password"))
        epw.pack(side=side, padx=8)
        epw.bind("<KeyRelease>", _touch)

        def _toggle_show():
            epw.configure(show="" if epw.cget("show") else "•")

        ctk.CTkButton(pr1, width=44, text="👁",
                      command=_toggle_show).pack(side=side, padx=2)
        b_open = ctk.CTkButton(pr1, width=120, text="🔓 " + self.t("Unlock"))
        b_open.pack(side=side, padx=2)

        nr = self.row(c1)
        ctk.CTkLabel(nr, text=self.t("Vault name"), width=140,
                     anchor=anch).pack(side=side)
        ename = ctk.CTkEntry(nr, width=250,
                             placeholder_text="my-secrets-2026")
        ename.pack(side=side, padx=8)
        ename.bind("<KeyRelease>", _touch)
        ctk.CTkButton(nr, width=150, text="➕ " + self.t("New vault"),
                      command=lambda: do_new()).pack(side=side, padx=2)

        # صف القفل/التغيير — يظهر فقط والخزنة مفتوحة (الصفحة تُبنى من جديد)
        if V.get("unlocked"):
            lr = self.row(c1)
            ctk.CTkButton(lr, width=120, text="🔒 " + self.t("Lock"),
                          command=lambda: do_lock()).pack(side=side, padx=2)
            enp1 = ctk.CTkEntry(lr, width=170, show="•",
                                placeholder_text=self.t("New password"))
            enp2 = ctk.CTkEntry(lr, width=170, show="•",
                                placeholder_text=self.t("Confirm password"))
            enp1.pack(side=side, padx=2)
            enp2.pack(side=side, padx=2)
            enp1.bind("<KeyRelease>", _touch)
            enp2.bind("<KeyRelease>", _touch)
            ctk.CTkButton(lr, width=160, text="🗝 " + self.t("Change password"),
                          command=lambda: do_chg()).pack(side=side, padx=2)
            b_del.configure(command=lambda: do_del())
            b_del.pack(side=side, padx=2)

        st1 = self.statuslabel(c1)

        def do_unlock():
            _touch()
            name = ovlt.get().strip()
            if not name or name == "—":
                return
            fp = vault_path(name)
            if not os.path.isfile(fp):
                st1.configure(text="✗ " + self.t("Vault file") + f": {name}",
                              text_color=CC("err"))
                return
            pw = epw.get()
            try:
                with open(fp, "rb") as f:
                    blob = f.read()
                data = json.loads(
                    vault_decrypt(blob, pw).decode("utf-8"))
                entries = data.get("entries") or []
                if not isinstance(entries, list):
                    raise ValueError("corrupted")
            except ValueError as e:
                wrong = "wrong master password" in str(e).lower()
                st1.configure(text="✗ " + (self.t("Wrong master password")
                                           if wrong
                                           else self.t("Vault corrupted")),
                              text_color=CC("err"))
                return
            except Exception:
                st1.configure(text="✗ " + self.t("Vault corrupted"),
                              text_color=CC("err"))
                return
            V.update({"name": name, "pw": pw, "entries": entries,
                      "unlocked": True, "last_touch": time.time(),
                      "edit_idx": None})
            self.show_tool("vault")                 # إعادة رسم الصفحة مفتوحة

        b_open.configure(command=do_unlock)

        def do_new():
            _touch()
            name = re.sub(r"[^A-Za-z0-9_\-]", "_",
                          ename.get().strip())[:40].strip("_-")
            if not name:
                self.toast("✗ " + self.t("Invalid vault name"), "warn")
                return
            if os.path.isfile(vault_path(name)):
                self.toast("✗ " + self.t("Vault name exists"), "warn")
                return
            pw = epw.get()
            if len(pw) < 4:
                self.toast("⚠ " + self.t("Password too short (min 4)"), "warn")
                return
            V.update({"name": name, "pw": pw, "entries": [],
                      "unlocked": True, "last_touch": time.time(),
                      "edit_idx": None})
            _save_vault()
            self.toast("✓ " + self.t("Vault created"), "ok")
            self.show_tool("vault")

        def do_chg():
            _touch()
            p1, p2 = enp1.get(), enp2.get()
            if p1 != p2:
                st1.configure(text="✗ " + self.t("Master passwords do not match"),
                              text_color=CC("err"))
                return
            if len(p1) < 4:
                self.toast("⚠ " + self.t("Password too short (min 4)"), "warn")
                return
            V["pw"] = p1
            _save_vault()
            enp1.delete(0, "end")
            enp2.delete(0, "end")
            st1.configure(text="✓ " + self.t("Change password"),
                          text_color=CC("ok"))
            self.toast("✓ " + self.t("Change password"), "ok")

        def do_lock():
            _touch()
            self._vault_lock_now()
            self.show_tool("vault")

        def do_del():
            _touch()
            name = V.get("name")
            if not name or not V.get("unlocked"):
                st1.configure(text="✗ " + self.t("Unlock") + f" — {name}",
                              text_color=CC("warn"))
                return
            if not messagebox.askyesno(APP_NAME,
                                       self.t("Delete vault") + f": {name}?"):
                return
            try:
                os.remove(vault_path(name))
            except Exception:
                pass
            self._vault_lock_now()
            self.show_tool("vault")
            self.toast("🗑 " + self.t("Vault deleted"), "ok")

        # ── مقفولة: بطاقة إدخالات فارغة ثم انتهاء ──────────
        if not V.get("unlocked"):
            c2 = self.card(p, "🗝️ " + self.t("Entries"))
            ctk.CTkLabel(c2, text="🔒 " + self.t("Unlock") + " / ➕ "
                         + self.t("New vault"),
                         text_color=CC("muted")).pack(pady=18)
            return

        # ── بطاقة 2: الإدخالات (مفتوحة) ────────────────────
        c2 = self.card(p, "🗝️ " + self.t("Entries"))
        cnt_lbl = ctk.CTkLabel(c2, text=f"({len(V['entries'])})",
                               text_color=CC("muted"))
        cnt_lbl.pack(anchor=anch, padx=14)
        sr = self.row(c2)
        esearch = ctk.CTkEntry(sr, width=300,
                               placeholder_text=self.t("Search…"))
        esearch.pack(side=side, padx=8)
        listf = ctk.CTkScrollableFrame(c2, height=320)
        listf.pack(fill="x", padx=10, pady=(0, 10))

        def _del_entry(i: int, e: dict):
            _touch()
            if not messagebox.askyesno(APP_NAME,
                                       self.t("Delete entry") + ": "
                                       + (e.get("t") or "—") + "?"):
                return
            if 0 <= i < len(V["entries"]):
                V["entries"].pop(i)
                _save_vault()
            render_entries(esearch.get().strip().lower())
            self.toast("🗑 " + self.t("Delete entry"), "ok")

        def render_entries(q: str = ""):
            for w in listf.winfo_children():
                w.destroy()
            vis_n = 0
            for i, e in enumerate(V["entries"]):
                hay = json.dumps(e, ensure_ascii=False).lower()
                if q and q not in hay:
                    continue
                vis_n += 1
                rf = ctk.CTkFrame(listf, fg_color="transparent")
                rf.pack(fill="x", padx=6, pady=3)
                ctk.CTkLabel(rf, text=e.get("t") or "—",
                             font=ctk.CTkFont(size=13, weight="bold")
                             ).pack(side=side, padx=(8, 4))
                if e.get("u"):
                    ctk.CTkLabel(rf, text=e["u"],
                                 text_color=CC("muted")).pack(side=side, padx=4)
                shown = {"on": False}
                lp = ctk.CTkLabel(rf, text="••••••••", width=90,
                                  font=ctk.CTkFont(family="Courier", size=12))

                def _toggle(e=e, lp=lp, shown=shown):
                    _touch()
                    shown["on"] = not shown["on"]
                    lp.configure(text=(e.get("p") or "—")
                                 if shown["on"] else "••••••••")
                lp.pack(side=side, padx=4)
                ctk.CTkButton(rf, width=36, text="👁",
                              command=_toggle).pack(side=side, padx=2)
                ctk.CTkButton(rf, width=44, text="🗝",
                              command=lambda e=e: _copy_secret(
                                  e.get("p") or "")).pack(side=side, padx=2)
                ctk.CTkButton(rf, width=44, text="📋",
                              command=lambda e=e: _copy_secret(
                                  e.get("u") or "")).pack(side=side, padx=2)
                ctk.CTkButton(rf, width=36, text="✏️",
                              command=lambda i=i: _fill_form(i)
                              ).pack(side=side, padx=2)
                ctk.CTkButton(rf, width=36, text="🗑", fg_color=C("err"),
                              hover_color=C("err"),
                              command=lambda i=i, e=e: _del_entry(i, e)
                              ).pack(side=side, padx=2)
            cnt_lbl.configure(text=f"({len(V['entries'])}) · {vis_n}")

        def _on_search(*_):
            _touch()
            render_entries(esearch.get().strip().lower())
        esearch.bind("<KeyRelease>", _on_search)

        # ── بطاقة 3: إضافة/تعديل إدخال ─────────────────────
        c3 = self.card(p)
        form_lbl = ctk.CTkLabel(c3, text="➕ " + self.t("Add entry"),
                                font=ctk.CTkFont(size=14, weight="bold"),
                                text_color=CC("primary"))
        form_lbl.pack(anchor=anch, padx=14, pady=(12, 0))
        f_title = self.field(c3, self.t("Title"), "", 320)
        f_user = self.field(c3, self.t("Username"), "", 320)
        fr2 = self.row(c3)
        ctk.CTkLabel(fr2, text=self.t("Password"), width=150,
                     anchor=anch).pack(side=side)
        f_pass = ctk.CTkEntry(fr2, width=250, show="•")
        f_pass.pack(side=side, padx=8)

        def _gen_pw():
            _touch()
            f_pass.delete(0, "end")
            f_pass.insert(0, _vault_genpw(16))
            f_pass.configure(show="")

        def _toggle_pw():
            f_pass.configure(show="" if f_pass.cget("show") else "•")

        ctk.CTkButton(fr2, width=44, text="🎲",
                      command=_gen_pw).pack(side=side, padx=2)
        ctk.CTkButton(fr2, width=44, text="👁",
                      command=_toggle_pw).pack(side=side, padx=2)
        f_url = self.field(c3, self.t("URL"), "", 320)
        f_notes = self.textbox(c3, 56)
        for w in (f_title, f_user, f_pass, f_url):
            w.bind("<KeyRelease>", _touch)

        def _clear_form():
            for w in (f_title, f_user, f_pass, f_url):
                w.delete(0, "end")
            f_notes.delete("1.0", "end")
            V["edit_idx"] = None
            form_lbl.configure(text="➕ " + self.t("Add entry"))

        def _fill_form(i: int):
            _touch()
            if not (0 <= i < len(V["entries"])):
                return
            e = V["entries"][i]
            V["edit_idx"] = i
            f_title.insert(0, e.get("t") or "")
            f_user.insert(0, e.get("u") or "")
            f_pass.configure(show="")
            f_pass.insert(0, e.get("p") or "")
            f_url.insert(0, e.get("url") or "")
            f_notes.insert("1.0", e.get("n") or "")
            form_lbl.configure(text="✏️ " + self.t("Edit entry")
                               + f" — {e.get('t') or ''}")

        def save_entry():
            _touch()
            t_ = f_title.get().strip()
            if not t_:
                self.toast("✗ " + self.t("Title"), "warn")
                return
            ent = {"t": t_, "u": f_user.get().strip(), "p": f_pass.get(),
                   "url": f_url.get().strip(),
                   "n": f_notes.get("1.0", "end").rstrip("\n"),
                   "ts": _dt.datetime.now().isoformat(timespec="seconds")}
            idx = V.get("edit_idx")
            if idx is None:
                V["entries"].append(ent)
            else:
                if 0 <= idx < len(V["entries"]):
                    V["entries"][idx] = ent
            V["edit_idx"] = None
            _save_vault()
            _clear_form()
            render_entries(esearch.get().strip().lower())
            self.toast("✓ " + self.t("Entry saved"), "ok")

        self.buttons(c3, [
            ("💾 " + self.t("Save entry"), save_entry),
            ("🧹 " + self.t("Clear form"),
             lambda: (_touch(), _clear_form()))])
        render_entries("")

    # ═════════════════════════════════════════════════════
    # 【18】 منطق PolyBuild — تكامل كامل
    # ═════════════════════════════════════════════════════
    PB_LANGS = ["auto", "python", "java", "javascript", "typescript", "c", "cpp",
                "csharp", "go", "rust", "kotlin", "dart", "ruby", "php"]
    PB_BACKENDS = {
        "python": ["pyinstaller", "nuitka", "cx_freeze"],
        "java": ["jpackage", "gradle", "maven"],
        "javascript": ["pkg", "nexe", "electron-builder"],
        "typescript": ["pkg", "electron-builder"],
        "c": ["gcc", "clang"], "cpp": ["g++", "clang++", "cmake"],
        "csharp": ["dotnet"], "go": ["go"], "rust": ["cargo"],
        "kotlin": ["gradle"], "dart": ["flutter", "dart"],
        "ruby": ["ocra"], "php": ["box"],
        "auto": ["auto"],
    }

    def _pb_script(self) -> Optional[str]:
        """كشف polybuild.py تلقائيًا: من الإعدادات أو نفس المجلد."""
        cfg = (self.settings.get("polybuild_path") or "").strip()
        if cfg and os.path.isfile(cfg):
            return cfg
        for cand in ("polybuild.py", "PolyBuild.py", "polybuild/polybuild.py"):
            fp = os.path.join(APP_DIR, cand)
            if os.path.isfile(fp):
                return fp
        return None

    @staticmethod
    def detect_language(path: str) -> str:
        """كشف لغة المشروع من الملفات الموجودة."""
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            return {".py": "python", ".js": "javascript", ".ts": "typescript",
                    ".java": "java", ".c": "c", ".cpp": "cpp", ".cc": "cpp",
                    ".cs": "csharp", ".go": "go", ".rs": "rust", ".kt": "kotlin",
                    ".dart": "dart", ".rb": "ruby", ".php": "php"}.get(ext, "auto")
        if not os.path.isdir(path):
            return "auto"
        markers = [("pubspec.yaml", "dart"), ("Cargo.toml", "rust"),
                   ("go.mod", "go"), ("pom.xml", "java"), ("build.gradle", "java"),
                   ("build.gradle.kts", "kotlin"), ("package.json", "javascript"),
                   ("tsconfig.json", "typescript"), ("requirements.txt", "python"),
                   ("pyproject.toml", "python"), ("setup.py", "python"),
                   ("CMakeLists.txt", "cpp"), ("composer.json", "php"),
                   ("Gemfile", "ruby")]
        names = set(os.listdir(path))
        for marker, lang in markers:
            if marker in names:
                return lang
        counts: Dict[str, int] = {}
        for root, _, files in os.walk(path):
            for fn in files:
                lang = ToolboxApp.detect_language(os.path.join(root, fn))
                if lang != "auto":
                    counts[lang] = counts.get(lang, 0) + 1
            if len(counts) > 0 and root.count(os.sep) - path.count(os.sep) > 2:
                break
        return max(counts, key=counts.get) if counts else "auto"

    def page_polybuild(self, p):
        script = self._pb_script()
        head = self.card(p, "🏗️ PolyBuild")
        ctk.CTkLabel(head,
                     text=(f"✓ detected: {script}" if script
                           else "✗ " + self.t("polybuild.py not found — set it in Settings")),
                     text_color=CC("ok") if script else CC("err"),
                     font=ctk.CTkFont(family="Courier", size=12)).pack(
            anchor="e" if self.rtl else "w", padx=14, pady=(0, 10))

        src = self._folder_picker(head, "project")
        lang = self.option(head, "language", self.PB_LANGS, "auto", 180)
        backend = self.option(head, "backend", ["auto"], "auto", 180)
        target = self.option(head, "target OS",
                             ["host", "windows", "linux", "macos", "android"], "host", 180)
        outdir = self._folder_picker(head, "output")

        r = self.row(head)
        side = "right" if self.rtl else "left"
        onefile = ctk.CTkCheckBox(r, text="onefile")
        onefile.select()
        onefile.pack(side=side, padx=6)
        console = ctk.CTkCheckBox(r, text="console")
        console.pack(side=side, padx=6)
        clean = ctk.CTkCheckBox(r, text="clean")
        clean.pack(side=side, padx=6)

        adv = self.card(p, "⚙️ Advanced")
        hidden = self.field(adv, "hidden-imports", "", 420)
        adddata = self.field(adv, "add-data", "", 420)
        extra = self.field(adv, "extra args", "", 420)

        def on_lang(_=None):
            opts = self.PB_BACKENDS.get(lang.get(), ["auto"])
            backend.configure(values=opts)
            backend.set(opts[0])
        lang.configure(command=lambda _: on_lang())

        def autodetect():
            d = src.get().strip()
            if not d:
                self.toast("select a project first", "warn")
                return
            det = self.detect_language(d)
            lang.set(det)
            on_lang()
            self.toast(f"detected: {det}", "ok")

        # ── المخرجات الملوّنة
        outcard = self.card(p, "📜 Build output")
        log = ctk.CTkTextbox(outcard, height=300,
                             font=ctk.CTkFont(family="Courier", size=12))
        log.pack(fill="both", expand=True, padx=12, pady=8)
        try:
            log.tag_config("ok", foreground=C("ok"))
            log.tag_config("warn", foreground=C("warn"))
            log.tag_config("err", foreground=C("err"))
            log.tag_config("info", foreground=C("muted"))
            self._pb_tags = True
        except Exception:
            self._pb_tags = False
        st = self.statuslabel(outcard)

        def write(line: str):
            """تلوين تلقائي: نجاح/تحذير/خطأ."""
            low = line.lower()
            tag = ("err" if any(k in low for k in ("error", "failed", "traceback", "fatal"))
                   else "warn" if any(k in low for k in ("warning", "warn", "deprecat"))
                   else "ok" if any(k in low for k in ("success", "completed", "done", "built"))
                   else "info")
            try:
                if self._pb_tags:
                    log.insert("end", line, tag)
                else:
                    log.insert("end", line)
                log.see("end")
            except Exception:
                pass

        def build_args() -> List[str]:
            sc = self._pb_script()
            if not sc:
                raise RuntimeError("polybuild.py not found")
            proj = src.get().strip()
            if not proj:
                raise ValueError("select a project folder/file")
            args = [sys.executable, sc, proj]
            if lang.get() != "auto":
                args += ["--lang", lang.get()]
            if backend.get() not in ("auto", "-"):
                args += ["--backend", backend.get()]
            if target.get() != "host":
                args += ["--target", target.get()]
            if outdir.get().strip():
                args += ["--output", outdir.get().strip()]
            if onefile.get():
                args.append("--onefile")
            if console.get():
                args.append("--console")
            if clean.get():
                args.append("--clean")
            for h in [x.strip() for x in hidden.get().split(",") if x.strip()]:
                args += ["--hidden-import", h]
            for a in [x.strip() for x in adddata.get().split(",") if x.strip()]:
                args += ["--add-data", a]
            if extra.get().strip():
                args += extra.get().split()
            return args

        def start_build():
            if self._pb_proc and self._pb_proc.poll() is None:
                self.toast("build already running", "warn")
                return
            try:
                args = build_args()
            except Exception as e:
                self.toast(str(e), "err")
                return
            log.delete("1.0", "end")
            write("$ " + " ".join(args) + "\n\n")
            st.configure(text="⏳ building…", text_color=CC("warn"))
            started = time.time()

            def worker():
                try:
                    self._pb_proc = subprocess.Popen(
                        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, encoding="utf-8", errors="replace", bufsize=1,
                        cwd=os.path.dirname(args[1]) or APP_DIR,
                        creationflags=_no_window_flags())
                except Exception as exc:
                    msg = f"✗ {exc}"
                    self._ui(st.configure, text=msg, text_color=CC("err"))
                    return

                # watchdog: لا subprocess بدون حد زمني
                def watchdog():
                    limit = 3600
                    while self._pb_proc and self._pb_proc.poll() is None:
                        if time.time() - started > limit:
                            try:
                                self._pb_proc.kill()
                            except Exception:
                                pass
                            self._ui(write, "\n[watchdog] timeout > 3600s — killed\n")
                            return
                        time.sleep(1)
                threading.Thread(target=watchdog, daemon=True).start()

                assert self._pb_proc.stdout is not None
                for line in self._pb_proc.stdout:
                    self._ui(write, line)
                rc = self._pb_proc.wait()
                took = time.time() - started
                self._ui(finish, rc, took, args)

            threading.Thread(target=worker, daemon=True).start()

        def finish(rc: int, took: float, args: List[str]):
            ok = rc == 0
            write(f"\n{'─' * 50}\n[exit {rc}] in {took:.1f}s\n")
            st.configure(text=("✓ " + self.t("Done") if ok else f"✗ {self.t('Failed')} (exit {rc})"),
                         text_color=CC("ok") if ok else CC("err"))
            self.toast("🏗️ " + (self.t("Done") if ok else self.t("Failed")),
                       "ok" if ok else "err")
            hist = jload(F_HISTORY, [])
            hist.insert(0, {
                "time": _dt.datetime.now().isoformat(timespec="seconds"),
                "project": src.get().strip(), "lang": lang.get(),
                "backend": backend.get(), "target": target.get(),
                "exit": rc, "seconds": round(took, 1), "cmd": " ".join(args),
            })
            jsave(F_HISTORY, hist[:MAX_HISTORY])
            self._pb_proc = None

        def stop_build():
            if self._pb_proc and self._pb_proc.poll() is None:
                try:
                    self._pb_proc.terminate()
                    write("\n[stopped by user]\n")
                    st.configure(text="⏹ stopped", text_color=CC("warn"))
                except Exception as e:
                    self.toast(str(e), "err")
            else:
                self.toast("no build running", "info")

        self.buttons(head, [("🔍 Auto-detect", autodetect),
                            ("▶ Build", start_build),
                            ("⏹ " + self.t("Stop"), stop_build)])

        # ── فحص أدوات البناء
        tools_card = self.card(p, "🧰 Check Build Tools")
        tools_out = self.textbox(tools_card, 220)
        tst = self.statuslabel(tools_card)

        def check_tools() -> str:
            checks = [("python", [sys.executable, "--version"]),
                      ("pyinstaller", ["pyinstaller", "--version"]),
                      ("nuitka", ["python", "-m", "nuitka", "--version"]),
                      ("node", ["node", "--version"]), ("npm", ["npm", "--version"]),
                      ("pkg", ["pkg", "--version"]), ("java", ["java", "-version"]),
                      ("javac", ["javac", "-version"]), ("gradle", ["gradle", "--version"]),
                      ("maven", ["mvn", "--version"]), ("gcc", ["gcc", "--version"]),
                      ("g++", ["g++", "--version"]), ("clang", ["clang", "--version"]),
                      ("cmake", ["cmake", "--version"]), ("go", ["go", "version"]),
                      ("cargo", ["cargo", "--version"]), ("dotnet", ["dotnet", "--version"]),
                      ("flutter", ["flutter", "--version"]), ("dart", ["dart", "--version"])]
            L = []
            for name, cmd in checks:
                rc, out_ = run_cmd(cmd, 10)
                first = (out_.strip().splitlines() or [""])[0][:52]
                L.append(f" {'✓' if rc == 0 else '✗'}  {name:<14} {first if rc == 0 else 'not found'}")
            return "\n".join(L)

        self.buttons(tools_card, [("🧰 " + self.t("Run"),
                                   lambda: self.run_async(check_tools,
                                                          lambda r_: self.set_box(tools_out, r_), tst))])

        # ── الإعدادات المسبقة
        pre = self.card(p, "💾 Build Presets")
        pname = self.field(pre, "preset name", "", 240)
        plist = self.option(pre, "presets",
                            list(self.settings.get("presets", {}).keys()) or ["-"], width=240)

        def save_preset():
            name = pname.get().strip()
            if not name:
                self.toast("name required", "warn")
                return
            self.settings.setdefault("presets", {})[name] = {
                "project": src.get().strip(), "lang": lang.get(),
                "backend": backend.get(), "target": target.get(),
                "output": outdir.get().strip(), "onefile": bool(onefile.get()),
                "console": bool(console.get()), "clean": bool(clean.get()),
                "hidden": hidden.get(), "adddata": adddata.get(), "extra": extra.get()}
            self.save_settings()
            plist.configure(values=list(self.settings["presets"].keys()))
            plist.set(name)
            self.toast(f"preset «{name}» saved", "ok")

        def load_preset():
            d = self.settings.get("presets", {}).get(plist.get())
            if not d:
                self.toast("preset not found", "warn")
                return
            for ent, key in ((src, "project"), (outdir, "output"),
                             (hidden, "hidden"), (adddata, "adddata"), (extra, "extra")):
                ent.delete(0, "end")
                ent.insert(0, d.get(key, ""))
            lang.set(d.get("lang", "auto"))
            on_lang()
            backend.set(d.get("backend", "auto"))
            target.set(d.get("target", "host"))
            for cb, key in ((onefile, "onefile"), (console, "console"), (clean, "clean")):
                cb.select() if d.get(key) else cb.deselect()
            self.toast(f"preset «{plist.get()}» loaded", "ok")

        def del_preset():
            name = plist.get()
            if name in self.settings.get("presets", {}):
                del self.settings["presets"][name]
                self.save_settings()
                vals = list(self.settings["presets"].keys()) or ["-"]
                plist.configure(values=vals)
                plist.set(vals[0])
                self.toast(f"preset «{name}» deleted", "ok")

        self.buttons(pre, [("💾 " + self.t("Save"), save_preset),
                           ("📂 " + self.t("Load"), load_preset),
                           ("🗑 " + self.t("Delete"), del_preset)])

        # ── سجل البناء
        hcard = self.card(p, "🕘 Build History (last 100)")
        hout = self.textbox(hcard, 220)

        def show_history():
            hist = jload(F_HISTORY, [])
            if not hist:
                self.set_box(hout, "no builds yet")
                return
            L = [f"{'WHEN':<20}{'LANG':<12}{'TARGET':<10}{'EXIT':>6}{'SEC':>8}  PROJECT",
                 "-" * 92]
            for h in hist:
                L.append(f"{h['time'].replace('T', ' '):<20}{h.get('lang', '-'):<12}"
                         f"{h.get('target', '-'):<10}{h.get('exit', '?'):>6}"
                         f"{h.get('seconds', 0):>8}  {os.path.basename(h.get('project', ''))}")
            self.set_box(hout, "\n".join(L))

        self.buttons(hcard, [(self.t("Refresh"), show_history),
                             ("🗑 " + self.t("Clear"),
                              lambda: (jsave(F_HISTORY, []), show_history()))])
        show_history()
        on_lang()


# ─────────────────────────────────────────────────────────────
# 【19】 الإقلاع (main)
# ─────────────────────────────────────────────────────────────
def main():
    """نقطة الدخول: يبني الثيم ثم يشغّل الواجهة."""
    settings = jload(F_SETTINGS, {})
    lang = settings.get("lang", "en")
    font = "Tajawal" if lang in RTL_LANGS else "Roboto"

    theme_path = build_theme_file(font)
    try:
        ctk.set_default_color_theme(theme_path)
    except Exception:
        ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode(settings.get("appearance", "Dark"))

    if platform.system() == "Windows":          # وضوح أفضل على شاشات HiDPI
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    app = ToolboxApp()
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[i] bye")
    except Exception:
        traceback.print_exc()
        print("\n[!] حدث خطأ غير متوقع. تحقّق من الاعتمادات:\n"
              "    pip install customtkinter psutil requests qrcode[pil] Pillow")
        sys.exit(1)
