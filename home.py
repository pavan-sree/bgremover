import streamlit as st
from rembg import remove
from PIL import Image
import os

def main():
    st.title("Upload Images and Backgrounds for Processing")

    uploaded_images = st.file_uploader("Upload images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    uploaded_backgrounds = st.file_uploader("Upload backgrounds...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    
    output_folder = st.text_input("Select output folder path:")
    
    if st.button("Process Images"):
        if not output_folder:
            st.error("Please provide an output folder path.")
            return

        if uploaded_images and uploaded_backgrounds:
            st.success(f"Processing this may take a while")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            for img_file in uploaded_images:
                image = Image.open(img_file)
                output = remove(image)

                for i, bg_file in enumerate(uploaded_backgrounds):
                    print("1/1[=======PROCESSING=======]1/1")
                    background = Image.open(bg_file)
                    background = background.resize(output.size)  
                    background.paste(output, (0, 0), output) 

                    output_path = os.path.join(output_folder, f"{os.path.splitext(img_file.name)[0]}_bg{i+1}.png")
                    background.save(output_path)

            st.success(f"Processed {len(uploaded_images)} images with {len(uploaded_backgrounds)} backgrounds each!")

if __name__ == "__main__":
    main()

