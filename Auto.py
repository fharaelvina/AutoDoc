import streamlit as st
import google.generativeai as palm

API_KEY = 'AIzaSyAOUOqy_XZs9grpMU4VrwigmisNeFsqTks'
palm.configure(api_key=API_KEY)

def generate_auto_documentation(user_input):
    """
    Generate auto documentation for the given code.

    Parameters:
    - user_input (str): The input code for documentation.

    Returns:
    str: Auto-generated documentation.
    """
    # Construct the prompt with user input
    prompt = f"""
    # Explain each line by adding comments or notes above the code
    code = {user_input}
    """
    
    # Use meaningful variable names
    response = palm.chat(messages=prompt)
    
    # Extract the content of the last message in the response
    documentation = response.last
    return documentation

def main():
    st.title("AutoDoc Generator")

    # Create a list to store generated documentation
    documentation_list = st.session_state.get("documentation_list", [])

    # Get user input using a text area
    user_input = st.text_area("Enter your code below", height=200)

    # Check if the user has entered code
    if st.button("Generate Documentation", key="gen_doc") and user_input:
        # Check if the input code is already in the list
        code_exists = any(code == user_input for code, _ in documentation_list)
        
        # If the code exists, update the documentation for the existing code
        if code_exists:
            index = next((i for i, (code, _) in enumerate(documentation_list) if code == user_input), None)
            if index is not None:
                documentation_list[index] = (user_input, generate_auto_documentation(user_input))
        else:
            # Generate auto documentation and append to the list
            documentation_list.append((user_input, generate_auto_documentation(user_input)))

    # Display all generated documentation
    for i, (user_code, doc) in enumerate(documentation_list):
        st.code(user_code, language='python')
        st.info(doc)

        # Add a new text area for entering code again
        new_code_expander = st.expander(f"Input New Code for Iteration {i+2}")
        with new_code_expander:
            new_code = st.text_area(f"Enter your new code for iteration {i+2} here", height=200)

            # Check if the user has entered new code
            if st.button(f"Generate Documentation for Iteration {i+2}", key=f"gen_doc_{i+2}") and new_code:
                # Check if the new code is already in the list
                code_exists = any(code == new_code for code, _ in documentation_list)
                
                # If the code exists, update the documentation for the existing code
                if code_exists:
                    index = next((i for i, (code, _) in enumerate(documentation_list) if code == new_code), None)
                    if index is not None:
                        documentation_list[index] = (new_code, generate_auto_documentation(new_code))
                else:
                    # Generate auto documentation for the new code and append to the list
                    documentation_list.append((new_code, generate_auto_documentation(new_code)))

    # Save the documentation list to session state
    st.session_state.documentation_list = documentation_list

    # Additional steps or workflow explanation in the sidebar
    st.sidebar.subheader("Additional Steps:")
    st.sidebar.write("""
    1. Input your code in the provided text area.
    2. Click the 'Generate Documentation' button to generate auto documentation or update existing documentation.
    3. Review the generated documentation and code explanation.
    4. If necessary, input a new code in the expander below and click 'Generate Documentation' to generate or update documentation for the new code.
    5. Repeat the process for additional iterations.
    """)

if __name__ == "__main__":
    main()
