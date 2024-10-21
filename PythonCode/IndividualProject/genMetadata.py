import os
from datetime import datetime, timezone
import json
import fnmatch
from analysisAgent import analyze_file

class WriteMetaData:
    def __init__(self, directory, extensions):
        # Initialize the class with the directory to scan and file extensions to look for
        self.directory = directory
        self.extensions = extensions

    def logFileMetadata(self):
        # Walk through the directory and process files with specified extensions. 
        # This design allows for easy extension to other file types
        for path, folder, files in os.walk(self.directory):
            for file_extension in self.extensions:
                for filename in fnmatch.filter(files, file_extension):
                    self.writeStats(os.path.join(path, filename), filename)

    @staticmethod
    def timeConvert(dt):
        # Convert timestamp to a formatted date string in UTC
        newtime = datetime.fromtimestamp(dt, tz=timezone.utc)
        return newtime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def sizeFormat(size):
        # Convert file size to KB and format it
        newform = format(size / 1024, ".2f")
        return newform + " KB"

    @staticmethod
    def get_file_content(filepath):
        # Read and return the content of a file, or an error message if reading fails. Designed as a function to be called by other classes
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def writeStats(self, full_filepath, file_name):
        # Get file metadata and write it to a JSON file
        metadata = os.stat(full_filepath)

        # Prepare file attributes dictionary
        fileattributes = {
            'File_Name': file_name,
            'Size_KB': self.sizeFormat(metadata.st_size),
            'Creation_Date': self.timeConvert(metadata.st_ctime),
            'Modified_Date': self.timeConvert(metadata.st_mtime),
            'Last_Access_Date': self.timeConvert(metadata.st_atime),
            'Content': analyze_file(self.get_file_content(full_filepath))
        }
        
        # Create MetaData directory if it doesn't exist
        metadata_dir = os.path.join(os.path.dirname(full_filepath), 'MetaData')
        os.makedirs(metadata_dir, exist_ok=True)
        json_file = os.path.join(metadata_dir, "data.json")
        
        # Read existing data or initialize an empty list
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
        
        # Append new data
        data.append(fileattributes)
        
        # Write updated data back to file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Set the directory to scan and file extensions to process
    directory = '/Users/joaotorres/Desktop/MSc AI - Programming/Intelligent Agents/reuessexgroupproject/MetaData'
    extensions = ["*.sql", "*.txt"]

    # Create WriteMetaData instance and start logging file metadata
    WriteMetaData(directory, extensions).logFileMetadata()
