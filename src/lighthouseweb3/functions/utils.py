#!/usr/bin/env python3

from io import BufferedReader, BytesIO
import os
from typing import List, Tuple, Dict, Any, BinaryIO


class NamedBufferedReader:
    """
    A wrapper class for BufferedReader that includes a name attribute.
    Useful for handling named file-like objects.
    """
    
    def __init__(self, buffer: BytesIO, name: str):
        """
        Initialize NamedBufferedReader.
        
        :param buffer: BytesIO object to read from
        :param name: Name to associate with the buffer
        :raises ValueError: If name is empty or invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        if not isinstance(buffer, BytesIO):
            raise ValueError("Buffer must be a BytesIO instance")
            
        self.reader = BufferedReader(buffer)
        self.name = name

    def read(self, *args, **kwargs) -> bytes:
        """Read from the underlying buffer."""
        return self.reader.read(*args, **kwargs)

    def close(self) -> None:
        """Close the underlying buffer."""
        self.reader.close()


def walk_dir_tree(path: str) -> Tuple[List[str], str]:
    """
    Walk through directory tree and collect file paths.
    
    :param path: Root directory path to walk through
    :return: Tuple of (list of file paths, root directory path)
    :raises ValueError: If path is invalid or doesn't exist
    """
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string")
    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")
    
    file_list = []
    roots = []
    
    try:
        for root, _, files in os.walk(path):
            roots.append(root)
            for file in files:
                file_list.append(os.path.join(root, file))
        
        if not roots:
            raise ValueError(f"No valid directory found at path: {path}")
            
        return file_list, roots[0]
    except Exception as e:
        raise ValueError(f"Failed to walk directory tree: {str(e)}")


def is_dir(path: str) -> bool:
    """
    Check if path points to a directory.
    
    :param path: Path to check
    :return: True if path is a directory, False otherwise
    :raises ValueError: If path is invalid
    """
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string")
    return os.path.isdir(path)


def extract_file_name(file: str) -> str:
    """
    Extract filename from file path.
    
    :param file: File path
    :return: Extracted filename
    :raises ValueError: If file path is invalid
    """
    if not file or not isinstance(file, str):
        raise ValueError("File path must be a non-empty string")
    return os.path.basename(file)  # Using os.path.basename instead of split


def extract_file_name_with_source(file: str, source: str) -> str:
    """
    Extract filename while preserving source directory structure.
    
    :param file: File path
    :param source: Source directory path
    :return: Extracted filename with source structure
    :raises ValueError: If file or source paths are invalid
    """
    if not file or not isinstance(file, str):
        raise ValueError("File path must be a non-empty string")
    if not source or not isinstance(source, str):
        raise ValueError("Source path must be a non-empty string")
        
    source = source.rstrip('/')  # Remove trailing slash if present
    base = os.path.basename(source)
    return base + file.split(base)[-1]


def read_files_for_upload(files: Dict[str, Any]) -> List[Tuple[str, Tuple[str, BinaryIO, str]]]:
    """
    Prepare files for upload by creating appropriate tuples with file information.
    
    :param files: Dictionary containing file information
    :return: List of tuples containing file upload information
    :raises ValueError: If files dictionary is invalid
    """
    if not isinstance(files, dict):
        raise ValueError("Files must be a dictionary")
    if "files" not in files or "is_dir" not in files or "path" not in files:
        raise ValueError("Files dictionary missing required keys")
        
    file_list = []
    try:
        for file in files["files"]:
            if not os.path.exists(file):
                raise ValueError(f"File does not exist: {file}")
                
            name = (extract_file_name_with_source(file, files["path"]) 
                   if files["is_dir"] 
                   else extract_file_name(file))
                   
            file_list.append(
                (
                    "file",
                    (
                        name,
                        open(file, "rb"),
                        "application/octet-stream",
                    ),
                )
            )
        return file_list
    except Exception as e:
        # Clean up any opened files if an error occurs
        for item in file_list:
            try:
                item[1][1].close()
            except:
                pass
        raise ValueError(f"Failed to prepare files for upload: {str(e)}")


def close_files_after_upload(files: List[Tuple[str, Tuple[str, BinaryIO, str]]]) -> None:
    """
    Close all file handles after upload.
    
    :param files: List of file tuples containing file handles
    """
    if files:
        for file in files:
            try:
                if file and len(file) > 1 and len(file[1]) > 1:
                    file[1][1].close()
            except Exception:
                # Continue closing other files even if one fails
                pass
