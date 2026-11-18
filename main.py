from __future__ import annotations
import asyncio, html, logging, os, random, time, uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from question_bank import SUBJECTS, make_test

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN', '').strip()
if not TOKEN or 'PASTE_YOUR' in TOKEN:
    raise SystemExit('BOT_TOKEN topilmadi. .env faylini yarating va BotFather tokenini kiriting.')
QUESTION_SECONDS = max(30, int(os.getenv('QUESTION_SECONDS', '30')))
ALLOWED_GROUP_IDS = {int(x.strip()) for x in os.getenv('ALLOWED_GROUP_IDS','').split(',') if x.strip().lstrip('-').isdigit()}
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger('milliy-cert-bot')
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

SUBJECT_LABELS = {'math':'Matematika','physics':'Fizika','history':'Tarix: O‘zbekiston + Jahon','uzbek':'Ona tili (o‘zbek)'}
LEVEL_LABELS = {'basic':'BASIC — murakkab','middle':'MIDDLE — juda qiyin','advanced':'ADVANCED — ekspert darajasi'}
SESSIONS: dict[str, 'Session'] = {}
USER_SESSION: dict[tuple[int,int], str] = {}

@dataclass
class Player:
    user_id: int
    name: str
    score: int = 0
    correct: int = 0
    answered: bool = False
    elapsed: float = 0.0

@dataclass
class Session:
    sid: str
    chat_id: int
    chat_type: str
    subject: str
    level: str
    questions: list[dict[str,Any]]
    players: dict[int,Player] = field(default_factory=dict)
    q_index: int = 0
    started_at: float = 0.0
    question_started: float = 0.0
    message_id: int | None = None
    timer_task: asyncio.Task | None = None
    closed: bool = False
    host_id: int | None = None


def main_menu(group=False):
    rows = [
        [InlineKeyboardButton(text='🧮 Matematika', callback_data='sub:math'), InlineKeyboardButton(text='⚛️ Fizika', callback_data='sub:physics')],
        [InlineKeyboardButton(text='🏛 Tarix', callback_data='sub:history'), InlineKeyboardButton(text='📚 Ona tili', callback_data='sub:uzbek')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def level_menu(subject):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='BASIC (qiyin)', callback_data=f'level:{subject}:basic')],
        [InlineKeyboardButton(text='MIDDLE (juda qiyin)', callback_data=f'level:{subject}:middle')],
        [InlineKeyboardButton(text='ADVANCED (ekspert)', callback_data=f'level:{subject}:advanced')],
    ])

def join_keyboard(sid):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🙋 Testga qo‘shilish', callback_data=f'join:{sid}')], [InlineKeyboardButton(text='🚀 Boshlash', callback_data=f'launch:{sid}')]])

def answer_keyboard(sid, q):
    labels = ['A','B','C','D']
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f'{labels[i]}) {opt}', callback_data=f'ans:{sid}:{i}') ] for i,opt in enumerate(q['options'])])

def safe_name(user):
    return html.escape((user.full_name or user.username or f'User {user.id}')[:50])

async def tell(message: Message, text: str, **kwargs):
    await message.answer(text, **kwargs)

@dp.message(CommandStart())
async def start(message: Message):
    txt = ('<b>🇺🇿 MILLIY SERTIFIKAT — HARDCORE TEST BOT</b>\n\n'
           '4 fan • 3 daraja • har testda 45 ta savol • har savolga kamida 30 soniya.\n\n'
           '<b>Shaxsiy test:</b> botga shaxsiy chatda /play yuboring.\n'
           '<b>Guruh testi:</b> guruhda /group yuboring, ishtirokchilar qo‘shiladi va boshlovchi ishga tushiradi.\n'
           '<b>Buyruqlar:</b> /help — yo‘riqnoma, /subjects — fanlar.')
    await tell(message, txt, reply_markup=main_menu())

