#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JSON Editor — إضافة نموذجية لـ Ultimate Toolbox Pro v4.2.

تحرير/تنسيق/تصغير/تحقق من JSON مع نسخ النتيجة. توضّح: مربعات النص،
قوائم الاختيار، تحديث التسميات، ومعالجة الأخطاء داخل الإضافة.
الدوال النقية (_fmt/_minify/_validate) قابلة للاختبار بمعزل عن الواجهة.
"""
import json

from toolbox_api import (register_tool, card, buttons, option, textbox,
                         statuslabel, set_box, toast, copy_text, t,
                         add_translations)

add_translations({
    "ar": {"JSON Editor": "محرر JSON", "Input (JSON)": "الإدخال (JSON)",
           "Format": "تنسيق", "Minify": "تصغير", "Validate": "تحقق",
           "Copy result": "نسخ النتيجة", "Sort keys": "ترتيب المفاتيح",
           "Output": "الناتج", "Result": "النتيجة",
           "Valid JSON ✓": "JSON سليم ✓", "Result copied": "تم نسخ النتيجة",
           "Input is empty": "الإدخال فارغ",
           "Format, minify or validate JSON — by a plugin":
               "تنسيق أو تصغير أو تحقق من JSON — عبر إضافة"},
    "zh": {"JSON Editor": "JSON 编辑器", "Input (JSON)": "输入 (JSON)",
           "Format": "格式化", "Minify": "压缩", "Validate": "校验",
           "Copy result": "复制结果", "Sort keys": "键排序",
           "Output": "输出", "Result": "结果",
           "Valid JSON ✓": "JSON 有效 ✓", "Result copied": "结果已复制",
           "Input is empty": "输入为空",
           "Format, minify or validate JSON — by a plugin":
               "格式化、压缩或校验 JSON——由插件提供"},
    "es": {"JSON Editor": "Editor JSON", "Input (JSON)": "Entrada (JSON)",
           "Format": "Formatear", "Minify": "Minificar", "Validate": "Validar",
           "Copy result": "Copiar resultado", "Sort keys": "Ordenar claves",
           "Output": "Salida", "Result": "Resultado",
           "Valid JSON ✓": "JSON válido ✓", "Result copied": "Resultado copiado",
           "Input is empty": "La entrada está vacía",
           "Format, minify or validate JSON — by a plugin":
               "Formatea, minifica o valida JSON — por un complemento"},
    "fr": {"JSON Editor": "Éditeur JSON", "Input (JSON)": "Entrée (JSON)",
           "Format": "Formater", "Minify": "Minifier", "Validate": "Valider",
           "Copy result": "Copier le résultat", "Sort keys": "Trier les clés",
           "Output": "Sortie", "Result": "Résultat",
           "Valid JSON ✓": "JSON valide ✓", "Result copied": "Résultat copié",
           "Input is empty": "L'entrée est vide",
           "Format, minify or validate JSON — by a plugin":
               "Formatez, minifiez ou validez du JSON — par une extension"},
    "ru": {"JSON Editor": "JSON-редактор", "Input (JSON)": "Ввод (JSON)",
           "Format": "Форматировать", "Minify": "Минифицировать",
           "Validate": "Проверить", "Copy result": "Копировать результат",
           "Sort keys": "Сортировать ключи", "Output": "Вывод",
           "Result": "Результат", "Valid JSON ✓": "Корректный JSON ✓",
           "Result copied": "Результат скопирован",
           "Input is empty": "Ввод пуст",
           "Format, minify or validate JSON — by a plugin":
               "Форматирование, минификация и проверка JSON — плагин"},
    "pt": {"JSON Editor": "Editor JSON", "Input (JSON)": "Entrada (JSON)",
           "Format": "Formatar", "Minify": "Minificar", "Validate": "Validar",
           "Copy result": "Copiar resultado", "Sort keys": "Ordenar chaves",
           "Output": "Saída", "Result": "Resultado",
           "Valid JSON ✓": "JSON válido ✓", "Result copied": "Resultado copiado",
           "Input is empty": "A entrada está vazia",
           "Format, minify or validate JSON — by a plugin":
               "Formate, minifique ou valide JSON — por um plugin"},
    "hi": {"JSON Editor": "JSON संपादक", "Input (JSON)": "इनपुट (JSON)",
           "Format": "फ़ॉर्मेट", "Minify": "मिनिफ़ाई", "Validate": "सत्यापित",
           "Copy result": "परिणाम कॉपी करें", "Sort keys": "कुंजियाँ क्रमित करें",
           "Output": "आउटपुट", "Result": "परिणाम",
           "Valid JSON ✓": "मान्य JSON ✓", "Result copied": "परिणाम कॉपी हुआ",
           "Input is empty": "इनपुट खाली है",
           "Format, minify or validate JSON — by a plugin":
               "JSON फ़ॉर्मेट/मिनिफ़ाई/सत्यापन — प्लगइन द्वारा"},
    "bn": {"JSON Editor": "JSON সম্পাদক", "Input (JSON)": "ইনপুট (JSON)",
           "Format": "ফরম্যাট", "Minify": "মিনিফাই", "Validate": "যাচাই",
           "Copy result": "ফলাফল কপি করুন", "Sort keys": "কী সাজান",
           "Output": "আউটপুট", "Result": "ফলাফল",
           "Valid JSON ✓": "বৈধ JSON ✓", "Result copied": "ফলাফল কপি হয়েছে",
           "Input is empty": "ইনপুট খালি",
           "Format, minify or validate JSON — by a plugin":
               "JSON ফরম্যাট/মিনিফাই/যাচাই — প্লাগইন দ্বারা"},
    "ur": {"JSON Editor": "JSON ایڈیٹر", "Input (JSON)": "ان پٹ (JSON)",
           "Format": "فارمیٹ", "Minify": "منیفائی", "Validate": "توثیق",
           "Copy result": "نتیجہ کاپی کریں", "Sort keys": "کلیدیں ترتیب دیں",
           "Output": "آؤٹ پٹ", "Result": "نتیجہ",
           "Valid JSON ✓": "درست JSON ✓", "Result copied": "نتیجہ کاپی ہوگیا",
           "Input is empty": "ان پٹ خالی ہے",
           "Format, minify or validate JSON — by a plugin":
               "JSON فارمیٹ/منیفائی/توثیق — پلگ ان کی طرف سے"},
})


# ── دوال نقية قابلة للاختبار بمعزل عن الواجهة ──────────────────────
def _parse(text: str):
    """json.loads مع رسالة خطأ موجزة — يرفع ValueError."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"line {e.lineno}, col {e.colno}: {e.msg}") from e


