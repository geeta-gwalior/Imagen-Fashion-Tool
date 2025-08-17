import streamlit as st
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel, Image
from vertexai.generative_models import GenerativeModel



# Set up the Streamlit page
st.title("Fashion Design Visualizer with Imagen 4")
st.write("Enter a detailed description of your fashion design to generate an image.")

# User input for the prompt
prompt = st.text_area("Design Description", height=150, placeholder="A high-fashion photograph of a model wearing a futuristic dress made of glowing, iridescent fabric. The setting is a minimalist, white studio with dramatic, cinematic lighting.")

# Generate image when the button is clicked
if st.button("Generate Design"):
    if not prompt:
        st.warning("Please enter a description.")
    else:
        with st.spinner("Generating your design..."):
            try:
                # Call the Imagen 4 API to generate the image
                generated_images = model.generate_images(
                    prompt=prompt,
                    number_of_images=1,
                    aspect_ratio="1:1"
                )

                # Display the generated image
                st.image(generated_images[0]._pil_image, caption="Generated Fashion Design")

                st.success("Design generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
