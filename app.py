import streamlit as st


def save_feedback(feedback: str) -> bool:
    if not feedback.strip():
        return False
    with open("feedback.txt", "a") as f:
        f.write(feedback.strip() + "\n")
    return True


def save_rating(rating: str) -> bool:
    if rating not in ("helpful", "not_helpful"):
        return False
    with open("ratings.txt", "a") as f:
        f.write(rating + "\n")
    return True


def main():
    st.title("Feedback")

    st.subheader("Was this helpful?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Helpful"):
            save_rating("helpful")
            st.success("Thanks for the rating!")
    with col2:
        if st.button("👎 Not helpful"):
            save_rating("not_helpful")
            st.success("Thanks for the rating!")

    st.subheader("Share your feedback")
    feedback = st.text_area("Share your feedback:")
    if st.button("Submit Feedback"):
        if save_feedback(feedback):
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter some feedback before submitting.")


if __name__ == "__main__":
    main()
