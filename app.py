import streamlit as st
from streamlit_option_menu import option_menu
import requests
from PIL import Image
import base64
import os
from streamlit_extras.mention import mention
#from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template
#test

# Set page title
st.set_page_config(page_title="Oussama Jmaa", page_icon = "desktop_computer", layout = "wide", initial_sidebar_state = "auto")

# Use the following line to include your style.css file
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

def get_pdf_text(pdf="Oussama_cv.pdf"):
    pdf = PdfReader(pdf)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    with open("bio.txt", "r") as f:
        bio_text = f.read()
    combined_text = bio_text + "\n\n" + "this is oussama's resume :\n" +text
    return combined_text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
  
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})

    st.session_state.chat_history = response['chat_history']
   
    st.write(bot_template.replace(
                "{{MSG}}", st.session_state.chat_history[1].content), unsafe_allow_html=True)


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def render_lottie(url, width, height):
    lottie_html = f"""
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.14/lottie.min.js"></script>
    </head>
    <body>
        <div id="lottie-container" style="width: {width}; height: {height};"></div>
        <script>
            var animation = lottie.loadAnimation({{
                container: document.getElementById('lottie-container'),
                renderer: 'svg',
                loop: true,
                autoplay: true,
                path: '{url}'
            }});
            animation.setRendererSettings({{
                preserveAspectRatio: 'xMidYMid slice',
                clearCanvas: true,
                progressiveLoad: false,
                hideOnTransparent: true
            }});
        </script>
    </body>
    </html>
    """
    return lottie_html

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

footer = """
footer{
    visibility:visible;
}
footer:after{
    content:'Copyright © 2023 Oussama Jmaa';
    position:relative;
    color:black;
}
"""
# PDF functions
def show_pdf(file_path):
        with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="600" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

def pdf_link(pdf_url, link_text="Click here to view PDF"):
    href = f'<a href="{pdf_url}" target="_blank">{link_text}</a>'
    return href

# Load assets
#lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
# Assets for about me
img_utown = Image.open("images/me.jpg")


# Assets for experiences
esprit_img = Image.open("images/esprit_img.png")
cpfmi_img = Image.open("images/cpfmi_img.jpg")
telecom_img = Image.open("images/telecom_img.jpg")
img_groundup = Image.open("images/coopva_img.jpg")
img_sagem = Image.open("images/sagemcom.png")
# Assets for projects





# Assets for contact
lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_abqysclq.json")

img_linkedin = Image.open("images/linkedin.png")
img_github = Image.open("images/github.png")
img_email = Image.open("images/email.png")

def social_icons(width=24, height=24, **kwargs):
        icon_template = '''
        <a href="{url}" target="_blank" style="margin-right: 20px;">
            <img src="{icon_src}" alt="{alt_text}" width="{width}" height="{height}">
        </a>
        '''

        icons_html = ""
        for name, url in kwargs.items():
            icon_src = {
                "linkedin": "https://img.icons8.com/ios-filled/100/ff8c00/linkedin.png",
                "github": "https://img.icons8.com/ios-filled/100/ff8c00/github--v2.png",
                "email": "https://img.icons8.com/ios-filled/100/ff8c00/filled-message.png"
            }.get(name.lower())

            if icon_src:
                icons_html += icon_template.format(url=url, icon_src=icon_src, alt_text=name.capitalize(), width=width, height=height)

        return icons_html
#####################
# Custom function for printing text
def txt(a, b):
  col1, col2 = st.columns([4,1])
  with col1:
    st.markdown(a)
  with col2:
    st.markdown(b)

def txt2(a, b):
  col1, col2 = st.columns([1,4])
  with col1:
    st.markdown(f'`{a}`')
  with col2:
    st.markdown(b)

def txt3(a, b):
  col1, col2 = st.columns([1,4])
  with col1:
    st.markdown(f'<p style="font-size: 20px;">{a}</p>', unsafe_allow_html=True)
  with col2:
    b_no_commas = b.replace(',', '')
    st.markdown(b_no_commas)

