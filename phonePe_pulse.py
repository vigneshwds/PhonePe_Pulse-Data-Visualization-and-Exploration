import pandas as pd
import mysql.connector as mysql
import plotly.express as px
import requests
import json
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image


#mysql connection
conn=mysql.connect(
    host="localhost",
    user="root",
    password="Groot",
    database="phonepedb"
)
cursor=conn.cursor()

#aggrecate_insurance
cursor.execute("SELECT * FROM aggrecated_insurance")
tab1=cursor.fetchall()
#get the column names
column_name = [des[0] for des in cursor.description]
aggrecate_insurance=pd.DataFrame(tab1, columns=column_name)

#aggrecate_transaction
cursor.execute("SELECT * FROM aggrecated_transaction")
tab2=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
aggrecate_transaction=pd.DataFrame(tab2, columns=column_name)

#aggrecate_user
cursor.execute("SELECT * FROM aggrecated_user")
tab3=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
aggrecate_user=pd.DataFrame(tab3, columns=column_name)

#map_insurance
cursor.execute("SELECT * FROM map_insurance")
tab4=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
map_insurance=pd.DataFrame(tab4, columns=column_name)

#map_transaction
cursor.execute("SELECT * FROM map_transaction")
tab5=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
map_transaction=pd.DataFrame(tab5, columns=column_name)

#map_user
cursor.execute("SELECT * FROM map_user")
tab6=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
map_user=pd.DataFrame(tab6, columns=column_name)

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
tab7=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
top_insurance=pd.DataFrame(tab7, columns=column_name)

#top_transaction
cursor.execute("SELECT * FROM top_transaction")
tab8=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
top_transaction=pd.DataFrame(tab8, columns=column_name)

#top_user
cursor.execute("SELECT * FROM top_user")
tab9=cursor.fetchall()

column_name = [des[0] for des in cursor.description]
top_user=pd.DataFrame(tab9, columns=column_name)

cursor.close()
conn.close()


