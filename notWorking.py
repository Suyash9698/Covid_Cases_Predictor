import sys
import subprocess
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import date

class Widget(QtWidgets.QWidget):
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

        self.button_india.setStyleSheet("background-image: url(output-onlinepngtools.png) 0 0 0 0 stretch stretch;")
        # self.label = QtWidgets.QLabel(self)
        self.button_world.setStyleSheet("background-image: url(world.jpeg) 3 0 0 0 stretch stretch;")
        self.button_china.setStyleSheet("background-image: url(china.png) 0 0 0 0 stretch stretch;")

        self.assess = QPushButton(self)
        self.assess.setToolTip("<b>Click to take self assessment test</b>")
        self.assess.setFixedWidth(100)
        self.assess.setFixedHeight(200)

        self.assess.setStyleSheet("background-image:url('ass_pic.png');border-radius: 50px;")
        
        #self.assess.clicked.connect(self.ass)

        f_date = date(2019, 11, 17)
        l_date = date.today()

        delta = l_date - f_date
        print(delta.days)

        

        self.resize(1200, 850)

    def widget_c(self):
        subprocess.call(["say", "-v", "Samantha","Hey, Welcome aboard! Let's chat."])
        
        

    
class Controller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Controller')

        self.show_widget()

    def show_widget(self):
        self.widget = Widget()
        self.widget.switch_window.connect(self.show_main)
        self.widget.show()

    def show_main(self):
        self.hide()
        self.window = IndiaNormal()
        self.window.switch_window.connect(self.show_widget)
        self.window.show()

class IndiaNormal(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Controller()
    widget.show_widget()
    app.exec()