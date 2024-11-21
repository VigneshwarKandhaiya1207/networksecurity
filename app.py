import streamlit as st
import pandas as pd
from src.networksecurity.utils.utils import load_object
from src.networksecurity.utils.ml_utils.model.estimator import NetworkModel
from src.networksecurity.pipeline.train_pipeline import TrainingPipeline

# Dummy functions to simulate train and predict pipelines
def train_model():
    st.write("Training the model...")
    run_pipeline=TrainingPipeline()
    run_pipeline.run_pipeline()
    st.write("Model training complete.")

def predict_model(input_data):
    st.write("Making prediction with input data:", input_data)
    preprocesor=load_object("final_model/preprocesser.pkl")
    final_model=load_object("final_model/model.pkl")
    network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
    df = pd.DataFrame([input_data])
    y_pred = network_model.predict(df)
    prediction = "Predicted value based on the input"  # Replace with real prediction logic
    st.write("Prediction: ", y_pred)

# Streamlit UI
def app():
    st.title('Train or Predict')

    # Dropdown to choose between train or predict
    option = st.selectbox("Select an option", ("Train", "Predict"))

    if option == "Train":
        # If train is selected, run training pipeline
        if st.button("Start Training"):
            train_model()
    
    elif option == "Predict":
        # If predict is selected, show input fields to enter values
        st.write("Enter input values for prediction:")
        
        # Example input fields (can be customized based on the model's input)
        having_IP_Address=st.number_input("having_IP_Address", value=0.0)
        URL_Length=st.number_input("URL_Length", value=0.0)
        Shortining_Service=st.number_input("Shortining_Service", value=0.0)
        having_At_Symbol=st.number_input("having_At_Symbol", value=0.0)
        double_slash_redirecting=st.number_input("double_slash_redirecting", value=0.0)
        Prefix_Suffix=st.number_input("Prefix_Suffix", value=0.0)
        having_Sub_Domain=st.number_input("having_Sub_Domain", value=0.0)
        SSLfinal_State=st.number_input("SSLfinal_State", value=0.0)
        Domain_registeration_length=st.number_input("Domain_registeration_length", value=0.0)
        Favicon=st.number_input("Favicon", value=0.0)
        port=st.number_input("port", value=0.0)
        HTTPS_token=st.number_input("HTTPS_token", value=0.0)
        Request_URL=st.number_input("Request_URL", value=0.0)
        URL_of_Anchor=st.number_input("URL_of_Anchor", value=0.0)
        Links_in_tags=st.number_input("Links_in_tags", value=0.0)
        SFH=st.number_input("SFH", value=0.0)
        Submitting_to_email=st.number_input("Submitting_to_email", value=0.0)
        Abnormal_URL=st.number_input("Abnormal_URL", value=0.0)
        Redirect=st.number_input("Redirect", value=0.0)
        on_mouseover=st.number_input("on_mouseover", value=0.0)
        RightClick=st.number_input("RightClick", value=0.0)
        popUpWidnow=st.number_input("popUpWidnow", value=0.0)
        Iframe=st.number_input("Iframe", value=0.0)
        age_of_domain=st.number_input("age_of_domain", value=0.0)
        DNSRecord=st.number_input("DNSRecord", value=0.0)
        web_traffic=st.number_input("web_traffic", value=0.0)
        Page_Rank=st.number_input("Page_Rank", value=0.0)
        Google_Index=st.number_input("Google_Index", value=0.0)
        Links_pointing_to_page=st.number_input("Links_pointing_to_page", value=0.0)
        Statistical_report=st.number_input("Statistical_report", value=0.0)
        
        # Button to trigger prediction
        if st.button("Make Prediction"):
            input_data = {"having_IP_Address":having_IP_Address,
                            "URL_Length": URL_Length,
                           "Shortining_Service":Shortining_Service,
                            "having_At_Symbol":having_At_Symbol,
                           "double_slash_redirecting": double_slash_redirecting,
                           "Prefix_Suffix": Prefix_Suffix,
                           "having_Sub_Domain": having_Sub_Domain,
                           "SSLfinal_State": SSLfinal_State,
                           "Domain_registeration_length": Domain_registeration_length,
                            "Favicon":Favicon,
                            "port":port,
                            "HTTPS_token":HTTPS_token,
                           "Request_URL": Request_URL,
                           "URL_of_Anchor": URL_of_Anchor,
                            "Links_in_tags":Links_in_tags,
                           "SFH": SFH,
                           "Submitting_to_email": Submitting_to_email,
                           "Abnormal_URL": Abnormal_URL,
                           "Redirect": Redirect,
                           "on_mouseover": on_mouseover,
                            "RightClick":RightClick,
                           "popUpWidnow": popUpWidnow,
                           "Iframe": Iframe,
                            "age_of_domain":age_of_domain,
                           "DNSRecord": DNSRecord,
                           "web_traffic": web_traffic,
                            "Page_Rank":Page_Rank,
                           "Google_Index": Google_Index,
                           "Links_pointing_to_page": Links_pointing_to_page,
                           "Statistical_report": Statistical_report}
            predict_model(input_data)

# Run the Streamlit app
if __name__ == "__main__":
    app()
