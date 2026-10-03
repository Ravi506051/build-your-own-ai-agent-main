"""Speech-to-speech AI agent with OpenAI or Ollama LLM providers."""

import argparse
import os
from datetime import datetime

import requests
from colorama import Fore, Style, init
from openai import OpenAI

from stt import record_audio, transcribe_audio
from tts import speak


def generate_reply(prompt: str) -> str:
    """Generate an assistant reply using OpenAI or Ollama based on env config."""
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    system_prompt = "You are a concise, helpful voice assistant."

    if provider == "openai":
        client = OpenAI()
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return (resp.choices[0].message.content or "").strip()

    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return data.get("message", {}).get("content", "").strip()


def play_audio(path: str) -> None:
    """Play audio if playsound is installed; otherwise leave file on disk."""
    try:
        from playsound import playsound

        playsound(path)
    except Exception:
        print(f"Saved audio to: {path}")


def run_text_mode() -> None:
    """Run text-only loop: user types text, assistant speaks to MP3."""
    print("Text mode enabled. Type /quit to exit.")
    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() == "/quit":
            break

        print(Fore.YELLOW + "Thinking..." + Style.RESET_ALL)
        reply = generate_reply(user_text)
        print(f"Assistant: {reply}")

        print(Fore.GREEN + "Speaking..." + Style.RESET_ALL)
        filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        out_path = speak(reply, filename)
        print(f"Speech saved to {out_path}")


def run_voice_mode() -> None:
    """Run full voice loop: record mic, transcribe, think, speak."""
    print("Voice mode enabled. Say a prompt every turn or type /quit when asked.")
    while True:
        marker = input("Press Enter to record (or /quit): ").strip().lower()
        if marker == "/quit":
            break

        print(Fore.CYAN + "Listening..." + Style.RESET_ALL)
        audio_file = record_audio(duration=5)
        text = transcribe_audio(audio_file)
        if not text:
            print("No speech detected. Try again.")
            continue
        print(f"You said: {text}")

        print(Fore.YELLOW + "Thinking..." + Style.RESET_ALL)
        reply = generate_reply(text)
        print(f"Assistant: {reply}")

        print(Fore.GREEN + "Speaking..." + Style.RESET_ALL)
        filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        out_path = speak(reply, filename)
        play_audio(out_path)


def parse_args() -> argparse.Namespace:
    """Parse command line flags for selecting text or voice mode."""
    parser = argparse.ArgumentParser(description="Speech-to-speech voice agent")
    parser.add_argument("--text", action="store_true", help="Text-only mode (default)")
    parser.add_argument("--voice", action="store_true", help="Voice input/output mode")
    return parser.parse_args()


def main() -> None:
    """Entrypoint for running the interactive voice agent."""
    init(autoreset=True)
    args = parse_args()
    if args.voice:
        run_voice_mode()
    else:
        run_text_mode()


if __name__ == "__main__":
    main()
