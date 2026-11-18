# 🇺🇿 Milliy Sertifikat Hardcore Telegram Bot

Python + aiogram 3 asosida ishlaydigan, ma’lumotlar bazasisiz (RAM/in-memory) test boti.

## Imkoniyatlar
- Matematika, fizika, tarix (O‘zbekiston + jahon), o‘zbek tili.
- BASIC / MIDDLE / ADVANCED darajalari.
- Har testda aynan 45 ta savol.
- Har savol uchun vaqt: `.env` dagi `QUESTION_SECONDS`, lekin kod 30 soniyadan kam qiymatga ruxsat bermaydi.
- Shaxsiy chatda alohida test: `/play`.
- Guruhda birgalikda test: `/group`, ishtirokchilar “Testga qo‘shilish” tugmasini bosadi, testni yaratuvchi boshlaydi.
- Guruh yakunida reyting: avval to‘g‘ri javoblar soni, teng bo‘lsa jami javob berish vaqti kam ishtirokchi yuqori o‘rinda.
- Har savolda javob variantlari aralashtiriladi.
- Ma’lumotlar bazasi yo‘q. Faol testlar faqat bot ishlayotgan paytda RAMda saqlanadi.
- Savollar internetdan yuklanmaydi; offline savol banki ishlaydi.

## Muhim mazmuniy izoh
Savollar milliy sertifikat mavzulariga moslashtirilgan original mashq savollari. Ular UZBMBning rasmiy, maxfiy yoki avvalgi imtihon savollari deb da’vo qilinmaydi. Hozirgi bankda har bir fan uchun 1 200 ta variant (har bir darajada 400 tadan) mavjud. Matematika va fizika savollarining sonli parametrlari avtomatik variantlanadi. Tarix va ona tili banklari esa ichki tekshirilgan fakt/qoidalar to‘plamidan takroriy shakllantiriladi; shu sabab bu ikki fan bo‘yicha “1 200 ta mutlaqo mustaqil ekspert savoli” deb qabul qilmaslik kerak.

## 1. O‘rnatish
Python 3.10 yoki yangiroq versiyasini o‘rnating.

Windows PowerShell:
```powershell
cd milliy_cert_bot
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
```

Linux/macOS:
```bash
cd milliy_cert_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
```

## 2. BotFather token
Telegram’da `@BotFather` ga kiring, `/newbot` yuboring va token oling. `.env` faylida:
```env
BOT_TOKEN=123456789:YOUR_TOKEN
QUESTION_SECONDS=30
ALLOWED_GROUP_IDS=
```
Bot ID alohida kiritilmaydi: Telegram bot ID token ichidan aniqlanadi. Sizga faqat token kerak.

## 3. Ishga tushirish
```bash
python main.py
```
Terminal ochiq turgan bo‘lishi kerak. Botni to‘xtatish: `Ctrl+C`.

## 4. Telegram’da ishlatish
- Shaxsiy test: botga `/start`, so‘ng `/play`.
- Guruh testi: botni guruhga qo‘shing, guruhda `/group` yuboring.
- Guruhda botga xabar yuborish va inline tugmalar ishlashi uchun botni guruhga qo‘shish kifoya. Guruh maxfiyligi (privacy mode) sabab oddiy xabarlarni o‘qishi shart emas; buyruqlar va callback tugmalari ishlaydi.

## 5. Cheklovlar
- Database yo‘q: restart bo‘lsa faol testlar va reytinglar yo‘qoladi.
- Guruhdagi har bir foydalanuvchi javobni inline tugma orqali yuboradi.
- Savolga 30 soniya minimal vaqt. 45 savol uchun umumiy vaqt taxminan 22.5 daqiqa.
- Bir nechta guruh va shaxsiy sessiyalar bir vaqtda ishlashi mumkin.

## 6. Test
Savol bankini tekshirish:
```bash
python question_bank.py
```
