import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from mysql_chat import init_database, get_response

def main():
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
        ]
    
    st.set_page_config(page_title="SQL Assistant", page_icon=":speech_balloon:")
    st.title("Chat with your MySQL Database")
    
    with st.sidebar:
        st.subheader("Database Configuration")
        st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")
        
        st.text_input("Host", value="localhost", key="Host")
        st.text_input("Port", value="3306", key="Port")
        st.text_input("User", value="root", key="User")
        st.text_input("Password", type="password", value="rohit", key="Password")
        st.text_input("Database", value="retail_sales_db", key="Database")
        
        if st.button("Connect"):
            with st.spinner("Connecting to database..."):
                db = init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to database!")
                
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
    
    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        
        with st.chat_message("Human"):
            st.markdown(user_query)
            
        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)
            
        st.session_state.chat_history.append(AIMessage(content=response))
    
if __name__ == "__main__":
    main()