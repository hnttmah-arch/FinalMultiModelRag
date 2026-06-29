import whisper


model = whisper.load_model(
    "base"
)

audio = "speech/sample_1.m4a"

result = model.transcribe(
    audio
)

print()

print("TEXT:")

print(
    result["text"]
)