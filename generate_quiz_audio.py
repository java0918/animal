import os
import asyncio
import edge_tts

questions = [
    "Qaysi mushuksimon hayvonning yuzida ko'zlaridan labiga qadar qora ko'z yoshi chizig'i bo'ladi va tirnoqlari itlarnikidek ichkariga kirmaydi?",
    "Yovvoyi tovushqon va xonaki quyon o'rtasidagi eng muhim biologik farq nima?",
    "Ushbu haybatli tovush qaysi qudratli yirtqichga tegishli?",
    "O'zbekiston Qizil kitobiga kiritilgan qaysi noyob antilopaning dumi qop-qora bo'lgani uchun qoraquyruq deb ataladi?",
    "Qaldirg'och va qorayaloq qanday farqlanadi?",
    "O'zbekiston tog'larining ramzi bo'lgan Qor qoploni oddiy leopardan qanday anatomik farq qiladi?"
]

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "audio", "quiz")
os.makedirs(output_dir, exist_ok=True)

async def main():
    print("O'zbek tili nutqida audio generatsiya qilinmoqda...")
    for idx, q in enumerate(questions):
        file_name = f"q{idx + 1}.mp3"
        out_path = os.path.join(output_dir, file_name)
        # Using uz-UZ-MadinaNeural for clean natural Uzbek voice
        communicate = edge_tts.Communicate(q, "uz-UZ-MadinaNeural", rate="-2%")
        await communicate.save(out_path)
        sz = os.path.getsize(out_path)
        print(f"Tayyor: {file_name} ({sz} bayt)")

if __name__ == "__main__":
    asyncio.run(main())
