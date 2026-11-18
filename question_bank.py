"""Deterministic, offline question factory. 1,200 original practice variants per subject.
Questions are practice material aligned to national-certificate subject areas, not copied official exam items.
"""
from __future__ import annotations
import random

SUBJECTS = {
 'math': 'Matematika', 'physics': 'Fizika', 'history': 'Tarix', 'uzbek': 'Ona tili'
}

# Carefully checked fact bank for chronology / people / events.
HISTORY = [
 ('Teshiktosh g‘oridan topilgan mashhur topilma qaysi davrga mansub?', 'Neandertal bola qoldiqlari', ['Bronza davri sopol idishlari','Temir davri yozuvi','Neandertal bola qoldiqlari','Kushon tangalari']),
 ('Zarautsoy qoyatosh rasmlari asosan qaysi faoliyat manzaralarini aks ettiradi?', 'Ovchilik', ['Dengiz savdosi','Ovchilik','Temir yo‘l qurilishi','Shahar hunarmandchiligi']),
 ('Avesto qaysi diniy ta’limotning muqaddas manbasi hisoblanadi?', 'Zardushtiylik', ['Buddaviylik','Moniylik','Zardushtiylik','Konfutsiylik']),
 ('Qadimgi Davan davlati qaysi hudud bilan bog‘liq?', 'Farg‘ona vodiysi', ['Zarafshon vodiysi','Farg‘ona vodiysi','Quyi Amudaryo deltasi','Surxon vohasi']),
 ('Qang‘ davlati asosan qaysi daryo havzasi bilan bog‘liq bo‘lgan?', 'Sirdaryo', ['Nil','Sirdaryo','Dajla','Gang']),
 ('Kushon davlatining yuksalishi qaysi hukmdor nomi bilan ko‘proq bog‘lanadi?', 'Kanishka', ['Doro I','Kanishka','Kir II','Attila']),
 ('Turk xoqonligi qachon tashkil topgan?', 'VI asr o‘rtalarida', ['Miloddan avvalgi III asrda','VI asr o‘rtalarida','IX asr oxirida','XIII asr boshida']),
 ('Arablarning Movarounnahrga yurishlari qaysi sarkarda nomi bilan bog‘liq?', 'Qutayba ibn Muslim', ['Amr ibn Os','Qutayba ibn Muslim','Xolid ibn Valid','Tariq ibn Ziyod']),
 ('Muqanna qo‘zg‘oloni qaysi xalifalik davrida yuz bergan?', 'Abbosiylar', ['Umaviylar','Abbosiylar','Fotimiylar','Usmoniylar']),
 ('Somoniylar davlatining poytaxti qaysi shahar edi?', 'Buxoro', ['Samarqand','Buxoro','Urganch','Toshkent']),
 ('Qoraxoniylar hukmronligi davrida yozilgan “Qutadg‘u bilig” muallifi kim?', 'Yusuf Xos Hojib', ['Mahmud Koshg‘ariy','Yusuf Xos Hojib','Ahmad Yassaviy','Rabg‘uziy']),
 ('“Devonu lug‘otit turk” asarining muallifi kim?', 'Mahmud Koshg‘ariy', ['Yusuf Xos Hojib','Mahmud Koshg‘ariy','Ahmad Yugnakiy','Alisher Navoiy']),
 ('Jaloliddin Manguberdi qaysi davlatning so‘nggi hukmdori sifatida tanilgan?', 'Xorazmshohlar davlati', ['Somoniylar davlati','Xorazmshohlar davlati','Qoraxoniylar davlati','G‘aznaviylar davlati']),
 ('Amir Temur markazlashgan davlatining poytaxti qaysi shahar bo‘lgan?', 'Samarqand', ['Buxoro','Samarqand','Xiva','Toshkent']),
 ('Mirzo Ulug‘bek rasadxonasi qaysi shaharda bunyod etilgan?', 'Samarqand', ['Buxoro','Samarqand','Hirot','Termiz']),
 ('“Boburnoma” asari muallifi kim?', 'Zahiriddin Muhammad Bobur', ['Alisher Navoiy','Zahiriddin Muhammad Bobur','Husayn Boyqaro','Abdullaxon II']),
 ('Shayboniyxon Movarounnahrda qaysi sulola hukmronligiga asos solgan?', 'Shayboniylar', ['Ashtarxoniylar','Shayboniylar','Mang‘itlar','Qo‘ng‘irotlar']),
 ('Buxoro amirligida Mang‘itlar sulolasi qaysi maqom bilan hukmronlik qilgan?', 'Amirlik', ['Xoqonlik','Amirlik','Respublika','Mustamlaka gubernatorligi']),
 ('Qo‘qon xonligida hukmronlik qilgan sulola qaysi?', 'Minglar', ['Mang‘itlar','Minglar','Shayboniylar','Qo‘ng‘irotlar']),
 ('Turkiston general-gubernatorligi qaysi imperiya tomonidan tashkil etilgan?', 'Rossiya imperiyasi', ['Britaniya imperiyasi','Rossiya imperiyasi','Usmonli imperiyasi','Fransiya imperiyasi']),
 ('1898-yil Andijon qo‘zg‘oloni rahbari kim edi?', 'Dukchi Eshon', ['Po‘latxon','Dukchi Eshon','Madali eshon','Junaidxon']),
 ('Turkiston Muxtoriyati 1917-yilda qaysi shaharda e’lon qilingan?', 'Qo‘qon', ['Toshkent','Qo‘qon','Buxoro','Samarqand']),
 ('O‘zbekiston SSR qachon tashkil topgan?', '1924-yilda', ['1918-yilda','1924-yilda','1936-yilda','1991-yilda']),
 ('O‘zbekiston davlat mustaqilligi qaysi sanada e’lon qilingan?', '1991-yil 31-avgust', ['1990-yil 20-iyun','1991-yil 31-avgust','1991-yil 1-sentabr','1992-yil 8-dekabr']),
 ('O‘zbekiston Respublikasi Konstitutsiyasi ilk bor qachon qabul qilingan?', '1992-yil 8-dekabr', ['1991-yil 31-avgust','1992-yil 8-dekabr','1993-yil 2-mart','1995-yil 24-aprel']),
 ('Buyuk fransuz inqilobi qaysi yilda boshlangan?', '1789-yilda', ['1640-yilda','1776-yilda','1789-yilda','1848-yilda']),
 ('AQSH Mustaqillik deklaratsiyasi qachon qabul qilingan?', '1776-yil 4-iyul', ['1775-yil 19-aprel','1776-yil 4-iyul','1783-yil 3-sentabr','1787-yil 17-sentabr']),
 ('G‘arbiy Rim imperiyasi qaysi yilda qulagan deb qabul qilinadi?', '476-yilda', ['395-yilda','410-yilda','476-yilda','527-yilda']),
 ('Konstantinopolni Usmonli turklar qaysi yilda egallagan?', '1453-yilda', ['1204-yilda','1389-yilda','1453-yilda','1492-yilda']),
 ('Birinchi jahon urushi qaysi yillarda davom etgan?', '1914–1918-yillarda', ['1904–1905-yillarda','1914–1918-yillarda','1917–1922-yillarda','1939–1945-yillarda']),
 ('Versal tinchlik shartnomasi Germaniya bilan qachon imzolangan?', '1919-yil 28-iyun', ['1918-yil 11-noyabr','1919-yil 28-iyun','1920-yil 10-yanvar','1922-yil 16-aprel']),
 ('Ikkinchi jahon urushi Yevropada qaysi voqea bilan boshlangan?', 'Germaniyaning Polshaga bostirib kirishi', ['Pearl-Harbor hujumi','Germaniyaning Polshaga bostirib kirishi','Fransiyaning Reyn hududiga kirishi','Barbarossa rejasi']),
 ('BMT qachon rasman tashkil topgan?', '1945-yil 24-oktabr', ['1919-yil 10-yanvar','1945-yil 24-oktabr','1946-yil 1-yanvar','1949-yil 4-aprel']),
 ('NATO qaysi yilda tashkil etilgan?', '1949-yilda', ['1945-yilda','1947-yilda','1949-yilda','1955-yilda']),
 ('Berlin devori qaysi yilda qulagan?', '1989-yilda', ['1961-yilda','1975-yilda','1989-yilda','1991-yilda']),
 ('Hindiston mustaqillikka qaysi yilda erishgan?', '1947-yilda', ['1935-yilda','1945-yilda','1947-yilda','1950-yilda']),
 ('Xitoy Xalq Respublikasi qachon e’lon qilingan?', '1949-yil 1-oktabr', ['1911-yil 10-oktabr','1921-yil 1-iyul','1949-yil 1-oktabr','1950-yil 25-iyun']),
 ('Meydzi islohotlari qaysi davlat tarixiga tegishli?', 'Yaponiya', ['Xitoy','Yaponiya','Koreya','Tailand']),
 ('Sanoat inqilobi dastlab qaysi mamlakatda boshlangan?', 'Buyuk Britaniya', ['Fransiya','Germaniya','Buyuk Britaniya','AQSH']),
 ('Qadimgi demokratiya taraqqiyotining muhim markazi qaysi polis edi?', 'Afina', ['Sparta','Afina','Korinf','Milet']),
 ('Spartak qo‘zg‘oloni qaysi davlat tarixiga tegishli?', 'Qadimgi Rim', ['Qadimgi Misr','Qadimgi Rim','Qadimgi Yunoniston','Makedoniya']),
]

