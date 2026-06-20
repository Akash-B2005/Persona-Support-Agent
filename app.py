import streamlit as st

from src.classifier import classify_persona
from src.generator import generate_response
from src.escalator import check_escalation

st.title("Persona Support Agent")

query = st.text_input("Ask a question")

if st.button("Submit"):

    if query:

        # Step 1: Persona Classification
        persona_result = classify_persona(query)

        persona = persona_result["persona"]
        confidence = persona_result["confidence"]

        # Step 2: RAG Retrieval
        retrieved_context = """
        Use Forgot Password page.
        Enter registered email.
        Check inbox.
        """

        # Step 3: Generate Response
        response = generate_response(
            query,
            persona,
            retrieved_context
        )

        # Step 4: Escalation Check
        escalation = check_escalation(
            query,
            persona,
            confidence
        )

        st.subheader("Persona")
        st.write(persona)

        st.subheader("Response")
        st.write(response)

        if escalation["escalate"]:
            st.error("Escalated to Human Support")
            st.json(escalation)