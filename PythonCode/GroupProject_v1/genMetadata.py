import os
from datetime import datetime
import json
import fnmatch

class WriteMetaData:
    def __init__(self, directory, extensions):
        self.directory = directory
        self.extensions = extensions

    def logFileMetadata(self):

        for path, folder, files in os.walk(self.directory):
            for file_extentions in self.extensions:
                for filenames in fnmatch.filter(files, file_extentions):
                    self.writestats(os.path.join(path, filenames), filenames)


    @staticmethod
    def timeConvert(dt):
        newtime = datetime.fromtimestamp(dt)
        return newtime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def sizeFormat(size):
        newform = format(size / 1024, ".2f")
        return newform + " KB"

    def writeStats(self, full_filepath, file_name):
        metadata = os.stat(full_filepath)

        fileattributes = {
            'File_Name': file_name,
            'Size_KB': self.sizeFormat(metadata.st_size),
            'Creation_Date': self.timeConvert(metadata.st_ctime),
            'Modified_Date': self.timeConvert(metadata.st_mtime),
            'Last_Access_Date': self.timeConvert(metadata.st_atime),
        }
        with open(os.path.join(self.directory, "data.json"), 'a') as generate:
            generate.write(json.dumps(fileattributes))

if __name__ == "__main__":
    directory = 'D:/SQL/New folder/'
    extensions = ["*.sql", "*.txt"]

    writemd = WriteMetaData(directory,extensions)
    writemd.logFileMetadata()