UZBEK = [
 ('“Ko‘nglimda bahor uyg‘ondi” gapida “bahor” so‘zi qanday ma’noda qo‘llangan?', 'Ko‘chma ma’noda', ['Atash ma’nosida','Ko‘chma ma’noda','Termin ma’nosida','Omonim ma’noda']),
 ('Qaysi qatorda paronimlar berilgan?', 'asr — asir', ['katta — ulkan','asr — asir','oq — qora','yuz — bet']),
 ('“Ko‘zi ochildi” iborasi qanday birlik?', 'Frazeologik birlik', ['Erkin birikma','Frazeologik birlik','Qo‘shma so‘z','Atama']),
 ('“Kitobxonlik” so‘zida so‘z yasovchi qo‘shimcha qaysi?', '-xon va -lik', ['-ob','-xon va -lik','-ni','-lar']),
 ('Qaysi so‘z yasama sifat hisoblanadi?', 'serhosil', ['oq','serhosil','uchinchi','tez']),
 ('“Ular ertaga kelishadi” gapidagi fe’l qaysi zamonda?', 'Kelasi zamon', ['O‘tgan zamon','Hozirgi zamon','Kelasi zamon','Shart mayli']),
 ('“Yozilgan xat” birikmasidagi “yozilgan” fe’lning qaysi vazifadosh shakli?', 'Sifatdosh', ['Ravishdosh','Harakat nomi','Sifatdosh','Sof fe’l']),
 ('“Kulib gapirdi” birikmasidagi “kulib” qaysi shakl?', 'Ravishdosh', ['Sifatdosh','Ravishdosh','Harakat nomi','Buyruq mayli']),
 ('“O‘qish — tafakkur mashqi” gapida “o‘qish” qanday shakl?', 'Harakat nomi', ['Sifatdosh','Ravishdosh','Harakat nomi','Ko‘makchi fe’l']),
 ('“Men kitobni ukamga berdim” gapida “ukamga” qaysi gap bo‘lagi?', 'Vositali to‘ldiruvchi', ['Ega','Vositasiz to‘ldiruvchi','Vositali to‘ldiruvchi','Hol']),
 ('“Kecha maktabga bordik” gapida “kecha” qaysi gap bo‘lagi?', 'Payt holi', ['O‘rin holi','Payt holi','Sabab holi','Aniqlovchi']),
 ('“Afsuski, u kechikdi” gapidagi “afsuski” qanday birlik?', 'Kirish so‘z', ['Undalma','Kirish so‘z','Yuklama','Bog‘lovchi']),
 ('“Aziz do‘stim, xatingni oldim” gapida “aziz do‘stim” nima?', 'Undalma', ['Ega','Undalma','Aniqlovchi','Kirish so‘z']),
 ('Qaysi qatorda bog‘langan qo‘shma gap berilgan?', 'Quyosh botdi va atrof qorong‘ilashdi.', ['Quyosh botgach, atrof qorong‘ilashdi.','Quyosh botdi va atrof qorong‘ilashdi.','Quyosh botgani uchun atrof qorong‘ilashdi.','Quyosh botsa, atrof qorong‘ilashadi.']),
 ('“Kim mehnat qilsa, u rohat ko‘radi” qanday qo‘shma gap?', 'Ergashgan qo‘shma gap', ['Bog‘langan qo‘shma gap','Ergashgan qo‘shma gap','Bog‘lovchisiz qo‘shma gap','Sodda gap']),
 ('Qaysi gapda tire ega va kesim orasida qo‘yilgan?', 'Bilim — eng katta boylik.', ['Men bugun keldim.','Bilim — eng katta boylik.','U kitobni o‘qidi.','Bahor keldi, gullar ochildi.']),
 ('Qaysi so‘zda tovush tushishi yuz bergan?', 'og‘iz + im → og‘zim', ['sana + oq → sanoq','og‘iz + im → og‘zim','yurak + i → yuragi','ong + la → angla']),
 ('Qaysi qatorda faqat jarangsiz undoshlar berilgan?', 'p, t, k, q, s, f', ['b, d, g, z','p, t, k, q, s, f','m, n, l, r','v, z, j, g‘']),
 ('“O‘n beshta” soni ma’no jihatidan qaysi tur?', 'Dona son', ['Chama son','Dona son','Jamlovchi son','Taqsim son']),
 ('“Uchovimiz” so‘zi qaysi son turiga asoslangan?', 'Jamlovchi son', ['Tartib son','Jamlovchi son','Kasr son','Chama son']),
 ('“Beshdan ikki” qaysi son turi?', 'Kasr son', ['Dona son','Tartib son','Kasr son','Taqsim son']),
 ('“Eng baland” sifatning qaysi darajasi?', 'Orttirma daraja', ['Oddiy daraja','Qiyosiy daraja','Orttirma daraja','Ozaytirma daraja']),
 ('“Men o‘zim bajardim” gapida “o‘zim” qaysi olmosh?', 'O‘zlik olmoshi', ['Kishilik olmoshi','O‘zlik olmoshi','Ko‘rsatish olmoshi','Gumon olmoshi']),
 ('“Hech kim kelmadi” birikmasidagi “hech kim” qaysi olmosh?', 'Bo‘lishsizlik olmoshi', ['So‘roq olmoshi','Belgilash olmoshi','Bo‘lishsizlik olmoshi','Gumon olmoshi']),
 ('“Na ... na” qanday yordamchi so‘z vazifasida keladi?', 'Takroriy inkor bog‘lovchisi', ['Ko‘makchi','Takroriy inkor bog‘lovchisi','Yuklama','Modal so‘z']),
 ('Ilmiy uslubning asosiy belgisi qaysi?', 'Aniqlik, mantiqiylik va terminlarga tayanish', ['Obrazlilik va hissiylik','Aniqlik, mantiqiylik va terminlarga tayanish','Erkin dialog ustunligi','Qoliplashgan hujjat shakli']),
 ('Rasmiy-idoraviy uslubga xos janr qaysi?', 'Ariza', ['Roman','Ariza','Qasida','Hikoya']),
 ('“Yuragi orqasiga tortdi” iborasi qanday ma’no bildiradi?', 'Qattiq qo‘rqdi', ['Juda quvondi','Qattiq qo‘rqdi','Shoshildi','G‘azablandi']),
 ('Qaysi qatorda antonim juftlik bor?', 'saxiy — xasis', ['go‘zal — chiroyli','saxiy — xasis','yuz — bet','tez — ildam']),
 ('Qaysi qatorda omonim so‘z keltirilgan?', 'ot (hayvon) — ot (ism)', ['katta — kichik','ot (hayvon) — ot (ism)','oq — qora','chiroyli — go‘zal']),
 ('“Yaxshi” so‘zining orttirma darajasi qaysi?', 'eng yaxshi', ['yaxshiroq','eng yaxshi','yaxshigina','yaxshidek']),
 ('Qaysi gap shaxsi noma’lum gap?', 'Eshik taqillatildi.', ['Men keldim.','Eshik taqillatildi.','Bahor keldi.','Bugun havo issiq.']),
 ('Qaysi gap shaxsi umumlashgan gapga misol?', 'Avval o‘yla, keyin so‘yla.', ['Men kitob o‘qidim.','Avval o‘yla, keyin so‘yla.','Eshik ochildi.','Tong otdi.']),
 ('“Balki” so‘zi kontekstga qarab qaysi vazifada kelishi mumkin?', 'Modal so‘z yoki bog‘lovchi', ['Faqat ot','Modal so‘z yoki bog‘lovchi','Faqat ko‘makchi','Faqat yuklama']),
 ('“Yuz” so‘zi qaysi javobda omonimlikni ko‘rsatadi?', 'son va bet ma’nolari', ['faqat rang ma’nolari','son va bet ma’nolari','faqat harakat ma’nolari','faqat kasb nomlari']),
 ('Qaysi birikmada qaratqich-qaralmish munosabati mavjud?', 'kitobning muqovasi', ['kitobni o‘qimoq','kitobning muqovasi','kitob bilan','kitob uchun']),
 ('“U juda tez yugurdi” gapida “juda” qaysi turkum?', 'Ravish', ['Sifat','Ravish','Olmosh','Yuklama']),
 ('Qaysi qatorda qo‘shma so‘z imlosi to‘g‘ri?', 'temiryo‘l', ['temir yo‘l','temir-yo‘l','temiryo‘l','temir_yol']),
 ('Qaysi tinish belgisi uyushiq bo‘laklar orasida sanash ohangida ishlatiladi?', 'Vergul', ['Nuqta','Vergul','Qavs','Qo‘shtirnoq']),
 ('Publitsistik uslubning asosiy maqsadi qaysi?', 'Jamoatchilik fikriga ta’sir etish va axborot berish', ['Faqat ilmiy isbot','Jamoatchilik fikriga ta’sir etish va axborot berish','Huquqiy buyruq berish','Badiiy obraz yaratish']),
]


