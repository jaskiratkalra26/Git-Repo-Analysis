import os
import logging
from dotenv import load_dotenv

# Import our custom modules
from settings import get_github_token, DEFAULT_CLONE_DIR
from core.repo_manager import RepoManager
from core.project_loader import ProjectLoader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for Phase-1 of the AI Code Review System.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    print("=== AI Code Review System: Phase 1 Setup ===")
    
    # 1. Ask user for repo_url
    repo_url = input("Enter GitHub Repository URL: ").strip()
    if not repo_url:
        logger.error("Error: Repository URL cannot be empty.")
        return

    # 2. Try to read GitHub token
    token = get_github_token()
    if token:
        logger.info("GitHub token found in environment.")
    else:
        logger.info("No GITHUB_TOKEN found. Proceeding with public access.")

    # 3. Initialize RepoManager
    try:
        repo_manager = RepoManager(DEFAULT_CLONE_DIR)
        
        # 4. Clone Repo
        logger.info("Starting cloning process...")
        project_path = repo_manager.clone_repository(repo_url, token)
        
        print(f"\nRepository cloned successfully.\nPath: {project_path}\n")

        # 5. Initialize ProjectLoader
        project_loader = ProjectLoader(project_path)

        # 6. Validate Project
        if project_loader.validate_project():
            print("Project validated.")
            
            # 7. Get and print metadata
            metadata = project_loader.get_project_metadata()
            print(f"Total files: {metadata['total_files']}")
            print(f"Total directories: {metadata['total_dirs']}")
        else:
            logger.error("Project validation failed. The cloned directory might be empty or invalid.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
