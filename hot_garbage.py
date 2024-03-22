import re

def fetch_trending_posts(cookie):
    headers = {
        "Cookie": cookie
    }
    response = requests.get("https://api.yodayo.com/v1/search/posts/trending?include_nsfw=true", headers=headers)
    response_text = response.text

    # Find the start and end indices of the "posts" list
    start_index = response_text.find('"posts":[') + len('"posts":')
    end_index = response_text.rfind("]}")

    # Extract the "posts" list as a string
    posts_str = response_text[start_index:end_index+1]

    # Split the posts string by '{' to get individual post objects
    post_objects = ['{' + obj for obj in posts_str.split('{')[1:]]

    # Parse each post object and extract the required data
    posts = []
    for post_obj in post_objects:
        post = {}
        post["title"] = re.search(r'"title":"(.+?)"', post_obj).group(1)
        post["description"] = re.search(r'"description":"(.+?)"', post_obj).group(1)
        post["likes"] = int(re.search(r'"likes":(\d+)', post_obj).group(1))
        post["nsfw"] = re.search(r'"nsfw":(\w+)', post_obj).group(1) == "true"
        post["hashtags"] = re.findall(r'"(.+?)"', re.search(r'"hashtags":\[(.+?)\]', post_obj).group(1))
        post["photo_media"] = [{"url": re.search(r'"url":"(.+?)"', media_obj).group(1)}
                               for media_obj in re.findall(r'{"uuid":".+?"sort_order":1.+?}', post_obj)]
        posts.append(post)

    return posts