def txt4(a, b):
  col1, col2 = st.columns([1.5,2])
  with col1:
    st.markdown(f'<p style="font-size: 25px; color: white;">{a}</p>', unsafe_allow_html=True)
  with col2: #can't seem to change color besides green
    st.markdown(f'<p style="font-size: 25px; color: red;"><code>{b}</code></p>', unsafe_allow_html=True)

#####################

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg.png')   


# Sidebar: If using streamlit_option_menu
with st.sidebar:
    with st.container():
        l, m, r = st.columns((1,3,1))
        with l:
            st.empty()
        # with m:
        #     st.image(img_lh, width=175)
        with r:
            st.empty()
    
    choose = option_menu(
                        "Oussama Jmaa", 
                        ["About Me", "Experience", "Technical Skills", "Projects", "Resume", "Certificates", "Contact","Interview ChatBot"],
                         icons=['person fill', 'globe', 'clock history', 'tools', 'book half', 'clipboard', 'trophy fill', 'heart', 'pencil square', 'image', 'paperclip', 'star fill', 'envelope'],
                         menu_icon="mortarboard", 
                         default_index=0,
                         styles={
        "container": {"padding": "0!important", "background-color": "#f5f5dc"},
        "icon": {"color": "darkorange", "font-size": "20px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#cfcfb4"},
    }
    )
    linkedin_url = "https://www.linkedin.com/in/oussama-jmaa-217098171/"
    github_url = "https://github.com/oussamaJMAA"
    email_url = "mailto:jemaaoussama64@gmail.com"
    with st.container():
        l, m, r = st.columns((0.11,2,0.1))
        with l:
            st.empty()
        with m:
            st.markdown(
                social_icons(30, 30,LinkedIn=linkedin_url, GitHub=github_url, Email=email_url),
                unsafe_allow_html=True)
        with r:
            st.empty()

st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
st.title("Oussama Jmaa")
# Create header
if choose == "About Me":
    #aboutme.createPage()
    with st.container():
        left_column, middle_column, right_column = st.columns((1,0.2,0.5))
        with left_column:
            st.header("About Me")
            st.subheader("Data Science/Computer Science Student")
            st.write("👋 Hello! I’m a final year Data Science student at Esprit School of Engineering, actively seeking an end-of-studies internship and the chance to start my career in AI. I’m passionate about learning new tech and applying my knowledge in practical ways..")
            st.write("👩‍💻 My academic focus includes data visualization, machine learning, and natural language processing. I’m all about turning data into insights that can drive decisions and innovation.")
            st.write("🏋🏻 In addition, I like to practice sports in my free time , football , basketball and play video games !")
            st.write("👨🏼‍💻 Academic interests: Machine learning, Deep Learning , Natural Language Processing ,Predictive Analysis")
            st.write("💭 Ideal Career Prospects: Data Analyst, Data Scientist, Data Engineer")
            st.write("📄 [Resume (1 page)](https://drive.google.com/file/d/17fhh3GLegzTNB9x4KcNlgRuldHflenOp/view?usp=sharing)")
            st.markdown('🤖 Check the **interview chatbot** section to interact with an LLM and ask him anything about my experience .')
        with middle_column:
            st.empty()
        with right_column:
            st.image(img_utown)

