import webbrowser

import subprocess
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.express as px
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QLabel, QPushButton, QComboBox, QGridLayout, \
    QDesktopWidget
from datetime import date
from urllib.request import urlopen
from bs4 import BeautifulSoup
from fbprophet import Prophet
import plotly.graph_objects as go
from PyQt5.QtGui import QFont
from gui_bot import ChatInterface
from assessment import Window
from test_red_cross import Wid
import requests

user_input = 0
user_input_world = 0
user_input_china = 0
user_input_italy = 0
user_input_usa = 0

#for estimation of real data from website
url = "https://www.worldometers.info/coronavirus/#countries"
html_page=requests.get(url).text

soup=BeautifulSoup(html_page,'lxml')

get_table=soup.find("table",id="main_table_countries_today").find("tbody")
rows=get_table.find_all("tr",style="")


for row in rows:
    cols=row.find_all("td")
    country_info=[col.text.strip() for col in cols]



class Widget(QtWidgets.QWidget):

    print("hello yashi!!!")
    switch_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.chatbot = QPushButton(self)
        self.chatbot.setFixedWidth(100)
        self.chatbot.setFixedHeight(250)
        self.chatbot.setStyleSheet("background-image:url('chatbot.jpeg');border-radius: 50px;")
        self.chatbot.setToolTip('<b>May I help you?</b>')
        self.setWindowTitle("COVID Prediction")
        self.chatbot.clicked.connect(self.widget_c)
        self.button_india = QtWidgets.QPushButton('INDIA', self)
        self.button_world = QtWidgets.QPushButton('WORLD', self)
        self.button_china = QtWidgets.QPushButton('CHINA', self)
        self.button_usa = QtWidgets.QPushButton('USA', self)
        self.button_usa.setStyleSheet(
            "QPushButton{color:#FFFFFF;background-image: url(usa.png) 0 0 0 0 stretch stretch;}")
        self.button_italy = QtWidgets.QPushButton('ITALY', self)
        self.button_italy.setStyleSheet("border-image: url('italy.png') 0 0 0 0 stretch stretch;")
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        # self.heading= QtWidgets.QLabel("COVID Prediction",self)
        self.button_india.setStyleSheet("background-image: url(output-onlinepngtools.png) 0 0 0 0 stretch stretch;")
        # self.label = QtWidgets.QLabel(self)
        self.button_world.setStyleSheet("background-image: url(world.jpeg) 3 0 0 0 stretch stretch;")
        self.button_china.setStyleSheet("background-image: url(china.png) 0 0 0 0 stretch stretch;")

        self.assess = QPushButton(self)
        self.assess.setToolTip("<b>Click to take self assessment test</b>")
        self.assess.setFixedWidth(100)
        self.assess.setFixedHeight(200)

        self.assess.setStyleSheet("background-image:url('ass_pic.png');border-radius: 50px;")
        self.assess.clicked.connect(self.ass)

        f_date = date(2019, 11, 17)
        l_date = date.today()

        delta = l_date - f_date
        print(delta.days)

        # self.label.setText("Days: " + str(delta.days))

        # self.button_india.setIcon(QIcon('ezgif.com-webp-to-png.png'))
        # self.button_india.setIconSize(QSize(50, 10))

        self.button_india.move(0, 0)
        self.button_india.resize(6, 2)

        left = QWidget(self)
        right = QWidget(self)
        layout1 = QHBoxLayout(self)
        layout2 = QVBoxLayout(left)
        layout3 = QVBoxLayout(right)

        layout2.addWidget(self.button_world)
        layout2.addWidget(self.button_india)
        left.setFixedWidth(100)
        layout1.addWidget(left)
        right.setFixedWidth(100)
        layout1.addWidget(self.browser)

        layout2.addWidget(self.button_china)
        layout2.addWidget(self.button_usa)
        layout2.addWidget(self.button_italy)
        layout3.addWidget(self.assess)
        layout3.addWidget(self.chatbot)

        layout1.addWidget(right)

        # self.button.clicked.connect(self.show_graph)

        self.button_india.clicked.connect(self.widget)
        self.button_world.clicked.connect(self.widget1)
        self.button_china.clicked.connect(self.widget2)
        self.button_italy.clicked.connect(self.widget3)
        self.button_usa.clicked.connect(self.widget4)
        self.resize(1200, 850)

        # def show_graph(self):
        df = pd.read_csv("WHO-COVID-19-global-data.csv", parse_dates=['Date'])
        print(df.head())
        pd.set_option('display.max_columns', None)
        df.rename(columns={'Date': 'date', 'Country_code': 'code', 'Country': 'country',
                           'Confirmed': 'confirmed', 'Deaths': 'deaths', 'Recovered': 'recovered'}, inplace=True)
        print(df.head())
        df['active'] = df['confirmed'] - df['deaths'] - df['recovered']
        top = df[df['date'] == df['date'].max()]
        world = top.groupby('country')[['confirmed', 'deaths', 'active']].sum().reset_index()
        print(world.head())

        fig = px.choropleth(world, locations="country", locationmode="country names", color='active',
                            hover_name="country",
                            range_color=[1, 1000], color_continuous_scale='Peach',
                            title="We are fighting against it since <b style='color:red'>" + str(
                                delta.days) + "</b> days!")

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def widget(self):
        subprocess.call(["say", "-v", "Samantha","INDIA"])
        self.switch_window.emit()
        self.c = Controller()
        self.c.show_main()

    def widget1(self):
        subprocess.call(["say", "-v", "Samantha","WORLD"])
        self.switch_window.emit()
        self.c = Controller()
        self.c.show_main_world()

    def widget2(self):
        subprocess.call(["say", "-v", "Samantha","China"])
        #engine.say("CHINA")
        #engine.runAndWait()
        self.switch_window.emit()
        self.c = Controller()
        self.c.show_main_china()

    def widget3(self):
        subprocess.call(["say", "-v", "Samantha","Italy"])
        #engine.say("ITALY")
        #engine.runAndWait()
        self.switch_window.emit()
        self.c = Controller()
        self.c.show_main_italy()

    def widget4(self):
        subprocess.call(["say", "-v", "Samantha","USA"])
        #engine.say("USA")
        #engine.runAndWait()
        self.switch_window.emit()
        self.c = Controller()
        self.c.show_main_usa()

    def widget_c(self):
        subprocess.call(["say", "-v", "Samantha","Hey, Welcome aboard! Let's chat."])
        #engine.say("Hey, Welcome aboard! Let's chat.")
        # engine.setProperty('volume', 500)

        #engine.runAndWait()
        self.switch_window.emit()

        self.c = Controller()
        self.c.chatt()

    def ass(self):
        self.switch_window.emit()

        self.c = Controller()
        self.c.ase()

    def closeEvent(self, event):
        Wid.fun(self)


