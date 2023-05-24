import streamlit as st

def main():      
    st.set_page_config(
        layout= "wide",
        page_title="IFC Stream",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(

        """
        ### Click on Browse File to begin 
        """
    )

if __name__ == "__main__":
    main()