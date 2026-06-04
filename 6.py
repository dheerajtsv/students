import streamlit as st
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import plotly.express as px
import shutil
import os

if not os.path.exists("/tmp/student.db"):
    shutil.copy("student.db", "/tmp/student.db")

con = sql.connect('/tmp/student.db')
cur = con.cursor()
results = pd.read_sql("SELECT * FROM private", con)


st.set_page_config(
    page_title="SDMS",
    layout="wide"
)


st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem !important;
    }
    header {visibility: hidden;}
    
    .student-card {
        background-color: #1a1a1a;
        padding: 2.5rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .big-number {
        font-size: 7rem !important;
        font-weight: 800;
        color: #00ff88;
        margin: 0.2rem 0;
        line-height: 1;
    }
    .university-row {
        display: flex;
        align-items: center;
        gap: 44 px;
    }
    
    .card-title {
        font-size: 1.6rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title('Student Data Management System')

tab1,tab2,tab3,tab4 = st.tabs(['Home','Data','Create Data','Charts'])
with tab1:
    st.write("An interactive dashboard to manage student data")
    col1,col2, col3 = st.columns(3)
    with col1:
        nos = pd.read_sql("SELECT COUNT(*) FROM private", con).iloc[0,0]

        st.markdown("### 👥 Total Students")
        st.image("https://img.icons8.com/fluency/96/student-male.png", width=90)

        st.markdown(f'<p class="big-number">{nos}</p>', unsafe_allow_html=True)
        st.caption("Students currently being served")
    with col2:
        cols = pd.read_sql("SELECT DISTINCT UNIVERSITY FROM private", con)
        st.markdown("### 🏛️ Colleges We Provide Service For")
        for idx, row in cols.iterrows():
            st.markdown(f"""
                <div class="university-row">
                    <span>{row['UNIVERSITY']}</span>
                </div>
                """, unsafe_allow_html=True)
    with col3:
        st.markdown("### 📬 Reach Out To Us")

        st.image("https://img.icons8.com/fluency/96/email.png", width=90)

        st.markdown("**Email:**")
        st.markdown("<h3 style='color:#4cc9f0; margin: 0;'>help@example.com</h3>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Other Ways to Connect:**")
        st.markdown("📱 +91 9618989124")
        st.markdown("🌐 www.example.com")
with tab2:
    st.info('Click on any cell and Press CTRL+F to search, click below button to see if ur data is reflected')
    if st.button('Refresh Data', type='primary'):
        con = sql.connect('/tmp/student.db')
        results = pd.read_sql("SELECT * FROM private", con)
        st.dataframe(results)
        st.rerun()
    results = pd.read_sql("SELECT * FROM private", con)
    st.dataframe(results)
    with st.expander('READ BEFORE INSERTION!'):
        st.write('''For now, only Inserting operation has been enabled.Double check the data before submitting''')
with tab3:
    with st.form(key='student'):
        st.title('Student Details Entry Form')
        name = st.text_input("Enter Student's Name")
        university = st.selectbox("Select University",options=results['UNIVERSITY'].unique())
        program = st.selectbox("Select Program",options=results['PROGRAM NAME'].unique())
        honours = st.selectbox("Select Specialization",options=results['Specialisation'].unique())
        semester = st.selectbox("Select Semester",options=results['SEMESTER'].unique())
        domain = st.selectbox("Select Domain",options=results['Domain'].unique())
        gen = st.slider('Input General Management Score (out of 50)',min_value=0,max_value=50)
        dom = st.slider('Domain Specific Score (out of 50)',min_value=0,max_value=50)
        total = st.slider('Total Score (out of 100)',min_value=0,max_value=100)
        selectBox = st.checkbox('Would the student like to consent to promotion of him for masters?')
        submitted = st.form_submit_button('Submit')
        if submitted:
            temp = 'No'
            if selectBox:
                temp='Yes'
            data = (name,university,program, honours, semester, domain, gen, dom, total, temp)
            con = sql.connect('student.db')
            cur = con.cursor()
            try:
                check = f'SELECT "NAME OF THE STUDENT" FROM private WHERE "NAME OF THE STUDENT"="{name}"'
                if pd.read_sql(check,con).size == 0:

                    cur.execute('''INSERT INTO private VALUES(?,?,?,?,?,?,?,?,?,?)''',data)
                    con.commit()
                    st.success("Data submitted successfully")
                else:
                    st.error('Student Already exist!')
            except:
                st.error('Something went wrong')
            cur.close()
            con.close()

with tab4:
    cols1,cols2 = st.columns(2)
    cols3,cols4 = st.columns(2)

    with cols1:
        st.info('Studnets by University')
        values = results['UNIVERSITY'].value_counts().reset_index()
        values['UNIVERSITY']= values['UNIVERSITY'].str.split().str[0]
        fig,ax = plt.subplots()
        ax.bar(
            data=values,
            x='UNIVERSITY',
            height='count'

        )
        st.pyplot(fig)
    with cols2:
        st.info('University by domains')
        inner1, inner2 = st.columns([0.2,0.8])
        with inner1:
            select = st.selectbox('Select University',options=results['UNIVERSITY'].unique())
            s = results[results['UNIVERSITY'] == select]['Specialisation'].value_counts().reset_index()
        with inner2:
            st.write("Number of Students in each domain from "+select)
            fig = px.bar(
                s,
                x='Specialisation',
                y='count'
            )
            st.plotly_chart(fig)