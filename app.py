import requests
import cohere
import streamlit as st

# Set your API keys here
PIXABAY_API_KEY = '46772125-eaba6b91b742d2daf04199f67'  # Replace with your actual Pixabay API key
GIPHY_API_KEY = 'UhLQkPWbHGlH942nkTRoxkto0cOdTTlT'      # Replace with your actual Giphy API key
COHERE_API_KEY = 'cv2iT1eJhSikUq7HcUeIjiCSKUQdOH1dsvE9HgTB'  # Replace with your actual API key
cohere_client = cohere.Client(COHERE_API_KEY)

# Streamlit app framework
st.title('🦜🔗 YouTube GPT Creator')
prompt = st.text_input('Enter your video topic')

def generate_text(prompt, model='command-xlarge-nightly', max_tokens=1000):
    try:
        response = cohere_client.generate(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.generations[0].text.strip()
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return None

# Functions to fetch images and gifs
def fetch_pixabay_images(query):
    url = f'https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query.replace(" ", "+")}&image_type=photo&per_page=5'
    response = requests.get(url)
    return response.json().get('hits', [])

def fetch_giphy_gifs(query):
    url = f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=5&offset=0&rating=g&lang=en'
    response = requests.get(url)
    return response.json().get('data', [])

# Generate and display results
if prompt:
    with st.spinner('Generating title...'):
        title_prompt = f"Write a YouTube video title about {prompt}"
        title = generate_text(title_prompt)

    # Step-by-step script generation
    if title:
        st.write("### Title:", title)

        # Generate Introduction
        with st.spinner('Generating introduction...'):
            intro_prompt = f"Write an engaging introduction for a YouTube video titled '{title}'"
            introduction = generate_text(intro_prompt)

        # Generate Main Content
        with st.spinner('Generating main content...'):
            content_prompt = f"Write the main content section for a YouTube video titled '{title}', with in-depth discussion on the topic '{prompt}'"
            main_content = generate_text(content_prompt)

        # Generate Conclusion
        with st.spinner('Generating conclusion...'):
            conclusion_prompt = f"Write a conclusion for a YouTube video titled '{title}'"
            conclusion = generate_text(conclusion_prompt)

        # Display script parts
        if introduction:
            st.write("### Introduction:")
            st.write(introduction)
        if main_content:
            st.write("### Main Content:")
            st.write(main_content)
        if conclusion:
            st.write("### Conclusion:")
            st.write(conclusion)

        # Combine full script for easy reference
        full_script = "\n\n".join([introduction, main_content, conclusion])
        st.write("### Full Script:", full_script)

        # Fetch and display related images
        images = fetch_pixabay_images(prompt)
        if images:
            st.write("### Related Images:")
            for image in images:
                st.image(image['webformatURL'], caption=image['tags'])

        # Fetch and display related GIFs
        gifs = fetch_giphy_gifs(prompt)
        if gifs:
            st.write("### Related GIFs:")
            for gif in gifs:
                st.image(gif['images']['fixed_height']['url'], caption=gif['title'])