def _fmt(text: str, sort_keys: bool = False) -> str:
    return json.dumps(_parse(text), indent=2, sort_keys=sort_keys,
                      ensure_ascii=False)


def _minify(text: str) -> str:
    return json.dumps(_parse(text), separators=(",", ":"),
                      ensure_ascii=False)


def _validate(text: str) -> str:
    _parse(text)
    return "ok"


@register_tool(tid="json_editor", title="JSON Editor", section="Plugins",
               icon="{ }", keywords="json format minify validate editor pretty")
def build(api, parent):
    card(parent, t("Format, minify or validate JSON — by a plugin"))
    src = textbox(parent, height=150, text='{"plugin": true, "n": 1}')

    sortm = option(parent, t("Sort keys"), ["No", "Yes"], default="No")
    status = statuslabel(parent)
    out = textbox(parent, height=170)

    def _apply(fn, *a):
        text = src.get("1.0", "end").strip()
        if not text:
            toast(t("Input is empty"), "warn")
            return
        try:
            res = fn(text, *a)
            set_box(out, res)
            status.configure(text=t("Valid JSON ✓"))
        except ValueError as e:
            status.configure(text=f"✗ {e}")

    buttons(parent, [
        (t("Format"), lambda: _apply(_fmt, sortm.get() == "Yes")),
        (t("Minify"), lambda: _apply(_minify)),
        (t("Validate"), lambda: _apply(_validate)),
        (t("Copy result"), lambda: copy_text(out.get("1.0", "end").strip())),
    ])
