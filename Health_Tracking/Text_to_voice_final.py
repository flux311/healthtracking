import torch
import sounddevice as sd

device = torch.device("cpu")

model, example_text = torch.hub.load(repo_or_dir = "snakers4/silero-models", model = "silero_tts", language = "ru", speaker = "v3_1_ru")
model.to(device)

audio = model.apply_tts(text = "Привет, я озвучиваю текст", speaker = "aidar", sample_rate = 48000)

sd.play(audio.numpy(), 48000)
sd.wait()
