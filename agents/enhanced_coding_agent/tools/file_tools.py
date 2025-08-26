"""
File Tools - Read and Write file operations

These tools handle all file system interactions for the coding agent:
- ReadFileTool: Read files from the workspace
- WriteFileTool: Write generated code and content to files
"""

import os
from typing import Dict, Any
from .base_tool import BaseTool

class ReadFileTool(BaseTool):
    """
    Tool for reading files from the agent's workspace
    
    Handles:
    - Reading solution files
    - Reading log files  
    - Reading any workspace content
    - Error handling for missing files
    """
    
    def __init__(self, workspace_path: str = "workspace"):
        super().__init__("read_file")
        self.workspace_path = workspace_path
    
    def execute(self, filename: str, directory: str = "") -> Dict[str, Any]:
        """
        Read content from a file
        
        Args:
            filename: Name of file to read
            directory: Subdirectory within workspace (optional)
            
        Returns:
            Dict with file content or error
        """
        try:
            # Construct full file path
            if directory:
                file_path = os.path.join(self.workspace_path, directory, filename)
            else:
                file_path = os.path.join(self.workspace_path, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return self.format_result(
                    success=False, 
                    error=f"File not found: {file_path}"
                )
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get file metadata
            file_stats = os.stat(file_path)
            
            return self.format_result(
                success=True,
                result={
                    "content": content,
                    "file_path": file_path,
                    "file_size": file_stats.st_size,
                    "line_count": len(content.split('\n')),
                    "last_modified": file_stats.st_mtime
                }
            )
            
        except UnicodeDecodeError:
            return self.format_result(
                success=False,
                error=f"Cannot read file {filename}: not a text file or encoding issue"
            )
        except PermissionError:
            return self.format_result(
                success=False,
                error=f"Permission denied reading file: {filename}"
            )
        except Exception as e:
            return self.format_result(
                success=False,
                error=f"Error reading file {filename}: {str(e)}"
            )
    
    def get_description(self) -> str:
        return "Read content from files in the agent workspace"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": self.get_description(),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to read"
                        },
                        "directory": {
                            "type": "string", 
                            "description": "Optional subdirectory within workspace (e.g., 'solutions', 'logs')"
                        }
                    },
                    "required": ["filename"]
                }
            }
        }

class WriteFileTool(BaseTool):
    """
    Tool for writing files to the agent's workspace
    
    Handles:
    - Writing generated code solutions
    - Creating log files
    - Saving any workspace content
    - Directory creation as needed
    """
    
    def __init__(self, workspace_path: str = "workspace"):
        super().__init__("write_file")
        self.workspace_path = workspace_path
    
    def execute(self, filename: str, content: str, directory: str = "", 
                overwrite: bool = True) -> Dict[str, Any]:
        """
        Write content to a file
        
        Args:
            filename: Name of file to create/write
            content: Content to write to the file
            directory: Subdirectory within workspace (optional)
            overwrite: Whether to overwrite existing files
            
        Returns:
            Dict with success status and file info
        """
        try:
            # Construct full file path
            if directory:
                dir_path = os.path.join(self.workspace_path, directory)
                file_path = os.path.join(dir_path, filename)
            else:
                dir_path = self.workspace_path
                file_path = os.path.join(self.workspace_path, filename)
            
            # Create directory if it doesn't exist
            os.makedirs(dir_path, exist_ok=True)
            
            # Check if file exists and overwrite policy
            if os.path.exists(file_path) and not overwrite:
                return self.format_result(
                    success=False,
                    error=f"File {filename} already exists and overwrite=False"
                )
            
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Get file info after writing
            file_stats = os.stat(file_path)
            
            return self.format_result(
                success=True,
                result={
                    "file_path": file_path,
                    "bytes_written": file_stats.st_size,
                    "line_count": len(content.split('\n')),
                    "created_new": not os.path.exists(file_path) or overwrite
                }
            )
            
        except PermissionError:
            return self.format_result(
                success=False,
                error=f"Permission denied writing to file: {filename}"
            )
        except OSError as e:
            return self.format_result(
                success=False,
                error=f"OS error writing file {filename}: {str(e)}"
            )
        except Exception as e:
            return self.format_result(
                success=False,
                error=f"Error writing file {filename}: {str(e)}"
            )
    
    def get_description(self) -> str:
        return "Write content to files in the agent workspace, creating directories as needed"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "write_file", 
                "description": self.get_description(),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        },
                        "directory": {
                            "type": "string",
                            "description": "Optional subdirectory within workspace (e.g., 'solutions', 'logs')"
                        },
                        "overwrite": {
                            "type": "boolean",
                            "description": "Whether to overwrite existing files (default: true)"
                        }
                    },
                    "required": ["filename", "content"]
                }
            }
        }
