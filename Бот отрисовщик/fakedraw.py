from PIL import Image, ImageFont, ImageDraw


def fake_qiwi_balance(message):
    text = message.text + " ₽"
    qiwi = Image.open("Image source/Qiwi/qiwi_balance.png")
    fnt = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 100)
    W = 1080
    w, h = fnt.getsize(text)
    d = ImageDraw.Draw(qiwi)
    d.text(((W - w) / 2, 296), text, font=fnt, fill=(255, 255, 255, 255))
    del d
    qiwi.save(f"ForScreen/{message.chat.id}_fakeqiwibalance.png.png", "PNG")
    return open(f"ForScreen/{message.chat.id}_fakeqiwibalance.png.png", "rb")


def fake_qiwi_transfer(message):
    if message.text == "Перевод на другой кошелек":
        text = ["432", "+78954328507", "08.03.2021 в 21:30"]
    else:
        text = message.text.split("\n")
    money = text[0] + " ₽"
    money2 = "- " + text[0].strip() + " ₽"
    phone = text[1].strip()
    date_time = text[2].strip()
    qiwi = Image.open("Image source/Qiwi/qiwi_check.png")
    font1 = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 53)
    font2 = ImageFont.truetype("Fonts/Roboto-Regular.ttf", 38)
    font3 = ImageFont.truetype("Fonts/Roboto-Regular.ttf", 45)
    font4 = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 45)
    W = 1080
    w1, h1 = font1.getsize(money2)
    w2, h2 = font1.getsize(phone)
    d = ImageDraw.Draw(qiwi)
    d.text(((W-w1)/2,685), money2, font=font1, fill=(0,0,0,255))
    d.text(((W-w2)/2 + 60,614), phone, font=font2, fill=(153,153,153,255))
    d.text((56,1890), date_time, font=font3, fill=(0,0,0,255))
    d.text((56,2072), money, font=font4, fill=(0,0,0,255))
    if message.text == "Перевод на другой кошелек":
        qiwi.save(f"ForScreen/example_fakeqiwitransfer.png", "PNG")
        return open(f"ForScreen/example_fakeqiwitransfer.png", "rb")
    else:
        qiwi.save(f"ForScreen/{message.chat.id}_fakeqiwitransfer.png", "PNG")
        return open(f"ForScreen/{message.chat.id}_fakeqiwitransfer.png", "rb")
		

def fake_sber_balance(message):
    if message.text == "Баланс":
        text = ["20:17", "15631", "8237"]
    else:
        text = message.text.split("\n")
    time = text[0]
    name = text[1] + " ₽"
    money = text[2]
    tink = Image.open("Image source/Sber/sber_balance.png")
    font_time = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 16)
    font_name = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 24)
    font_money = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 18)
    d = ImageDraw.Draw(tink)
    d.text((15,20), time, font=font_time, fill=(225, 238, 229,255))

    if (len(text[1]) == 4):
        d.text((490,543), name, font=font_name, fill=(37,152,97,255))
    elif (len(text[1]) <= 3):
        d.text((500,543), name, font=font_name, fill=(37,152,97,255))
    elif (len(text[1]) == 5):
        d.text((480,543), name, font=font_name, fill=(37,152,97,255))
    elif (len(text[1]) == 6):
        d.text((455,543), name, font=font_name, fill=(37,152,97,255))
    elif (len(text[1]) == 7):
        d.text((430,543), name, font=font_name, fill=(37,152,97,255))
    elif (len(text[1]) == 8):
        d.text((400,543), name, font=font_name, fill=(37,152,97,255))
    elif (len(text[1]) == 9):
        d.text((370,543), name, font=font_name, fill=(37,152,97,255))	

    d.text((115, 580), money, font=font_money, fill=(132,132,132,255))
    if message.text == "Баланс":
        tink.save(f"ForScreen/example__fakesberbalance.png", "PNG")
        return open(f"ForScreen/example__fakesberbalance.png", "rb")
    else:
        tink.save("ForScreen/{message.chat.id}_fakesberbalance.png", "PNG")
        return open("ForScreen/{message.chat.id}_fakesberbalance.pn", "rb")


def fake_yandex_balance(message):
    if message.text == "Баланс":
        text = ["20:17", "shpex", "8 561,51"]
    else:
        text = message.text.split("\n")
    time = text[0]
    name = text[1]
    money = text[2]
    tink = Image.open("Image source/Yandex/ya_balance.png")
    font_money = ImageFont.truetype("Fonts/ArialRegular.ttf", 96)
    font_name = ImageFont.truetype("Fonts/ArialRegular.ttf", 30)
    font_time = ImageFont.truetype("Fonts/Roboto-Medium.ttf", 21)
    d = ImageDraw.Draw(tink)

    d.text((330,9), time, font=font_time, fill=(255,255,255,255))
    d.text((140,90), name, font=font_name, fill=(255,255,255,255))  
    d.text((50,380), money, font=font_money, fill=(255,255,255,255))

    if message.text == "Баланс":
        tink.save(f"ForScreen/example__fakeyandexbalance.png", "PNG")
        return open(f"ForScreen/example__fakeyandexbalance.png", "rb")
    else:
        tink.save("ForScreen/{message.chat.id}_fakeyandexbalance.png", "PNG")
        return open("ForScreen/{message.chat.id}_fakeyandexbalance.png", "rb")
	