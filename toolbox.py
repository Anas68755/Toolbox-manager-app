#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate Toolbox Pro v3.1
=========================
صندوق أدوات متكامل لسطح المكتب — Windows / Linux / macOS
Python 3.9+ · customtkinter · offline-first

التشغيل:  python toolbox.py
الاعتمادات الأساسية:   customtkinter, psutil
الاعتمادات الاختيارية: requests, qrcode, Pillow
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
import hashlib
import html
import io
import json
import math
import os
import platform
import random
import re
import shutil
import socket
import string
import subprocess
import sys
import threading
import time
import traceback
import urllib.parse
import urllib.request
import uuid
import webbrowser
import zipfile
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

# tkinter (يأتي مع بايثون) — نحتاج Canvas و filedialog
try:
    import tkinter as tk
    from tkinter import filedialog
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
}

# ─────────────────────────────────────────────────────────────
# 【2】 الثوابت والمسارات
# ─────────────────────────────────────────────────────────────
APP_NAME = "Ultimate Toolbox Pro"
APP_VERSION = "3.1"
APP_DIR = os.path.dirname(os.path.abspath(__file__))

F_SETTINGS = os.path.join(APP_DIR, "ultimate_toolbox_settings.json")
F_TASKS    = os.path.join(APP_DIR, "ultimate_toolbox_tasks.json")
F_NOTES    = os.path.join(APP_DIR, "ultimate_toolbox_notes.txt")
F_THEME    = os.path.join(APP_DIR, "ultimate_toolbox_theme.json")
F_HISTORY  = os.path.join(APP_DIR, "polybuild_history.json")

SUBPROCESS_TIMEOUT = 30          # لا subprocess بدون timeout
NET_TIMEOUT = 12
MAX_HISTORY = 100

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
}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {}, "ar": _AR, "zh": _ZH, "es": _ES, "fr": _FR,
    "ru": _RU, "pt": _PT, "hi": _HI, "bn": _BN, "ur": _UR,
}

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


