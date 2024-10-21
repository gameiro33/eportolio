import pytest
import os
import shutil
from directorySearchAgent import DirectorySearchAgent, ArchiveFiles

@pytest.fixture
def test_directory():
    # Create a temporary directory structure for testing
    test_dir = 'test_directory'
    sub_dir = os.path.join(test_dir, 'sub_directory')
    os.makedirs(sub_dir, exist_ok=True)
    
    # Create some test files
    open(os.path.join(test_dir, 'file1.txt'), 'w').close()
    open(os.path.join(test_dir, 'file2.sql'), 'w').close()
    open(os.path.join(sub_dir, 'file3.txt'), 'w').close()
    open(os.path.join(sub_dir, 'file4.jpg'), 'w').close()

    yield test_dir

    # Cleanup after tests
    shutil.rmtree(test_dir)

@pytest.fixture
def archive_setup():
    # Create temporary source and archive directories
    source_dir = 'source_dir'
    archive_dir = 'archive_dir'
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)
    
    # Create some test files
    test_files = ['file1.txt', 'file2.sql']
    for file in test_files:
        open(os.path.join(source_dir, file), 'w').close()

    yield source_dir, archive_dir, test_files

    # Cleanup after tests
    shutil.rmtree(source_dir)
    shutil.rmtree(archive_dir)

def test_getdirectories(test_directory):
    agent = DirectorySearchAgent(test_directory, ['*.txt', '*.sql'])
    result = agent.getdirectories()
    
    expected = [
        os.path.join(test_directory, 'file1.txt'),
        os.path.join(test_directory, 'file2.sql'),
        os.path.join(test_directory, 'sub_directory', 'file3.txt')
    ]
    
    assert set(result) == set(expected)

def test_archivefiles_copy(archive_setup):
    source_dir, archive_dir, test_files = archive_setup
    source_files = [os.path.join(source_dir, file) for file in test_files]
    archiver = ArchiveFiles(source_files, archive_dir)
    archiver.archivefiles(move=0)

    # Check if files are copied to archive directory
    for file in test_files:
        assert os.path.exists(os.path.join(archive_dir, file))
    
    # Check if original files still exist in source directory
    for file in test_files:
        assert os.path.exists(os.path.join(source_dir, file))

def test_archivefiles_move(archive_setup):
    source_dir, archive_dir, test_files = archive_setup
    source_files = [os.path.join(source_dir, file) for file in test_files]
    archiver = ArchiveFiles(source_files, archive_dir)
    archiver.archivefiles(move=1)

    # Check if files are moved to archive directory
    for file in test_files:
        assert os.path.exists(os.path.join(archive_dir, file))
    
    # Check if original files no longer exist in source directory
    for file in test_files:
        assert not os.path.exists(os.path.join(source_dir, file))
