#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════
 Ultimate Toolbox Pro — Plugin API  (toolbox_api.py)
 ═══════════════════════════════════════════════════════════════════
 v4.2.0  •  API version 1.0

 واجهة برمجية عامة تسمح لأي ملف Python داخل مجلد plugins/ بإضافة
 أداة جديدة إلى الشريط الجانبي للتطبيق دون تعديل toolbox.py.

 ▸ الاستخدام الأساسي:

     from toolbox_api import register_tool, card, field, buttons, toast

     @register_tool(
         tid="my_tool",              # معرّف فريد (أحرف صغيرة/أرقام/_)
         title="My Tool",            # العنوان (إنجليزي — قابل للترجمة)
         section="Plugins",          # قسم جديد أو موجود
         icon="🧩",                  # أي إيموجي
         keywords="demo sample",     # كلمات تظهر في البحث
     )
     def build(api, parent):
         card(parent, "Hello from plugin")
         e = field(parent, "Your name")
         buttons(parent, [("Greet", lambda: toast(f"Hi, {e.get() or '…}!"))])

 ▸ بناء الصفحة:
   يستدعى builder مرة واحدة عند فتح الأداة بنفس طريقة أدوات التطبيق،
   ويتلقّى (api, parent) حيث parent إطار قابل للتمرير داخل الصفحة.

 ▸ الخيوط (Threads):
   استخدم run_async(work, done=…) لكل عملية طويلة؛ يعمل work في
   خيط خلفي ويعاد done في الخيط الرئيسي تلقائيًا. للتحديثات اللحظية
   من داخل الخيط استخدم ui(fn) — هي القناة الآمنة الوحيدة للواجهة.

 ▸ الترجمة:
   تُترجم مفاتيحك تلقائيًا إذا أضفتها عبر add_translations({lang: {key: text}}).
   اللغات المدعومة: en, ar, zh, es, fr, ru, pt, hi, bn, ur.

 ▸ نموذج الثقة:
   الإضافات كود Python كامل الصلاحيات يُحمَّل محليًا — ثبّت فقط إضافات
   من مصادر تثق بها. أخطاء أي إضافة معزولة ولا تُسقط التطبيق.
════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

__api_version__ = "1.0"

# ── الحالة الداخلية (تُضبط من toolbox.py عند الإقلاع) ──────────────
_APP: Any = None                                    # نسخة ToolboxApp
_TRANSLATIONS: Dict[str, Dict[str, str]] = {}       # مرجع لقاموس الترجمة
_T_CACHE: Dict[Any, str] = {}                       # مرجع لذاكرة الترجمة
_REGISTRY: List[Dict[str, Any]] = []                # الأدوات المسجّلة


# ── ربط داخلي ───────────────────────────────────────────────────────
def _bind(app: Any, translations: Optional[Dict[str, Dict[str, str]]] = None,
          tcache: Optional[Dict[Any, str]] = None) -> None:
    """يستدعى من ToolboxApp مرة واحدة عند الإقلاع — لا تستخدمه."""
    global _APP, _TRANSLATIONS, _T_CACHE
    _APP = app
    if translations is not None:
        _TRANSLATIONS = translations
    if tcache is not None:
        _T_CACHE = tcache


def _app() -> Any:
    if _APP is None:
        raise RuntimeError(
            "toolbox_api is not bound — load plugins only from inside the app")
    return _APP


def app() -> Any:
    """النسخة الجارية من التطبيق — للاستخدامات المتقدمة فقط.

    يُفضَّل استخدام دوال الـ API أعلاه؛ هذه البوابة لمن يحتاج شيئًا
    غير مغطّى، مع قبول مسؤولية التوافق مع بنية التطبيق الداخلية.
    """
    return _app()


# ═══════════════════════════ التسجيل ════════════════════════════════

def register_tool(tid: str, title: str, section: str = "Plugins",
                  icon: str = "🧩", keywords: str = "") -> Callable:
    """مُزيّن يسجّل دالة بناء صفحة أداة جديدة.

    tid      : معرّف فريد يتكوّن من [a-z0-9_] فقط (يُرفض غير ذلك بهدوء).
    title    : العنوان الإنجليزي — يُستخدم كمفتاح ترجمة أيضًا.
    section  : اسم القسم؛ إن كان جديدًا يُنشأ تلقائيًا في القائمة.
    icon     : إيموجي يظهر بجانب العنوان.
    keywords : كلمات مفتاحية إضافية لمحرك البحث الضبابي.
    """
    clean = "".join(c for c in str(tid).lower() if c.isalnum() or c == "_")
    if not clean or clean[0].isdigit():
        clean = "plugin_" + (clean or "tool")

    def deco(fn: Callable) -> Callable:
        _REGISTRY.append({
            "tid": clean,
            "title": str(title),
            "section": str(section or "Plugins"),
            "icon": str(icon or "🧩"),
            "description": str(keywords or ""),
            "builder": fn,
        })
        return fn
    return deco


def get_registry() -> List[Dict[str, Any]]:
    """نسخة من قائمة الأدوات المسجّلة حتى الآن (للاختبار والفحص)."""
    return list(_REGISTRY)


def api_version() -> str:
    return __api_version__


# ═══════════════════════ الترجمة وقت التشغيل ════════════════════════

