import numpy as np
import pickle
import pandas as pd
import streamlit as st
import joblib
import time


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.subheader("**Enter password to access application**")
        st.text_input(
            "Password:", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Incorrect password, please try again.")
        return False
    else:
        # Password correct.
        return True


if check_password():
    
  st.sidebar.info("Welcome, please use dropdown box to navigate to other pages.")

  pages = ["Home", "Data Exploration", "Predict Player Salary"]
  message = '''Select one of the options in the dropdown list to access specific page'''
  choice = st.sidebar.selectbox("Choose a page: ",pages, help = message)
  listo = ['','Page Description', 'How to access different pages', 'About app']

  if choice == "Home":
    st.sidebar.markdown("**Help:** ")
    learn =  st.sidebar.selectbox("What would you like assistance with?", listo)
    st.markdown("<h1 style='text-align: center; color: green;'>The Value of MLB Players</h1>", unsafe_allow_html=True)

    st.image('https://www.sportico.com/wp-content/uploads/2022/04/Valuation_List_1280x720-1.png?w=1280&h=720&crop=1')

    st.markdown("This application provides a model to predict the salary that should be given to players based on performance metrics.", unsafe_allow_html=True)

    
  elif choice == "Data Exploration":
    tab1, tab2 = st.tabs(["Exploratory Analysis", "Data Visualizations"])
    
    with tab1:
        option = st.selectbox(
                    'Select a feature to explore:',
                    ('View dataset', 'Generate profile report','Descriptive statistics'))
        if option == "View dataset":
            df = pd.read_csv('batting_basic')
            dataframe = st.dataframe(df)

            @st.experimental_memo
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')


            csv = convert_df(df)

            st.download_button(
                "Download telco dataset",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
            )
        #elif option == "
    with tab2:  
        sc = st.selectbox("Select a plot to visualize: ", ('Histogram',
                                                                     'Boxplots',
                                                                     "Position Group Totals",
                                                                     ))
        
       
    
  
  elif choice == "Predict Player Salary":

    st.markdown("<h1 style='text-align: center; color: green;'>Predict Player Salary</h1>", unsafe_allow_html=True)
    st.image("capstonehome.jpeg", use_column_width= 'always')

    st.markdown("Enter the following statistics for a batter and \
                        get an estimated salary value.")

    note = "Average Salary Difference is the average increase/decrease of a salary across a player's entire career."
    difference = st.number_input("Salary Difference", help = note)
    

    age = st.slider('Age', 18, 50, 27)


    hits = st.slider('Hits', 0, 250, 100)


    runs= st.slider('Runs', 0, 200, 50)


    rbi = st.slider('RBIs', 0, 200, 60)


    walks = st.slider('Walks', 0, 250, 60)


    so = st.slider('Strikeouts', 0, 250, 75)


    sb = st.slider('Stolen Bases', 0, 100, 12)


    ops = st.number_input("Input OPS value")

    if st.button("Predict Salary"):

        # unpickle the batting model
        bb_model = joblib.load("batting_basic_model.pkl")

        # store inputs into df

        column_names = ['Salary Difference', 'Age', 'H', 'R', 'RBI', 'BB', 'SO', 'SB', 'OPS']
        df = pd.DataFrame([[difference, age, hits, runs, rbi, walks, so, sb, ops]], 
                         columns = column_names)

          # get prediction
        prediction = bb_model.predict(df)
        st.write(prediction)

        # convert prediction
        converted = round(np.exp(prediction)[0],0)
        #converted = np.exp(prediction)

        with st.spinner('Calculating...'):
            time.sleep(1)
        st.success('Done!')

        st.dataframe(df)

        # output prediction
        st.header(f"Predicted Player Salary: ${converted:,}")
        #st.header("Predicted Player Salary:", prediction)





    # 2022 batter dataframe
    batter_2022_df = pd.read_csv('batting_merged_2022', index_col = 0)
    # reformat 2022 batter df for model prediction
    df_to_predict = batter_2022_df.drop(columns = ['Name', '2022 Salary'])

    # load in model
    bb_model = joblib.load("batting_basic_model.pkl")

    # make prediction
    predictions_2022 = bb_model.predict(df_to_predict)

    # Add prediction column
    batter_2022_df["Predicted Salary"] = np.around(np.exp(predictions_2022),0)

    pred_button = st.button("Prediction comparisions")

    if pred_button:
      st.markdown("### Predictions vs. 2022 MLB Stats")

      # Add value column
      batter_2022_df.loc[batter_2022_df['Predicted Salary'] > batter_2022_df['2022 Salary'], 'Value?'] = 'Under-valued'
      batter_2022_df.loc[batter_2022_df['Predicted Salary'] < batter_2022_df['2022 Salary'], 'Value?'] = 'Over-valued'

      # reorder columns
      batter_2022_df = batter_2022_df[['Name', '2022 Salary', 'Predicted Salary', 'Value?', 'Avg Career Salary Difference', 'Age', \
                                     'H', 'R', 'RBI', 'BB', 'SO', 'SB', 'OPS']]

      # formatting as Millions
      batter_2022_df['2022 Salary'] = batter_2022_df['2022 Salary']
      batter_2022_df['Predicted Salary'] = batter_2022_df['Predicted Salary']
      batter_2022_df['Avg Career Salary Difference'] = batter_2022_df['Avg Career Salary Difference']

      batter_2022_df = batter_2022_df.rename(columns = {'2022 Salary':'2022 Salary ($ Millions)',
                                                       'Predicted Salary':'Predicted Salary ($ Millions)',
                                                       'Avg Career Salary Difference':'Avg Career Salary Difference ($ Millions)'})



      selected_reward = st.selectbox("Choose a Player", batter_2022_df.Name, 0)

      selected_reward_price = batter_2022_df.loc[batter_2022_df.Name == selected_reward].iloc[0:13]

      st.dataframe(selected_reward_price)

      def convert_df(churn):
        return churn.to_csv(index=False).encode('utf-8')


        csv = convert_df(pd.DataFrame(selected_reward_price))

        st.download_button(
            "Download predictions",
            csv,
            "player_salary.csv",
            "text/csv",
            key='download-csv'
        )