def Tran_amt_count_yq(df, year, quarter):
    tcay=df[(df["Years"]==year) & (df["Quarters"]==quarter)]
    tcay.reset_index(drop=True, inplace=True) #sorting the index from 0 to n

    #groupby state wise
    tcay_g=tcay.groupby("States")[["Transaction_count", "Transaction_amount"]].sum() #sum the transaction count
    tcay_g.reset_index(inplace=True)

    #India-Map
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    responds=requests.get(url)
    jfile=json.loads(responds.content)
    state_names=[]
    for feature in jfile["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort() 

    st.subheader(":blue[Geo Visualization Dashboard]")

    fig=px.choropleth(tcay_g, geojson=jfile, locations="States", featureidkey="properties.ST_NM", 
                        color="Transaction_amount", color_continuous_scale="Rainbow", 
                        range_color=(tcay_g["Transaction_amount"].min(), tcay_g["Transaction_amount"].max()), 
                        hover_name="States", title=f"{year} All India Transaction Amount in Quarter {quarter}", fitbounds="locations", height=550)
    fig.update_geos(visible=False)
    st.plotly_chart(fig)   

    fig=px.choropleth(tcay_g, geojson=jfile, locations="States", featureidkey="properties.ST_NM", 
                        color="Transaction_count", color_continuous_scale="Rainbow", 
                        range_color=(tcay_g["Transaction_count"].min(), tcay_g["Transaction_count"].max()), 
                        hover_name="States", title=f"{year} All India Transaction Count in Quarter {quarter}", fitbounds="locations", height=550)
    fig.update_geos(visible=False)
    st.plotly_chart(fig) 

    #Plot
    col1,col2=st.columns(2)

    with col1:
        st.subheader(":blue[States Transaction Amount]")
        fig=px.bar(tcay_g, x="States", y="Transaction_amount", title=f"{year} Transaction Amount {quarter} Quarter", color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig)

    with col2:
        st.subheader(":blue[States Transaction Count]")
        fig=px.bar(tcay_g, x="States", y="Transaction_count", title=f"{year} Transaction Count {quarter} Quarter", color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig)

    return tcay


def agg_tran_transaction(year, quarter, tran_type):
    tcay = aggrecate_transaction[(aggrecate_transaction["Transaction_type"] == tran_type) & 
                                 (aggrecate_transaction["Quarters"] == quarter) &
                                 (aggrecate_transaction["Years"] == year)]
    tcay.reset_index(drop=True, inplace=True)

    tcay_g = tcay.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()

    # India-Map
    st.subheader(":blue[Geo Visualization Dashboard]")

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    jfile = json.loads(response.content)
    
    state_names = [feature["properties"]["ST_NM"] for feature in jfile["features"]]
    state_names.sort()

    fig = px.choropleth(tcay_g, geojson=jfile, locations="States", featureidkey="properties.ST_NM", 
                             color="Transaction_amount", color_continuous_scale="Rainbow", 
                             range_color=(tcay_g["Transaction_amount"].min(), tcay_g["Transaction_amount"].max()), 
                             hover_name="States", title=f"{year} Transaction Amount {quarter} Quarter", fitbounds="locations", height=550)
    fig.update_geos(visible=False)
    st.plotly_chart(fig)

    fig = px.choropleth(tcay_g, geojson=jfile, locations="States", featureidkey="properties.ST_NM", 
                             color="Transaction_count", color_continuous_scale="Rainbow", 
                             range_color=(tcay_g["Transaction_count"].min(), tcay_g["Transaction_count"].max()), 
                             hover_name="States", title=f"{year} Transaction_count {quarter} Quarter", fitbounds="locations", height=550)
    fig.update_geos(visible=False)
    st.plotly_chart(fig)

    #Plot
    col1,col2=st.columns(2)
    with col1:
        st.subheader(":blue[States Transaction Amount]")
        fig=px.bar(tcay_g, x="States", y="Transaction_amount", title=f"{year} Transaction Amount {quarter} Quarter", color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig)
 
    with col2:
        st.subheader(":blue[States Transaction Count]")
        fig=px.bar(tcay_g, x="States", y="Transaction_count", title=f"{year} Transaction Count {quarter} Quarter", color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig) 


def agg_user(year, quarter):
    tcay=aggrecate_user[(aggrecate_user["Years"]==year) & (aggrecate_user["Quarters"]==quarter)]
    tcay.reset_index(drop=True, inplace=True)
    tcay_g=pd.DataFrame(tcay.groupby("Brand_Name")["Transaction_count"].sum())
    tcay_g.reset_index(inplace=True)

    #Bar plot
    st.subheader(":blue[All India Mobile Brands Transaction Count]")
    fig_agg_user=px.bar(tcay_g, x="Brand_Name", y="Transaction_count", title=f"{year} Brand and Transaction count in {quarter} Quarter", 
                        color_discrete_sequence=px.colors.sequential.Blues_r, hover_name="Brand_Name")
    st.plotly_chart(fig_agg_user)     


def agg_us_state(state):
    agg_us_line=aggrecate_user[aggrecate_user["States"]==state]
    agg_us_line.reset_index(drop=True, inplace=True)

    #bar analysis state 
    st.subheader(":blue[Mobile Brands Transaction Count State Wise]")
    fig_trend=px.bar(agg_us_line, x="Brand_Name", y="Transaction_count", hover_name="Transaction_percentage", title=f"{state} Brand wise Transaction count", color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig_trend)   


def agg_use_p(df, year, quarter):
    aua=df[(df["Years"]==year) & (df["Quarters"]==quarter)]
    aua.reset_index(drop=True, inplace=True)

    st.subheader(":blue[Pie Graph]")
    fig=px.pie(aua, names="Brand_Name", values="Transaction_count", hover_data="Transaction_percentage",
                    title=f"{year} Brand wise Transaction count percentage in Quarter {quarter}", color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig)     


def map_ins_plot1(df, state):
    mip=df[df["States"]==state]
    mip_g=mip.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    mip_g.reset_index(inplace=True)

    #bar plots
    col1,col2=st.columns(2)

    with col1:
        st.subheader(":blue[Districts Transaction Amount]")
        fig=px.bar(mip_g, x="Transaction_amount", y="Districts", title=f"{state} District Transaction Amount", color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig)

    with col2:
        st.subheader(":blue[Districts Transaction Amount]")
        fig=px.bar(mip_g, x="Transaction_count", y="Districts", title=f"{state} District Transaction Count", color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig)   


def map_ins_plot2(state):
    mip=map_ins_df[map_ins_df["States"]==state]
    mip_g=mip.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    mip_g.reset_index(inplace=True)

    #bar plot
    fig=px.bar(mip_g, x="Transaction_count", y="Districts", title=f"{state} District Transaction Count", color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig)  


def map_user_plot1(df, year, quarter):
    mua=df[(df["Years"]==year) & (df["Quarters"]==quarter)]
    mua.reset_index(drop=True, inplace=True)

    mua_g=mua.groupby("States")[["Registered_Users", "AppOpens"]].sum()
    mua_g.reset_index(inplace=True)

    #line plot
    st.subheader(":blue[Registered Users vs AppOpens Users]")
    fig=px.line(mua_g, x="States", y=["Registered_Users", "AppOpens"], title=f"{year} Registered Users and AppOpnes in Quarter {quarter}",
                color_discrete_sequence= px.colors.sequential.Blues_r, markers=True)
    st.plotly_chart(fig)

    return mua 


def map_user_bar(df, state):
    mua_d=df[df["States"]==state]
    mua_d.reset_index(drop=True, inplace=True)

    mua_dg=pd.DataFrame(mua_d.groupby("Districts")["Registered_Users"].sum())
    mua_dg.reset_index(inplace=True)

    #Bar Chart
    st.subheader(":blue[District - Registered Users]")
    fig= px.bar(mua_dg, x= "Registered_Users",y= "Districts",orientation="h",
                                        title= f"{state} Registered Users in District wise",height=800,
                                        color_discrete_sequence= px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig)


def top_user_plot1(df, year, quarter):
    tua=df[(df["Years"]==year) & (df["Quarters"]==quarter)]
    tua.reset_index(drop=True, inplace=True)

    tua_g=pd.DataFrame(tua.groupby("States")["Registered_Users"].sum())
    tua_g.reset_index(inplace=True)

    #bar plot
    st.subheader(":blue[Top Registered Users]")
    fig=px.bar(tua_g, x="States", y="Registered_Users", title=f"{year} Top Registered User in Quarter {quarter}", color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig)  

    return tua  


def top_use_q(state):
    tua2=top_user_df[top_user_df["States"]==state]
    tua2.reset_index(drop=True, inplace=True)

    tua2_g=pd.DataFrame(tua2.groupby("Quarters")["Registered_Users"].sum())
    tua2_g.reset_index(inplace=True)

    st.subheader(":blue[States]")

    return st.dataframe(tua2_g)


#Question and Answer function blocks
def qus1():
    brand=aggrecate_user[["Brand_Name", "Transaction_count"]]
    brand_g=brand.groupby("Brand_Name")["Transaction_count"].sum().sort_values(ascending=False)
    brand_gp=pd.DataFrame(brand_g)
    brand_gp.reset_index(inplace=True)

    fig=px.pie(brand_gp, values="Transaction_count", names="Brand_Name",hole=0.45, color_discrete_sequence=px.colors.sequential.dense_r,
            title= "Top Mobile Brands based on Transaction_count")
    return st.plotly_chart(fig)

def qus2():
    tran= aggrecate_transaction[["States", "Transaction_amount"]]
    tran1= tran.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    tran2= pd.DataFrame(tran1).reset_index().head(10)

    fig= px.bar(tran2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig)

def qus3():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig= px.pie(htd2, values= "Transaction_amount", names= "Districts", hole=0.45, title="Top 10 Districts of Highest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig)

def qus4():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig= px.pie(htd2, values= "Transaction_amount", names= "Districts", hole=0.45, title="Top 10 Districts of Lowest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig)

def qus5():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig)

def qus6():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig= px.bar(sa2, x= "States", y= "AppOpens", title="Lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig)

def qus7():
    stc= aggrecate_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig= px.bar(stc2, x= "States", y= "Transaction_count", title= "States With Lowest Transaction Count",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig)

def qus8():
    stc= aggrecate_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig= px.bar(stc2, x= "States", y= "Transaction_count", title= "States With Highest Transaction Count",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig)

def qus9():
    ht= aggrecate_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig= px.bar(ht2, x= "States", y= "Transaction_amount",title= "Higesht Transaction Amount and States",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig)

def qus10():
    dt= map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "Districts With Lowest Transaction Amount",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig)


#Streamlit

st.set_page_config(layout="wide")
col1, col2=st.columns(2)
with col1:
    st.image(Image.open(r"C:\Capstone files\PhonePe_Project\248807513-f43c154d-50db-4d22-aaa0-02e79d3034d3.png"), width=200)

st.title(":violet[PhonePe Pulse Data Visualization and Exploration]")

with st.sidebar:
    user=option_menu("Menu", ["Home", "Data Exploration", "Top Chart", "About"], icons=["house", "graph-up", "bar-chart", "book"], menu_icon="cast")

if user=="Home":
    col1,col2= st.columns(2)
    with col1:
        st.markdown("**A User-Friendly Tool Using Streamlit and Plotly**")
        st.markdown("**:blue[Project Overview]**")
        st.markdown("**PhonePe Pulse is a data analytics initiative by PhonePe, one of india's leading digital payment plotforms. The Project provides insights into digital payment trends accross India using data collected from PhonePe transactions.**")
        st.markdown("**:blue[Domain :] FinTech**")
        st.markdown("**:blue[Technologies Used :] Github cloning, Python Scripting, MySQL, mysql-connector-python, Streamlit and Plotly**")
        st.write("This project inspired from [PhonePe Pulse](https://www.phonepe.com/pulse/explore/transaction/2022/4/) ", " Data source:","[Git Hub](https://github.com/PhonePe/pulse.git)")
        st.info("Amount and Count values(₹) are in Indian Rupee(INR)",icon="ℹ️")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        st.image(Image.open(r"C:\Capstone files\PhonePe_Project\DigPayment.png"))

    with col2:
        st.image(Image.open(r"rigtSlider.jpg"), width=450)    

elif user=="Data Exploration":
    tab1, tab2, tab3=st.tabs(["**Aggregated Analysis**", "**Map Analysis**", "**Top Analysis**"])

    with tab1:
        button=st.radio("**Select the type of Analysis**",["Insurance Analysis", "Transaction Analysis", "User Analysis"], horizontal=True)

        if button=="Insurance Analysis":

            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the year**", (aggrecate_insurance["Years"].unique()))
            with col2:    
                quarters=st.selectbox("**Select the quarter**", (aggrecate_insurance["Quarters"].unique()))

            Tran_amt_count_yq(aggrecate_insurance, years, quarters)
            
        elif button=="Transaction Analysis":
            
            col1, col2, col3=st.columns(3)
            with col1:
                years=st.selectbox("**Select the year**", (aggrecate_transaction["Years"].unique()))
            with col2:
                quarters=st.selectbox("**Select the quarter**", (aggrecate_transaction["Quarters"].unique()))
            with col3:
                tran_types=st.selectbox("**Select the Transaction type**", ("Recharge & bill payments", "Peer-to-peer payments", "Merchant payments", "Financial Services", "Others"))

            agg_tran_transaction(years, quarters, tran_types) 

        elif button=="User Analysis":
            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the year**", (aggrecate_user["Years"].unique()))
            with col2:
                quarters=st.selectbox("**Select the quarter**", (aggrecate_user["Quarters"].unique())) 

            agg_user(years, quarters)   

            states=st.selectbox("**Select the State**", (aggrecate_user["States"].unique()))  
            
            agg_us_state(states)

            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the years**", (aggrecate_user["Years"].unique()))
            with col2:
                quarters=st.selectbox("**Select the quarter** ", (aggrecate_user["Quarters"].unique()))

            agg_user_pie=agg_use_p(aggrecate_user, years, quarters)

    with tab2:
        button2=st.radio("**Select the type of  Analysis**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"], horizontal=True)

        if button2=="Map Insurance Analysis":

            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the years**", (map_insurance["Years"].unique()))
            with col2:    
                quarters=st.selectbox("**Select the quarters**", (map_insurance["Quarters"].unique()))

            map_ins_df=Tran_amt_count_yq(map_insurance, years, quarters)  

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("**Select the State**", (map_ins_df["States"].unique()))

            map_ins_plot1(map_ins_df, states)

        elif button2=="Map Transaction Analysis":

            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the years**", (map_transaction["Years"].unique()))
            with col2:    
                quarters=st.selectbox("**Select the quarters**", (map_transaction["Quarters"].unique()))

            map_tran_df=Tran_amt_count_yq(map_transaction, years, quarters) 

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Selec the State", (map_tran_df["States"].unique()))

            map_ins_plot1(map_tran_df, states)

        elif button2=="Map User Analysis":

            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("Select the years", (map_user["Years"].unique()))
            with col2:    
                quarters=st.selectbox("Select the quarters", (map_user["Quarters"].unique()))

            map_line=map_user_plot1(map_user, years, quarters)

            col1, col2=st.columns(2)

            with col1:
                states=st.selectbox("Selec the State", (map_line["States"].unique()))

            map_user_bar(map_line, states)

    with tab3:
        button3=st.radio("**Select the type of  Analysis**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"], horizontal=True)

        if button3=="Top Insurance Analysis":

            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the year**  ", (top_insurance["Years"].unique()))
            with col2:    
                quarters=st.selectbox("**Select the quarter**  ", (top_insurance["Quarters"].unique()))

            top_ins_df=Tran_amt_count_yq(top_insurance, years, quarters)
    
        elif button3=="Top Transaction Analysis":
            
            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the year**  ", (top_transaction["Years"].unique()))
            with col2:    
                quarters=st.selectbox("**Select the quarter**  ", (top_transaction["Quarters"].unique()))

            top_tran_df=Tran_amt_count_yq(top_transaction, years, quarters)  

        elif button3=="Top User Analysis":
            col1, col2=st.columns(2)
            with col1:
                years=st.selectbox("**Select the year**  ", (top_user["Years"].unique()))
            with col2:    
                quarters=st.selectbox("**Select the quarter**  ", (top_user["Quarters"].unique()))

            top_user_df=top_user_plot1(top_user, years, quarters)    

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("**Select the State** ", (top_user_df["States"].unique()))

            top_use_q(states)    


