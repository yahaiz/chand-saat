# ⏱️ چند ساعت؟ (ChandSaat) - نسخه 0.1.0

<div align="center">

![ChandSaat Logo](icon.png)

**نرم‌افزار مدیریت، ثبت و تحلیل ساعات مطالعه روزانه و تست‌زنی دسکتاپ**

[![Build Status](https://github.com/yahaiz/chand-saat/actions/workflows/build.yml/badge.svg)](https://github.com/yahaiz/chand-saat/actions)
[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com)
[![PyWebView](https://img.shields.io/badge/UI-PyWebView-indigo.svg)](https://pywebview.flowrl.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📖 معرفی برنامه

**«چند ساعت؟» (ChandSaat)** یک نرم‌افزار دسکتاپ کاربردی جهت ثبت، خلاصه‌سازی و تحلیل ساعات مطالعه و تعداد تست‌های روزانه برای داوطلبان آزمون‌ها و دانشجویان است. این برنامه با تلفیق FastAPI، SQLite و پنجره نیتیو PyWebView، رابط کاربری سریع و مستقلی بدون نیاز به مرورگر خارجی ارائه می‌دهد.

> 🤖 **نکته توسعه (Vibe Coding):** این پروژه با استفاده از هوش مصنوعی (AI-Assisted / Vibe Coding) پیاده‌سازی شده و ساختار کدهای آن بر پایه معماری ماژولار و پایدار توسعه یافته است.

---

## ✨ امکانات اصلی

- ⏱️ **تایمر پومودورو (Pomodoro Timer):** زمان‌بندی جلسات مطالعه و استراحت.
- 📊 **تحلیل آمار روزانه:** محاسبه میزان پیشرفت ساعات مطالعه و تست‌ها.
- 🗄️ **پایگاه داده SQLite:** ذخیره‌سازی داده‌ها به همراه انتقال خودکار داده‌های اکسل قبلی.
- 📥 **خروجی اکسل (Excel Export):** دریافت فایل اکسل از سوابق ثبت‌شده.
- 🖥️ **رابط کاربری دسکتاپ:** پنجره نیتیو دسکتاپ با پشتیبانی از High-DPI و کنترل‌های اختصاصی.

---

## 🛠️ تکنولوژی‌ها

- **فرانت‌اند:** Vanilla CSS3, TailwindCSS, Vazirmatn Font
- **بک‌اند:** FastAPI, Uvicorn, SQLite3
- **دسکتاپ:** PyWebView, Tkinter (Splash Screen)
- **کامپایل و CI/CD:** PyInstaller, Inno Setup, GitHub Actions

---

## 🏛️ ساختار پروژه

```
chand-saat/
│── core/            # تنظیمات متمرکز و لاگر
│── database/        # دیتابیس SQLite و لایه داده
│── services/        # مدیریت تنظیمات برنامه
│── routes/          # اندپکیک‌های FastAPI
│── ui/              # مدیریت پنجره و اسپلش اسکرین
│── static/          # استایل‌های CSS
│── templates/       # قالب‌های HTML
│── tests/           # تست‌های خودکار Pytest
│── .github/         # گردش‌کار GitHub Actions
│── main.py          # نقطه ورود اصلی
│── make_release.py  # اسکریپت کامپایل ریلیز
│── ChandSaat.spec   # پیکربندی PyInstaller
│── setup.iss        # پیکربندی Inno Setup
```

---

## 🚀 راهنمای نصب و اجرا

### پیش‌نیازها
- پایتون نسخه 3.10 یا بالاتر

### اجرا از سورس‌کد
```bash
# 1. دریافت پروژه
git clone https://github.com/yahaiz/chand-saat.git
cd chand-saat

# 2. ایجاد و فعال‌سازی محیط مجازی
python -m venv .venv
.\.venv\Scripts\activate

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. اجرای برنامه
python main.py
```

### ساخت نسخه اجرایی (Setup & Portable)
```bash
python make_release.py
```

---

## 📄 لایسنس

این پروژه تحت لایسنس [MIT](LICENSE) منتشر شده است.
