import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(page_title="E-Commerce AI Manager")

st.title("🛍️ E-Commerce AI Manager")
st.write("Your Smart Online Store Manager")

menu = st.sidebar.selectbox(
    "Select Menu",
    ["Dashboard", "Products", "Orders", "AI Manager"],
)

if menu == "Dashboard":
    st.header("Store Dashboard")
    a, b, c = st.columns(3)
    a.metric("Products", 25)
    b.metric("Orders", 40)
    c.metric("Revenue", "PKR 85,000")

elif menu == "Products":
    st.header("Product Management")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0)
    stock = st.number_input("Stock", min_value=0)

    if st.button("Add Product"):
        st.success(f"{name} added successfully!")

elif menu == "Orders":
    st.header("Order Management")
    customer = st.text_input("Customer Name")
    if st.button("Create Order"):
        st.success("Order created successfully!")

elif menu == "AI Manager":
    st.header("🤖 Real AI Business Manager")

    question = st.text_input("Ask your AI Manager")

    if st.button("Generate Advice"):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.error("Gemini API key not found!")

        elif not question.strip():
            st.warning("Please enter a question.")

        else:
            for model in ("gemini-3.5-flash", "gemini-3.8-flash"):
                try:
                    client = genai.Client(
                        api_key=api_key,
                        http_options=types.HttpOptions(timeout=45000),
                    )
                    with st.spinner("AI Manager is thinking..."):
                        response = client.models.generate_content(
                            model=model,
                            contents=(
                                "You are an expert Ecommerce Manager. "
                                "Give practical advice for an online store in Pakistan. "
                                + question
                            ),
                        )
                        answer = (response.text or "").strip()
                        if not answer:
                            raise RuntimeError(f"{model} returned an empty response.")

                    st.success("AI Recommendation")
                    st.write(answer)
                    break

                except Exception as e:
                    error_message = str(e).lower()
                    is_temporary = any(
                        code in error_message
                        for code in (
                            "429",
                            "500",
                            "502",
                            "503",
                            "504",
                            "unavailable",
                            "timeout",
                            "timed out",
                            "connection",
                        )
                    )
                    if is_temporary and model != "gemini-2.5-flash":
                        time.sleep(1)
                        continue

                    st.error(f"AI service temporarily unavailable: {e}")
                    break
