import streamlit as st
import requests
import re

def fetch_trending_posts(cookie_components, csrf_token):
    headers = {
        "Cookie": "; ".join(cookie_components),
        "X-CSRF-Token": csrf_token
    }
    response = requests.get("https://api.yodayo.com/v1/search/posts/trending?include_nsfw=true", headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        st.error(f"Error fetching posts. Status code: {response.status_code}")
        st.write(f"Error response: {response.text}")
        return []

    st.write(f"Response content: {response.content}")
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

def main():
    st.title("Trending Posts Analysis")

    # Input cookie components
    gorilla_csrf = st.text_input("Enter _gorilla_csrf:", "_gorilla_csrf=MTcxMTA3OTM1M3xJbWM1VUhkSFNGSllSaTlpY1ZodFJHeDBRVWRZZG5aR05FdEphRVIwZWl0c1YySlNNMWswT1hoYVNIYzlJZ089fJOG6jVATH8dgF0Mymy3gXAXlIRMp2I7rcmTg3SuisFo")
    access_token = st.text_input("Enter access_token:", "access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozODU3MTksImV4cCI6MTcxMTY4NDE1M30.n_bT2cjnI11GoUIDgd_AbomLAIz37jJtAYAgCLfdgyHjwIzo7-C_03dBa5zPYcB-nqwxAmUz8CoTVtsgAYod4bz76nkRNxdXjfDsd3nCqMJ2qxEVDYLGacNKLLicSnuVo2NHv0moj2d7K9djZJbQsyUr-gAj_9uvSNx0Hh8gg74uYO9Drt1UrivPqX-D_We9bGV1dfrCWpJAzC9IvLXhZgZFmve945_IkiHgkjIII44_xlwIZ79zXcAK0ACQdpiKrURJAVhE4SiZ5lxXJuCBVHoPpPijuHC-eOe6AuEfRjxdiZ-JnJc5lkZgOV9NnBaVpzT6Xm88sPtTcEt24vxvT0pUVBQDLiulce5qxibzHVTByVma2UCqa-paG6VvaqUSuA4kRBHO9w1GtfMNQB3TF0LCblIuqq99mElioIcTDli-tq05FFBe33-taZxxJVcU3H4DhfZRQfFCKAfFCVl_bfo6ukybMv2ubTwWHjNpqmrVZ0ADLLdgp2X_xjksZAGPpBpc9cKlzLEpvA7LAHYC1O4QVp6-1M0n1R8tvBuQ76AyZTX8y0yzYrJX3mlEkcBYseySdxL-bOVdtglWn2FFjmWPDHhhWb_feXfOEZKqgraw4O7wTH_uIdAxNS6x6IRiggasqJbsOktcVmmUNbkhjtobztMQtXtAG0DxGyevDhk")
    session_uuid = st.text_input("Enter session_uuid:", "session_uuid=2217dc62-ea78-4ba7-9f7f-93684bf840b6")
    csrf_token = st.text_input("Enter X-CSRF-Token:", "waZxH9cm56MaLLVNgNNDF7awzAIu0cJ5mlRDImEYaiFCdYEHo3HwVfBy1ag00tSpR8jkim1m/dzD4DRB7mkOXQ==")

    if st.button("Fetch Posts"):
        cookie_components = [gorilla_csrf, access_token, session_uuid]
        posts = fetch_trending_posts(cookie_components, csrf_token)
        st.write(f"Total posts fetched: {len(posts)}")

        # Display post details
        for post in posts:
            st.subheader(post["title"])
            st.write(f"User: {post['profile']['name']}")
            st.write(f"Likes: {post['likes']}")
            st.write(f"Description: {post['description']}")
            st.write(f"NSFW: {post['nsfw']}")
            st.write(f"Hashtags: {', '.join(post['hashtags'])}")
            for media in post["photo_media"]:
                st.image(media["url"])
            st.write("---")

if __name__ == "__main__":
    main()
