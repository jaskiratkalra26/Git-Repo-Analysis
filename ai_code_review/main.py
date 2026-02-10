import os
import logging
from dotenv import load_dotenv

# Import our custom modules
from settings import get_github_token, DEFAULT_CLONE_DIR
from core.repo_manager import RepoManager
from core.project_loader import ProjectLoader
from scanner.directory_scanner import DirectoryScanner
from scanner.file_collector import FileCollector
from scanner.readme_extractor import ReadmeExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the AI Code Review System.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    print("=== AI Code Review System: Phase 2 ===")
    
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
            print("Project validated successfuly.")

            # --- Phase 2: Project Scanning ---
            print("\nStarting Phase-2: Project Scanning...")

            # 7. Directory Scanner
            scanner = DirectoryScanner(project_path)
            scan_result = scanner.scan()

            # 8. File Collector
            collector = FileCollector(scan_result["all_files"])
            code_files = collector.get_code_files()
            file_type_counts = collector.categorize_files()

            # 9. Readme Extractor
            readme_extractor = ReadmeExtractor(project_path)
            readme_path = readme_extractor.find_readme()
            # We don't necessarily need to print the content, but we extract it as requested.
            readme_content = readme_extractor.extract_content()

            # Summary Output
            print("\n## Project Scan Summary:\n")
            print(f"Total files: {scan_result['total_files']}")
            print(f"Total directories: {scan_result['total_directories']}")
            print(f"Code files detected: {len(code_files)}")

            print("\nFile type distribution:")
            if file_type_counts:
                for ext, count in file_type_counts.items():
                    print(f"{ext}: {count}")
            else:
                print("No supported code files found.")

            print(f"\nREADME found: {'Yes' if readme_path else 'No'}")

        else:
            logger.error("Project validation failed. The cloned directory might be empty or invalid.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
