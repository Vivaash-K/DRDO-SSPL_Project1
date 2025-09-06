import sounddevice as sd
import soundfile as sf
import numpy as np
import os
from datetime import datetime
import queue
import threading

# Global variables for recording control
recording_queue = queue.Queue()
is_recording = False

def record_audio(duration=None, sample_rate=44100):
    """
    Record audio from the microphone and save it as a WAV file.
    
    Args:
        duration (float, optional): Duration of recording in seconds. If None, recording continues until stopped.
        sample_rate (int): Sample rate for the recording (default: 44100 Hz)
    
    Returns:
        str: Path to the saved WAV file
    """
    global is_recording
    CHUNK = 1024
    FORMAT = sd.default.dtype
    CHANNELS = 1
    
    print("Recording started...")
    is_recording = True
    
    # Create a queue to store the recorded data
    q = queue.Queue()
    
    def callback(indata, frames, time, status):
        """This is called for each audio block."""
        if status:
            print(status)
        if is_recording:
            q.put(indata.copy())
    
    # Open stream
    with sd.InputStream(samplerate=sample_rate,
                       channels=CHANNELS,
                       callback=callback):
        while is_recording:
            sd.sleep(100)  # Sleep for 100ms between checks
    
    print("Recording finished.")
    
    # Get the recorded data from the queue
    recorded_data = []
    while not q.empty():
        recorded_data.append(q.get())
    
    if not recorded_data:
        raise Exception("No audio data was recorded")
    
    # Combine all the recorded data
    audio_data = np.concatenate(recorded_data, axis=0)
    
    # Create recordings directory if it doesn't exist
    if not os.path.exists('recordings'):
        os.makedirs('recordings')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recordings/recording_{timestamp}.wav"
    
    # Save the recording
    sf.write(filename, audio_data, sample_rate)
    print(f"Recording saved to {filename}")
    
    return filename

def stop_recording():
    """Stop the current recording."""
    global is_recording
    is_recording = False

if __name__ == "__main__":
    try:
        # Example usage
        print("Starting audio recording...")
        print("Press Enter to stop recording")
        recorded_file = record_audio()
        print(f"Recording completed and saved to: {recorded_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your microphone is properly connected")
        print("2. Check if your microphone is set as the default input device")
        print("3. Try running the script with administrator privileges")
        print("4. Check if any other application is using the microphone") 