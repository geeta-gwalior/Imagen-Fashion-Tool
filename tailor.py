import streamlit as st
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel, Image
from vertexai.generative_models import GenerativeModel



# Set up session state for the gallery
if "gallery" not in st.session_state:
    st.session_state.gallery = []

st.set_page_config(layout="wide")
st.title("🇮🇳 Indian Fashion Visualizer with Imagen 4")
st.write("Craft your traditional or contemporary Indian design with structured details to get precise, high-quality images.")

#
# Main design form
#
with st.form("design_form"):
    st.header("1. Describe Your Design")
    
    col1, col2 = st.columns(2)
    with col1:
        main_description = st.text_area(
            "Main Design Description",
            height=150,
            placeholder="A stunning bridal lehenga with a heavy flare and intricate floral embroidery."
        )
        occasion = st.selectbox(
            "Select an Occasion",
            ["Wedding", "Festival (Diwali, Holi)", "Everyday Casual", "Office Wear", "Party/Reception"]
        )
        garment_type = st.selectbox(
            "Garment Type",
            ["Saree", "Lehenga", "Salwar Kameez", "Kurta Pyjama", "Anarkali", "Sherwani", "Indo-Western Dress"]
        )
    
    with col2:
        fabrics = st.multiselect(
            "Select Fabric(s)",
            ["Silk", "Cotton", "Georgette", "Chiffon", "Velvet", "Brocade", "Raw Silk"]
        )
        embellishments = st.multiselect(
            "Select Embellishment(s)",
            ["Zardozi work", "Embroidery", "Mirror work", "Sequins", "Beadwork", "Block print", "Bandhani"]
        )
        cultural_details = st.text_input(
            "Add specific cultural details (e.g., 'Kanjivaram pattern', 'Rajasthani style')"
        )
        background = st.text_input(
            "Describe the background or scene",
            placeholder="A luxurious Indian palace."
        )
        
    aspect_ratio = st.radio(
        "Aspect Ratio",
        ["1:1", "4:3", "9:16"],
        horizontal=True
    )

    submitted = st.form_submit_button("🎨 Generate Design")

# Now, place the slider outside the form so it is interactive
number_of_images = st.slider(
    "Number of Images to Generate",
    min_value=1,
    max_value=4,
    value=1
)

if submitted:
    if not main_description:
        st.warning("Please provide a main design description.")
    else:
        with st.spinner("Generating your design... this may take a moment."):
            # Construct the final, detailed prompt
            fabric_string = ", ".join(fabrics)
            embellishment_string = ", ".join(embellishments)
            
            prompt = f"A photorealistic image of a model wearing a {garment_type} for a {occasion}. The garment is made of {fabric_string} and features {embellishment_string}. {main_description}. {cultural_details}. The background is {background}."

            try:
                # Generate the images
                generated_images_response = model.generate_images(
                    prompt=prompt,
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio
                )

                st.session_state.current_generation = {
                    "prompt": prompt,
                    "images": generated_images_response
                }

            except Exception as e:
                st.error(f"An error occurred: {e}")

#
# Display generated images and gallery management
#
if "current_generation" in st.session_state and st.session_state.current_generation["images"]:
    st.divider()
    st.header("Generated Designs ✨")
    
    # Corrected line: Access the .images attribute
    images_list = st.session_state.current_generation["images"].images
    
    cols = st.columns(len(images_list))
    for i, img in enumerate(images_list):
        with cols[i]:
            st.image(img._pil_image, use_column_width=True)
            if st.button(f"Save Design {i+1}", key=f"save_btn_{i}"):
                st.session_state.gallery.append({
                    "prompt": st.session_state.current_generation["prompt"],
                    "image": img
                })
                st.success(f"Design {i+1} saved to gallery!")

#
# Display the gallery
#
st.divider()
st.header("My Saved Gallery 📂")

if st.session_state.gallery:
    gallery_cols = st.columns(4)
    for i, item in enumerate(st.session_state.gallery):
        with gallery_cols[i % 4]:
            st.image(item["image"]._pil_image, caption=item["prompt"], use_column_width=True)
else:
    st.info("Your gallery is empty. Generate and save a design to start building your portfolio!")
