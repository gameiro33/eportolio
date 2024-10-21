import os
import fnmatch
import shutil
from genMetadata import WriteMetaData

class DirectorySearchAgent:
    """"The Directory Search agent searches a directory for specific file types"""
    def __init__(self, directory, extensions):

        self.directory = directory
        self.extensions = extensions

    def getdirectories(self):
        filepath_list = []
        for path, folder, files in os.walk(self.directory):
            for file_extentions in self.extensions:
                for filenames in fnmatch.filter(files, file_extentions):
                    filepath_list.append(os.path.join(path, filenames))
        return filepath_list

class ArchiveFiles:
    "Archives files class given source and archive directories"
    def __init__(self, source_dir, archive_dir):

        self.source_dir = source_dir
        self.archive_dir = archive_dir


    def archivefiles(self,move=1):
        """Arhive files to given archive directory. default behaviour is to move the files,
        when move == 0 it will copy the files"""

        for i in self.source_dir:
            if move == 1:
                shutil.move(i, self.archive_dir)
            else:
                shutil.copy(i, self.archive_dir)


if __name__ == "__main__":
    dir = "D:/forensics/"
    file_types = ["*.sql", "*.txt"]
    ds_agent = DirectorySearchAgent(dir, file_types)
    dirlist = ds_agent.getdirectories()

    archive_dir = "D:/forensics/archive/"
    archive = ArchiveFiles(dirlist, archive_dir)
    archive.archivefiles(move=0)

    metadata = WriteMetaData(archive_dir, file_types)
    metadata.logFileMetadata()

