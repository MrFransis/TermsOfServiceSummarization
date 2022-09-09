import os
from typing import AnyStr
import nltk
import streamlit as st
from transformers import pipeline, AutoTokenizer
import re


def main() -> None:
    # header
    st.title(":bookmark_tabs: Terms Of Service Summarizer :bookmark_tabs:")
    st.markdown("The app aims to extract the main information from Terms Of Conditions, which are often too long and "
                "difficult to understand. ")
    st.markdown("To test it just copy-paste a Terms Of Conditions in the textarea or select one of the examples that "
                "we have prepared for you, then you will see the summary represented as the most important sentences.")
    st.markdown("If you want more info in how we built our NLP algorithm check the documentation in the following "
                "GitHub repo: :point_right: https://github.com/balditommaso/TermsOfServiceSummarization :point_left:")
    st.markdown(":skull_and_crossbones: NOTE :skull_and_crossbones::")
    st.markdown("the App is still under development and we do not give any guarantee on the quality of the summaries, "
                "so we suggest a careful reading of the document.")

    @st.cache(allow_output_mutation=True, suppress_st_warning=True, show_spinner=False)
    def create_pipeline():
        with st.spinner("Loading the model..."):
            tos_pipeline = pipeline(task="summarization",
                                    model="ML-unipi/bart-large-tos",
                                    tokenizer="ML-unipi/bart-large-tos",
                                    device=0
                                    )
        return tos_pipeline

    def display_summary(summary_sentences: list) -> None:
        st.subheader("Summary :male-detective:")
        for sentence in summary_sentences:
            st.markdown(f"<li>{sentence}</li>", unsafe_allow_html=True)

    def get_list_files() -> list:
        names = []
        for file in os.listdir("./samples/"):
            if file.endswith(".txt"):
                names.append(file.replace(".txt", ""))

        return names

    def fetch_file_content(filename: str) -> AnyStr:
        with open(f"./samples/{filename.lower()}.txt", "r", encoding="utf-8") as file:
            text = file.read()
        return text

    def join_sentences(sentences: list) -> str:
        return " ".join([sentence for sentence in sentences])

    def split_sentences_by_token_length(sentences: list, split_token_length: int) -> list:
        accumulated_lists = []
        result_list = []
        cumulative_token_length = 0

        for sentence in sentences:
            # token_list = [token for token in nltk.word_tokenize(sentence)]
            token_list = tokenizer(sentence, max_length=1024, truncation=True)
            token_length = len(token_list["input_ids"])
            if token_length > 10:
                if token_length + cumulative_token_length > split_token_length and result_list:
                    accumulated_lists.append(join_sentences(result_list))
                    result_list = [sentence]
                    cumulative_token_length = token_length
                else:
                    result_list.append(sentence)
                    cumulative_token_length += token_length
        if result_list:
            accumulated_lists.append(join_sentences(result_list))
        return accumulated_lists

    nltk.download("punkt")
    pipe = create_pipeline()
    tokenizer = AutoTokenizer.from_pretrained("ML-unipi/bart-large-tos")

    if "target_text" not in st.session_state:
        st.session_state.target_text = ""
    if "sample_choice" not in st.session_state:
        st.session_state.sample_choice = ""

    st.header("Input")
    sample_choice = st.selectbox(
        label="Select a sample:",
        options=get_list_files()
    )

    st.session_state.target_text = fetch_file_content(sample_choice)
    target_text_input = st.text_area(
        value=st.session_state.target_text,
        label="Paste your own Term Of Service:",
        height=240
    )

    summarize_button = st.button(label="Try it!")

    if summarize_button:
        if target_text_input != "":
            summary_sentences = []
            with st.spinner("Summarizing in progress..."):
                sentences = split_sentences_by_token_length(nltk.sent_tokenize(target_text_input, language="english"),
                                                            split_token_length=1024
                                                            )
                for sentence in sentences:
                    # token_list = [token for token in nltk.word_tokenize(sentence)]
                    # st.markdown(sentence)
                    # st.markdown(str(len(token_list)))
                    output = pipe(sentence)
                    summary = output[0]["summary_text"]

                    for line in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', summary):
                        if line.find(".") != -1:
                            line = line.replace("..", ".")
                            summary_sentences.append(line)
                display_summary(summary_sentences)


if __name__ == "__main__":
    main()
