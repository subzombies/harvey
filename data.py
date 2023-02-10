import streamlit as st
import pandas as pd
import csv
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ["James Allen", "Oliver Philpott"]
usernames = ["jallen","ophilpott"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
"harvey_finance", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/Password is incorrect")


if authentication_status == None:
    st.warning("Please Enter Login Details")

if authentication_status:

    def main():
        st.title("Customer Information")
        add_page = st.sidebar.selectbox("Go to", ["Add Mandate", "View Data","Generate Submission"])
        UserPath = st.sidebar.text_input("Enter File Location Path")
        authenticator.logout("Logout", "sidebar")
        st.write(UserPath + r'\PTXSub.csv')
        df = pd.read_csv(UserPath + r"\RealData.csv", na_values=['NA'])
        df2 = pd.read_csv(UserPath + r"\Payments.csv")
        if add_page == "Add Mandate":
            name = st.text_input("Name")
            account_number = st.text_input("Account Number")
            sort_code = st.text_input("Sort Code")
            ref = st.text_input("Reference")
            amount = st.text_input("Amount")
            code = st.selectbox('Code',('17', '0N', '0X'))

            if st.button("Submit"):
                with open(UserPath + r'mandates.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([sort_code,account_number,ref,amount,code])
                st.success("Data added to Mandates Submission File")


        if add_page == "Generate Submission":
            date = st.selectbox('Month',('01', '02', '03','04','05','06','07','08','09','10','11','12','All'))
            year = st.selectbox('Year',('2021','2022','2023','2024'))
            status = st.selectbox('Status',('Pending','Paid','Cancelled','Bounced'))

            df2 = pd.read_csv(UserPath + r"Payments.csv", dtype ='str')
            dfdate = df2
            if date != "All":
                dfdate = df2[df2['Date'].str.contains('/' + str(date))]
            dfdate = dfdate[dfdate['Date'].str.contains('/' + str(year))]
            dfdatepending = dfdate.loc[dfdate['Status'] == status]
            st.write(dfdatepending)

            dfexport = pd.DataFrame()
            dfexport["Sort"] = dfdatepending['Sort']
            dfexport["Number"] = dfdatepending['Number']
            dfexport["Name"] = dfdatepending['Name']
            dfexport["Ref"] = dfdatepending['Ref']
            dfexport["Type"] = dfdatepending['Type']
            st.write(dfexport)

            if st.button("Submit"):
                dfexport.Number = dfexport.Number.astype("str")
                dfexport.Sort = dfexport.Sort.astype("str")
                dfexport.to_csv(UserPath + r"PTXSub.csv",header=False,index=False)
                st.success("Data added to Mandates Submission File")
                
        if add_page == "View Data":
            
            
            # User input for customer number
            customer_number = st.text_input("Enter customer number:")

            rslt_df = df.loc[df['Agg no'] == int(customer_number)]
            rslt_df2 = df2.loc[df2['Agreement'] == int(customer_number), df2.columns!='Amount Total']
            

            st.write(rslt_df)
            st.write(rslt_df2)  

    if __name__ == "__main__":
        main()


    

