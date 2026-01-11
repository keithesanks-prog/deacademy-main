import os
import shutil
import glob

# Define categories and patterns
moves = {
    "01_AWS": [
        "aws_*.html", 
        "arch_*.html", 
        "arch_*.png",
        "legacy_data_landscape.png"
    ],
    "02_Snowflake": [
        "snowflake_*.html",
        "snowflake_*.png"
    ],
    "04_Projects": [
        "project_*.html",
        "data_engineering_ecosystem.html"
    ],
    "06_Data_Modeling": [
        "system_design_visual.html",
        "cloud_concepts_visual.html"
    ]
}

base_dir = r"c:\Users\ksank\training"

def organize():
    print(f"Organizing files in {base_dir}...")
    
    for folder, patterns in moves.items():
        target_dir = os.path.join(base_dir, folder)
        os.makedirs(target_dir, exist_ok=True)
        print(f"Created/Verified {target_dir}")
        
        for pattern in patterns:
            # Full path pattern
            full_pattern = os.path.join(base_dir, pattern)
            files = glob.glob(full_pattern)
            
            for f in files:
                filename = os.path.basename(f)
                dest = os.path.join(target_dir, filename)
                
                try:
                    shutil.move(f, dest)
                    print(f"Moved {filename} -> {folder}/")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    organize()
