import pandas as pd
import json
import msgpack
import os

def load_sessions_data():
    """Load and flatten sessions data"""
    with open('../data/sessions.json', 'r') as f:
        sessions = json.load(f)
    
    flattened_data = []
    
    for session in sessions:
        base_data = {
            'code': session.get('code'),
            'title': session.get('title'),
            'abstract': session.get('abstract'),
            'type': session.get('type'),
            'length': session.get('length'),
            'sessionID': session.get('sessionID')
        }
        
        # Flatten all attributes
        attrs = session.get('attributes', {})
        for attr_name in ['roles', 'topics', 'level', 'features', 'services', 'industries', 'segments', 'areas_of_interest']:
            base_data[attr_name] = attrs.get(attr_name, [])
        
        flattened_data.append(base_data)
    
    return pd.DataFrame(flattened_data)

def create_messagepack_file():
    """Create MessagePack version of sessions.json for faster loading"""
    print("Creating MessagePack file...")
    
    # Load original JSON data
    with open('../data/sessions.json', 'r') as f:
        # amazonq-ignore-next-line
        sessions_data = json.load(f)
    
    # Save as MessagePack (compatible with both Python and Node.js)
    with open('../data/sessions.msgpack', 'wb') as f:
        msgpack.pack(sessions_data, f, use_bin_type=True)
    
    # Get file sizes for comparison
    json_size = os.path.getsize('../data/sessions.json')
    msgpack_size = os.path.getsize('../data/sessions.msgpack')
    compression_ratio = (1 - msgpack_size / json_size) * 100
    
    print(f"MessagePack file created successfully!")
    print(f"JSON size: {json_size:,} bytes")
    print(f"MessagePack size: {msgpack_size:,} bytes")
    print(f"Size reduction: {compression_ratio:.1f}%")

def process_attribute(attribute_name, folder_name=None):
    """Generic function to process any attribute"""
    if folder_name is None:
        folder_name = attribute_name
    
    df = load_sessions_data()
    folder_path = f'../data/{folder_name}'
    os.makedirs(folder_path, exist_ok=True)
    
    # Get all values for this attribute
    all_values = []
    for values_list in df[attribute_name]:
        all_values.extend(values_list)
    
    if not all_values:
        print(f"No data found for {attribute_name}")
        return
    
    value_counts = pd.Series(all_values).value_counts()
    
    # Create distribution file
    dist_df = pd.DataFrame({
        attribute_name.rstrip('s'): value_counts.index,
        'session_count': value_counts.values,
        'percentage': (value_counts.values / len(df) * 100).round(2)
    })
    dist_df.to_csv(f'{folder_path}/distribution.csv', index=False)
    
    # Create individual session files
    for value in value_counts.index:
        value_sessions = []
        for _, session in df.iterrows():
            if value in session[attribute_name]:
                value_sessions.append({
                    'code': session['code'],
                    'title': session['title'],
                    'type': session['type']
                })
        
        if value_sessions:
            value_df = pd.DataFrame(value_sessions)
            safe_filename = value.replace('/', '_').replace(' ', '_').replace('&', 'and').replace('(', '').replace(')', '').replace('-', '_').lower()
            value_df.to_csv(f'{folder_path}/{safe_filename}_sessions.csv', index=False)
    
    print(f"Processed {attribute_name}: {len(value_counts)} unique values")

def process_all_attributes():
    """Process all session attributes"""
    print("Processing all session attributes...")
    
    # Process each attribute type
    process_attribute('roles')
    process_attribute('segments') 
    process_attribute('topics')
    process_attribute('services')
    process_attribute('level', 'levels')
    process_attribute('features')
    process_attribute('areas_of_interest')
    process_attribute('industries')
    
    print("\nAll attributes processed successfully!")

if __name__ == "__main__":
    # Process all attributes first
    process_all_attributes()
    
    # Create MessagePack file for faster loading
    # amazonq-ignore-next-line
    create_messagepack_file()
