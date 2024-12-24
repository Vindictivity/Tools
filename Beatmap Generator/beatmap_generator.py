import xml.etree.ElementTree as ET
import gzip
import json
import os

def extract_als():
    print("\nFinding Current Working Directory...")
    scriptdir = os.path.abspath(os.path.dirname(__file__))
    
    print("Searching for nearby ALS files...")
    als_files = [f for f in os.listdir(scriptdir) if f.endswith('.als')]

    if not als_files:
        print("No ALS files found in the current directory...")
        return

    print(f"Found files: {', '.join(als_files)}...")

    print("\nGenerating storage...")
    output_folder = os.path.normpath(os.path.join(scriptdir, "beatmaps"))
    os.makedirs(output_folder, exist_ok=True)

    for als_file in als_files:
        print(f"\nProcessing {als_file}...")
        base_name = os.path.splitext(als_file)[0]
        output_json = os.path.join(output_folder, f"{base_name}.json")
        
        try:
            while True:
                try:
                    bpm = float(input(f"Enter the BPM for {als_file}: "))
                    if bpm <= 0.0:
                        raise ValueError("BPM must be greater than 0.")
                    break
                except ValueError as e:
                    print(f"Invalid BPM: {e}. Please enter a positive number.")
            
            seconds_per_beat = 60 / bpm
            
            print("Decompressing...")
            with gzip.open(os.path.join(scriptdir, als_file), 'rb') as gz:
                decompressed_content = gz.read()

            print("Parsing content...")
            root = ET.fromstring(decompressed_content)

            timestamps_in_seconds = {}
            invalid_timestamps = []
            
            print("Extracting beatmap...")
            for locator in root.findall(".//Locator"):
                time_element = locator.find("./Time")
                if time_element is not None:
                    locator_time_in_beats = float(time_element.get('Value', '0.0'))
                    locator_time_in_seconds = locator_time_in_beats * seconds_per_beat
                    timestamps_in_seconds[str(round(locator_time_in_seconds, 1))] = {}
                else:
                    invalid_timestamps.append("N/A")

            sorted_timestamps = {str(key): value for key, value in sorted(timestamps_in_seconds.items(), key=lambda item: float(item[0]))}

            for i, invalid in enumerate(invalid_timestamps, start=1):
                key = f"invalid_timestamp_{i}"
                sorted_timestamps[key] = {}
                
            print(f"Saving beatmap to {base_name}.json...")
            with open(output_json, 'w') as json_file:
                json.dump(sorted_timestamps, json_file, indent=4)

            print(f"Successfully converted {als_file}...")
        except OSError as e:
            print(f"Failed to decompress {als_file}: {e}...")
        except ET.ParseError as e:
            print(f"Failed to parse XML for {als_file}: {e}...")


print("I'll be converting your ALS files to JSON beatmaps...")
input("Press 'Enter' when all your ALS files are in the same folder as me...")
extract_als()
input("\nConversions finished, press 'Enter' when you're ready to close...")
