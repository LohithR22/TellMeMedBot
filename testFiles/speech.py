import asyncio
import websockets
import json
import sounddevice as sd
import numpy as np
import keyboard  # You'll need to install this: pip install keyboard

# Your existing credentials and settings remain the same
API_KEY = "cb110c58aac13b4afef4fec600ac5da0e382dc37"
APP_ID = "com.lohithrgowda22"
WS_URL = f"wss://revapi.reverieinc.com/stream?apikey={API_KEY}&appid={APP_ID}&appname=stt_stream&src_lang=hi&domain=generic"
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024

# Global flag to control recording
is_recording = True

async def send_audio(websocket):
    """Captures audio from the microphone and sends it to the WebSocket server."""
    print("🎤 Recording... Press 'q' to stop")
    
    def callback(indata, frames, time, status):
        if status:
            print(f"Error in recording: {status}")
        if is_recording:
            audio_data = indata.tobytes()
            asyncio.run_coroutine_threadsafe(websocket.send(audio_data), loop)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, 
                       dtype='int16', callback=callback):
        while is_recording:
            await asyncio.sleep(0.1)  # Small delay to prevent CPU overload

    await websocket.send(json.dumps({"event": "end"}))

async def receive_transcription(websocket):
    """Receives transcription responses from the WebSocket."""
    async for response in websocket:
        if not is_recording:
            break
        data = json.loads(response)
        if data.get("success"):
            if data["cause"] == "partial":
                print(f"[PARTIAL] {data['display_text']}")
            elif data["cause"] == "EOF received":
                print(f"[FINAL] {data['display_text']}")
        else:
            print(f"[ERROR] {data['cause']}")

def stop_recording():
    """Callback for stopping the recording."""
    global is_recording
    is_recording = False
    print("\nStopping recording...")

async def main():
    """Main function to handle the WebSocket connection and recording."""
    global loop
    loop = asyncio.get_event_loop()
    
    # Setup keyboard listener
    keyboard.on_press_key('q', lambda _: stop_recording())
    
    async with websockets.connect(WS_URL) as websocket:
        print("Connected to Reverie STT WebSocket...")
        await asyncio.gather(
            send_audio(websocket),
            receive_transcription(websocket)
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        stop_recording()
    finally:
        print("Session ended")
