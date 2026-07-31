# راهنمای جامع مدیریت ورژن، ساخت آیکون و کامپایل نصب‌کننده (Setup) در چند ساعت؟ (ChandSaat)

این مستند آموزشی برای این طراحی شده است که در آینده به راحتی بتوانید ورژن نرم‌افزار را ارتقا دهید، آیکون‌ها را تغییر دهید و فایل نصب‌کننده استاندارد ویندوز (`Setup.exe`) بسازید.

---

## 💡 علت بروز خطای `[Errno 13] Permission denied` و نحوه حل آن

### علت خطا:
وقتی برنامه‌ای را توسط فایل نصب‌کننده (`Setup.exe`) در پوشه سیستم مانند `C:\Program Files (x86)` نصب می‌کنید، ویندوز به دلایل امنیتی **اجازه نوشتن/تغییر فایل** (مثل دیتابیس SQLite یا فایل اکسل) را در داخل آن پوشه به برنامه‌های معمولی بدون دسترسی Administrator نمی‌دهد.

### راه حل استاندارد در `core/config.py`:
ذخیره‌سازی فایل‌های داده کاربر (`study_log.db` و `settings.json`) را از پوشه اجرای برنامه به پوشه استاندارد داده‌های کاربر در ویندوز یعنی `%LOCALAPPDATA%\ChandSaat` تغییر دادیم:

```python
# core/config.py
if getattr(sys, 'frozen', False):
    # مسیر داده‌های کاربر در ویندوز (نامحدود و بدون نیاز به دسترسی Admin)
    APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "ChandSaat")
    os.makedirs(APP_DATA_DIR, exist_ok=True)
else:
    APP_DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

---

## 📌 ۱. نحوه ارتقا و تغییر شماره ورژن (Versioning)

برای تغییر شماره ورژن (مثلاً ارتقا از `1.1.0` به `1.2.0` یا `2.0.0`)، کافیست ۳ مکان زیر را به‌روزرسانی کنید:

1. **در فایل `core/config.py`**:
   مقدار ثابت `APP_VERSION` را تغییر دهید:
   ```python
   APP_VERSION = "1.2.0"
   ```

2. **در فایل `setup.iss`**:
   خط سوم را به‌روز کنید:
   ```inno
   #define MyAppVersion "1.2.0"
   OutputBaseFilename=ChandSaat_Setup_v1.2.0
   ```

3. **در فایل `make_release.py`**:
   متغیر `VERSION` را تغییر دهید:
   ```python
   VERSION = "1.2.0"
   ```

---

## 🎨 ۲. نحوه تغییر آیکون و لوگوی برنامه

یک فایل تصویر `PNG` یا `JPG` با کیفیت بالا با نام `icon.ico` در پوشه اصلی پروژه بگذارید.
اگر تصویر `PNG` دارید، می‌توانید با اسکریپت زیر در پایتون آن را به `.ico` استاندارد و چندسایزه تبدیل کنید:

```python
from PIL import Image

img = Image.open("logo.png")
img.save("icon.ico", format="ICO", sizes=[(256, 256)])
```

### کجاها آیکون ست شده است؟
- **فایل `ChandSaat.spec`**: آیکون فایل `.exe` اصلی را تعیین می‌کند (`icon='icon.ico'`).
- **فایل `setup.iss`**: آیکون برنامه نصب‌کننده و فایل Uninstaller را تعیین می‌کند (`SetupIconFile=g:\my-daily-log\icon.ico`).

---

## 🚀 ۳. نحوه اجرای خودکار کامپایل و ساخت Setup تنها با ۱ دستور

کافیست در ترمینال دستور زیر را اجرا کنید:

```bash
.\.venv\Scripts\python.exe make_release.py
```

### این اسکریپت به طور اتوماتیک مراحل زیر را انجام می‌دهد:
1. کامپایل کد پایتون به فایل‌های اجرایی نیتیو دسکتاپ با **PyInstaller**.
2. فراخوانی کامپایلر **Inno Setup (`ISCC.exe`)** و ساخت فایل نصب‌کننده ویندوز با ویزارد کامل.
3. ساخت پکیج پورتابل زیپ‌شده.

---

## 📦 ۴. خروجی‌های ساخته‌شده

تمامی خروجی‌ها در پوشه `g:\my-daily-log\installer\` قرار می‌گیرند:

- 💿 **فایل نصب‌کننده ویندوز (پیشنهادی)**: `ChandSaat_Setup_v1.1.0.exe`
- 📦 **نسخه بدون نیاز به نصب (Portable)**: `ChandSaat_v1.1.0_Portable.zip`

---

## 🛠️ ۵. سیاست اصولی تست و انتشار در CI/CD (Best Practice Release Policy)

1. **تست‌های داخلی (Internal Test Builds):**
   - برای گرفتن خروجی‌های تستی (`.apk` یا `.exe`) هرگز نباید `Tag` یا `Release` در گیت‌هاب ایجاد شود.
   - تمامی فایل‌های بیلد تستی باید از طریق **GitHub Actions Artifacts** (`actions/upload-artifact`) آپلود شوند تا مستقیماً از تب Actions قابل دانلود و تست باشند.

2. **انتشار نهایی (Official Release):**
   - فقط زمانی که توسعه و تست‌های یک نسخه (مثلاً `v0.3.0`) به اتمام رسید، تگ اصلی ثبت و ریلیز رسمی گیت‌هاب ایجاد می‌شود.

