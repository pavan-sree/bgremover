import streamlit as st
from rembg import remove
from PIL import Image
import os
import shutil
import zipfile
import time

def zip_output_folder(folder_path, zip_name):
    """Creates a zip file from the processed images folder."""
    zip_path = f"{zip_name}.zip"
    
    # Small delay to ensure all files are saved
    time.sleep(1)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    
    return zip_path

def main():
    st.title("Upload Images and Backgrounds for Processing")

    uploaded_images = st.file_uploader("Upload images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    uploaded_backgrounds = st.file_uploader("Upload backgrounds...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    output_folder = "processed_images"

    if "zip_ready" not in st.session_state:
        st.session_state.zip_ready = False
        st.session_state.zip_path = ""

    if st.button("Process Images"):
        if not uploaded_images or not uploaded_backgrounds:
            st.error("Please upload both images and backgrounds.")
            return

        # Ensure output folder is clean
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)

        st.info("⏳ Processing images... Please wait.")

        for img_file in uploaded_images:
            image = Image.open(img_file)
            output = remove(image)

            for i, bg_file in enumerate(uploaded_backgrounds):
                background = Image.open(bg_file)
                background = background.resize(output.size)
                background.paste(output, (0, 0), output)
                output_path = os.path.join(output_folder, f"{os.path.splitext(img_file.name)[0]}_bg{i+1}.png")
                background.save(output_path)

        # Create ZIP file
        zip_path = zip_output_folder(output_folder, "processed_images")

        # Ensure ZIP exists before enabling download
        if os.path.exists(zip_path):
            st.session_state.zip_ready = True
            st.session_state.zip_path = zip_path
            st.success("✅ Processing complete! Click below to download.")

    # Show download button **only after** processing is done
    if st.session_state.zip_ready:
        with open(st.session_state.zip_path, "rb") as file:
            st.download_button(
                label="📥 Proceed to Download",
                data=file,
                file_name="processed_images.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
