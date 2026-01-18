from pathlib import Path

def create_directory_structure(base_path, tracks, num_weeks):
    """Create the required folder structure"""
    print("Creating directory structure...")
    
    directories = [
        f"{base_path}/Status Records/Power BI Track",
        f"{base_path}/Status Records/AWS Cloud Track",
        f"{base_path}/Participation Records/Power BI Track",
        f"{base_path}/Participation Records/AWS Cloud Track",
        f"{base_path}/Lab and Quizzes/Power BI Track",
        f"{base_path}/Lab and Quizzes/AWS Cloud Track",
    ]
    
    # Create Zoom attendance directories
    for track in tracks:
        for week in range(1, num_weeks + 1):
            dir_path = f"{base_path}/Zoom Attendance/{track}/Week {week}"
            directories.append(dir_path)
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
