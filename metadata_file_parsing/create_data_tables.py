import json
import pandas as pd
from pathlib import Path
import re
# Define the directory containing the JSON files

json_directory = 'D:/metadata_ig/posts_info/info/'

df = pd.read_csv('C:/Users/Marianna/OneDrive/Рабочий стол/IG_project/reduced_file.txt', sep='\t', names=['influencer_name', 'JSON_PostMetadata_file_name', 'Image_file_name', 'Link', 'IfExists'])



# Define lists to collect post data and comment data
posts_data = []
comments_data = []
tagged_users_data = []

def extract_hashtags(caption):
    # The regular expression pattern for matching hashtags
    pattern = r'#\w+'
    # Find all occurrences of the pattern in the caption
    hashtags = re.findall(pattern, caption)
    return hashtags


import csv

# Function to format multiline text correctly for CSV
def format_multiline(text):
    if text is None:
        return ''
    # Replace internal quotes with double quotes
    text = text.replace('"', '""')
    # Enclose in double quotes if not already
    if not (text.startswith('"') and text.endswith('"')):
        text = f'"{text}"'
    return text



# Process each file in the directory
#for json_file in json_directory.glob('*.info'):
'''for json_file in range(len(df)):
    file_name = df['influencer_name'][json_file] + '-' + df['JSON_PostMetadata_file_name'][json_file]
    print(file_name)
    file_path =  json_directory + file_name
    print(file_path)'''
json_directory = Path('D:/metadata_ig/posts_info/info/')
# Iterate over rows in the DataFrame
for index, row in df.iterrows():
    # Construct file name from DataFrame columns
    file_name = f"{row['influencer_name']}-{row['JSON_PostMetadata_file_name']}"
    # Build the full path for the file
    file_path = json_directory / f"{file_name}"

    # Check if the file exists before attempting to open it
    if file_path.exists():
        try:
            # Open and load the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"Data loaded successfully from {file_path}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from {file_path}")
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")
    else:
        print(f"File does not exist: {file_path}")

    '''# Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)'''

    caption = data['edge_media_to_caption']['edges']

    for caption_data in caption:
        caption_text = caption_data['node']['text']
        hashtags = extract_hashtags(caption_text)


    tagged_users = data['edge_media_to_tagged_user']['edges']
    for tagg_data in tagged_users:
        tagg_node = tagg_data['node']

        tagg_users_info = {
            'FileName': file_name,
            'TaggedUsername': tagg_node['user']['username'],
            'TaggedUserFullname': tagg_node['user'].get('full_name', ''),
            'TaggUsrnameID': tagg_node['user']['id'],

        }
        tagged_users_data .append(tagg_users_info)


    # Extract post data
    post_info = {
        'FileName': file_name,
        'OwnerUsername': data['owner']['username'],
        'OwnerFullname': data['owner'].get('full_name', ''),
        'OwnerID': data['owner']['id'],
        'OwnerProfilePic': data['owner'].get('profile_pic_url', ''),
        'PostDescription': data.get('accessibility_caption', ''),
        'LikesNum': data['edge_media_preview_like']['count'],
        'PostID': data['id'],
        'ImageWidth': data['dimensions']['width'],
        'ImageHeight': data['dimensions']['height'],
        'Location': data.get('location', None),
        'Caption':  caption_text,
        'Hashtags': hashtags,
        'CommentsCount': data.get('edge_media_to_parent_comment', {}).get('count', 0)

    }
    posts_data.append(post_info)

    # Extract comments data and flatten the nested structure
    def process_comments(comments, file_name):
        for comment_data in comments:
            comment = comment_data['node']

            comment_info = {
                'FileName': file_name,
                'CommentID': comment['id'],
                'Text': comment.get('text', ''),
                'CreatedAt': comment.get('created_at', ''),
                'DidReportAsSpam': comment.get('did_report_as_spam', False),
                'LikesCount': comment['edge_liked_by']['count'],
                'Owner': comment['owner']['username'], #comment.get('owner', {}).get('username', '')

            }
            comments_data.append(comment_info)
            # Recursively process threaded comments
            if comment.get('edge_threaded_comments', {}).get('count', 0) > 0:
                process_comments(comment.get('edge_media_to_parent_comment', {}).get('edges', []), file_name)

    # Initialize the comment extraction process for top-level comments
    process_comments(data.get('edge_media_to_parent_comment', {}).get('edges', []), file_name)

# Prepare post data with proper formatting
for post in posts_data:
    post['PostDescription'] =  format_multiline(post['PostDescription'])
    post['Caption'] = format_multiline(post['Caption'])
    post['Hashtags'] = format_multiline(str(post['Hashtags']))  # Ensure hashtags are treated as a string

# Prepare comment data with proper formatting
for comment in comments_data:
    comment['Text'] = format_multiline(comment['Text'])



# Define CSV file path
posts_csv_path = 'posts.csv'
comments_csv_path = 'comments.csv'

# Write posts data to a CSV file
with open(posts_csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=list(posts_data[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(posts_data)

# Write comments data to a CSV file
with open(comments_csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=list(comments_data[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(comments_data)



# Create a DataFrame for posts and comments
df_posts = pd.DataFrame(posts_data)
df_comments = pd.DataFrame(comments_data)
df_taggusers = pd.DataFrame(tagged_users_data)

# Save DataFrames to CSV files
df_taggusers.to_csv('tagged_users.csv', index=False)
# Save DataFrames to CSV files
df_posts.to_csv('posts.csv', index=False)
df_comments.to_csv('comments.csv', index=False)
