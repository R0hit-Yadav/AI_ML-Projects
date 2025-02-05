import streamlit as st
import os
import base64
from logic import generate_slide_titles, generate_slide_content, create_presentation 


#to genrate download link
def get_ppt_download_link(ppt_path):
    with open(ppt_path, "rb") as file:
        ppt_contents = file.read()

#path and bit
    b64_ppt = base64.b64encode(ppt_contents).decode()
    filename = os.path.basename(ppt_path)

    return f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64_ppt}" download="{filename}">Download PowerPoint</a>'

#main function 
def main():
    st.title("PowerPoint Presentation Generator (Llama 3.2)🖥️📊")
    st.subheader("Generate a professional PowerPoint presentation on any topic")

    topic = st.text_input("Enter the topic for your presentation:")
    n_slide = st.number_input("Enter the number of slides:", min_value=1, max_value=20, value=5)


    if st.button("Generate Presentation🔎") and topic:
        st.info("Generating presentation... Please wait.🔃")
        
        # Generate slide titles and content
        slide_titles = generate_slide_titles(topic,n_slide)
        slide_contents = [generate_slide_content(title) for title in slide_titles]

        # Create and save the presentation
        ppt_path = create_presentation(topic, slide_titles, slide_contents)

        # Display success message and download link
        st.success("Presentation generated successfully!✅")
        st.markdown(get_ppt_download_link(ppt_path), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
