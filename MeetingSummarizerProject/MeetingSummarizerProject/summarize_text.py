from transformers import pipeline
import os
from datetime import datetime

def summarize_text(text):
    """
    Summarize the given text using a pre-trained model.
    
    Args:
        text (str): The text to summarize
    
    Returns:
        str: Path to the saved summary file
    """
    print("Loading summarization model...")
    
    # Use a simpler model that doesn't require sentencepiece
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Split text into chunks if it's too long (BART has a max length of 1024 tokens)
    max_chunk_length = 1000
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    
    print("Generating summary...")
    
    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    # Combine summaries
    final_summary = " ".join(summaries)
    
    # Create summaries directory if it doesn't exist
    if not os.path.exists('summaries'):
        os.makedirs('summaries')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"summaries/summary_{timestamp}.txt"
    
    # Save the summary
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(final_summary)
    
    print(f"Summary saved to: {summary_file}")
    return summary_file

if __name__ == "__main__":
    # Test the summarization
    test_text = "This is a test transcript. We discussed several important points in the meeting. First, we talked about project timelines. Then we covered budget concerns. Finally, we addressed team assignments."
    try:
        summary_file = summarize_text(test_text)
        print("\nSummary completed successfully!")
        print(f"Summary saved to: {summary_file}")
        
        # Print the summary
        with open(summary_file, 'r', encoding='utf-8') as f:
            print("\nGenerated Summary:")
            print(f.read())
            
    except Exception as e:
        print(f"An error occurred during summarization: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have enough disk space")
        print("2. Check your internet connection")
        print("3. Ensure you have enough RAM")
        print("4. Try using a different model") 