def pack(question, correct, wrong, explanation, difficulty):
    correct=str(correct)
    distractors=[]
    for value in list(wrong):
        value=str(value)
        if value != correct and value not in distractors:
            distractors.append(value)
    suffix=1
    while len(distractors)<3:
        candidate=f'{correct} + {suffix}'
        if candidate not in distractors and candidate != correct:
            distractors.append(candidate)
        suffix+=1
    opts=distractors[:3]+[correct]
    return {'question':question,'options':opts,'answer':3,'explanation':explanation,'difficulty':difficulty}

def shuffle_q(q, rng):
    pairs=list(enumerate(q['options'])); rng.shuffle(pairs)
    correct=next(i for i,(old,_) in enumerate(pairs) if old==q['answer'])
    q['options']=[v for _,v in pairs]; q['answer']=correct
    return q


def gen_math(level, n, rng):
    out=[]
    for i in range(n):
        a=rng.randint(3,19); b=rng.randint(2,13); c=rng.randint(2,11)
        if level=='basic':
            x=rng.randint(-8,12); m=rng.randint(2,9); k=rng.randint(-15,20); ans=m*x+k
            q=f'{m}(x − {x}) + {k} ifodaning qiymatini toping.'
            correct=str(k); wrong=[str(k+m),str(k-m),str(-k)]
            # Replace with a real equation-solving problem.
            q=f'{m}x + {k} = {ans+m*x}. Tenglamaning ildizini toping.'; correct=str(x); wrong=[str(x+1),str(x-1),str(-x)]
            exp=f'{m}x={ans+m*x}-{k}={m*x}; x={x}.'
        elif level=='middle':
            # Quadratic with integer roots, ask sum of reciprocal squares.
            r1=rng.choice([v for v in range(-8,9) if v != 0]); r2=rng.choice([v for v in range(-8,9) if v not in (0,r1)])
            s=r1+r2; p=r1*r2
            ans=(s*s-2*p)/(p*p)
            q=f'x² − ({s})x + ({p}) = 0 tenglamaning ildizlari x₁ va x₂. 1/x₁² + 1/x₂² qiymatini toping.'
            correct=f'{ans:g}'; wrong=[f'{(s*s+2*p)/(p*p):g}',f'{s*s-2*p:g}',f'{1/abs(p):g}']; exp='Viyet bo‘yicha x₁+x₂=s, x₁x₂=p. Yig‘indi (s²−2p)/p².'
        else:
            # Parameterized discriminant threshold.
            r1=rng.randint(-9,9); r2=rng.randint(-9,9)
            A=rng.randint(1,5); B=-A*(r1+r2); C=A*r1*r2
            disc=B*B-4*A*C
            q=f'{A}x² + ({B})x + ({C}) = 0 tenglama ildizlari α, β. (α−β)² qiymatini toping.'
            correct=str(disc//(A*A)); wrong=[str((r1+r2)**2),str(abs(r1*r2)),str(disc)]; exp='(α−β)²=(α+β)²−4αβ=D/A².'
        out.append(shuffle_q(pack(q,correct,wrong,exp,level),rng))
    return out


def gen_physics(level,n,rng):
    out=[]
    for i in range(n):
        if level=='basic':
            m=rng.randint(2,20); a=rng.randint(2,12); F=m*a
            q=f'Massasi {m} kg jismga natijaviy {F} N kuch ta’sir qilmoqda. Tezlanish qancha?'
            correct=f'{a} m/s²'; wrong=[f'{a+1} m/s²',f'{F} m/s²',f'{m/a:g} m/s²']; exp='Nyutonning ikkinchi qonuni: a=F/m.'
        elif level=='middle':
            R1=rng.randint(2,12); R2=rng.randint(2,12); U=rng.choice([12,18,24,36,48]); Req=R1*R2/(R1+R2); I=U/Req
            q=f'{R1} Ω va {R2} Ω qarshiliklar parallel ulangan, uchlariga {U} V kuchlanish berilgan. Umumiy tok kuchini toping.'
            correct=f'{I:.2f} A'; wrong=[f'{U/(R1+R2):.2f} A',f'{U/R1+U/R2+1:.2f} A',f'{Req/U:.2f} A']; exp='Parallel ulashda 1/R=1/R₁+1/R₂, so‘ng I=U/R.'
        else:
            # Projectile max height with v0, angle chosen 30/45/60; g=10.
            v=rng.choice([20,30,40,50]); angle=rng.choice([30,45,60]); import math
            h=(v*math.sin(math.radians(angle)))**2/20
            q=f'Jism {v} m/s boshlang‘ich tezlik bilan gorizontga {angle}° burchak ostida otildi. g=10 m/s². Eng yuqori ko‘tarilish balandligini toping.'
            correct=f'{h:.2f} m'; wrong=[f'{v*v/20:.2f} m',f'{v*math.sin(math.radians(angle))/10:.2f} m',f'{h*2:.2f} m']; exp='H=v₀²sin²α/(2g).'
        out.append(shuffle_q(pack(q,correct,wrong,exp,level),rng))
    return out


def gen_history(level,n,rng):
    out=[]
    for i in range(n):
        item=HISTORY[i%len(HISTORY)]; q,correct,opts=item
        if level=='middle': q='Tarixiy fakt va davrni tahlil qiling: '+q
        elif level=='advanced': q='Milliy sertifikatning murakkab tarixiy tahlil darajasi: '+q+' Berilgan variantlardan aniq javobni belgilang.'
        wrong=[x for x in opts if x!=correct]
        out.append(shuffle_q(pack(q,correct,wrong,'Tarixiy fakt: '+correct,level),rng))
    return out


def gen_uzbek(level,n,rng):
    out=[]
    for i in range(n):
        item=UZBEK[i%len(UZBEK)]; q,correct,opts=item
        if level=='middle': q='Grammatik va mazmuniy tahlil asosida javobni aniqlang: '+q
        elif level=='advanced': q='Murakkab lingvistik tahlil: '+q+' Javobni me’yoriy qoida asosida tanlang.'
        wrong=[x for x in opts if x!=correct]
        out.append(shuffle_q(pack(q,correct,wrong,'Izoh: '+correct,level),rng))
    return out

GENERATORS={'math':gen_math,'physics':gen_physics,'history':gen_history,'uzbek':gen_uzbek}

def build_bank(subject):
    rng=random.Random(20261118 + sum(map(ord,subject)))
    bank=[]
    for level in ('basic','middle','advanced'):
        bank.extend(GENERATORS[subject](level,400,rng))
    return bank

_BANKS={s:build_bank(s) for s in SUBJECTS}

def make_test(subject, level, count=45):
    if subject not in _BANKS or level not in ('basic','middle','advanced'):
        raise ValueError('Noto‘g‘ri fan yoki daraja')
    pool=[q.copy() for q in _BANKS[subject] if q['difficulty']==level]
    rng=random.SystemRandom()
    # Fresh option order for every run; test contains no duplicate item.
    chosen=rng.sample(pool,min(count,len(pool)))
    result=[]
    for q in chosen:
        q['options']=list(q['options']); pairs=list(enumerate(q['options'])); rng.shuffle(pairs)
        q['answer']=next(i for i,(old,_) in enumerate(pairs) if old==q['answer'])
        q['options']=[v for _,v in pairs]
        result.append(q)
    return result

if __name__=='__main__':
    for s,b in _BANKS.items():
        print(s, len(b), {l:sum(q['difficulty']==l for q in b) for l in ('basic','middle','advanced')})