# Create section for Work Experience
elif choose == "Experience":
    #st.write("---")
    st.header("Experience")
    with st.container():
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image(img_sagem)
        with text_column:
            st.subheader("Data Science Intern, [SagemCom](https://www.sagemcom.com/fr)")
            st.write("*June to August 2023*")
            st.markdown("""
             - Implemented a machine learning-based predictive maintenance system to forecast equipment failures, enhance maintenance planning, and reduce downtime.
             - Utilized sensor data analytics for preemptive equipment servicing, which led to significant cuts in operational expenses. 
             - Offered consulting services incorporating web scraping to analyze market trends, facilitating strategic, data-driven decisions .                                
            
            `Python` `Machine learning` `NLP` `LLMS` `Web Scraping` `Selenium` `BeautifulSoup4`
            """)
    with st.container():
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image(img_groundup)
        with text_column:
            st.subheader("Computer vision Intern, [COOPVA](https://coopva.solutions/)")
            st.write("*June to August 2023*")
            st.markdown("""
            - Developed a computer vision application leveraging YOLOv8 for real-time object detection and face recognition, aimed at supporting Alzheimer’s patients.
            - Integrated YOLOv8 algorithms with Open-CV for the development of a sophisticated facial and object recognition system to provide contextual assistance to Alzheimer’s patients.
            - Employed Python, YOLOv8, and Open-CV to build a gui application capable of showing the results.
            
            `Python` `YOLOv8` `Open-CV` `Web Scraping` `Selenium` `BeautifulSoup4`
            
            """)
    with st.container():
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image(telecom_img)
        with text_column:
            st.subheader("Web Development Intern, [Telecom](https://www.tunisietelecom.tn/entreprise/)")
            st.write("*June to July 2022*")
            st.markdown("""
            - Co-engineered an interactive web platform featuring quizzes and courses in cybersecurity and networking, aimed at boosting employee proficiency and knowledge.
            - Implemented a dynamic content recommendation engine using PHP7.4 and SYMFONY4.4, facilitating personalized learning experiences for users.
            - Integrated BeautifulSoup and SQL for data-driven website functionalities, enhancing learning tools with up-to-date, relevant content.            

            `PHP` `Symfony` `Javascript` `SQL` `Python` `BeautifulSoup4`   
            """)
    with st.container():
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image(cpfmi_img)
        with text_column:
            st.subheader("Web Development Intern, [CPFMI](https://cpfmi.com/)")
            st.write("*July to August 2021*")
            st.markdown("""
            - Completed an internship at CPFMI, where I developed a comprehensive management application for products, sales, users, and transactions
            - Utilized a stack comprising HTML5, CSS3, PHP7.4, SYMFONY4.4, JQuery, and SQL to create a robust platform for business operations.
            - Engineered a user-friendly interface and backend systems to enhance administrative efficiency and streamline company workflows.

            `PHP` `Symfony` `Javascript` `SQL` `JQUERY` 
            """)
    with st.container():
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image(esprit_img)
        with text_column:
            st.subheader("Web Development Intern, [Esprit](https://esprit.tn/)")
            st.write("*June to July 2021*")
            st.markdown("""
            - Developed a web application dedicated to managing end-of-studies internships, aiming to simplify the placement process for students.
            - Designed features to facilitate interaction between students, institutions, and hosting companies, ensuring a smooth internship management experience.

             `PHP` `Symfony` `Javascript` `SQL` `JQUERY` 
            """)
    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:0px;
    }
    </style>
    ''', unsafe_allow_html=True)
#st.write("##")

# Create section for Technical Skills
elif choose == "Technical Skills":
    #st.write("---")
    st.header("Technical Skills")
    txt3("Programming Languages","`Python`, `SQL`, `Java`, `Javascript`")
    txt3("Academic Interests","`Machine learning`, `Deep learning`, `Natural Language Processing`")
    txt3("Data Visualization", " `matplotlib`, `seaborn`, `Plotly`")
    txt3("Database Systems", "`MySQL`, `PostgreSQL` ,`Oracle`, `SQLite` `Google BigQuery`")
    txt3("Cloud Platforms", "`Google Cloud Platform`, `HuggingFace`")
    txt3("Natural Language Processing", "`NLTK`, `Word2Vec`, `TF-IDF`, `Bert` ,`Llms`")
    txt3("Version Control", "`Git / Github`")
    txt3("Data Science Techniques", "`Regression`, `Clustering`, `Random Forest`, `Xgboost`, `Principal Components Analysis`, `Text Classification`, `Sentiment Analysis`, `Graph based neural networks`")
    txt3("Machine Learning Frameworks", "`Numpy`, `Pandas`, `Scikit-Learn`, `TensorFlow`, `Keras`, `Pytorch`")



elif choose == "Projects":
    # Create section for Projects
    #st.write("---")
    st.header("Projects")
    with st.container():
        text_column, image_column = st.columns((3,1))
        with text_column:
            st.subheader("PRM-Conceptual-Graphs-Recommendations")
            st.write("*Academic Project, Esprit School Of Engineering*")
            st.markdown("""
            - Collaborated in a six-member team on an NLP project focused on constructing a conceptual graph and developing a GNN-based recommendation system.
            - The system was designed to enhance project risk management by providing personalized advice to stakeholders and risk owners, driven by their specific queries and profiles.
            - Leveraged cutting-edge tools such as Python, LLMS, YOLOv8, HuggingFace, and Django for deployment, ensuring a responsive and intelligent application.
            """)
            
            mention(label="Github Repo", icon="github", url="https://github.com/oussamaJMAA/PRM-Conceptual-Graphs-Recommendations",)
        with image_column:
            st.image( Image.open("images/gnn_img.png"))
    with st.container():
        text_column, image_column = st.columns((3,1))
        with text_column:
            st.subheader("Educational Interactive-Intelligent Platform")
            st.write("*Academic Project, Esprit School Of Engineering*")
            st.markdown("""
            - Directed research towards crafting an online educational tool that converts textual descriptions of mathematical problems into graphical interpretations, augmenting comprehension through visual aids.
            - Integrated sentiment analysis algorithms to gauge the complexity and nature of mathematical language, supporting the creation of more precise and educational graphics.
            - Employed OpenAI’s API for the automatic verification of user-submitted answers, ensuring accurate and efficient learning progression.
            - Developed a sophisticated recommendation system within the application, programmed to suggest relevant mathematical prompts to users, tailored to their learning history and proficiency.
            """)
            
            mention(label="Final Report", icon="📄", url="https://drive.google.com/file/d/1GxAJzRq50JSsbPtblNG98CpcgVUL0-PG/view?usp=sharing",)
            mention(label="Github Repo", icon="github", url="https://github.com/oussamaJMAA/educational_interactive_platform",)
        with image_column:
            st.image(Image.open("images/education_img.png"))
    with st.container():
        text_column, image_column = st.columns((3,1))
        with text_column:
            st.subheader("Identification of the most relevant CVs for tenders")
            st.write("*Self-initiated project*")
            st.markdown("""
            - Conducted a comprehensive case study to pinpoint the most suitable CVs for tender applications.
            - Carried out an integration and exploration of datasets, employing data cleaning and visualization techniques to distill key insights.
            - Fine tuned and leveraged the Doc2Vec model to train on these datasets, employing this method to derive semantic meanings from texts and enhance model accuracy.            
            - Employed cosine similarity calculations to assess the degree of alignment between C.V.s and tenders, thus streamlining the matchmaking process.
                        """)
    
            mention(label="Github Repo", icon="github", url="https://github.com/oussamaJMAA/Identification-of-the-most-relevant-CVs-for-tenders",)
        with image_column:
            st.image(Image.open("images/jobmatching_img.png"))
    with st.container():
        text_column, image_column = st.columns((3,1))
        with text_column:
            st.subheader("Computer vision project on Face Mask Detection")
            st.write("*Self-initiated project using MaskedFace-Net dataset*")
            st.markdown("""
           - Developed a face mask detection system that utilizes real-time video streams to identify individuals wearing masks, ensuring compliance with health and safety protocols. Established a preprocessing pipeline using OpenCV for image acquisition, manipulation, and augmentation to enhance the diversity of the training dataset.
           - Experimented with various Convolutional Neural Network (CNN) architectures including AlexNet, VGG-16, and ResNet for feature extraction and classification. Benchmarked models to compare accuracy and computational efficiency, optimizing for real-world application constraints.
            """)
        
            mention(label="Github Repo", icon="github", url="https://github.com/oussamaJMAA/face_mask_detection")
        with image_column:
            st.image(Image.open("images/mask_img.jpg"))
    with st.container():
        text_column, image_column = st.columns((3,1))
        with text_column:
            st.subheader("Data science project on Email/SMS spam Classification from kaggle")
            st.write("*Self-initiated project using a Kaggle dataset*")
            
            st.markdown("""
            - Developed an email and SMS spam classifier using natural language processing (NLP) and machine learning techniques.
            - Applied Term Frequency-Inverse Document Frequency (TF-IDF) to weigh and normalize the text data, enhancing the classifier’s ability to discern relevant terms in messages.
            - Implemented a suite of machine learning algorithms including Naive Bayes, Support Vector Machine (SVM), and Random Forest – to train the classification model effectively.
            - Deployed the finely-tuned model using Flask, a lightweight web framework, which enables the seamless integration of the spam classifier into a web application.
                         """)
        
            mention(label="Github Repo", icon="github", url="https://github.com/oussamaJMAA/Email-Sms-spam-classifier",)
        with image_column:
            st.image(Image.open("images/spam_img.png"))
    with st.container():
        text_column, image_column = st.columns((3,1))
        with text_column:
            st.subheader("Data Science project on Flight Fare Prediction from kaggle")
            st.write("*Self-initiated project using a Kaggle dataset*")
            st.markdown("""
            - Built a sophisticated flight fare prediction model leveraging data science principles and machine learning to anticipate price fluctuations.
            - Integrated TF-IDF to parse and analyze textual data from various sources, ensuring the model accounts for dynamic pricing factors such as date, demand, and class.
            - Coupled TF-IDF with potent machine learning algorithms, including Gradient Boosting and Random forest, to construct a predictive framework capable of learning complex fare patterns.           
            - Deployed the predictive model through the Flask web framework
            """)
            #st.write("[Final Report](https://drive.google.com/file/d/1YuYxSTuDstSvyUa-bn782sLE5kCfbyH8/view?usp=sharing) | [Pitch Deck](https://www.canva.com/design/DAFeSnJeqgM/uXpz0kw8e7If4T1PG2tpaQ/view?utm_content=DAFeSnJeqgM&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink) | [Product Demo](https://www.youtube.com/watch?v=XMlt-kfdC7g)")
            mention(label="Github Repo", icon="github", url="https://github.com/oussamaJMAA/Flight-Fare-Prediction")
            
        with image_column:
            st.image(Image.open("images/flight_img.jpg"))
    with st.container():
        text_column, image_column = st.columns((3,1))
        with text_column:
            st.subheader("Data Science fake news prediction  from Kaggle")
            st.write("Self-initiated project using a Kaggle dataset*")
            st.markdown("""
            - Created a robust fake news detection system by utilizing machine learning and natural language processing technologies to accurately classify news content.
            - Integrated TF-IDF techniques to quantify the importance of words in news articles, allowing the model to recognize patterns indicative of misinformation.
            -Engaged an array of machine learning algorithms — such as Logistic Regression, Decision Trees, and Ensemble methods — to empower the classifier to decipher intricate nuances between genuine and fake news.
            """)
            #st.write("[Github Repo](https://github.com/harrychangjr/biopics) | [RPubs](https://rpubs.com/harrychangjr/biopics)")
            mention(label="Github Repo", icon="github", url="https://github.com/oussamaJMAA/fake_news_classifier")
        with image_column:
            st.image(Image.open("images/fake_img.jpg"))
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Optimisation for Large-Scale Data-Driven Inference: Anime Recommendation System")
    #         st.write("*Completed assignment for module DSA4212: Optimisation for Large-Scale Data-Driven Inference in Academic Year 2022/23 Semester 2*")
    #         st.markdown("""
    #         - Built recommendation system using various non-factor models, including content-based collaborative filtering and clustering
    #         - Utilised matrix factorisation (single value decomposition) to optimise performance of recommendation system with lower test MSE
    #         - Provided optional recommendations to further optimise performance e.g scraping additional data, using deep learning methods
    #         """)
    #         #st.write("[Github Repo](https://github.com/harrychangjr/dsa4212) | [Report](https://github.com/harrychangjr/dsa4212/blob/main/DSA4212%20Assignment%202%20Group%2039%20Report.pdf)")
    #         mention(label="Github Repo", icon="github", url="https://github.com/harrychangjr/dsa4212",)
    #     with image_column:
    #         st.image(images_projects[5])
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Optimisation for Large-Scale Data-Driven Inference: Word Embedding")
    #         st.write("*Completed assigmment for module DSA4212: Optimisation for Large-Scale Data-Driven Inference in Academic Year 2022/23 Semester 2*")
    #         st.markdown("""
    #         - Trained Word2Vec model on 20 Newsgroups dataset from scikit-learn package in Python, which provides a number of similar words based on input word
    #         - Evaluated usefulness of model by applying model to text classification (46% accuracy) and sentiment analysis (86.4% accuracy)
    #         """)
    #         #st.write("[Github Code](https://github.com/harrychangjr/dsa4212/blob/main/DSA4212%20Assignment%203%20Group%2039.ipynb) | [Report](https://github.com/harrychangjr/dsa4212/blob/main/DSA4212%20Assignment%203%20Group%2039%20Report.pdf)")
    #         mention(label="Github Code", icon="github", url="https://github.com/harrychangjr/dsa4212/blob/main/DSA4212%20Assignment%203%20Group%2039.ipynb",)
    #     with image_column:
    #         st.image(images_projects[6])
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Data-Driven Marketing: Exploration of cellphone billing and subscriber data")
    #         st.write("*Self-initiated project based on past assignment from module BT4211: Data-Driven Marketing*")
    #         st.markdown("""
    #         - Performed preliminary churn analysis, customer segmentation and descriptive analysis to understand more about dataset
    #         - Trained logit and probit models, as well as providing model estimations for duration models
    #         - Utilised random forest classifier to predict customer churn
    #         """)
    #         #st.write("[Github Repo](https://github.com/harrychangjr/cellphone-billing) | [RPubs](https://rpubs.com/harrychangjr/cellphone)")
    #         mention(label="Github Repo", icon="github", url="https://github.com/harrychangjr/cellphone-billing",)
    #     with image_column:
    #         st.image(images_projects[7])
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Data Visualization: Analysis on Spotify Dataset from [tidytuesday](https://github.com/rfordatascience/tidytuesday/blob/master/data/2020/2020-01-21)")
    #         st.write("*Completed group project for module DSA2101: Essential Data Analytics Tools: Data Visualization in Academic Year 2021/22 Semester 2*")
    #         st.markdown("""
    #         - Investigated variables that differentiates songs of different genres, which could be useful in designing recommendation systems
    #         - Explored how do the four seasons affect number of songs produced in each period
    #         - Visualizations used: ridgeline faceted density plot, boxplot, line chart, faceted donut chart
    #         """)
    #         #st.write("[Github Code](https://github.com/harrychangjr/dsa2101/blob/main/DSA2101_Group%20B.Rmd) | [RPubs](https://rpubs.com/harrychangjr/dsa2101-groupb)")
    #         mention(label="Github Code", icon="github", url="https://github.com/harrychangjr/dsa2101/blob/main/DSA2101_Group%20B.Rmd",)
    #     with image_column:
    #         st.image(images_projects[8])
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Computers and the Humanities: Chloropleths using Google Sheets and Folium in Python")
    #         st.write("*Completed assignment for module GET1030: Computers and the Humanities in Academic Year 2020/21 Semester 2*")
    #         st.markdown("""
    #         - Visualized the total number of performances of A Doll's House by country, using a chloropleth from Google Sheets
    #         - Drafted scatterplots and boxplots using seaborn to investigate relationship between number of events per country and number of years these plays have been performed
    #         - Created chloropleth using Folium in Google Colab to compare total performance counts in China, categorised by province
    #         """)
    #         #st.write("[Google Sheets](https://docs.google.com/spreadsheets/d/1NBlGM7Sjcybbpl1Esa55qLRJw-Seti1LhC93EhV_68w/edit?usp=sharing) | [Google Colab](https://colab.research.google.com/drive/1RHqtb5XC7PkJDpNEb-BY3tO-8mI2j32E?usp=sharing)")
    #         mention(label="Google Drive", icon="🗂️", url="https://drive.google.com/drive/folders/1Iva0oLZim6zJlAndoSzR63pUq4NCznim?usp=share_link",)
    #     with image_column:
    #         st.image(images_projects[9])
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Computers and the Humanities: Network Analysis on Harry Potter Film Database")
    #         st.write("*Completed assignment for module GET1030: Computers and the Humanities in Academic Year 2020/21 Semester 2*")
    #         st.markdown("""
    #         - Utilised custom Python file based on NetworkX and Glob to create networks using Harry Potter film database
    #         - Drafted visualizations using matplotlib and seaborn to compare densities and weighted degree values of nodes from generated networks
    #         - Customised network visualization using Gephi to investigate relationship between various Harry Potter film directors
    #         """)
    #         #st.write("[Github Code](https://github.com/harrychangjr/get1030/blob/main/A0201825N_GET1030_Tutorial_4.ipynb)")
    #         mention(label="Github Code", icon="github", url="https://github.com/harrychangjr/get1030/blob/main/A0201825N_GET1030_Tutorial_4.ipynb",)
    #     with image_column:
    #         st.image(images_projects[10])
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Computers and the Humanities: Text Processing and Analysis on Song Lyrics")
    #         st.write("*Completed assignment for module GET1030: Computers and the Humanities in Academic Year 2020/21 Semester 2*")
    #         st.markdown("""
    #         - Utilised custom Python file based on NetworkX and Glob to create networks using Harry Potter film database
    #         - Drafted visualizations using matplotlib and seaborn to compare proportions of nouns and verbs between different songs
    #         - Analysed type/token ratios of songs from both albums to evaluate which album produced better quality songs based on words used
    #         """)
    #         #st.write("[Github Code](https://github.com/harrychangjr/get1030/blob/main/A0201825N%20-%20GET1030%20Tutorial%203.ipynb)")
    #         mention(label="Github Code", icon="github", url="https://github.com/harrychangjr/get1030/blob/main/A0201825N%20-%20GET1030%20Tutorial%203.ipynb",)
    #     with image_column:
    #         st.image(images_projects[11])
    # with st.container():
    #     text_column, image_column = st.columns((3,1))
    #     with text_column:
    #         st.subheader("Computers and the Humanities: Spotify in the Covid-19 Era")
    #         st.write("*Completed group project for module GET1030: Computers and the Humanities in Academic Year 2020/21 Semester 2*")
    #         st.markdown("""
    #         - Compiled and scraped Spotify data from [Spotify](https://www.spotifycharts.com), [Kaggle](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks), and [OWID](https://ourworldindata.org/coronavirus/country/singapore) to analyse top songs played in Singapore during Covid-19
    #         - Drafted Tableau dashboard to showcase correlation between various features of top songs, including tempo, acousticness and popularity
    #         - Embedded 30-second snippet of featured song on dashboard for increased interactiveness
    #         """)
    #         #st.write("[Github Code](https://github.com/harrychangjr/get1030/blob/main/A0201825N%20-%20GET1030%20Tutorial%203.ipynb)")
    #         mention(label="Final Report", icon="📄", url="https://github.com/harrychangjr/get1030/blob/main/GET1030%20Final%20Project.pdf",)
    #     with image_column:
    #         st.image(images_projects[12])
    

    


elif choose == "Resume":   
    resume_url = "https://drive.google.com/file/d/17fhh3GLegzTNB9x4KcNlgRuldHflenOp/view?usp=sharing"
    st.header("Resume")
    st.write("*In case your current browser cannot display the PDF documents, do refer to the hyperlink below!*")

    st.markdown(pdf_link(resume_url, "**Resume (1 page)**"), unsafe_allow_html=True)
    show_pdf("Oussama_cv.pdf")
    with open("Oussama_cv.pdf", "rb") as file:
        btn = st.download_button(
            label="Download Resume (1 page)",
            data=file,
            file_name="Oussama_cv.pdf",
            mime="application/pdf"
        )
elif choose == "Certificates": 
    st.header("Certificates")
    st.subheader("Some Certificates from my past Courses!")
    with st.container():  
        col1, col2, col3 = st.columns((1,1,1))
        with col1:
            st.subheader("Generative Ai with Llms")
            show_pdf("genai.pdf")
        with col2:
            st.subheader("NLP Specialization")
            show_pdf("nlp.pdf")
        with col3:
            st.subheader("Deep Learning Specialization")
            show_pdf("deep_learning.pdf")
    with st.container():  
        col4, col5, col6 = st.columns((1,1,1))
        with col1:
            st.subheader("Machine Learning Specialization")
            show_pdf("ml.pdf")
        with col2:
            st.subheader("Mlops Certification")
            show_pdf("mlops.pdf")
        with col3:
            st.subheader("SQL Certification")
            show_pdf("sql.pdf")
elif choose == "Contact":

    st.header("Contact")
    def social_icons(width=24, height=24, **kwargs):
        icon_template = '''
        <a href="{url}" target="_blank" style="margin-right: 10px;">
            <img src="{icon_src}" alt="{alt_text}" width="{width}" height="{height}">
        </a>
        '''

        icons_html = ""
        for name, url in kwargs.items():
            icon_src = {
                "linkedin": "https://cdn-icons-png.flaticon.com/512/174/174857.png",
                "github": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
                "email": "https://cdn-icons-png.flaticon.com/512/561/561127.png"
            }.get(name.lower())

            if icon_src:
                icons_html += icon_template.format(url=url, icon_src=icon_src, alt_text=name.capitalize(), width=width, height=height)

        return icons_html
    with st.container():
        text_column, mid, image_column = st.columns((1,0.2,0.5))
        with text_column:
            st.write("Let's connect! You may either reach out to me at jemaaoussama64@gmail.com or use the form below!")
            
            contact_form = """
            <form action="https://formsubmit.co/jemaaoussama64@gmail.com" method="POST">
            <input type="hidden" name="_captcha value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="text" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit" >Send a Message</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)
            st.write("Alternatively, feel free to check out my social accounts below!")
            linkedin_url = "https://www.linkedin.com/in/oussama-jmaa-217098171/"
            github_url = "https://github.com/oussamaJMAA"
            email_url = "mailto:jemaaoussama64@gmail.com"
            st.markdown(
                social_icons(32, 32, LinkedIn=linkedin_url, GitHub=github_url, Email=email_url),
                unsafe_allow_html=True)
            st.markdown("")

elif choose =="Interview ChatBot":
    st.header("Interview ChatBot :book:")
    st.subheader("This is a chatbot that will help you to get to know me!")
    st.subheader("Feel free to ask him anything about my experience and knowledge")
    #load_dotenv()
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    
    user_question = st.text_input("Ask a question about oussama:")
    if user_question:
        raw_text = get_pdf_text()

                # get the text chunks
        text_chunks = get_text_chunks(raw_text)

                # create vector store
        vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
        st.session_state.conversation = get_conversation_chain(
                    vectorstore)
        user_prompt = f"""You are an AI assistant dedicated to assisting oussama in his job search by providing recruiters with relevant and concise information. 
    If you do not know the answer, politely admit it and let recruiters know how to contact oussama to get more information directly from him. 
    Don't put a breakline in the front of your answer.
    Human: {user_question}
    """
        handle_userinput(user_prompt)


st.markdown("*Copyright © 2023 Oussama Jmaa*")

