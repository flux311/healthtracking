import torch
import sounddevice as sd
import soundfile as sf
import os  # ← Добавляем импорт


def speak_silero(text, speaker='xenia', output_file=None, auto_delete=False):
    device = torch.device('cpu')
    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',model='silero_tts',language='ru',speaker='v3_1_ru')
    model.to(device)

    print(f"🎤 Озвучиваю: '{text}'")
    print(f"🗣 Голос: {speaker}")

    audio = model.apply_tts(text=text, speaker=speaker, sample_rate=48000)

    # Сохраняем файл
    if output_file:
        sf.write(output_file, audio.numpy(), 48000)
        print(f"💾 Сохранено в: {os.path.abspath(output_file)}")

    # Воспроизводим
    print("🔊 Воспроизвожу...")
    sd.play(audio.numpy(), 48000)
    sd.wait()

    # 🗑 Автоудаление
    if output_file and auto_delete:
        os.remove(output_file)
        print(f"🗑 Файл {output_file} удален")

    print("✅ Готово!")


# Тест с автоудалением
speak_silero(text="Привет, я удалю себя после прослушивания",speaker='aidar',output_file="temp_audio.wav",auto_delete=True) # ← Включаем автоудаление