@dp.message(Command('help'))
async def help_cmd(message: Message):
    await tell(message, '<b>Yo‘riqnoma</b>\n/play — shaxsiy test (faqat bot bilan private chatda).\n/group — guruh testini yaratish.\n/subjects — fan tanlash.\n/cancel — o‘zingiz qatnashayotgan testdan chiqish.\n\nGuruhda avval /group, keyin fan va darajani tanlang. Boshqalar “Testga qo‘shilish” tugmasini bosadi. Boshlovchi “Boshlash”ni bosadi. Yakunda reyting: ball, so‘ng tezlik bo‘yicha.')

@dp.message(Command('subjects'))
async def subjects(message: Message):
    await tell(message, '<b>Fan tanlang:</b>', reply_markup=main_menu())

@dp.message(Command('play'))
async def play(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        await tell(message, 'Shaxsiy test uchun botga private chatda /play yuboring. Guruhda /group buyrug‘idan foydalaning.')
        return
    await tell(message, '<b>Shaxsiy test uchun fanni tanlang:</b>', reply_markup=main_menu())

@dp.message(Command('group'))
async def group_start(message: Message):
    if message.chat.type == ChatType.PRIVATE:
        await tell(message, 'Guruh rejimi uchun botni guruhga qo‘shing va guruh ichida /group yuboring.')
        return
    if ALLOWED_GROUP_IDS and message.chat.id not in ALLOWED_GROUP_IDS:
        await tell(message, 'Bu guruh bot ruxsat etilgan ro‘yxatida emas.')
        return
    await tell(message, '<b>Guruh testini sozlash — fan tanlang:</b>', reply_markup=main_menu())

@dp.message(Command('cancel'))
async def cancel(message: Message):
    key=(message.chat.id,message.from_user.id)
    sid=USER_SESSION.pop(key,None)
    if sid and sid in SESSIONS:
        s=SESSIONS[sid]
        s.players.pop(message.from_user.id,None)
        await tell(message,'Testdan chiqdingiz.')
    else:
        await tell(message,'Siz faol testda emassiz.')

@dp.callback_query(F.data.startswith('sub:'))
async def choose_subject(call: CallbackQuery):
    subject=call.data.split(':',1)[1]
    if subject not in SUBJECT_LABELS: return await call.answer('Noto‘g‘ri fan',show_alert=True)
    if call.message.chat.type == ChatType.PRIVATE:
        await call.message.edit_text(f'<b>{SUBJECT_LABELS[subject]}</b>\nDarajani tanlang:',reply_markup=level_menu(subject))
    else:
        # Store pending configuration per chat; no database, memory only.
        PENDING[call.message.chat.id]={'subject':subject,'host':call.from_user.id}
        await call.message.edit_text(f'<b>{SUBJECT_LABELS[subject]}</b>\nDarajani tanlang:',reply_markup=level_menu(subject))
    await call.answer()

PENDING: dict[int,dict[str,Any]]={}

@dp.callback_query(F.data.startswith('level:'))
async def choose_level(call: CallbackQuery):
    _,subject,level=call.data.split(':')
    if call.message.chat.type == ChatType.PRIVATE:
        await call.answer('45 savol tayyorlanmoqda…')
        await create_private_session(call.message.chat.id,call.from_user,subject,level,call.message)
    else:
        cfg=PENDING.get(call.message.chat.id)
        if not cfg or cfg.get('host') != call.from_user.id:
            return await call.answer('Test sozlamasini faqat boshlovchi tanlaydi.',show_alert=True)
        sid=uuid.uuid4().hex[:8]
        questions=make_test(subject,level,45)
        s=Session(sid,call.message.chat.id,'group',subject,level,questions,host_id=call.from_user.id)
        SESSIONS[sid]=s
        await call.message.edit_text(f'<b>🏆 Guruh testi ochildi!</b>\nFan: {SUBJECT_LABELS[subject]}\nDaraja: {LEVEL_LABELS[level]}\nSavollar: 45 ta\nHar savol: {QUESTION_SECONDS} soniya\n\nIshtirokchilar tugmani bosib qo‘shilsin. Kamida 1 ishtirokchi bo‘lgach, boshlovchi boshlaydi.',reply_markup=join_keyboard(sid))
        PENDING.pop(call.message.chat.id,None)
        await call.answer('Guruh testi yaratildi')

async def create_private_session(chat_id,user,subject,level,origin_message):
    sid=uuid.uuid4().hex[:8]
    s=Session(sid,chat_id,'private',subject,level,make_test(subject,level,45),host_id=user.id)
    s.players[user.id]=Player(user.id,safe_name(user))
    SESSIONS[sid]=s; USER_SESSION[(chat_id,user.id)]=sid
    await origin_message.answer(f'<b>🎯 Shaxsiy test boshlandi!</b>\n{SUBJECT_LABELS[subject]} • {LEVEL_LABELS[level]}\n45 savol • {QUESTION_SECONDS} soniya/savol\n\nTayyorlaning!')
    await send_question(s)

@dp.callback_query(F.data.startswith('join:'))
async def join(call: CallbackQuery):
    sid=call.data.split(':',1)[1]; s=SESSIONS.get(sid)
    if not s or s.closed: return await call.answer('Bu test faol emas.',show_alert=True)
    if s.started_at: return await call.answer('Test allaqachon boshlangan.',show_alert=True)
    if call.from_user.id not in s.players:
        s.players[call.from_user.id]=Player(call.from_user.id,safe_name(call.from_user))
        USER_SESSION[(s.chat_id,call.from_user.id)]=sid
    await call.answer('Testga qo‘shildingiz!')
    names='\n'.join(f'• {p.name}' for p in s.players.values())
    try: await call.message.edit_text(f'<b>🏆 Guruh testi</b>\nFan: {SUBJECT_LABELS[s.subject]}\nDaraja: {LEVEL_LABELS[s.level]}\nIshtirokchilar ({len(s.players)}):\n{names}\n\nBoshlovchi testni boshlashi mumkin.',reply_markup=join_keyboard(sid))
    except Exception: pass

@dp.callback_query(F.data.startswith('launch:'))
async def launch(call: CallbackQuery):
    sid=call.data.split(':',1)[1]; s=SESSIONS.get(sid)
    if not s or s.closed: return await call.answer('Test topilmadi.',show_alert=True)
    if call.from_user.id != s.host_id: return await call.answer('Faqat testni yaratgan boshlovchi boshlashi mumkin.',show_alert=True)
    if not s.players: return await call.answer('Avval ishtirokchilar qo‘shilsin.',show_alert=True)
    if s.started_at: return await call.answer('Test boshlangan.',show_alert=True)
    s.started_at=time.monotonic(); await call.answer('Test boshlandi!')
    await send_question(s)

async def send_question(s: Session):
    if s.closed: return
    if s.q_index >= len(s.questions):
        await finish_session(s); return
    q=s.questions[s.q_index]
    s.question_started=time.monotonic()
    for p in s.players.values(): p.answered=False
    header=f'<b>❓ {s.q_index+1}/45</b>  |  {SUBJECT_LABELS[s.subject]}\n<b>{LEVEL_LABELS[s.level]}</b>\n⏳ {QUESTION_SECONDS} soniya\n\n'
    body=header+html.escape(q['question'])+'\n\n'+ '\n'.join(f'<b>{"ABCD"[i]}.</b> {html.escape(o)}' for i,o in enumerate(q['options']))
    markup=answer_keyboard(s.sid,q)
    if s.chat_type=='private':
        msg=await bot.send_message(s.chat_id,body,reply_markup=markup)
    else:
        msg=await bot.send_message(s.chat_id,body,reply_markup=markup)
    s.message_id=msg.message_id
    if s.timer_task and not s.timer_task.done(): s.timer_task.cancel()
    s.timer_task=asyncio.create_task(question_timeout(s.sid,s.q_index))

async def question_timeout(sid,index):
    try:
        await asyncio.sleep(QUESTION_SECONDS)
        s=SESSIONS.get(sid)
        if not s or s.closed or s.q_index!=index: return
        q=s.questions[index]
        try: await bot.edit_message_reply_markup(s.chat_id,s.message_id,reply_markup=None)
        except Exception: pass
        # Private: show answer/explanation; group: do not expose individual answers before the round closes.
        await bot.send_message(s.chat_id,f'⏰ <b>Vaqt tugadi!</b> To‘g‘ri javob: <b>{"ABCD"[q["answer"]]}) {html.escape(q["options"][q["answer"]])}</b>\n{html.escape(q.get("explanation",""))}')
        s.q_index+=1
        await send_question(s)
    except asyncio.CancelledError: return
    except Exception: log.exception('Timer error')

@dp.callback_query(F.data.startswith('ans:'))
async def answer(call: CallbackQuery):
    _,sid,raw=call.data.split(':'); s=SESSIONS.get(sid)
    if not s or s.closed: return await call.answer('Test yakunlangan.',show_alert=True)
    p=s.players.get(call.from_user.id)
    if not p: return await call.answer('Bu test ishtirokchisi emassiz. Guruhda “Qo‘shilish”ni bosing.',show_alert=True)
    if p.answered: return await call.answer('Bu savolga javob bergansiz.')
    if s.q_index>=45: return await call.answer('Test tugagan.')
    choice=int(raw); q=s.questions[s.q_index]
    p.answered=True
    elapsed=max(0.0,time.monotonic()-s.question_started)
    p.elapsed+=elapsed
    correct=(choice==q['answer'])
    if correct:
        p.correct+=1
        # Faster correct responses earn a tiny tie-break bonus, while ranking still prioritizes correct count.
        p.score+=100
    await call.answer('✅ To‘g‘ri!' if correct else '❌ Noto‘g‘ri',show_alert=False)
    if s.chat_type=='private':
        try: await call.message.edit_reply_markup(reply_markup=None)
        except Exception: pass
        feedback=('✅ To‘g‘ri!' if correct else f'❌ Noto‘g‘ri. To‘g‘ri javob: {"ABCD"[q["answer"]]}')
        await call.message.answer(f'{feedback}\n{html.escape(q.get("explanation",""))}')
        if s.timer_task and not s.timer_task.done(): s.timer_task.cancel()
        s.q_index+=1
        await send_question(s)
    else:
        # Group round ends once every active participant has answered; otherwise timer closes it.
        if all(x.answered for x in s.players.values()):
            if s.timer_task and not s.timer_task.done(): s.timer_task.cancel()
            try: await call.message.edit_reply_markup(reply_markup=None)
            except Exception: pass
            await bot.send_message(s.chat_id,f'📌 <b>{s.q_index+1}-savol yakunlandi.</b> Barcha ishtirokchilar javob berdi.')
            s.q_index+=1
            await send_question(s)

async def finish_session(s):
    if s.closed: return
    s.closed=True
    if s.timer_task and not s.timer_task.done(): s.timer_task.cancel()
    for uid in list(s.players): USER_SESSION.pop((s.chat_id,uid),None)
    ranked=sorted(s.players.values(),key=lambda p:(-p.correct,p.elapsed))
    lines=[f'<b>🏆 TEST YAKUNLANDI — YAKUNIY REYTING</b>',f'Fan: {SUBJECT_LABELS[s.subject]}',f'Daraja: {LEVEL_LABELS[s.level]}','']
    for i,p in enumerate(ranked,1):
        medal='🥇' if i==1 else '🥈' if i==2 else '🥉' if i==3 else f'{i}.'
        lines.append(f'{medal} <b>{p.name}</b> — {p.correct}/45 ({p.correct*100/45:.1f}%) | {p.elapsed:.1f} soniya')
    lines+=['','<i>Tartiblash: avval to‘g‘ri javoblar soni, teng bo‘lsa umumiy javob berish vaqti kam bo‘lgan ishtirokchi yuqorida.</i>']
    await bot.send_message(s.chat_id,'\n'.join(lines))
    SESSIONS.pop(s.sid,None)

async def on_shutdown():
    for s in SESSIONS.values():
        if s.timer_task and not s.timer_task.done(): s.timer_task.cancel()

async def main():
    log.info('Milliy sertifikat bot ishga tushmoqda…')
    await dp.start_polling(bot, close_bot_session=True)

if __name__=='__main__':
    try: asyncio.run(main())
    except (KeyboardInterrupt,SystemExit): pass
