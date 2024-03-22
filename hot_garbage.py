import requests
import streamlit as st

# Streamlit app
def app():
    st.title("Yodayo API Data Processing")

    # Get user input for tokens and cookies
    x_csrf_token = st.text_input("Enter your X-CSRF-Token:", type="password")
    gorilla_csrf = st.text_input("Enter your _gorilla_csrf:", type="password")
    access_token = st.text_input("Enter your access_token:", type="password")
    session_uuid = st.text_input("Enter your session_uuid:", type="password")

    # Create a session and set the cookies
    session = requests.Session()
    jar = requests.cookies.RequestsCookieJar()
    jar.set("access_token", access_token)
    jar.set("session_uuid", session_uuid)
    session.cookies = jar

    # Function to fetch data from the API
    def fetch_data(page=1, size=50):
        url = f"https://api.yodayo.com/v1/search/posts/trending?include_nsfw=true"
        headers = {
            "X-CSRF-Token": x_csrf_token,
            "_gorilla_csrf": gorilla_csrf,
            "Authorization": f"Bearer {access_token}"
        }
        payload = {
            "page": {
                "current": page,
                "size": size
            },
            "top_time": "day"
        }
        response = session.post(url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Try to parse the response as JSON
                data = response.json()
                return data
            except ValueError:
                st.error("Error: Could not parse the response as JSON.")
        else:
            st.error(f"Error: API request failed with status code {response.status_code}")

        # Return None if there was an error
        return None

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

    # Fetch data from the API
    data = fetch_data()

    # Check if data fetching was successful
    if data is None:
        st.error("Error: Could not fetch data from the API.")
    else:
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
