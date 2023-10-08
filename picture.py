from PIL import Image, ImageDraw, ImageFont


def make_image(daily, weekly, _id):
    im = Image.new(mode="RGBA", size=(512, 512), color=(105, 151, 193))
    header_font = ImageFont.truetype("OpenSans-Bold.ttf", 36)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 18)
    draw = ImageDraw.Draw(im)
    draw.text((130, 10), 'YOUR QUESTS', (255, 255, 255), header_font)

    draw.text((210, 60), "Daily", (0, 0, 0), header_font)
    draw.text((20, 110), daily["name"], (0, 0, 0), header_font)
    draw.text((20, 160), daily["description"], (0, 0, 0), font)
    draw.text((300, 130), "reward: " + str(daily["reward"]), (0, 0, 0), font)
    draw.text((300, 160), "deadline: " + daily["date"], (0, 0, 0), font)
    draw.rectangle((10, 210, 502, 240), fill=(212, 46, 46))
    draw.rectangle((10, 210, int(492 * daily["progress"]), 240),
                   fill=(79, 212, 46))
    draw.rectangle((10, 210, 502, 240),
                   outline=(0, 0, 0), width=5)

    draw.text((210, 260), "Weekly", (0, 0, 0), header_font)
    draw.text((20, 310), weekly["name"], (0, 0, 0), header_font)
    draw.text((20, 360), weekly["description"], (0, 0, 0), font)
    draw.text((300, 330), "reward: " + str(weekly["reward"]), (0, 0, 0), font)
    draw.text((300, 360), "deadline: " + weekly["date"], (0, 0, 0), font)
    draw.rectangle((10, 410, 502, 440), fill=(212, 46, 46))
    draw.rectangle((10, 410, int(492 * weekly["progress"]), 440),
                   fill=(79, 212, 46))
    draw.rectangle((10, 410, 502, 440),
                   outline=(0, 0, 0), width=5)

    # to differentiate images between users
    im.save(f"images/{_id}_quest_update.png")
    return f"images/{_id}_quest_update.png"