def add_translations(mapping_by_lang: Dict[str, Dict[str, str]]) -> None:
    """أضف ترجمات مفاتيحك: {"ar": {"My Tool": "أداتي"}, "fr": {…}}.

    تُدمج في قاموس التطبيق الرئيسي وتُفرغ ذاكرة الترجمة فورًا، فتعمل
    حتى لو أُضيفت بعد أول عرض للأداة.
    """
    for lang, mapping in (mapping_by_lang or {}).items():
        try:
            _TRANSLATIONS.setdefault(str(lang), {}).update(dict(mapping))
        except Exception:
            continue
    try:
        _T_CACHE.clear()
    except Exception:
        pass


# ═══════════════════════ سلوك التطبيق ═══════════════════════════════

def t(key: str) -> str:
    """ترجمة مفتاح إلى لغة واجهة التطبيق الحالية."""
    try:
        return _app().t(str(key))
    except RuntimeError:
        return str(key)


def lang() -> str:
    """رمز اللغة الحالية (en / ar / …)."""
    return getattr(_app(), "lang", "en")


def is_rtl() -> bool:
    """هل الاتجاه الحالي من اليمين إلى اليسار؟"""
    return bool(getattr(_app(), "rtl", False))


def ui(fn: Callable, *args, **kwargs) -> None:
    """جدولة fn في الخيط الرئيسي — القناة الآمنة الوحيدة من الخيوط."""
    _app()._ui(fn, *args, **kwargs)


def run_async(work: Callable[[], Any],
              done: Optional[Callable[[Any], None]] = None,
              label: Any = None, busy_text: Optional[str] = None) -> None:
    """تشغيل work في خيط خلفي؛ يعاد done(result) في الخيط الرئيسي."""
    _app().run_async(work, done=done, label=label, busy_text=busy_text)


def stop_event(key: str) -> Any:
    """حدث إيقاف مرتبط بالمفتاح — مفيد لحلقات التوليد/المسح الطويلة."""
    app = _app()
    ev = app._stop_flags.get(key)
    if ev is None:
        import threading
        ev = threading.Event()
        app._stop_flags[key] = ev
    return ev


def toast(msg: str, kind: str = "info", ms: int = 2600) -> None:
    """إشعار سريع أسفل النافذة (kind: info / ok / warn / err)."""
    try:
        _app().toast(str(msg), kind=kind, ms=ms)
    except RuntimeError:
        pass


def popup(title: str, message: str) -> None:
    """نافذة تنبيه موحّدة مع المحتوى."""
    _app().popup(str(title), str(message))


def set_status(text: str) -> None:
    """كتابة نص في شريط الحالة السفلي."""
    _app().set_status(str(text))


def copy_text(text: str) -> None:
    """نسخ إلى الحافظة مع توست تأكيد."""
    _app().copy_text(str(text))


def open_tool(tid: str) -> None:
    """الانتقال إلى أداة أخرى بمعرّفها (مثل open_tool('calc'))."""
    _app().show_tool(str(tid))


# ═══════════════════════ الإعدادات ══════════════════════════════════

def setting(key: str, default: Any = None) -> Any:
    """قراءة إعداد محفوظ (يُدار ويُحفظ تلقائيًا مع إعدادات التطبيق)."""
    return _app().settings.get(str(key), default)


def set_setting(key: str, value: Any, save: bool = True) -> None:
    """كتابة إعداد؛ save=True يحفظه على القرص فورًا."""
    app = _app()
    app.settings[str(key)] = value
    if save:
        app.save_settings()


# ═══════════════════════ عناصر الواجهة ══════════════════════════════
# كلها تفويض لعناصر التطبيق الموحّدة — تحترم الثيم والاتجاه (RTL) تلقائيًا.

def card(parent: Any, title: str = "") -> Any:
    """بطاقة موحّدة بإطار وزوايا — إن title فارغًا تُعاد بطاقة بلا عنوان."""
    return _app().card(parent, str(title))


def row(parent: Any) -> Any:
    """صف أفقي شفاف لتجميع العناصر."""
    return _app().row(parent)


def field(parent: Any, label: str, default: str = "", width: int = 300,
          show: Optional[str] = None) -> Any:
    """حقل إدخال سطر واحد مع تسمية. show='*' لكلمات المرور."""
    return _app().field(parent, str(label), str(default), width=width, show=show)


def option(parent: Any, label: str, values: List[str],
           default: Optional[str] = None, width: int = 220,
           command: Optional[Callable] = None) -> Any:
    """قائمة اختيار منسدلة مع تسمية."""
    return _app().option(parent, str(label), list(values or []),
                         default=default, width=width, command=command)


def textbox(parent: Any, height: int = 160, text: str = "") -> Any:
    """مربع نص متعدد الأسطر بخط ثابت العرض."""
    return _app().textbox(parent, height=height, text=str(text or ""))


def buttons(parent: Any, items: List[Tuple[str, Callable]]) -> Any:
    """صف أزرار: [("Text", callback), …]"""
    return _app().buttons(parent, list(items or []))


def statuslabel(parent: Any) -> Any:
    """تسمية حالة صغيرة داخل الصفحة (تُحدَّث بـ .configure(text=…))."""
    return _app().statuslabel(parent)


def set_box(box: Any, text: str) -> None:
    """استبدال محتوى مربع نص بأمان (يفتح/يغلق الحالة تلقائيًا)."""
    _app().set_box(box, str(text))
