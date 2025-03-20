import json
import csv
import io


def json_to_csv(json_str):
    """Convert JSON ad group data to CSV with ad_group only in first row."""
    if isinstance(json_str, str):
        data = json.loads(json_str)
    else:
        data = json_str

    output = io.StringIO()
    csv_writer = csv.writer(output)
    header = ['ad_group', 'keyword', 'copy_title', 'copy_description']
    csv_writer.writerow(header)

    for item in data:
        ad_group = item.get('ad_group', '')
        keywords = item.get('keywords', [])
        copy_titles = item.get('copy_title', [])
        copy_descriptions = item.get('copy_description', [])

        max_length = max(
            len(keywords),
            len(copy_titles),
            len(copy_descriptions)
        )

        # Removed empty group handling
        for i in range(max_length):
            # Populate ad_group only in the first row
            ad_group_value = ad_group if i == 0 else ''
            keyword = keywords[i] if i < len(keywords) else ''
            title = copy_titles[i] if i < len(copy_titles) else ''
            description = copy_descriptions[i] if i < len(copy_descriptions) else ''

            csv_writer.writerow([ad_group_value, keyword, title, description])

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