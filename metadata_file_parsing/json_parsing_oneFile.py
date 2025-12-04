import json

# Load the JSON data from the file with .info extension
with open('/Users/mariannamalaireu/PycharmProjects/IG_project/json_metadata/00s_supermodels-2036456981958560066.info', 'r') as file:
    data = json.load(file)

# Now 'data' is a Python dictionary containing the information from the .info file
print(data)


#probably later
'''"edge_media_preview_like": {
  "count": 256,
  "edges": []
},
"edge_media_to_tagged_user": {
  "edges": []
},'''

import re

def extract_hashtags(caption):
    # The regular expression pattern for matching hashtags
    pattern = r'#\w+'
    # Find all occurrences of the pattern in the caption
    hashtags = re.findall(pattern, caption)
    return hashtags

def process_comments(comments):
    for comment_data in comments:
        comment = comment_data['node']
        text = comment.get('text', '')
        created_at = comment.get('created_at', '')
        did_report_as_spam = comment.get('did_report_as_spam', False)
        likes_count = comment.get('edge_liked_by', {}).get('count', 0)
        comment_id = comment.get('id', '')
        comment_owner = comment.get('owner', {}).get('username', '')
        sub_comment_count = comment.get('edge_threaded_comments', {}).get('count', 0)

        # Print the comment details
        print(f"Comment ID: {comment_id}")
        print(f"Owner: {comment_owner}")
        print(f"Text: {text}")
        print(f"Created at: {created_at}")
        print(f"Reported as spam: {did_report_as_spam}")
        print(f"Likes: {likes_count}")
        print(f"Sub-comments: {sub_comment_count}")
        print()

        # Recursively process the threaded comments
        threaded_comments = comment.get('edge_threaded_comments', {}).get('edges', [])
        process_comments(threaded_comments)


# Accessing the owner of the post
owner_username = data['owner']['username']
owner_fullname = data['owner']['full_name']
owner_id = data['owner']['id']
owner_profile_pic = data['owner']['profile_pic_url']
post_description = data['accessibility_caption']
likes_num = data['edge_media_preview_like']['count']
post_id = data['id']
img_width= data['dimensions']['width']
img_height = data['dimensions']['height']
location = data['location']
timestamp = data['taken_at_timestamp']




tagged_users = data['edge_media_to_tagged_user']['edges']
for tagg_data in  tagged_users:
    tagg_node = tagg_data['node']
    text = tagg_node['user']
    tag_username = tagg_node['user']['username']
    tag_username_id = tagg_node['user']['id']
    tag_user_full_name = tagg_node['user']['full_name']

    print(f"Tagged user: {tag_user_full_name}")






caption = data['edge_media_to_caption']['edges']
hashtags = extract_hashtags(caption)

for caption_data in caption:
    caption_node = caption_data['node']
    caption_text = caption_node['text']
    hashtags = extract_hashtags(caption_text)
    print(f"Hashtags: {hashtags}")
    print(f"Caption Text: {caption_text}")


comments_num = data['edge_media_to_parent_comment']['count']

comments = data['edge_media_to_parent_comment']['edges']

print(process_comments(comments))


# Process the comments
for comment_data in comments:
    comment = comment_data['node']
    text = comment['text']
    created_at = comment['created_at']
    did_report_as_spam = comment['did_report_as_spam']
    likes_count = comment['edge_liked_by']['count']
    comment_id = comment['id']
    comment_owner = comment['owner']['username']
    sub_comment_count = comment['edge_threaded_comments']['count']
    comment['edge_threaded_comments']['edges']
    # Print out the comment details (or process them in some other way)
    print(f"Comment ID: {comment_id}")
    print(f"Text: {text}")
    print(f"Created at: {created_at}")
    print(f"Reported as spam: {did_report_as_spam}")
    print(f"Likes: {likes_count}")
    print()


# Printing owner data
print(f"Owner's Username: {owner_username}")
print(f"Owner's ID: {owner_id}")
print(f"Owner's Profile Picture URL: {owner_profile_pic}")
print(f"The extracted ID is: {post_id}")
# If you need to access other data, follow the correct keys from the JSON you posted