class IndiaNormal(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('India Statistics')
        self.resize(1000, 800)
        self.browser1 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser2 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser3 = QtWebEngineWidgets.QWebEngineView(self)

        self.button_scrap = QPushButton(self)
        self.button_scrap.setText("Live Data")
        self.lab = QLabel(self)

        self.label = QLabel(self)
        self.button = QPushButton(self)
        self.button.setText("Predict")
        self.label.setText("Enter the number of days")
        self.label.setFont(QFont('Arial', 20))
        self.entry_field = QTextEdit(self)
        self.entry_field.setFixedHeight(50)
        self.entry_field.setPlaceholderText("Write here.....")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser1)
        lay.addWidget(self.browser3)

        lay1.addWidget(self.button_scrap, 2)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.label)
        lay1.addWidget(self.entry_field)
        lay1.addWidget(self.button)
        lay1.addWidget(self.browser2, 2)
        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(650)
        wid1.setFixedWidth(650)

        # first plot
        df_india_cumulative = pd.read_csv("india_cases_cumulative_datewise.csv", parse_dates=['Date'])
        df_india_cumulative.rename(columns={'Date': 'date', 'Country_code': 'code', 'Country': 'country',
                                            'New_cases': 'new_cases', 'Cumulative_cases': 'cumulative_cases',
                                            'New_deaths': 'new_deaths', 'Cumulative_deaths': 'cumulative_deaths'},
                                   inplace=True)
        total_cases_cumulative = df_india_cumulative.groupby('date')['cumulative_cases'].sum().reset_index()
        total_cases_cumulative['date'] = pd.to_datetime(total_cases_cumulative['date'])

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=total_cases_cumulative.date.dt.date, y=total_cases_cumulative.cumulative_cases,
                                  mode='lines+markers', name="Cumulative Cases"))
        fig1.update_layout(title_text="Trend of Corona Virus in India on daily basis(Cumulative)",
                           plot_bgcolor='rgb(230,230,230)')

        # second plot
        df_india = pd.read_csv("india_state_wise.csv", parse_dates=True)
        df_india.rename(columns={'State': 'state', 'Active': 'active', 'Recovered': 'recovered', 'Deaths': 'deaths',
                                 'Confirmed': 'confirmed', }, inplace=True)
        total_active = df_india.groupby('state')['active'].sum().sort_values(ascending=False).head(10).reset_index()
        fig2 = px.bar(total_active, x=total_active.active, y=total_active.state,
                      hover_data=[total_active.active, total_active.state], color=total_active.active,
                      title="Top 10 states with the most Active Cases in India", labels={'Total Active Cases': 'State'},
                      height=400)
        # third plot
        fig3 = px.bar(df_india_cumulative, x=total_cases_cumulative.date.dt.date, y=df_india_cumulative['new_cases'],
                      barmode='group')
        fig3.update_layout(title_text="Trend of Corona Virus in India on daily basis", plot_bgcolor='rgb(230,250,230)')

        self.browser1.setHtml(fig1.to_html(include_plotlyjs='cdn'))
        self.browser2.setHtml(fig2.to_html(include_plotlyjs='cdn'))
        self.browser3.setHtml(fig3.to_html(include_plotlyjs='cdn'))
        self.button_scrap.clicked.connect(self.scrap_live_data)
        self.button.clicked.connect(self.switch)

    def scrap_live_data(self):
        # uClient = urlopen("https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data")
        # html_page = uClient.read()
        # uClient.close()
        # page_soup = BeautifulSoup(html_page, "html.parser")
        # print(page_soup)
        # d = page_soup.find('tbody').find_all('tr', class_="")
        # # print(d[6])
        # india_tds = d[6].find_all("td")
        # # print(india_tds)
        # india_text = "Cases " + india_tds[0].text + "\nDeaths " + india_tds[1].text



        #for India
        cols=rows[2].find_all("td")
        c=[col.text.strip() for col in cols]
        print(c[1],c[2],c[4])


        india_text = "Cases " + c[2] + "\nDeaths " + c[4]


        self.lab.setText(india_text)
        subprocess.call(["say", "-v", "Samantha",india_text])
        #engine.say(text=india_text)
        #engine.runAndWait()

    def switch(self):
        global user_input
        user_input = self.entry_field.toPlainText()
        subprocess.call(["say", "-v", "Samantha",f"Predicting for {user_input} days"])
        #engine.say("Predicting for " + user_input + " days")
        print("Predicting for" + user_input + "days")
        #engine.runAndWait()
        self.switch_window.emit()


