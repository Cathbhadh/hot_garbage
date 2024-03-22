import streamlit as st
import requests
import json

# Function to fetch data from the API
def fetch_data():
    url = "https://api.yodayo.com/v1/search/posts/trending?include_nsfw=true"
    headers = {
        "Cookie": "_gorilla_csrf=MTcxMTA5MjQwMHxJbVZIYmtkUGRtWlhSMmRWVlVkMVJsVkJSM2t5TUZkdlFtaHNTRWRwVW1Gd2FrdHJSMGQ0UVhFellVRTlJZ289fOntumACkEjK3RFvg1K07DtcfgLSup16Qu7-0IcbmMWz; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozODU3MTksImV4cCI6MTcxMTY4NDE1M30.n_bT2cjnI11GoUIDgd_AbomLAIz37jJtAYAgCLfdgyHjwIzo7-C_03dBa5zPYcB-nqwxAmUz8CoTVtsgAYod4bz76nkRNxdXjfDsd3nCqMJ2qxEVDYLGacNKLLicSnuVo2NHv0moj2d7K9djZJbQsyUr-gAj_9uvSNx0Hh8gg74uYO9Drt1UrivPqX-D_We9bGV1dfrCWpJAzC9IvLXhZgZFmve945_IkiHgkjIII44_xlwIZ79zXcAK0ACQdpiKrURJAVhE4SiZ5lxXJuCBVHoPpPijuHC-eOe6AuEfRjxdiZ-JnJc5lkZgOV9NnBaVpzT6Xm88sPtTcEt24vxvT0pUVBQDLiulce5qxibzHVTByVma2UCqa-paG6VvaqUSuA4kRBHO9w1GtfMNQB3TF0LCblIuqq99mElioIcTDli-tq05FFBe33-taZxxJVcU3H4DhfZRQfFCKAfFCVl_bfo6ukybMv2ubTwWHjNpqmrVZ0ADLLdgp2X_xjksZAGPpBpc9cKlzLEpvA7LAHYC1O4QVp6-1M0n1R8tvBuQ76AyZTX8y0yzYrJX3mlEkcBYseySdxL-bOVdtglWn2FFjmWPDHhhWb_feXfOEZKqgraw4O7wTH_uIdAxNS6x6IRiggasqJbsOktcVmmUNbkhjtobztMQtXtAG0DxGyevDhk; session_uuid=2217dc62-ea78-4ba7-9f7f-93684bf840b6",
        "X-CSRF-Token": "SL79mfkhUYI0RTc7QvpPqemuH8/85bPAyIEJAFob0Qcw1zujDvdLhyBf1m9Clvl4g6+ZnjpspWlEKA8bSjEMpw=="
    }
    body = {
        "page": {
            "current": 1,
            "size": 5
        },
        "top_time": "day"
    }
    response = requests.get(url, headers=headers, json=body)
    data = response.json()
    return data

# Main Streamlit app
def main():
    st.title("Trending Posts Analysis")

    # Fetch data from the API
    data = fetch_data()

    # Display the number of posts
    num_posts = len(data["posts"])
    st.write(f"Total number of posts: {num_posts}")

    # Display post details
    for post in data["posts"]:
        st.subheader(post["title"])
        st.write(f"Description: {post['description']}")
        st.write(f"Likes: {post['likes']}")
        st.write(f"Hashtags: {', '.join(post['hashtags'])}")
        st.image(post["photo_media"][0]["url"])
        st.write("---")

if __name__ == "__main__":
    main()