elif user=="Top Chart":
    questions= st.selectbox("**Select the Question**",('1. Top Brands Of Mobiles Used',
                                                        '2. States With Lowest Trasaction Amount',
                                                        '3. Districts With Highest Transaction Amount',
                                                        '4. Top 10 Districts With Lowest Transaction Amount',
                                                        '5. Top 10 States With AppOpens',
                                                        '6. Least 10 States With AppOpens',
                                                        '7. States With Lowest Trasaction Count',
                                                        '8. States With Highest Trasaction Count',
                                                        '9.States With Highest Trasaction Amount',
                                                        '10. Top 50 Districts With Lowest Transaction Amount'))    
    
    st.subheader(":blue[Top Chart]")

    if questions=="1. Top Brands Of Mobiles Used":
        qus1()   

    elif questions=="2. States With Lowest Trasaction Amount":
        qus2()

    elif questions=="3. Districts With Highest Transaction Amount":
        qus3()

    elif questions=="4. Top 10 Districts With Lowest Transaction Amount":
        qus4()

    elif questions=="5. Top 10 States With AppOpens":
        qus5()

    elif questions=="6. Least 10 States With AppOpens":
        qus6()

    elif questions=="7. States With Lowest Trasaction Count":
        qus7()

    elif questions=="8. States With Highest Trasaction Count":
        qus8()

    elif questions=="9.States With Highest Trasaction Amount":
        qus9()

    elif questions=="10. Top 50 Districts With Lowest Transaction Amount":
        qus10()    

elif user=="About":
    st.subheader("About PhonePe Pulse")
    st.write("""
    The Indian digital payments story has truly captured the world's imaginatiobluen. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.

When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?
This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.

This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.

PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.

""")      

    st.image(Image.open(r"C:\Capstone files\PhonePe_Project\DigPayment.png"), width=800)
