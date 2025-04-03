import streamlit as st

def style_page():
  st.html("""
  <style>
  hr {
      margin: -0.5em 0 0 0;
      background-color: red;
  }
  p.prompt {
      margin: 0;
      font-size: 14px;
  }

  img.spinner {
      margin: 0 0 0 0;
  }

  div.block-container {
    padding-top: 2rem;
  }

  ul[data-testid="stSidebarNavItems"] {
    padding-top: 3.5rem;
  }
  </style>
  """)