import requests
import cohere
import streamlit as st


PIXABAY_API_KEY = '46772125-eaba6b91b742d2daf04199f67' 
GIPHY_API_KEY = 'UhLQkPWbHGlH942nkTRoxkto0cOdTTlT'      
COHERE_API_KEY = 'cv2iT1eJhSikUq7HcUeIjiCSKUQdOH1dsvE9HgTB'  
cohere_client = cohere.Client(COHERE_API_KEY)

st.title('🦜🔗 YouTube GPT Creator')
prompt = st.text_input('Enter your video topic')

def generate_text(prompt, model='command-r', max_tokens=500):
    try:
        response = cohere_client.chat(
            model=model,
            message=prompt,
            temperature=0.7,
            max_tokens=max_tokens,
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return None



def fetch_pixabay_images(query):
    url = f'https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query.replace(" ", "+")}&image_type=photo&per_page=5'
    response = requests.get(url)
    return response.json().get('hits', [])

def fetch_giphy_gifs(query):
    url = f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=5&offset=0&rating=g&lang=en'
    response = requests.get(url)
    return response.json().get('data', [])


if prompt:
    with st.spinner('Generating title...'):
        title_prompt = f"Write a YouTube video title about {prompt}"
        title = generate_text(title_prompt)

   
    if title:
        st.write("### Title:", title)

        
        with st.spinner('Generating introduction...'):
            intro_prompt = f"Write an engaging introduction for a YouTube video titled '{title}'"
            introduction = generate_text(intro_prompt)

        
        with st.spinner('Generating main content...'):
            content_prompt = f"Write the main content section for a YouTube video titled '{title}', with in-depth discussion on the topic '{prompt}'"
            main_content = generate_text(content_prompt)

        
        with st.spinner('Generating conclusion...'):
            conclusion_prompt = f"Write a conclusion for a YouTube video titled '{title}'"
            conclusion = generate_text(conclusion_prompt)

       
        if introduction:
            st.write("### Introduction:")
            st.write(introduction)
        if main_content:
            st.write("### Main Content:")
            st.write(main_content)
        if conclusion:
            st.write("### Conclusion:")
            st.write(conclusion)

       
        full_script = "\n\n".join([introduction, main_content, conclusion])
        st.write("### Full Script:", full_script)

        
        images = fetch_pixabay_images(prompt)
        if images:
            st.write("### Related Images:")
            for image in images:
                st.image(image['webformatURL'], caption=image['tags'])

        
        gifs = fetch_giphy_gifs(prompt)
        if gifs:
            st.write("### Related GIFs:")
            for gif in gifs:
                st.image(gif['images']['fixed_height']['url'], caption=gif['title'])

