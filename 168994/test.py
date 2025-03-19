import json
import csv
import io

def json_to_csv(json_data):
    """
    Convert JSON data to CSV format.
    
    Args:
        json_data (str): JSON string with the structure:
            [{ad_group: string, keywords: string[], copy_title: string[], copy_description:[]}]
    
    Returns:
        str: CSV formatted string
    """
    # Parse JSON string if it's a string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    # Create CSV in memory
    output = io.StringIO()
    csv_writer = csv.writer(output)
    
    # Write header row
    header = ['ad_group', 'keyword', 'copy_title', 'copy_description']
    csv_writer.writerow(header)
    
    # Write data rows
    for item in data:
        ad_group = item.get('ad_group', '')
        keywords = item.get('keywords', [])
        copy_titles = item.get('copy_title', [])
        copy_descriptions = item.get('copy_description', [])
        
        # Find the maximum length among arrays
        max_length = max(
            len(keywords),
            len(copy_titles),
            len(copy_descriptions)
        )
        
        # If all arrays are empty, write one row with just the ad_group
        if max_length == 0:
            csv_writer.writerow([ad_group, '', '', ''])
            continue
        
        # Write rows, padding shorter arrays with empty strings
        for i in range(max_length):
            keyword = keywords[i] if i < len(keywords) else ''
            title = copy_titles[i] if i < len(copy_titles) else ''
            description = copy_descriptions[i] if i < len(copy_descriptions) else ''
            
            csv_writer.writerow([ad_group, keyword, title, description])
    
    # Get the CSV as a string
    result = output.getvalue()
    output.close()
    
    return result


# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = [
        {
            "ad_group": "Shoes",
            "keywords": ["running shoes", "athletic footwear", "sports shoes"],
            "copy_title": ["Best Running Shoes", "Premium Athletic Footwear"],
            "copy_description": ["High quality running shoes for athletes", "Durable footwear for all sports"]
        },
        {
            "ad_group": "Clothing",
            "keywords": ["t-shirts", "shorts"],
            "copy_title": ["Comfortable T-shirts", "Athletic Shorts"],
            "copy_description": ["100% cotton t-shirts", "Breathable shorts for sports"]
        }
    ]
    
    # Convert to CSV
    csv_output = json_to_csv(sample_data)
    
    # Print result
    print(csv_output)
    
    # Optionally save to file
    with open('output.csv', 'w', newline='') as f:
        f.write(csv_output)