class IndiaPrediction(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        global user_input
        self.setWindowTitle('India Prediction')
        self.resize(1000, 800)
        self.browser4 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser5 = QtWebEngineWidgets.QWebEngineView(self)

        self.stuck_pre = QLabel(self)
        self.stuck_pre1 = QLabel(self)
        self.stuck_pre.setText("Select the center from drop down list")
        self.stuck_pre.setStyleSheet("font-weight: bold");
        self.stuck_pre1.setText("Click to locate")
        self.stuck_pre1.setStyleSheet("font-weight: bold");
        self.comboBox_agra = QComboBox(self)
        self.comboBox_agra.addItem("Agra")
        self.comboBox_agra.addItem("SN Medical College Agra")
        self.comboBox_agra.addItem("National Jalma Institute For Leprosy Agra")
        self.comboBox_agra.addItem("District Hospital Agra")
        self.comboBox_agra.addItem("Scientific Pathology Agra")
        # self.comboBox_agra.move(50, 250)
        self.comboBox_lucknow = QComboBox(self)
        self.comboBox_lucknow.addItem("Lucknow")
        self.comboBox_lucknow.addItem("Charak Diagnostic Center Lucknow")
        self.comboBox_lucknow.addItem("Dept of Microbiology, Apollomedics Super Speciality Hospitals Lucknow")
        self.comboBox_lucknow.addItem("King George's Medical University Lucknow")
        self.comboBox_lucknow.addItem("Indian Institute Of Toxicology Research, Gheru Campus Lucknow")
        self.comboBox_lucknow.addItem("Dr. Ram Manohar Lohia Institute of Medical Sciences Lucknow")
        self.comboBox_lucknow.addItem("Ram Manohar Lohiya Hospital Lucknow")
        self.comboBox_lucknow.addItem("Sanjay Gandhi Postgraduate Institute of Medical Sciences Lucknow")
        self.comboBox_lucknow.addItem("Command Hospital Lucknow")
        self.comboBox_lucknow.addItem("Birbal Sahni Institute of Palaeosciences Lucknow")
        self.comboBox_lucknow.addItem("Balrampur Hospital Lucknow")
        self.comboBox_lucknow.addItem("CSIR-CDRI Lucknow")
        self.comboBox_lucknow.addItem("RML MEHROTRA PATHOLOGY PVT LTD Lucknow")
        # self.comboBox_lucknow.move(50, 250)
        self.comboBox_kanpur = QComboBox(self)
        self.comboBox_kanpur.addItem("Kanpur")
        self.comboBox_kanpur.addItem("KPM HOSPITAL Kanpur")
        self.comboBox_kanpur.addItem("LLR HOSPITAL Kanpur")
        self.comboBox_kanpur.addItem("REGENCY HOSPITAL Kanpur")
        self.comboBox_kanpur.addItem("UHM GOVERNMENT HOSPITAL Kanpur")
        self.comboBox_jhansi = QComboBox(self)
        self.comboBox_jhansi.addItem("Jhansi")
        self.comboBox_jhansi.addItem("MAHARANI LAXMI BAI MEDICAL COLLEGE Jhansi")
        self.comboBox_jhansi.addItem("DISTRICT HOSPITAL Jhansi")
        self.comboBox_jhansi.addItem("CHC BADAGAON Jhansi")
        self.comboBox_jhansi.addItem("ARMY HOSPITAL Jhansi")
        self.comboBox_jhansi.addItem("DIVISIONAL RAILWAY HOSPITAL Jhansi")
        self.comboBox_varanasi = QComboBox(self)
        self.comboBox_varanasi.addItem("Varanasi")
        self.comboBox_varanasi.addItem("Sir Sunderlal Hospital of Banaras Hindu University Varanasi")
        self.comboBox_varanasi.addItem("Pandit Deendayal upadhyay zila chikitsalaya Varanasi")
        self.comboBox_varanasi.addItem("ESIC Hospital Varanasi")
        self.comboBox_prayag = QComboBox(self)
        self.comboBox_prayag.addItem("Prayagraj")
        self.comboBox_prayag.addItem("TB Sapru hospital Prayagraj")
        self.comboBox_prayag.addItem("Medical College Prayagraj")
        self.comboBox_noida = QComboBox(self)
        self.comboBox_noida.addItem("Noida")
        self.comboBox_noida.addItem("Fortis Hospital Noida")
        self.comboBox_noida.addItem("Kailash Hospital Sector 27 Noida")
        self.comboBox_noida.addItem("Indo Gulf Hospital & diagnostics Noida")
        self.comboBox_noida.addItem("Manas hospital Noida")
        self.comboBox_meerut = QComboBox(self)
        self.comboBox_meerut.addItem("Meerut")
        self.comboBox_meerut.addItem("Anand Hospital Meerut")
        self.comboBox_meerut.addItem("New Meerut Hospital Meerut")
        self.comboBox_meerut.addItem("Yashlok Hospital Meerut")
        self.comboBox_meerut.addItem("Nexaa Hospital Meerut")
        self.comboBox_meerut.addItem("IIMT Life Line hospital Meerut")
        self.search_button_agra = QPushButton(self)
        self.search_button_agra.setText("Locate Agra")
        self.search_button_lucknow = QPushButton(self)
        self.search_button_lucknow.setText("Locate Lucknow")
        self.search_button_kanpur = QPushButton(self)
        self.search_button_kanpur.setText("Locate Kanpur")
        self.search_button_jhansi = QPushButton(self)
        self.search_button_jhansi.setText("Locate Jhansi")
        self.search_button_varanasi = QPushButton(self)
        self.search_button_varanasi.setText("Locate Varanasi")
        self.search_button_prayag = QPushButton(self)
        self.search_button_prayag.setText("Locate Prayagraj")
        self.search_button_noida = QPushButton(self)
        self.search_button_noida.setText("Locate Noida")
        self.search_button_meerut = QPushButton(self)
        self.search_button_meerut.setText("Locate Meerut")

        self.lab = QLabel(self)
        self.lab1 = QLabel(self)
        self.lab.setText("Future Prediction graphs are plotted according to the past data.")
        self.lab1.setText("They are not subjected to other measures taken.")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QGridLayout(wid1)
        lay.addWidget(self.browser4, 2)
        lay.addWidget(self.browser5, 2)
        lay1.addWidget(self.stuck_pre, 0, 0)
        lay1.addWidget(self.comboBox_agra, 1, 0)
        lay1.addWidget(self.comboBox_lucknow, 2, 0)
        lay1.addWidget(self.comboBox_kanpur, 3, 0)
        lay1.addWidget(self.comboBox_jhansi, 4, 0)
        lay1.addWidget(self.comboBox_varanasi, 5, 0)
        lay1.addWidget(self.comboBox_prayag, 6, 0)
        lay1.addWidget(self.comboBox_noida, 7, 0)
        lay1.addWidget(self.comboBox_meerut, 8, 0)
        lay1.addWidget(self.stuck_pre1, 0, 1)
        lay1.addWidget(self.search_button_agra, 1, 1)
        lay1.addWidget(self.search_button_lucknow, 2, 1)
        lay1.addWidget(self.search_button_kanpur, 3, 1)
        lay1.addWidget(self.search_button_jhansi, 4, 1)
        lay1.addWidget(self.search_button_varanasi, 5, 1)
        lay1.addWidget(self.search_button_prayag, 6, 1)
        lay1.addWidget(self.search_button_noida, 7, 1)
        lay1.addWidget(self.search_button_meerut, 8, 1)
        lay.addWidget(self.lab)
        lay.addWidget(self.lab1)

        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(750)
        wid1.setFixedWidth(500)
        wid1.setFixedHeight(300)

        self.search_button_agra.clicked.connect(self.fb_agra)
        self.search_button_lucknow.clicked.connect(self.fb_lucknow)
        self.search_button_kanpur.clicked.connect(self.fb_kanpur)
        self.search_button_jhansi.clicked.connect(self.fb_jhansi)
        self.search_button_varanasi.clicked.connect(self.fb_varanasi)
        self.search_button_prayag.clicked.connect(self.fb_prayag)
        self.search_button_noida.clicked.connect(self.fb_noida)
        self.search_button_meerut.clicked.connect(self.fb_meerut)

        df_india_cumulative = pd.read_csv("india_cases_cumulative_datewise.csv", parse_dates=['Date'])
        df_india_cumulative.rename(columns={'Date': 'date', 'Country_code': 'code', 'Country': 'country',
                                            'New_cases': 'new_cases', 'Cumulative_cases': 'cumulative_cases',
                                            'New_deaths': 'new_deaths', 'Cumulative_deaths': 'cumulative_deaths'},
                                   inplace=True)
        total_cases_cumulative = df_india_cumulative.groupby('date')['cumulative_cases'].sum().reset_index()
        total_cases_cumulative['date'] = pd.to_datetime(total_cases_cumulative['date'])
        confirm_india = df_india_cumulative.groupby('date').sum()['new_cases'].reset_index()
        # print(confirm_india.head())
        confirm_india.columns = ['ds', 'y']
        confirm_india['ds'] = pd.to_datetime(confirm_india['ds'])
        m = Prophet(interval_width=0.95)
        m.fit(confirm_india)

        future_confirm = m.make_future_dataframe(periods=int(user_input))
        print("AA gya" + user_input)
        forecast = m.predict(future_confirm)
        # print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail())
        # m.plot(forecast)

        fig4 = go.Figure()
        fig4.add_trace(
            go.Scatter(x=forecast['ds'].tail(10), y=forecast['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig4.update_layout(
            title_text="Future Prediction of Confirmed Cases in India on daily basis ",
            plot_bgcolor='rgb(0,0,0)')
        # graph for future prediction of confirmed cases

        deaths_india = df_india_cumulative.groupby('date').sum()['new_deaths'].reset_index()
        deaths_india.columns = ['ds', 'y']
        deaths_india['ds'] = pd.to_datetime(deaths_india['ds'])
        n = Prophet(interval_width=0.95)
        n.fit(deaths_india)
        future_death = n.make_future_dataframe(periods=int(user_input))
        forecast_death = n.predict(future_death)
        print(forecast_death[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        fig5 = go.Figure()
        fig5.add_trace(
            go.Scatter(x=forecast_death['ds'].tail(10), y=forecast_death['yhat'].tail(10), mode='lines+markers',
                       name="Future"))
        fig5.update_layout(title_text="Future Prediction of Death Cases in India on daily basis ",
                           plot_bgcolor='rgb(0,0,0)')
        # graph for future prediction of deaths
        self.browser4.setHtml(fig4.to_html(include_plotlyjs='cdn'))
        self.browser5.setHtml(fig5.to_html(include_plotlyjs='cdn'))

    def fb_agra(self):
        if self.comboBox_agra.currentText() != "Agra":
            #engine.say("Locating " + self.comboBox_agra.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_agra.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    def fb_lucknow(self):
        if self.comboBox_lucknow.currentText() != "Lucknow":
            #engine.say("Locating " + self.comboBox_lucknow.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_lucknow.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    def fb_kanpur(self):
        if self.comboBox_kanpur.currentText() != "Kanpur":
            #engine.say("Locating " + self.comboBox_kanpur.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_kanpur.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    def fb_jhansi(self):
        if self.comboBox_jhansi.currentText() != "Jhansi":
            #engine.say("Locating " + self.comboBox_jhansi.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_jhansi.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    def fb_varanasi(self):
        if self.comboBox_varanasi.currentText() != "Varanasi":
            #engine.say("Locating " + self.comboBox_varanasi.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_varanasi.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    def fb_prayag(self):
        if self.comboBox_prayag.currentText() != "Prayagraj":
            #engine.say("Locating " + self.comboBox_prayag.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_prayag.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    def fb_noida(self):
        if self.comboBox_noida.currentText() != "Noida":
            #engine.say("Locating " + self.comboBox_noida.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_noida.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    def fb_meerut(self):
        if self.comboBox_meerut.currentText() != "Meerut":
            #engine.say("Locating " + self.comboBox_meerut.currentText() + "on Google Map")
            #engine.runAndWait()
            place = self.comboBox_meerut.currentText().replace(" ", "+")
            webbrowser.open("https://www.google.com/maps/place/" + place)

    # def switch(self):
    #     self.user_input = self.entry_field.toPlainText()
    #     engine.say("Predicting for " + self.user_input + " days")
    #     # print("Predicting for"+user_input+"days")
    #     engine.runAndWait()
    #     self.switch_window.emit()


class WorldNormal(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('World Statistics')
        self.resize(1000, 800)
        self.browser1 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser2 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser3 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser4 = QtWebEngineWidgets.QWebEngineView(self)

        self.button_scrap = QPushButton(self)
        self.button_scrap.setText("Live Data")
        self.lab = QLabel(self)

        self.label = QLabel(self)
        self.button = QPushButton(self)
        self.button.setText("Predict")
        self.label.setText("Enter the number of days")
        self.label.setFont(QFont('Arial', 15))
        self.entry_field = QTextEdit(self)
        self.entry_field.setFixedHeight(30)
        self.entry_field.setPlaceholderText("Write here.....")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.button_scrap)
        lay.addWidget(self.lab)
        lay.addWidget(self.browser2, 2)
        lay.addWidget(self.browser4, 2)

        lay1.addWidget(self.label)
        lay1.addWidget(self.entry_field)
        lay1.addWidget(self.button)
        lay1.addWidget(self.browser1, 4)
        lay1.addWidget(self.browser3, 4)
        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(650)
        wid1.setFixedWidth(650)

        
    def scrap_live_data(self):
        cols=rows[0].find_all("td")
        c=[col.text.strip() for col in cols]
        print(c[1],c[2],c[4])


        india_text = "Cases " + c[2] + "\nDeaths " + c[4]


        self.lab.setText(india_text)
        subprocess.call(["say", "-v", "Samantha",india_text])

    def switch(self):
        global user_input_world
        user_input_world = self.entry_field.toPlainText()
        subprocess.call(["say", "-v", "Samantha",f"Predicting for {user_input_world} days"])
        #engine.say("Predicting for " + user_input_world + " days")
        print("Predicting for" + user_input_world + "days")
        #engine.runAndWait()
        self.switch_window.emit()


class WorldPrediction(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        global user_input_world
        self.setWindowTitle('World Prediction')
        self.resize(1000, 800)
        self.browser4 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser5 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser6 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser7 = QtWebEngineWidgets.QWebEngineView(self)
        self.lab = QLabel(self)
        self.lab1 = QLabel(self)
        self.lab.setText("Future Prediction graphs are plotted according to the past data.")
        self.lab1.setText("They are not subjected to other measures taken.")
        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser4)
        lay.addWidget(self.browser5)
        lay1.addWidget(self.browser6, 2)
        lay1.addWidget(self.browser7, 2)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.lab1)

        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(650)
        wid1.setFixedWidth(650)

        #
        df = pd.read_csv("WHO-COVID-19-global-data.csv", parse_dates=['Date'])
        # print(df.head())
        # pd.set_option('display.max_columns', None)
        df.rename(columns={'Date': 'date', 'Country_code': 'code', 'Country': 'country',
                           'Confirmed': 'confirmed', 'Deaths': 'deaths', 'Recovered': 'recovered'}, inplace=True)

        # print(df.head())
        df['active'] = df['confirmed'] - df['deaths'] - df['recovered']
        confirmed_cases = df.groupby('date').sum()['confirmed'].reset_index()
        confirmed_cases['date'] = pd.to_datetime(confirmed_cases['date'])
        confirm_world = df.groupby('date').sum()['confirmed'].reset_index()

        confirm_world.columns = ['ds', 'y']
        confirm_world['ds'] = pd.to_datetime(confirm_world['ds'])
        m = Prophet(interval_width=0.95)
        m.fit(confirm_world)

        future_confirm = m.make_future_dataframe(periods=int(user_input_world))
        print("AA gya" + user_input_world)
        forecast = m.predict(future_confirm)
        # print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail())
        # m.plot(forecast)
        # plot for confirmed cases world
        fig4 = go.Figure()
        fig4.add_trace(
            go.Scatter(x=forecast['ds'].tail(10), y=forecast['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig4.update_layout(
            title_text="Future Prediction of Confirmed Cases in the World on daily basis ",
            plot_bgcolor='rgb(0,0,0)')

        active_cases = df.groupby('date').sum()['active'].reset_index()
        active_cases['date'] = pd.to_datetime(active_cases['date'])
        active_world = df.groupby('date').sum()['active'].reset_index()

        active_world.columns = ['ds', 'y']
        active_world['ds'] = pd.to_datetime(active_world['ds'])
        o = Prophet(interval_width=0.95)
        o.fit(active_world)

        future_active = o.make_future_dataframe(periods=int(user_input_world))
        print("AA gya" + user_input_world)
        forecast1 = o.predict(future_active)

        # plot for confirmed cases world
        fig5 = go.Figure()
        fig5.add_trace(
            go.Scatter(x=forecast1['ds'].tail(10), y=forecast1['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig5.update_layout(
            title_text="Future Prediction of Active Cases in the World on daily basis ",
            plot_bgcolor='rgb(0,0,0)')

        death_cases = df.groupby('date').sum()['deaths'].reset_index()
        death_cases['date'] = pd.to_datetime(death_cases['date'])
        death_world = df.groupby('date').sum()['deaths'].reset_index()

        death_world.columns = ['ds', 'y']
        death_world['ds'] = pd.to_datetime(death_world['ds'])
        p = Prophet(interval_width=0.95)
        p.fit(death_world)

        future_death = p.make_future_dataframe(periods=int(user_input_world))
        print("AA gya" + user_input_world)
        forecast2 = p.predict(future_death)

        # plot for death cases world
        fig6 = go.Figure()
        fig6.add_trace(
            go.Scatter(x=forecast2['ds'].tail(10), y=forecast2['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig6.update_layout(
            title_text="Future Prediction of Death Cases in the World on daily basis ",
            plot_bgcolor='rgb(0,0,0)')

        recovered_cases = df.groupby('date').sum()['recovered'].reset_index()
        recovered_cases['date'] = pd.to_datetime(recovered_cases['date'])
        recovered_world = df.groupby('date').sum()['recovered'].reset_index()

        recovered_world.columns = ['ds', 'y']
        recovered_world['ds'] = pd.to_datetime(recovered_world['ds'])
        q = Prophet(interval_width=0.95)
        q.fit(recovered_world)

        future_recovered = q.make_future_dataframe(periods=int(user_input_world))
        print("AA gya" + user_input_world)
        forecast3 = q.predict(future_recovered)

        # plot for confirmed cases world
        fig7 = go.Figure()
        fig7.add_trace(
            go.Scatter(x=forecast3['ds'].tail(10), y=forecast3['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig7.update_layout(
            title_text="Future Prediction of Recovered Cases in the World on daily basis ",
            plot_bgcolor='rgb(0,0,0)')

        self.browser4.setHtml(fig4.to_html(include_plotlyjs='cdn'))
        self.browser5.setHtml(fig5.to_html(include_plotlyjs='cdn'))
        self.browser6.setHtml(fig6.to_html(include_plotlyjs='cdn'))
        self.browser7.setHtml(fig7.to_html(include_plotlyjs='cdn'))

    # def switch(self):
    #     self.user_input = self.entry_field.toPlainText()
    #     engine.say("Predicting for " + self.user_input + " days")
    #     # print("Predicting for"+user_input+"days")
    #     engine.runAndWait()
    #     self.switch_window.emit()


class ChinaNormal(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('China Statistics')
        self.resize(1000, 800)
        self.browser1 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser2 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser3 = QtWebEngineWidgets.QWebEngineView(self)

        self.button_scrap = QPushButton(self)
        self.button_scrap.setText("Live Data")
        self.lab = QLabel(self)

        self.label = QLabel(self)
        self.button = QPushButton(self)
        self.button.setText("Predict")
        self.label.setText("Enter the number of days")
        self.label.setFont(QFont('Arial', 20))
        self.entry_field = QTextEdit(self)
        self.entry_field.setFixedHeight(50)
        self.entry_field.setPlaceholderText("Write here.....")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser1)
        lay.addWidget(self.browser3)

        lay1.addWidget(self.button_scrap, 2)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.label)
        lay1.addWidget(self.entry_field)
        lay1.addWidget(self.button)
        lay1.addWidget(self.browser2, 2)
        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(650)
        wid1.setFixedWidth(650)

        df_china = pd.read_csv("china_dataset.csv", parse_dates=['Date'])
        df_china.rename(columns={'Date': 'date', 'Country': 'country',
                                 'Confirmed': 'confirmed', 'Deaths': 'deaths',
                                 'Recovered': 'recovered'},
                        inplace=True)
        china_cases_confirmed = df_china.groupby('date')['confirmed'].sum().reset_index()
        china_cases_confirmed['date'] = pd.to_datetime(china_cases_confirmed['date'])

        # first plot
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=china_cases_confirmed.date.dt.date, y=china_cases_confirmed.confirmed,
                                  mode='lines+markers', name="Confirmed Cases"))
        fig1.update_layout(title_text="Trend of Confirmed Corona Virus in China on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        china_cases_deaths = df_china.groupby('date')['deaths'].sum().reset_index()
        china_cases_deaths['date'] = pd.to_datetime(china_cases_deaths['date'])

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=china_cases_deaths.date.dt.date, y=china_cases_deaths.deaths,
                                  mode='lines+markers', name="Death Cases"))
        fig2.update_layout(title_text="Trend of Death Corona Virus in China on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        china_cases_recovered = df_china.groupby('date')['recovered'].sum().reset_index()
        china_cases_recovered['date'] = pd.to_datetime(china_cases_recovered['date'])

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=china_cases_recovered.date.dt.date, y=china_cases_recovered.recovered,
                                  mode='lines+markers', name="Recovered Cases"))
        fig3.update_layout(title_text="Trend of Recovered Corona Virus in China on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        self.browser1.setHtml(fig1.to_html(include_plotlyjs='cdn'))
        self.browser2.setHtml(fig2.to_html(include_plotlyjs='cdn'))
        self.browser3.setHtml(fig3.to_html(include_plotlyjs='cdn'))
        self.button_scrap.clicked.connect(self.scrap_live_data)
        self.button.clicked.connect(self.switch)

    def scrap_live_data(self):
        cols=rows[197].find_all("td")
        c=[col.text.strip() for col in cols]
        print(c[1],c[2],c[4])


        india_text = "Cases " + c[2] + "\nDeaths " + c[4]


        self.lab.setText(india_text)
        subprocess.call(["say", "-v", "Samantha",india_text])

    def switch(self):
        global user_input_china
        user_input_china = self.entry_field.toPlainText()
        subprocess.call(["say", "-v", "Samantha",f"Predicting for {user_input_china} days"])
        #engine.say("Predicting for " + user_input_china + " days")
        print("Predicting for" + user_input_china + "days")
        #engine.runAndWait()
        self.switch_window.emit()


class ChinaPrediction(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        global user_input_china
        self.setWindowTitle('China Prediction')
        self.resize(1000, 800)
        self.browser4 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser5 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser6 = QtWebEngineWidgets.QWebEngineView(self)
        self.lab = QLabel(self)
        self.lab1 = QLabel(self)
        self.lab.setText("Future Prediction graphs are plotted according to the past data.")
        self.lab1.setText("They are not subjected to other measures taken.")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser4)
        lay.addWidget(self.browser5)
        lay1.addWidget(self.browser6, 3)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.lab1)

        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(640)
        wid1.setFixedWidth(640)
        # wid1.setFixedHeight(300)

        df_china = pd.read_csv("china_dataset.csv", parse_dates=['Date'])
        df_china.rename(columns={'Date': 'date', 'Country': 'country',
                                 'Confirmed': 'confirmed', 'Deaths': 'deaths',
                                 'Recovered': 'recovered'},
                        inplace=True)
        china_cases_confirmed = df_china.groupby('date')['confirmed'].sum().reset_index()
        china_cases_confirmed['date'] = pd.to_datetime(china_cases_confirmed['date'])

        confirm_china = df_china.groupby('date').sum()['confirmed'].reset_index()
        # print(confirm_india.head())
        confirm_china.columns = ['ds', 'y']
        confirm_china['ds'] = pd.to_datetime(confirm_china['ds'])
        m = Prophet(interval_width=0.95)
        m.fit(confirm_china)

        future_confirm = m.make_future_dataframe(periods=int(user_input_china))
        print("AA gya" + user_input_china)
        forecast = m.predict(future_confirm)
        # print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail())
        # m.plot(forecast)

        fig4 = go.Figure()
        fig4.add_trace(
            go.Scatter(x=forecast['ds'].tail(10), y=forecast['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig4.update_layout(
            title_text="Future Prediction of Confirmed Cases in China on daily basis ",
            plot_bgcolor='rgb(0,0,0)')
        # graph for future prediction of confirmed cases

        deaths_china = df_china.groupby('date').sum()['deaths'].reset_index()
        deaths_china.columns = ['ds', 'y']
        deaths_china['ds'] = pd.to_datetime(deaths_china['ds'])
        n = Prophet(interval_width=0.95)
        n.fit(deaths_china)
        future_death = n.make_future_dataframe(periods=int(user_input_china))
        forecast_death = n.predict(future_death)
        print(forecast_death[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        fig5 = go.Figure()
        fig5.add_trace(
            go.Scatter(x=forecast_death['ds'].tail(10), y=forecast_death['yhat'].tail(10), mode='lines+markers',
                       name="Future"))
        fig5.update_layout(title_text="Future Prediction of Death Cases in China on daily basis ",
                           plot_bgcolor='rgb(0,0,0)')
        china_cases_recovered = df_china.groupby('date')['recovered'].sum().reset_index()
        china_cases_recovered['date'] = pd.to_datetime(china_cases_recovered['date'])
        recovered_china = df_china.groupby('date').sum()['recovered'].reset_index()
        recovered_china.columns = ['ds', 'y']
        recovered_china['ds'] = pd.to_datetime(recovered_china['ds'])
        o = Prophet(interval_width=0.95)
        o.fit(recovered_china)
        future_recovered = o.make_future_dataframe(periods=int(user_input_china))
        forecast_recovered = o.predict(future_recovered)
        print(forecast_recovered[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        fig6 = go.Figure()
        fig6.add_trace(
            go.Scatter(x=forecast_recovered['ds'].tail(10), y=forecast_recovered['yhat_upper'].tail(10),
                       mode='lines+markers',
                       name="Future"))
        fig6.update_layout(title_text="Future Prediction of Recovered Cases in China on daily basis ",
                           plot_bgcolor='rgb(0,0,0)')

        # graph for future prediction of recovered
        self.browser4.setHtml(fig4.to_html(include_plotlyjs='cdn'))
        self.browser5.setHtml(fig5.to_html(include_plotlyjs='cdn'))
        self.browser6.setHtml(fig6.to_html(include_plotlyjs='cdn'))

    # def switch(self):
    #     self.user_input = self.entry_field.toPlainText()
    #     engine.say("Predicting for " + self.user_input + " days")
    #     # print("Predicting for"+user_input+"days")
    #     engine.runAndWait()
    #     self.switch_window.emit()


class ItalyNormal(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Italy Statistics')
        self.resize(1000, 800)
        self.browser1 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser2 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser3 = QtWebEngineWidgets.QWebEngineView(self)

        self.button_scrap = QPushButton(self)
        self.button_scrap.setText("Live Data")
        self.lab = QLabel(self)

        self.label = QLabel(self)
        self.button = QPushButton(self)
        self.button.setText("Predict")
        self.label.setText("Enter the number of days")
        self.label.setFont(QFont('Arial', 20))
        self.entry_field = QTextEdit(self)
        self.entry_field.setFixedHeight(50)
        self.entry_field.setPlaceholderText("Write here.....")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser1)
        lay.addWidget(self.browser3)

        lay1.addWidget(self.button_scrap, 2)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.label)
        lay1.addWidget(self.entry_field)
        lay1.addWidget(self.button)
        lay1.addWidget(self.browser2, 2)
        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(650)
        wid1.setFixedWidth(650)

        df_italy = pd.read_csv("italy_dataset.csv", parse_dates=['Date'])
        df_italy.rename(columns={'Date': 'date', 'Country': 'country',
                                 'Confirmed': 'confirmed', 'Deaths': 'deaths',
                                 'Recovered': 'recovered'},
                        inplace=True)
        italy_cases_confirmed = df_italy.groupby('date')['confirmed'].sum().reset_index()
        italy_cases_confirmed['date'] = pd.to_datetime(italy_cases_confirmed['date'])

        # first plot
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=italy_cases_confirmed.date.dt.date, y=italy_cases_confirmed.confirmed,
                                  mode='lines+markers', name="Confirmed Cases"))
        fig1.update_layout(title_text="Trend of Confirmed Corona Virus in Italy on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        italy_cases_deaths = df_italy.groupby('date')['deaths'].sum().reset_index()
        italy_cases_deaths['date'] = pd.to_datetime(italy_cases_deaths['date'])

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=italy_cases_deaths.date.dt.date, y=italy_cases_deaths.deaths,
                                  mode='lines+markers', name="Death Cases"))
        fig2.update_layout(title_text="Trend of Death Corona Virus in Italy on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        italy_cases_recovered = df_italy.groupby('date')['recovered'].sum().reset_index()
        italy_cases_recovered['date'] = pd.to_datetime(italy_cases_recovered['date'])

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=italy_cases_recovered.date.dt.date, y=italy_cases_recovered.recovered,
                                  mode='lines+markers', name="Recovered Cases"))
        fig3.update_layout(title_text="Trend of Recovered Corona Virus in Italy on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        self.browser1.setHtml(fig1.to_html(include_plotlyjs='cdn'))
        self.browser2.setHtml(fig2.to_html(include_plotlyjs='cdn'))
        self.browser3.setHtml(fig3.to_html(include_plotlyjs='cdn'))
        self.button_scrap.clicked.connect(self.scrap_live_data)
        self.button.clicked.connect(self.switch)

    def scrap_live_data(self):
        cols=rows[6].find_all("td")
        c=[col.text.strip() for col in cols]
        print(c[1],c[2],c[4])


        india_text = "Cases " + c[2] + "\nDeaths " + c[4]


        self.lab.setText(india_text)
        subprocess.call(["say", "-v", "Samantha",india_text])

    def switch(self):
        global user_input_italy
        user_input_italy = self.entry_field.toPlainText()
        subprocess.call(["say", "-v", "Samantha",f"Predicting for {user_input_italy} days"])
        #engine.say("Predicting for " + user_input_italy + " days")
        print("Predicting for" + user_input_italy + "days")
        #engine.runAndWait()
        self.switch_window.emit()


class ItalyPrediction(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        global user_input
        self.setWindowTitle('Italy Prediction')
        self.resize(1000, 800)
        self.browser4 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser5 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser6 = QtWebEngineWidgets.QWebEngineView(self)
        self.lab = QLabel(self)
        self.lab1 = QLabel(self)
        self.lab.setText("Future Prediction graphs are plotted according to the past data.")
        self.lab1.setText("They are not subjected to other measures taken.")
        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser4)
        lay.addWidget(self.browser5)
        lay1.addWidget(self.browser6, 3)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.lab1)

        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(640)
        wid1.setFixedWidth(640)
        # wid1.setFixedHeight(300)

        df_italy = pd.read_csv("italy_dataset.csv", parse_dates=['Date'])
        df_italy.rename(columns={'Date': 'date', 'Country': 'country',
                                 'Confirmed': 'confirmed', 'Deaths': 'deaths',
                                 'Recovered': 'recovered'},
                        inplace=True)
        italy_cases_confirmed = df_italy.groupby('date')['confirmed'].sum().reset_index()
        italy_cases_confirmed['date'] = pd.to_datetime(italy_cases_confirmed['date'])

        confirm_italy = df_italy.groupby('date').sum()['confirmed'].reset_index()
        # print(confirm_india.head())
        confirm_italy.columns = ['ds', 'y']
        confirm_italy['ds'] = pd.to_datetime(confirm_italy['ds'])
        m = Prophet(interval_width=0.95)
        m.fit(confirm_italy)

        future_confirm = m.make_future_dataframe(periods=int(user_input_italy))
        print("AA gya" + user_input_italy)
        forecast = m.predict(future_confirm)
        # print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail())
        # m.plot(forecast)

        fig4 = go.Figure()
        fig4.add_trace(
            go.Scatter(x=forecast['ds'].tail(10), y=forecast['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig4.update_layout(
            title_text="Future Prediction of Confirmed Cases in Italy on daily basis ",
            plot_bgcolor='rgb(0,0,0)')
        # graph for future prediction of confirmed cases

        deaths_italy = df_italy.groupby('date').sum()['deaths'].reset_index()
        deaths_italy.columns = ['ds', 'y']
        deaths_italy['ds'] = pd.to_datetime(deaths_italy['ds'])
        n = Prophet(interval_width=0.95)
        n.fit(deaths_italy)
        future_death = n.make_future_dataframe(periods=int(user_input_italy))
        forecast_death = n.predict(future_death)
        print(forecast_death[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        fig5 = go.Figure()
        fig5.add_trace(
            go.Scatter(x=forecast_death['ds'].tail(10), y=forecast_death['yhat'].tail(10), mode='lines+markers',
                       name="Future"))
        fig5.update_layout(title_text="Future Prediction of Death Cases in Italy on daily basis ",
                           plot_bgcolor='rgb(0,0,0)')
        recovered_italy = df_italy.groupby('date').sum()['recovered'].reset_index()
        recovered_italy.columns = ['ds', 'y']
        recovered_italy['ds'] = pd.to_datetime(recovered_italy['ds'])
        o = Prophet(interval_width=0.95)
        o.fit(recovered_italy)
        future_recovered = o.make_future_dataframe(periods=int(user_input_italy))
        forecast_recovered = o.predict(future_recovered)
        print(forecast_recovered[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        fig6 = go.Figure()
        fig6.add_trace(
            go.Scatter(x=forecast_recovered['ds'].tail(10), y=forecast_recovered['yhat_upper'].tail(10),
                       mode='lines+markers',
                       name="Future"))
        fig6.update_layout(title_text="Future Prediction of Recovered in Italy on daily basis",
                           plot_bgcolor='rgb(0,0,0)')
        # graph for future prediction of recovered
        self.browser4.setHtml(fig4.to_html(include_plotlyjs='cdn'))
        self.browser5.setHtml(fig5.to_html(include_plotlyjs='cdn'))
        self.browser6.setHtml(fig6.to_html(include_plotlyjs='cdn'))

    # def switch(self):
    #     self.user_input = self.entry_field.toPlainText()
    #     engine.say("Predicting for " + self.user_input + " days")
    #     # print("Predicting for"+user_input+"days")
    #     engine.runAndWait()
    #     self.switch_window.emit()


class USANormal(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('USA Statistics')
        self.resize(1000, 800)
        self.browser1 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser2 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser3 = QtWebEngineWidgets.QWebEngineView(self)

        self.button_scrap = QPushButton(self)
        self.button_scrap.setText("Live Data")
        self.lab = QLabel(self)

        self.label = QLabel(self)
        self.button = QPushButton(self)
        self.button.setText("Predict")
        self.label.setText("Enter the number of days")
        self.label.setFont(QFont('Arial', 20))
        self.entry_field = QTextEdit(self)
        self.entry_field.setFixedHeight(50)
        self.entry_field.setPlaceholderText("Write here.....")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser1)
        lay.addWidget(self.browser3)

        lay1.addWidget(self.button_scrap, 2)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.label)
        lay1.addWidget(self.entry_field)
        lay1.addWidget(self.button)
        lay1.addWidget(self.browser2, 2)
        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(650)
        wid1.setFixedWidth(650)

        df_usa = pd.read_csv("usa_dataset.csv", parse_dates=['Date'])
        df_usa.rename(columns={'Date': 'date', 'Country': 'country',
                               'Confirmed': 'confirmed', 'Deaths': 'deaths',
                               'Recovered': 'recovered'},
                      inplace=True)
        usa_cases_confirmed = df_usa.groupby('date')['confirmed'].sum().reset_index()
        usa_cases_confirmed['date'] = pd.to_datetime(usa_cases_confirmed['date'])

        # first plot
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=usa_cases_confirmed.date.dt.date, y=usa_cases_confirmed.confirmed,
                                  mode='lines+markers', name="Confirmed Cases"))
        fig1.update_layout(title_text="Trend of Confirmed Corona Virus in USA on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        usa_cases_deaths = df_usa.groupby('date')['deaths'].sum().reset_index()
        usa_cases_deaths['date'] = pd.to_datetime(usa_cases_deaths['date'])

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=usa_cases_deaths.date.dt.date, y=usa_cases_deaths.deaths,
                                  mode='lines+markers', name="Death Cases"))
        fig2.update_layout(title_text="Trend of Death Corona Virus in USA on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        usa_cases_recovered = df_usa.groupby('date')['recovered'].sum().reset_index()
        usa_cases_recovered['date'] = pd.to_datetime(usa_cases_recovered['date'])

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=usa_cases_recovered.date.dt.date, y=usa_cases_recovered.recovered,
                                  mode='lines+markers', name="Recovered Cases"))
        fig3.update_layout(title_text="Trend of Recovered Corona Virus in USA on daily basis",
                           plot_bgcolor='rgb(230,230,230)')

        self.browser1.setHtml(fig1.to_html(include_plotlyjs='cdn'))
        self.browser2.setHtml(fig2.to_html(include_plotlyjs='cdn'))
        self.browser3.setHtml(fig3.to_html(include_plotlyjs='cdn'))
        self.button_scrap.clicked.connect(self.scrap_live_data)
        self.button.clicked.connect(self.switch)

    def scrap_live_data(self):
        cols=rows[1].find_all("td")
        c=[col.text.strip() for col in cols]
        print(c[1],c[2],c[4])


        india_text = "Cases " + c[2] + "\nDeaths " + c[4]


        self.lab.setText(india_text)
        subprocess.call(["say", "-v", "Samantha",india_text])

    def switch(self):
        global user_input_usa
        user_input_usa = self.entry_field.toPlainText()
        #engine.say("Predicting for " + user_input_usa + " days")
        subprocess.call(["say", "-v", "Samantha",f"Predicting for {user_input_usa} days"])
        print("Predicting for" + user_input_usa + "days")
        #engine.runAndWait()
        self.switch_window.emit()


class USAPrediction(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        global user_input
        self.setWindowTitle('USA Prediction')
        self.resize(1000, 800)
        self.browser4 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser5 = QtWebEngineWidgets.QWebEngineView(self)
        self.browser6 = QtWebEngineWidgets.QWebEngineView(self)
        self.lab = QLabel(self)
        self.lab1 = QLabel(self)
        self.lab.setText("Future Prediction graphs are plotted according to the past data.")
        self.lab1.setText("They are not subjected to other measures taken.")

        wid = QWidget(self)
        wid1 = QWidget(self)
        layy = QHBoxLayout(self)
        lay = QVBoxLayout(wid)
        lay1 = QVBoxLayout(wid1)
        lay.addWidget(self.browser4)
        lay.addWidget(self.browser5)
        lay1.addWidget(self.browser6, 3)
        lay1.addWidget(self.lab)
        lay1.addWidget(self.lab1)

        layy.addWidget(wid)
        layy.addWidget(wid1)
        wid.setFixedWidth(690)
        wid1.setFixedWidth(640)
        # wid1.setFixedHeight(300)

        df_usa = pd.read_csv("usa_dataset.csv", parse_dates=['Date'])
        df_usa.rename(columns={'Date': 'date', 'Country': 'country',
                               'Confirmed': 'confirmed', 'Deaths': 'deaths',
                               'Recovered': 'recovered'},
                      inplace=True)
        usa_cases_confirmed = df_usa.groupby('date')['confirmed'].sum().reset_index()
        usa_cases_confirmed['date'] = pd.to_datetime(usa_cases_confirmed['date'])

        confirm_usa = df_usa.groupby('date').sum()['confirmed'].reset_index()
        # print(confirm_india.head())
        confirm_usa.columns = ['ds', 'y']
        confirm_usa['ds'] = pd.to_datetime(confirm_usa['ds'])
        m = Prophet(interval_width=0.95)
        m.fit(confirm_usa)

        future_confirm = m.make_future_dataframe(periods=int(user_input_usa))
        print("AA gya" + user_input_usa)
        forecast = m.predict(future_confirm)
        # print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail())
        # m.plot(forecast)

        fig4 = go.Figure()
        fig4.add_trace(
            go.Scatter(x=forecast['ds'].tail(10), y=forecast['yhat'].tail(10), mode='lines+markers', name="Future"))
        fig4.update_layout(
            title_text="Future Prediction of Confirmed Cases in USA on daily basis ",
            plot_bgcolor='rgb(0,0,0)')
        # graph for future prediction of confirmed cases

        deaths_usa = df_usa.groupby('date').sum()['deaths'].reset_index()
        deaths_usa.columns = ['ds', 'y']
        deaths_usa['ds'] = pd.to_datetime(deaths_usa['ds'])
        n = Prophet(interval_width=0.95)
        n.fit(deaths_usa)
        future_death = n.make_future_dataframe(periods=int(user_input_usa))
        forecast_death = n.predict(future_death)
        print(forecast_death[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        fig5 = go.Figure()
        fig5.add_trace(
            go.Scatter(x=forecast_death['ds'].tail(10), y=forecast_death['yhat'].tail(10), mode='lines+markers',
                       name="Future"))
        fig5.update_layout(title_text="Future Prediction of Death Cases in USA on daily basis ",
                           plot_bgcolor='rgb(0,0,0)')
        recovered_usa = df_usa.groupby('date').sum()['recovered'].reset_index()
        recovered_usa.columns = ['ds', 'y']
        recovered_usa['ds'] = pd.to_datetime(recovered_usa['ds'])
        o = Prophet(interval_width=0.95)
        o.fit(recovered_usa)
        future_recovered = o.make_future_dataframe(periods=int(user_input_usa))
        forecast_recovered = o.predict(future_recovered)
        print(forecast_recovered[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        fig6 = go.Figure()
        fig6.add_trace(
            go.Scatter(x=forecast_recovered['ds'].tail(10), y=forecast_recovered['yhat'].tail(10), mode='lines+markers',
                       name="Future"))
        fig6.update_layout(title_text="Future Prediction of Recovered Cases in USA on daily basis ",
                           plot_bgcolor='rgb(0,0,0)')
        # graph for future prediction of recovered
        self.browser4.setHtml(fig4.to_html(include_plotlyjs='cdn'))
        self.browser5.setHtml(fig5.to_html(include_plotlyjs='cdn'))
        self.browser6.setHtml(fig6.to_html(include_plotlyjs='cdn'))

    # def switch(self):
    #     self.user_input = self.entry_field.toPlainText()
    #     engine.say("Predicting for " + self.user_input + " days")
    #     # print("Predicting for"+user_input+"days")
    #     engine.runAndWait()
    #     self.switch_window.emit()


width = 400
height = 400


class Controller:

    def __init__(self):
        pass

    def show_widget(self):
        self.widget = Widget()
        # self.bot=ChatInterface()
        # self.bot.show()
        self.widget.show()
        # self.widget.switch_window.connect(self.show_main)
        subprocess.call(["say", "-v", "Samantha","Welcome to Covid Prediction"])

        
        #engine.say("Welcome to COVID Prediction")
        #engine.runAndWait()

    def show_main(self):
        self.window = IndiaNormal()
        self.window.switch()
        self.window.switch_window.connect(self.fu)
        # self.widget.close()
        self.window.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Statistics section of India"])
        #engine.say("Welcome to Statistics section of India")
        #engine.runAndWait()

    def show_main_world(self):
        self.window2 = WorldNormal()
        self.window2.switch()
        self.window2.switch_window.connect(self.fu_world)
        # self.widget.close()
        self.window2.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Statistics section of World"])
        #engine.say("Welcome to Statistics section of the World")
        #engine.runAndWait()

    def show_main_china(self):
        self.window4 = ChinaNormal()
        self.window4.switch()
        self.window4.switch_window.connect(self.fu_china)
        # self.widget.close()
        self.window4.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Statistics section of China"])
        #engine.say("Welcome to Statistics section of China")
        #engine.runAndWait()

    def show_main_italy(self):
        self.window6 = ItalyNormal()
        self.window6.switch()
        self.window6.switch_window.connect(self.fu_italy)
        # self.widget.close()
        self.window6.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Statistics section of Italy"])
        #engine.say("Welcome to Statistics section of Italy")
        #engine.runAndWait()

    def show_main_usa(self):
        self.window8 = USANormal()
        self.window8.switch()
        self.window8.switch_window.connect(self.fu_usa)
        # self.widget.close()
        self.window8.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Statistics section of USA"])
        #engine.say("Welcome to Statistics section of USA")
        #engine.runAndWait()

    def fu(self):
        self.window1 = IndiaPrediction()
        self.window1.__init__()
        self.window.close()
        self.window1.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Prediction section of India"])
        #engine.say("Welcome to Prediction section of India")
        #engine.runAndWait()
        #engine.say(
        #    "Future Prediction graphs are plotted according to the past data.They are not subjected to other measures taken.")

        #engine.runAndWait()

    def fu_china(self):
        self.window5 = ChinaPrediction()
        self.window5.__init__()
        self.window4.close()
        self.window5.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Prediction section of China"])
        #engine.say("Welcome to Prediction section of China")
        #engine.runAndWait()
        #engine.say(
        #    "Future Prediction graphs are plotted according to the past data.They are not subjected to other measures taken.")

        #engine.runAndWait()

    def fu_world(self):
        self.window3 = WorldPrediction()
        self.window3.__init__()
        self.window2.close()
        self.window3.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Prediction section of World"])
        #engine.say("Welcome to Prediction section of World")
        #engine.runAndWait()
        #engine.say(
        #    "Future Prediction graphs are plotted according to the past data.They are not subjected to other measures taken.")

        #engine.runAndWait()

    def fu_italy(self):
        self.window7 = ItalyPrediction()
        self.window7.__init__()
        self.window6.close()
        self.window7.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Prediction section of Italy"])
        #engine.say("Welcome to Prediction section of Italy")
        #engine.runAndWait()
        #engine.say(
        #    "Future Prediction graphs are plotted according to the past data.They are not subjected to other measures taken.")

        #engine.runAndWait()

    def fu_usa(self):
        self.window9 = USAPrediction()
        self.window9.__init__()
        self.window8.close()
        self.window9.show()
        subprocess.call(["say", "-v", "Samantha","Welcome to Prediction section of USA"])
        #engine.say("Welcome to Prediction section of USA")
        #engine.runAndWait()
        #engine.say(
        #    "Future Prediction graphs are plotted according to the past data.They are not subjected to other measures taken.")

        #engine.runAndWait()

    def chatt(self):
        self.window10 = ChatInterface()
        # self.window10.__init__()

    def ase(self):
        self.window11 = Window()
        # self.window10.__init__()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Controller()
    widget.show_widget()
    app.exec()
