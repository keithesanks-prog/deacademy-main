import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_operations.log'),
        logging.StreamHandler()
    ]
)

def read_file(filepath):
    """Read a file and handle potential errors."""
    try:
        logging.info(f"Attempting to read file: {filepath}")
        with open(filepath, 'r') as file:
            content = file.read()
        logging.info(f"Successfully read file: {filepath}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None
    except PermissionError:
        logging.error(f"Permission denied when reading: {filepath}")
        return None
    except Exception as e:
        logging.critical(f"Unexpected error reading {filepath}: {str(e)}")
        return None

def write_file(filepath, content):
    """Write content to a file and handle potential errors."""
    try:
        logging.info(f"Attempting to write to file: {filepath}")
        with open(filepath, 'w') as file:
            file.write(content)
        logging.info(f"Successfully wrote to file: {filepath}")
        return True
    except PermissionError:
        logging.error(f"Permission denied when writing to: {filepath}")
        return False
    except OSError as e:
        logging.error(f"OS error when writing to {filepath}: {str(e)}")
        return False
    except Exception as e:
        logging.critical(f"Unexpected error writing to {filepath}: {str(e)}")
        return False

def copy_file(source, destination):
    """Copy a file from source to destination with error handling."""
    try:
        logging.info(f"Attempting to copy {source} to {destination}")
        
        # Check if source exists
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source file does not exist: {source}")
        
        # Read source file
        content = read_file(source)
        if content is None:
            return False
        
        # Write to destination
        success = write_file(destination, content)
        if success:
            logging.info(f"Successfully copied {source} to {destination}")
        return success
        
    except FileNotFoundError as e:
        logging.error(str(e))
        return False
    except Exception as e:
        logging.critical(f"Unexpected error during copy operation: {str(e)}")
        return False

def delete_file(filepath):
    """Delete a file with error handling."""
    try:
        logging.info(f"Attempting to delete file: {filepath}")
        os.remove(filepath)
        logging.info(f"Successfully deleted file: {filepath}")
        return True
    except FileNotFoundError:
        logging.warning(f"File not found (already deleted?): {filepath}")
        return False
    except PermissionError:
        logging.error(f"Permission denied when deleting: {filepath}")
        return False
    except Exception as e:
        logging.critical(f"Unexpected error deleting {filepath}: {str(e)}")
        return False

def create_directory(dirpath):
    """Create a directory with error handling."""
    try:
        logging.info(f"Attempting to create directory: {dirpath}")
        os.makedirs(dirpath, exist_ok=True)
        logging.info(f"Successfully created directory: {dirpath}")
        return True
    except PermissionError:
        logging.error(f"Permission denied when creating directory: {dirpath}")
        return False
    except Exception as e:
        logging.critical(f"Unexpected error creating directory {dirpath}: {str(e)}")
        return False

# Demo: Test the robust file operations
if __name__ == "__main__":
    logging.info("=" * 50)
    logging.info("Starting File Operations Demo")
    logging.info("=" * 50)
    
    # Test 1: Read an existing file
    print("\n--- Test 1: Read existing file ---")
    content = read_file("destination.txt")
    if content:
        print(f"Content: {content[:50]}...")
    
    # Test 2: Try to read a non-existent file
    print("\n--- Test 2: Read non-existent file ---")
    read_file("nonexistent_file.txt")
    
    # Test 3: Write to a new file
    print("\n--- Test 3: Write to new file ---")
    write_file("test_output.txt", "This is a test file created by the automation script.")
    
    # Test 4: Copy a file
    print("\n--- Test 4: Copy file ---")
    copy_file("destination.txt", "destination_backup.txt")
    
    # Test 5: Try to copy a non-existent file
    print("\n--- Test 5: Copy non-existent file ---")
    copy_file("missing_source.txt", "destination.txt")
    
    # Test 6: Create a directory
    print("\n--- Test 6: Create directory ---")
    create_directory("test_logs")
    
    # Test 7: Try to access a protected file (simulated)
    print("\n--- Test 7: Permission error simulation ---")
    # This would fail on a protected system file
    # read_file("C:\\Windows\\System32\\config\\SAM")
    
    logging.info("=" * 50)
    logging.info("File Operations Demo Completed")
    logging.info("=" * 50)
    print("\n✓ Check 'file_operations.log' for detailed logs")
