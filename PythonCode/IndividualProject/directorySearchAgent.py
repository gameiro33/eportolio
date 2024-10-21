import os
import fnmatch
import shutil
from genMetadata import WriteMetaData

class DirectorySearchAgent:
    # A class to search for files with specific extensions in a given directory. 
    # OOP approach to enhance agent like arquitecture
    
    def __init__(self, directory, extensions):
        # Initialize the DirectorySearchAgent, where directory is the root directory to search in 
        # extensions is a list of file extensions to search for
        self.directory = directory
        self.extensions = extensions

    def getdirectories(self):
        # Search for files with specified extensions in the given directory 
        # Return a list of full file paths matching the specified extensions
        filepath_list = []
        for path, folder, files in os.walk(self.directory):
            for file_extension in self.extensions:
                for filename in fnmatch.filter(files, file_extension):
                    filepath_list.append(os.path.join(path, filename))
        return filepath_list

class ArchiveFiles:
    # A class to archive files from a source directory to an archive directory. OOP approach to enhance agent like arquitecture
    
    def __init__(self, source_dir, archive_dir):
        # Initialize the ArchiveFiles object, where source_dir is a list of source file paths and archive_dir is the destination directory for archiving
        self.source_dir = source_dir
        self.archive_dir = archive_dir

    def archivefiles(self, move=1):
        # Archive files by either moving or copying them to the archive directory.
        # move is a boolean that indicates if the files should be moved or copied. 
        # Default is 1 (move) because in a forensic context, we want to move the files to the archive directory to keep the original directory clean
        for file_path in self.source_dir:
            if move == 1:
                shutil.move(file_path, self.archive_dir)
            else:
                shutil.copy(file_path, self.archive_dir)

if __name__ == "__main__":
    # Set the root directory to search for files
    dir = "/Users/joaotorres/Desktop/MSc AI - Programming/Intelligent Agents/reuessexgroupproject/Forensics"
    # Define file types to search for. In this case, we are looking for SQL and txt file (could be extended to other file types)
    file_types = ["*.sql", "*.txt"]
    
    # Create a DirectorySearchAgent and get the list of matching files
    ds_agent = DirectorySearchAgent(dir, file_types)
    dirlist = ds_agent.getdirectories()

    # Set the archive directory
    archive_dir = "/Users/joaotorres/Desktop/MSc AI - Programming/Intelligent Agents/reuessexgroupproject/Archive"
    
    # Create an ArchiveFiles object and copy files to the archive directory
    archive = ArchiveFiles(dirlist, archive_dir)
    archive.archivefiles(move=0)  # 0 means copy, not move. This is better for testing purposes as we don't want to lose the original files

    # Generate metadata for the archived files
    metadata = WriteMetaData(archive_dir, file_types)
    metadata.logFileMetadata()
