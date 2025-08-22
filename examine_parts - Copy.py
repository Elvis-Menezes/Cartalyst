import sqlite3
import os

def examine_parts_data():
    """Examine parts data to understand structure and naming patterns."""
    conn = sqlite3.connect('parts.db')
    cursor = conn.cursor()
    
    # Get sample parts data
    cursor.execute("SELECT PartNo, PartDescription, Category FROM parts LIMIT 20")
    parts = cursor.fetchall()
    
    print("Sample Parts Data:")
    print("-" * 80)
    for part_no, description, category in parts:
        print(f"Part No: {part_no}")
        print(f"Description: {description}")
        print(f"Category: {category}")
        print("-" * 40)
    
    # Get unique categories
    cursor.execute("SELECT DISTINCT Category FROM parts")
    categories = cursor.fetchall()
    
    print("\nUnique Categories:")
    print("-" * 40)
    for category in categories:
        print(f"- {category[0]}")
    
    # Check available images
    image_dir = 'static/images/parts'
    if os.path.exists(image_dir):
        images = os.listdir(image_dir)
        print(f"\nAvailable Images ({len(images)}):")
        print("-" * 40)
        for img in images:
            print(f"- {img}")
    
    conn.close()

if __name__ == '__main__':
    examine_parts_data()