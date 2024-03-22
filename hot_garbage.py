import ast
import streamlit as st
import requests
import json

def fetch_trending_posts(cookie):
    headers = {
        "Cookie": cookie
    }
    response = requests.get("https://api.yodayo.com/v1/search/posts/trending?include_nsfw=true", headers=headers)
    content = response.content.decode('utf-8')
    data = ast.literal_eval(content)
    posts = data["posts"]
    return posts


def main():
    st.title("Trending Posts Analysis")

    # Input cookie
    cookie_input = st.text_input("Enter cookie:", "_gorilla_csrf=MTcxMTA3OTM1M3xJbWM1VUhkSFNGSllSaTlpY1ZodFJHeDBRVWRZZG5aR05FdEphRVIwZWl0c1YySlNNMWswT1hoYVNIYzlJZ089fJOG6jVATH8dgF0Mymy3gXAXlIRMp2I7rcmTg3SuisFo; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozODU3MTksImV4cCI6MTcxMTY4NDE1M30.n_bT2cjnI11GoUIDgd_AbomLAIz37jJtAYAgCLfdgyHjwIzo7-C_03dBa5zPYcB-nqwxAmUz8CoTVtsgAYod4bz76nkRNxdXjfDsd3nCqMJ2qxEVDYLGacNKLLicSnuVo2NHv0moj2d7K9djZJbQsyUr-gAj_9uvSNx0Hh8gg74uYO9Drt1UrivPqX-D_We9bGV1dfrCWpJAzC9IvLXhZgZFmve945_IkiHgkjIII44_xlwIZ79zXcAK0ACQdpiKrURJAVhE4SiZ5lxXJuCBVHoPpPijuHC-eOe6AuEfRjxdiZ-JnJc5lkZgOV9NnBaVpzT6Xm88sPtTcEt24vxvT0pUVBQDLiulce5qxibzHVTByVma2UCqa-paG6VvaqUSuA4kRBHO9w1GtfMNQB3TF0LCblIuqq99mElioIcTDli-tq05FFBe33-taZxxJVcU3H4DhfZRQfFCKAfFCVl_bfo6ukybMv2ubTwWHjNpqmrVZ0ADLLdgp2X_xjksZAGPpBpc9cKlzLEpvA7LAHYC1O4QVp6-1M0n1R8tvBuQ76AyZTX8y0yzYrJX3mlEkcBYseySdxL-bOVdtglWn2FFjmWPDHhhWb_feXfOEZKqgraw4O7wTH_uIdAxNS6x6IRiggasqJbsOktcVmmUNbkhjtobztMQtXtAG0DxGyevDhk; session_uuid=2217dc62-ea78-4ba7-9f7f-93684bf840b6")

    if st.button("Fetch Posts"):
        posts = fetch_trending_posts(cookie_input)
        st.write(f"Total posts fetched: {len(posts)}")

        # Display post details
        for post in posts:
            st.subheader(post["title"])
            st.write(f"User: {post['profile']['name']}")
            st.write(f"Likes: {post['likes']}")
            st.write(f"Description: {post['description']}")
            st.write(f"NSFW: {post['nsfw']}")
            st.write(f"Hashtags: {', '.join(post['hashtags'])}")
            st.image(post["photo_media"][0]["url"])
            st.write("---")

if __name__ == "__main__":
    main()
