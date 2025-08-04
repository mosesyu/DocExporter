"""
Script to copy a specific folder from a GitHub repository using SSH.
No git history is preserved - only the files are copied.
"""

import os
import shutil
import tempfile
import subprocess
import sys
import stat
from config_utils import load_config

# Load configuration from JSON file
config = load_config()
github_config = config['github']

# Configuration from config file
REPO_URL = github_config['repo_url']
FOLDER_PATH = github_config['folder_path']
DESTINATION = github_config['destination']
TEMP_DIR = github_config.get('temp_dir', './temp')  # Optional with default

def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        raise


def remove_readonly(func, path, excinfo):
    """Remove read-only attribute and retry deletion."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_rmtree(path):
    """Safely remove directory tree, handling read-only files on Windows."""
    if os.path.exists(path):
        shutil.rmtree(path, onerror=remove_readonly)


def clone_repo_ssh_sparse(repo_url, temp_dir, folder_path):
    """Clone the repository using SSH with sparse-checkout to get only the specified folder."""
    print(f"Cloning repository with sparse-checkout: {repo_url}")
    print(f"Target folder: {folder_path}")
    
    # Initialize empty git repository
    run_command(f"git init", cwd=temp_dir)
    
    # Add remote origin
    run_command(f"git remote add origin {repo_url}", cwd=temp_dir)
    
    # Enable sparse-checkout
    run_command("git config core.sparseCheckout true", cwd=temp_dir)
    
    # Set sparse-checkout pattern
    sparse_checkout_file = os.path.join(temp_dir, ".git", "info", "sparse-checkout")
    os.makedirs(os.path.dirname(sparse_checkout_file), exist_ok=True)
    with open(sparse_checkout_file, 'w') as f:
        f.write(f"{folder_path}/*\n")
    
    # Pull only the specified folder
    print("Downloading only the specified folder...")
    run_command("git pull origin master --depth 1", cwd=temp_dir)
    
    print(f"Sparse checkout completed to: {temp_dir}")


def copy_folder(source_folder, destination_folder):
    """Copy the specified folder from the cloned repo to the destination."""
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"Source folder not found: {source_folder}")
    
    # Create destination directory if it doesn't exist
    if destination_folder != "." and os.path.dirname(destination_folder):
        os.makedirs(os.path.dirname(destination_folder), exist_ok=True)
    
    # Remove destination if it already exists
    if os.path.exists(destination_folder):
        print(f"Removing existing destination: {destination_folder}")
        safe_rmtree(destination_folder)
    
    print(f"Copying folder from {source_folder} to {destination_folder}")
    shutil.copytree(source_folder, destination_folder)
    print("Folder copied successfully!")


def main():
    """Main function to execute the folder copying process."""
    # Validate configuration
    if not REPO_URL or REPO_URL == "git@github.com:username/repository.git":
        print("Error: Please configure REPO_URL with your actual repository URL")
        print("Example: REPO_URL = 'git@github.com:microsoft/vscode.git'")
        sys.exit(1)
    
    if not FOLDER_PATH:
        print("Error: Please configure FOLDER_PATH with the folder you want to copy")
        print("Example: FOLDER_PATH = 'src/vs/editor'")
        sys.exit(1)
    
    if not DESTINATION:
        print("Error: Please configure DESTINATION with your target location")
        print("Example: DESTINATION = './my_copied_folder'")
        sys.exit(1)
    
    # Create temporary directory
    if TEMP_DIR:
        temp_dir = TEMP_DIR
        os.makedirs(temp_dir, exist_ok=True)
    else:
        temp_dir = tempfile.mkdtemp(prefix="github_clone_")
    
    try:
        # Clone the repository with sparse-checkout
        clone_repo_ssh_sparse(REPO_URL, temp_dir, FOLDER_PATH)
        
        # Extract repo name from URL
        repo_name = REPO_URL.split('/')[-1].replace('.git', '')
        
        # Construct paths
        source_folder = os.path.join(temp_dir, FOLDER_PATH)
        destination_folder = os.path.abspath(os.path.join(DESTINATION, repo_name))
        
        # Copy the folder
        copy_folder(source_folder, destination_folder)
        
        print(f"\nSuccess! Folder '{FOLDER_PATH}' has been copied to '{destination_folder}'")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            print(f"Cleaning up temporary directory: {temp_dir}")
            safe_rmtree(temp_dir)

main()