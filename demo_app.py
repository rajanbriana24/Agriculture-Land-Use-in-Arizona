import streamlit as st

## How to run the app
## $ pip install streamlit
## $ streamlit run demo_app.py


def app():
    st.title('Welcome to Our App')

    # input box
    name = st.text_input('Enter your location')

    if st.button('Send'):
        st.toast(f'{name} was sent!')
        col1, col2 = st.columns(2)
        with col1:
            st.write("Best crops for you: Cotton")
            st.write("Irrigation: rainfed")
        with col2:
            # chatbot
            st.write("Chatbot")
            st.text_area('Ask me more about the agriculture of Cotton!')
            st.button('Send', key='chatbot')


if __name__ == '__main__':
    app()
