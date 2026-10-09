#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick Benchmark — إضافة نموذجية لـ Ultimate Toolbox Pro v4.2.

قياس سريع لسرعة المعالج (هاش SHA-256) وعمليات الذاكرة، مع تنفيذ
غير متزامن عبر run_async + تحديثات لحظية آمنة عبر ui() وإمكانية
الإيقاف عبر stop_event(). يوضّح النمط الصحيح للخيوط في الإضافات.
"""
import hashlib
import os
import sys
import time

from toolbox_api import (register_tool, card, buttons, statuslabel, toast,
                         run_async, ui, stop_event, t, add_translations,
                         is_rtl)
import customtkinter as ctk

add_translations({
    "ar": {"Quick Benchmark": "قياس سريع",
           "Run benchmark": "ابدأ القياس", "Stop": "إيقاف",
           "Measures single-core hashing speed — by a plugin":
               "يقيس سرعة الهاش أحادي النواة — عبر إضافة",
           "Ready": "جاهز", "Benchmark stopped": "أُلغي القياس",
           "CPU hash speed": "سرعة هاش المعالج",
           "1MB blocks hashed in {sec}s": "كتل 1MB خلال {sec} ثانية"},
    "zh": {"Quick Benchmark": "快速基准测试", "Run benchmark": "开始测试",
           "Stop": "停止",
           "Measures single-core hashing speed — by a plugin":
               "测量单核哈希速度——由插件提供",
           "Ready": "就绪", "Benchmark stopped": "测试已停止",
           "CPU hash speed": "CPU 哈希速度",
           "1MB blocks hashed in {sec}s": "{sec} 秒内哈希的 1MB 块"},
    "es": {"Quick Benchmark": "Prueba rápida", "Run benchmark": "Iniciar",
           "Stop": "Detener",
           "Measures single-core hashing speed — by a plugin":
               "Mide velocidad de hash de un núcleo — por un complemento",
           "Ready": "Listo", "Benchmark stopped": "Prueba detenida",
           "CPU hash speed": "Velocidad de hash CPU",
           "1MB blocks hashed in {sec}s": "bloques de 1MB en {sec}s"},
    "fr": {"Quick Benchmark": "Test rapide", "Run benchmark": "Démarrer",
           "Stop": "Arrêter",
           "Measures single-core hashing speed — by a plugin":
               "Mesure la vitesse de hachage mono-cœur — par une extension",
           "Ready": "Prêt", "Benchmark stopped": "Test arrêté",
           "CPU hash speed": "Vitesse de hachage CPU",
           "1MB blocks hashed in {sec}s": "blocs de 1Mo en {sec}s"},
    "ru": {"Quick Benchmark": "Быстрый тест", "Run benchmark": "Запустить",
           "Stop": "Остановить",
           "Measures single-core hashing speed — by a plugin":
               "Измеряет скорость хеширования одного ядра — плагин",
           "Ready": "Готово", "Benchmark stopped": "Тест остановлен",
           "CPU hash speed": "Скорость хеширования CPU",
           "1MB blocks hashed in {sec}s": "блоков 1МБ за {sec}с"},
    "pt": {"Quick Benchmark": "Teste rápido", "Run benchmark": "Iniciar",
           "Stop": "Parar",
           "Measures single-core hashing speed — by a plugin":
               "Mede velocidade de hash de um núcleo — por um plugin",
           "Ready": "Pronto", "Benchmark stopped": "Teste parado",
           "CPU hash speed": "Velocidade de hash da CPU",
           "1MB blocks hashed in {sec}s": "blocos de 1MB em {sec}s"},
    "hi": {"Quick Benchmark": "त्वरित बेंचमार्क", "Run benchmark": "शुरू करें",
           "Stop": "रोकें",
           "Measures single-core hashing speed — by a plugin":
               "सिंगल-कोर हैशिंग गति मापता है — प्लगइन द्वारा",
           "Ready": "तैयार", "Benchmark stopped": "बेंचमार्क रोका गया",
           "CPU hash speed": "CPU हैश गति",
           "1MB blocks hashed in {sec}s": "{sec}s में 1MB ब्लॉक"},
    "bn": {"Quick Benchmark": "দ্রুত বেঞ্চমার্ক", "Run benchmark": "শুরু করুন",
           "Stop": "থামান",
           "Measures single-core hashing speed — by a plugin":
               "সিঙ্গেল-কোর হ্যাশিং গতি মাপে — প্লাগইন দ্বারা",
           "Ready": "প্রস্তুত", "Benchmark stopped": "বেঞ্চমার্ক থামানো হয়েছে",
           "CPU hash speed": "CPU হ্যাশ গতি",
           "1MB blocks hashed in {sec}s": "{sec}s-এ 1MB ব্লক"},
    "ur": {"Quick Benchmark": "فوری بینچ مارک", "Run benchmark": "شروع کریں",
           "Stop": "روکیں",
           "Measures single-core hashing speed — by a plugin":
               "سنگل کور ہیشنگ اسپیڈ ناپتا ہے — پلگ ان کی طرف سے",
           "Ready": "تیار", "Benchmark stopped": "بینچ مارک روک دیا گیا",
           "CPU hash speed": "CPU ہیش اسپیڈ",
           "1MB blocks hashed in {sec}s": "{sec} سیکنڈ میں 1MB بلاکس"},
})

_BLOCK = 1 << 20          # 1MB
_ROUNDS = 4               # مجموعًا ~2-3 ثوانٍ على الأجهزة الحديثة


# ── دالة نقية قابلة للاختبار (تعمل أيضًا بلا واجهة) ─────────────────
def bench_cpu(rounds: int = _ROUNDS, stop=None, on_progress=None) -> float:
    """يرجع MB/s لسرعة هاش SHA-256 أحادي النواة."""
    data = os.urandom(_BLOCK)
    total = 0
    t0 = time.perf_counter()
    for i in range(rounds):
        if stop is not None and stop.is_set():
            break
        h = hashlib.sha256()
        for _ in range(3):                # 3MB في كل جولة
            h.update(data)
        total += 3 * _BLOCK
        if on_progress is not None:
            on_progress(i + 1, rounds)
    dt = time.perf_counter() - t0
    return (total / dt / (1 << 20)) if dt > 0 else 0.0


@register_tool(tid="quickbench", title="Quick Benchmark", section="Plugins",
               icon="⚡", keywords="benchmark cpu speed hash performance test")
def build(api, parent):
    c = card(parent, t("Measures single-core hashing speed — by a plugin"))
    ctk.CTkLabel(
        c, justify="left",
        text=("• SHA-256  •  1MB × 12 (4 rounds × 3)\n"
              "• Single thread\n"
              f"• Python {sys.version.split()[0]}"),
        text_color="#9a9aa8").pack(
        anchor="e" if is_rtl() else "w", padx=14, pady=(0, 8))

    status = statuslabel(parent)
    status.configure(text=t("Ready"))

    ev_key = "quickbench_stop"

    def work():
        stop = stop_event(ev_key)
        stop.clear()

        def prog(i, n):
            ui(lambda i=i, n=n: status.configure(text=f"⏳ {i}/{n}"))
        mbps = bench_cpu(stop=stop, on_progress=prog)
        return ("stopped" if stop.is_set() else "ok", mbps)

    def done(res):
        kind, mbps = res
        if kind == "stopped":
            status.configure(text=t("Benchmark stopped"))
        else:
            status.configure(text=f"⚡ {t('CPU hash speed')}: {mbps:,.0f} MB/s")
            toast(f"⚡ {mbps:,.0f} MB/s", "ok")

    buttons(parent, [(t("Run benchmark"), lambda: run_async(work, done=done)),
                     (t("Stop"), lambda: stop_event(ev_key).set())])
