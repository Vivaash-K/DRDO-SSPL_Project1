from faster_whisper import WhisperModel
import os
from datetime import datetime
import torch
import numpy as np
import soundfile as sf

def transcribe_audio(audio_file_path):
    """
    Transcribe audio from a WAV file using Faster Whisper with basic speaker detection.
    
    Args:
        audio_file_path (str): Path to the WAV file to transcribe
    
    Returns:
        str: Path to the saved transcription file
    """
    print(f"Loading Whisper model...")
    # Load the Whisper model (using the base model for faster processing)
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    print(f"Processing audio file: {audio_file_path}")
    # Transcribe the audio
    segments, info = model.transcribe(
        audio_file_path,
        beam_size=5,
        word_timestamps=True
    )
    
    # Create transcriptions directory if it doesn't exist
    if not os.path.exists('transcriptions'):
        os.makedirs('transcriptions')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcription_file = f"transcriptions/transcription_{timestamp}.txt"
    
    # Process segments and format with speaker detection
    transcription_text = []
    current_speaker = None
    last_end_time = 0
    
    for segment in segments:
        # Use timing to detect speaker changes
        if last_end_time > 0 and segment.start - last_end_time > 1.0:
            # If there's a pause longer than 1 second, assume it's a new speaker
            current_speaker = f"SPEAKER_{len(transcription_text) % 2 + 1}"
            transcription_text.append(f"\n[{current_speaker}]:")
        
        if current_speaker is None:
            current_speaker = "SPEAKER_1"
            transcription_text.append(f"[{current_speaker}]:")
        
        transcription_text.append(segment.text)
        last_end_time = segment.end
    
    # Save the transcription
    with open(transcription_file, 'w', encoding='utf-8') as f:
        f.write(" ".join(transcription_text))
    
    print(f"Transcription saved to: {transcription_file}")
    return transcription_file

if __name__ == "__main__":
    # Get the most recent recording from the recordings directory
    recordings_dir = "recordings"
    if not os.path.exists(recordings_dir):
        print("No recordings directory found. Please record some audio first.")
        exit(1)
    
    # Get the most recent WAV file
    wav_files = [f for f in os.listdir(recordings_dir) if f.endswith('.wav')]
    if not wav_files:
        print("No WAV files found in the recordings directory.")
        exit(1)
    
    # Sort by modification time (newest first)
    latest_recording = max(
        [os.path.join(recordings_dir, f) for f in wav_files],
        key=os.path.getmtime
    )
    
    print(f"Found latest recording: {latest_recording}")
    
    try:
        # Transcribe the audio
        transcription_file = transcribe_audio(latest_recording)
        print("\nTranscription completed successfully!")
        print(f"Transcription saved to: {transcription_file}")
        
        # Print the first few lines of the transcription
        with open(transcription_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\nFirst 200 characters of transcription:")
            print(content[:200] + "..." if len(content) > 200 else content)
            
    except Exception as e:
        print(f"An error occurred during transcription: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have enough disk space")
        print("2. Check if the audio file is not corrupted")
        print("3. Ensure you have a stable internet connection (for model download)")
        print("4. Try using a different audio file") 