def http_post_json(url: str, payload: dict,
                   headers: Optional[dict] = None) -> Any:
    """POST JSON — للمساعد الذكي وغيره."""
    headers = dict(headers or {})
    headers.setdefault("Content-Type", "application/json")
    headers.setdefault("User-Agent", f"{APP_NAME}/{APP_VERSION}")
    data = json.dumps(payload).encode("utf-8")
    if HAS_REQUESTS:
        r = requests.post(url, data=data, headers=headers, timeout=NET_TIMEOUT)
        return r.json()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=NET_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def run_cmd(args: List[str], timeout: int = SUBPROCESS_TIMEOUT) -> Tuple[int, str]:
    """تنفيذ أمر خارجي — دائمًا بـ timeout."""
    try:
        p = subprocess.run(args, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
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
    "polybuild_path": "",
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

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1280x800")
        self.minsize(1000, 640)
        ctk.set_appearance_mode(self.settings.get("appearance", "Dark"))

        self._build_layout()
        self._bind_keys()
        self.show_tool(self.current)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(1200, self._tick_monitor)

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

        # الشريط الجانبي
        self.sidebar = ctk.CTkScrollableFrame(self, width=248, corner_radius=0,
                                              fg_color=CC("surface"))
        self.sidebar.grid(row=1, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.search_entry = ctk.CTkEntry(self.sidebar,
                                         placeholder_text=self.t("Search tools…"),
                                         height=34)
        self.search_entry.pack(fill="x", padx=8, pady=(6, 8))
        self.search_entry.bind("<KeyRelease>", lambda e: self._rebuild_nav())

        self.nav_holder = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_holder.pack(fill="both", expand=True)

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

    # ── بناء الشريط الجانبي (مع الطي والبحث والمفضلة والحديثة)
    def _rebuild_nav(self):
        for w in self.nav_holder.winfo_children():
            w.destroy()
        self.nav_buttons.clear()
        q = (self.search_entry.get() or "").strip().lower() if hasattr(self, "search_entry") else ""

        def match(tool: Tool) -> bool:
            if not q:
                return True
            hay = f"{tool.title} {self.t(tool.title)} {tool.keywords} {tool.tid}".lower()
            return q in hay

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
        for sec in SECTIONS:
            items = [t for t in TOOLS if t.section == sec and match(t)]
            if not items:
                continue
            is_open = q != "" or sec not in collapsed
            self._nav_header(f"{'▾' if is_open else '▸'} {self.t(sec)}",
                             cmd=lambda s=sec: self._toggle_section(s))
            if is_open:
                for tool in items:
                    self._nav_button(tool)

    def _nav_header(self, text: str, cmd: Optional[Callable] = None):
        b = ctk.CTkButton(self.nav_holder, text=text, anchor="e" if self.rtl else "w",
                          height=28, fg_color="transparent",
                          hover_color=CC("surface2"), text_color=CC("muted"),
                          font=ctk.CTkFont(size=12, weight="bold"),
                          command=cmd or (lambda: None))
        b.pack(fill="x", padx=6, pady=(8, 2))

    def _nav_button(self, tool: Tool):
        active = tool.tid == self.current
        b = ctk.CTkButton(
            self.nav_holder, text=f"  {tool.icon}  {self.t(tool.title)}",
            anchor="e" if self.rtl else "w", height=32,
            fg_color=CC("primary") if active else "transparent",
            hover_color=CC("primary_h") if active else CC("surface2"),
            text_color=("#ffffff" if active else C("text")),
            font=ctk.CTkFont(size=13),
            command=lambda tid=tool.tid: self.show_tool(tid))
        b.pack(fill="x", padx=6, pady=1)
        self.nav_buttons[tool.tid] = b

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
        self._rebuild_nav()
        self.show_tool(self.current)          # تبديل فوري بلا إعادة تشغيل
        self.toast(f"{LANG_NAMES[code]} ✓", "ok")

    # ── الحفظ والإغلاق
    def save_settings(self):
        jsave(F_SETTINGS, self.settings)

    def on_close(self):
        self.save_settings()
        try:
            if self._pb_proc and self._pb_proc.poll() is None:
                self._pb_proc.terminate()
        except Exception:
            pass
        self.destroy()

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
                self.after(0, lambda: self._async_ok(res, done, label))
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                self.after(0, lambda: self._async_err(err, label))

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

        def refresh(*_):
            for w in listf.winfo_children():
                w.destroy()
            q = entry.get().strip().lower()
            hits = [t for t in TOOLS
                    if not q or q in f"{t.title} {self.t(t.title)} {t.keywords}".lower()][:30]
            for tool in hits:
                ctk.CTkButton(
                    listf, text=f"{tool.icon}  {self.t(tool.title)}   ·   {self.t(tool.section)}",
                    anchor="e" if self.rtl else "w", height=32, fg_color="transparent",
                    hover_color=CC("primary"), text_color=CC("text"),
                    command=lambda tid=tool.tid: (self._close_palette(), self.show_tool(tid))
                ).pack(fill="x", pady=1)

        def go_first(_=None):
            q = entry.get().strip().lower()
            hits = [t for t in TOOLS
                    if not q or q in f"{t.title} {self.t(t.title)} {t.keywords}".lower()]
            if hits:
                self._close_palette()
                self.show_tool(hits[0].tid)

        entry.bind("<KeyRelease>", refresh)
        entry.bind("<Return>", go_first)
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
        ctk.CTkButton(header, text="⭐" if fav else "☆", width=40, height=30,
                      fg_color="transparent", hover_color=CC("surface2"),
                      text_color=CC("warn") if fav else CC("muted"),
                      command=lambda: self.toggle_fav(tid)).pack(side=side, padx=8)

        self.page = ctk.CTkScrollableFrame(self.content_wrap, fg_color="transparent")
        self.page.grid(row=1, column=0, sticky="nsew", padx=10, pady=8)

        builder = getattr(self, f"page_{tid}", None)
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

    def toggle_fav(self, tid: str):
        favs = list(self.settings.get("favorites", []))
        if tid in favs:
            favs.remove(tid)
        else:
            favs.append(tid)
        self.settings["favorites"] = favs
        self.save_settings()
        self.show_tool(self.current)

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
        self.after(1200, self._tick_monitor)

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
        ctk.CTkLabel(k, text="المفاتيح تُحفظ محليًا فقط في ultimate_toolbox_settings.json",
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
                L.append("\n [!] psutil غير مثبت — التفاصيل محدودة. pip install psutil")
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
                psutil.Process(pid).terminate()
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

        self.set_box(out, local_info())

        def public_ip():
            def work():
                return http_get("https://api.ipify.org?format=json")[1]
            self.run_async(work,
                           lambda r_: self.set_box(out, out.get("1.0", "end").rstrip() +
                                                   f"\n Public IP  : {json.loads(r_).get('ip','?')}"),
                           st)

        self.buttons(c, [(self.t("Refresh"), lambda: self.set_box(out, local_info())),
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

        def scan() -> str:
            stop.clear()
            h = host.get().strip()
            a, _, b = rng.get().strip().partition("-")
            lo, hi = int(a), int(b or a)
            hi = min(hi, 65535)
            if hi - lo > 5000:
                raise ValueError("range too wide (max 5000 ports)")
            found = []
            common = {21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
                      80: "http", 110: "pop3", 143: "imap", 443: "https",
                      3306: "mysql", 3389: "rdp", 5432: "postgres", 6379: "redis",
                      8080: "http-alt", 27017: "mongodb"}
            for port in range(lo, hi + 1):
                if stop.is_set():
                    break
                s = socket.socket()
                s.settimeout(0.25)
                if s.connect_ex((h, port)) == 0:
                    found.append(f"  {port:>6}  OPEN   {common.get(port, '')}")
                s.close()
            return "\n".join(found) or "no open ports found"

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
        method = self.option(c, "method", ["GET", "POST"], "GET", 120)
        url = self.field(c, "URL", "https://api.github.com", 440)
        ctk.CTkLabel(c, text="JSON body (POST)", text_color=CC("muted")).pack(
            anchor="e" if self.rtl else "w", padx=14)
        body = self.textbox(c, 110)
        out = self.textbox(c, 300)
        st = self.statuslabel(c)

        def send() -> str:
            u = url.get().strip()
            if method.get() == "GET":
                code, text = http_get(u)
                head = f"HTTP {code}\n\n"
            else:
                payload = json.loads(body.get("1.0", "end").strip() or "{}")
                text = json.dumps(http_post_json(u, payload), ensure_ascii=False, indent=2)
                head = "POST OK\n\n"
            try:
                text = json.dumps(json.loads(text), ensure_ascii=False, indent=2)
            except Exception:
                pass
            return head + text[:200000]

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
        ctk.CTkLabel(c, text="خوارزمية 3 مراحل: الحجم ← بادئة 8KB ← تجزئة كاملة",
                     text_color=CC("muted")).pack(anchor="e" if self.rtl else "w", padx=14)
        folder = self._folder_picker(c)
        out = self.textbox(c, 340)
        st = self.statuslabel(c)

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
            L = [f"scanned groups: {len(by_size)}  ·  duplicate groups: {len(dupes)}",
                 f"reclaimable: {human_size(wasted)}", ""]
            for h, paths in list(dupes.items())[:200]:
                L.append(f"■ {h[:16]}…  ({human_size(os.path.getsize(paths[0]))})")
                for fp in paths:
                    L.append(f"    {fp}")
                L.append("")
            return "\n".join(L)

        self.buttons(c, [("🔍 " + self.t("Run"),
                          lambda: self.run_async(find, lambda r_: self.set_box(out, r_), st)),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

    def page_rename(self, p):
        c = self.card(p, "✏️ " + self.t("Bulk Rename"))
        folder = self._folder_picker(c)
        find_e = self.field(c, "find", "", 200)
        repl_e = self.field(c, "replace", "", 200)
        pre_e = self.field(c, "prefix", "", 200)
        suf_e = self.field(c, "suffix", "", 200)
        case_m = self.option(c, "case", ["keep", "lower", "UPPER", "Title"], "keep", 160)
        dry = ctk.CTkCheckBox(c, text="Dry run (preview only)")
        dry.select()
        dry.pack(anchor="e" if self.rtl else "w", padx=14, pady=4)
        out = self.textbox(c, 280)
        st = self.statuslabel(c)

        def do() -> str:
            d = folder.get().strip()
            if not os.path.isdir(d):
                raise ValueError("folder not found")
            preview = bool(dry.get())
            L, n = [], 0
            for name in sorted(os.listdir(d)):
                src = os.path.join(d, name)
                if not os.path.isfile(src):
                    continue
                base, ext = os.path.splitext(name)
                if find_e.get():
                    base = base.replace(find_e.get(), repl_e.get())
                cm = case_m.get()
                base = (base.lower() if cm == "lower" else base.upper() if cm == "UPPER"
                        else base.title() if cm == "Title" else base)
                new = f"{pre_e.get()}{base}{suf_e.get()}{ext}"
                if new == name:
                    continue
                L.append(f"  {name}  →  {new}")
                n += 1
                if not preview:
                    os.rename(src, os.path.join(d, new))
            head = "PREVIEW — nothing renamed\n" if preview else "RENAMED\n"
            return f"{head}{n} file(s)\n\n" + "\n".join(L[:500])

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
            res = {a: file_hash(path, a) for a in ("md5", "sha1", "sha256", "sha512")}
            L = [f" size   : {human_size(os.path.getsize(path))}"]
            L += [f" {a:<7}: {v}" for a, v in res.items()]
            exp = expect.get().strip().lower()
            if exp:
                ok = exp in res.values()
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
                w.writerows(data)
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
        out = self.textbox(c, 220)

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
        self.buttons(c, [(self.t("Run"), test)])
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
            codes.configure(text="   ".join(hexes) + "   (اضغط على أي لون لنسخه)")

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
        ctk.CTkLabel(c, text="آمنة: تُحلَّل التعابير عبر ast — لا eval إطلاقًا",
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
                    f" next milestone  : {(a.replace(year=a.year + years + 1) - _dt.date.today()).days} days",
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
                    self.toast("⏰ Time is up!", "ok", 6000)
                    self.bell()
                else:
                    cdisp.configure(text=time.strftime("%M:%S", time.gmtime(left)),
                                    text_color=CC("text"))
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
                    self.toast("🍅 " + ("Break time!" if st["work"] else "Back to work!"),
                               "ok", 5000)
                    if st["work"]:
                        st["cycles"] += 1
                    st["work"] = not st["work"]
                    start()
                else:
                    disp.configure(text=time.strftime("%M:%S", time.gmtime(left)))
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
            return f"✓ imported from {path}\nرجاءً أعد تشغيل التطبيق لتطبيق كل شيء."

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
        ctk.CTkLabel(c, text="سطر واحد لكل عنصر", text_color=CC("muted")).pack(
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
            L += ["", " 💡 أضف مفتاح OpenWeather في الإعدادات لتفاصيل أدق."]
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

        def fetch() -> str:
            u = url.get().strip()
            if not u.startswith("http"):
                u = "https://" + u
            code, text = http_get("https://is.gd/create.php?" +
                                  urllib.parse.urlencode({"format": "simple", "url": u}))
            if code >= 400:
                raise RuntimeError(text[:200])
            return f" short : {text.strip()}\n long  : {u}"

        self.buttons(c, [("🔗 " + self.t("Run"),
                          lambda: self.run_async(fetch, lambda r_: self.set_box(out, r_), st)),
                         (self.t("Copy"),
                          lambda: self.copy_text(out.get("1.0", "end").split()[2]
                                                 if len(out.get("1.0", "end").split()) > 2 else ""))])

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
        ctk.CTkLabel(c, text="يعمل مع OpenAI أو أي endpoint متوافق (تُضبط المفاتيح في الإعدادات)",
                     text_color=CC("muted")).pack(anchor="e" if self.rtl else "w", padx=14)
        model = self.field(c, "model", "gpt-4o-mini", 240)
        prompt = self.textbox(c, 140, "اشرح لي فكرة الـ threading باختصار.")
        out = self.textbox(c, 300)
        st = self.statuslabel(c)

        def ask() -> str:
            key = self._key("openai")
            if not key:
                return ("⚠ API key required.\n\n" + self.t("Settings") +
                        " → API Keys → openai\n"
                        "يمكن أيضًا ضبط openai_base لأي خادم متوافق (Ollama, LM Studio, …)")
            base = self._key("openai_base") or "https://api.openai.com/v1"
            d = http_post_json(
                base.rstrip("/") + "/chat/completions",
                {"model": model.get().strip(),
                 "messages": [{"role": "user", "content": prompt.get("1.0", "end").strip()}],
                 "temperature": 0.7},
                {"Authorization": f"Bearer {key}"})
            if "error" in d:
                raise RuntimeError(d["error"].get("message", "api error"))
            return d["choices"][0]["message"]["content"]

        self.buttons(c, [("🤖 " + self.t("Run"),
                          lambda: self.run_async(ask, lambda r_: self.set_box(out, r_), st)),
                         (self.t("Copy"), lambda: self.copy_text(out.get("1.0", "end")))])

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
                           else "✗ polybuild.py غير موجود — حدّده في " + self.t("Settings")),
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
                        cwd=os.path.dirname(args[1]) or APP_DIR)
                except Exception as exc:
                    msg = f"✗ {exc}"
                    self.after(0, lambda m=msg: st.configure(text=m, text_color=CC("err")))
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
                            self.after(0, lambda: write("\n[watchdog] timeout > 3600s — killed\n"))
                            return
                        time.sleep(1)
                threading.Thread(target=watchdog, daemon=True).start()

                assert self._pb_proc.stdout is not None
                for line in self._pb_proc.stdout:
                    self.after(0, lambda ln=line: write(ln))
                rc = self._pb_proc.wait()
                took = time.time() - started
                self.after(0, lambda: finish(rc, took, args))

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
