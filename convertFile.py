import os
import subprocess

# Function for converting the AAC file generated from Beatoven workflow to an MP3 file
def convert_aac_to_mp3(aac_file_path):
    """
    Converts an AAC file to MP3 using ffmpeg and deletes the original AAC file if the conversion is successful.

    Args:
    aac_file_path (str): Path to the AAC file to be converted.

    Returns:
    str: Path to the converted MP3 file, or None if the conversion fails.
    """
    # Define the output MP3 file path by replacing the .aac extension with .mp3
    mp3_file_path = aac_file_path.replace('.aac', '.mp3')

    try:
        # Run ffmpeg command to convert AAC to MP3
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", aac_file_path, mp3_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Check if the conversion was successful
        if result.returncode != 0:
            print(f"ffmpeg failed with error: {result.stderr.decode()}")
            return None

        # Delete the original AAC file
        os.remove(aac_file_path)
        print(f"Deleted original AAC file: '{aac_file_path}'")
        print(f"Conversion successful: '{mp3_file_path}'")

        return mp3_file_path
    except Exception as e:
        print(f"Error during AAC to MP3 conversion: {e}")
        return None