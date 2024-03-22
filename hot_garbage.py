import requests
import streamlit as st

# Function to fetch data from the API
def fetch_data(page=1, size=50):
    url = f"https://api.yodayo.com/v1/search/posts/trending?include_nsfw=true"
    headers = {
        "X-CSRF-Token": st.secrets["X-CSRF-Token"],  # Use st.secrets to access the X-CSRF-Token secret
        "_gorilla_csrf": st.secrets["_gorilla_csrf"],  # Use st.secrets to access the _gorilla_csrf secret
        "Authorization": f"Bearer {st.secrets['access_token']}"  # Add Authorization header if needed
    }
    payload = {
        "page": {
            "current": page,
            "size": size
        },
        "top_time": "day"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Function to process the data
def process_data(data):
    nsfw_count = {
        "true": 0,
        "false": 0
    }
    unique_names = set()
    total_posts = data["page"]["total_results"]

    for post in data["posts"]:
        if post["nsfw"]:
            nsfw_count["true"] += 1
        else:
            nsfw_count["false"] += 1

        unique_names.add(post["profile"]["name"])

    nsfw_percentages = {
        "true": (nsfw_count["true"] / total_posts) * 100,
        "false": (nsfw_count["false"] / total_posts) * 100
    }

    return nsfw_count, nsfw_percentages, len(unique_names), total_posts

# Streamlit app
def app():
    st.title("Yodayo API Data Processing")

    # Fetch data from the API
    data = fetch_data()

    # Process the data
    nsfw_count, nsfw_percentages, unique_name_count, total_posts = process_data(data)

    # Display the results
    st.subheader("NSFW Count")
    st.write(f"True: {nsfw_count['true']}")
    st.write(f"False: {nsfw_count['false']}")

    st.subheader("NSFW Percentages")
    st.write(f"True: {nsfw_percentages['true']:.2f}%")
    st.write(f"False: {nsfw_percentages['false']:.2f}%")

    st.subheader("Number of Unique Names")
    st.write(unique_name_count)

    st.subheader("Total Posts")
    st.write(total_posts)

if __name__ == "__main__":
    app()
