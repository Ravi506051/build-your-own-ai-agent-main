"""Text-to-speech helpers using edge-tts."""

import asyncio
import edge_tts


async def _save_speech(text: str, output_path: str, voice: str) -> None:
    """Run edge-tts communicate and save synthesized speech."""
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_path)


def speak(text: str, output_path: str = "output.mp3") -> str:
    """Generate speech from text and return the saved MP3 path."""
    voice = "en-US-AriaNeural"
    asyncio.run(_save_speech(text=text, output_path=output_path, voice=voice))
    return output_path
