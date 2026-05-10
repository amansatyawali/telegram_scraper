import subprocess
import json
import os

def get_audio_codec(input_path: str) -> str:
    """Use ffprobe to detect the audio codec"""
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_name",
        "-of", "json",
        input_path
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    return data["streams"][0]["codec_name"]


def codec_to_extension(codec: str) -> str:
    """Map codec to correct file extension"""
    mapping = {
        "aac": "aac",
        "mp3": "mp3",
        "opus": "opus",
        "vorbis": "ogg",
        "flac": "flac",
        "pcm_s16le": "wav"
    }
    return mapping.get(codec, "m4a")  # default fallback


def extract_audio(input_path: str, output_base_path: str):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Detect codec
    codec = get_audio_codec(input_path)
    ext = codec_to_extension(codec)

    output_path = f"{output_base_path}.{ext}"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vn",
        "-acodec", "copy",
        output_path
    ]

    subprocess.run(command, check=True)

    print(f"✅ Audio extracted: {output_path}")
    print(f"🎧 Codec detected: {codec}")



video_input = "data/46382_-_6247039995140382929_-__-_.mp4"
audio_output = "output/audio"

extract_audio(video_input, audio_output)