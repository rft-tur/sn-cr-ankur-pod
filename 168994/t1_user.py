import json, csv, io

def json2csv(jsonStr):
    
    if isinstance(jsonStr, str):
        data = json.loads(jsonStr)
    else:
        data = jsonStr
    
    output = io.StringIO()
    csvWriter = csv.writer(output)
    
    header = ['ad_group', 'keyword', 'copy_title', 'copy_description']
    csvWriter.writerow(header)
    
    for item in data:
        adGroup = item.get('ad_group', '')
        keywords = item.get('keywords', [])
        copyTitles = item.get('copy_title', [])
        copyDescriptions = item.get('copy_description', [])
        
        maxLength = max(
            len(keywords),
            len(copyTitles),
            len(copyDescriptions)
        )
        
        if maxLength == 0:
            csvWriter.writerow([adDroup, '', '', ''])
            continue
        
        for i in range(maxLength):
            keyword = keywords[i] if i < len(keywords) else ''
            title = copyTitles[i] if i < len(copyTitles) else ''
            description = copyDescriptions[i] if i < len(copyDescriptions) else ''
            
            csvWriter.writerow([adGroup, keyword, title, description])
    
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
    csv_output = json2csv(sample_data)
    
    # Print result
    print(csv_output)
    
    # Optionally save to file
    with open('output.csv', 'w', newline='') as f:
        f.write(csv_output)