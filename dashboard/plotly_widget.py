from PyQt6 import QtWebEngineWidgets
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from plotly import express as px


class PlotlyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)

        self.show_button = QPushButton('Plot', self)
        self.hide_button = QPushButton('Hide', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        self.layout.addWidget(self.show_button)
        self.layout.addWidget(self.hide_button)
        self.layout.addWidget(self.browser)
        self.browser.setMinimumHeight(300)
        self.browser.setMinimumWidth(400)

        self.browser.setStyleSheet("background-color: #181818;")

        graph = self.create_graph()
        self.set_graph(graph)

        # noinspection PyUnresolvedReferences
        self.show_button.clicked.connect(self.show_graph)
        # noinspection PyUnresolvedReferences
        self.hide_button.clicked.connect(self.hide_graph)

    @staticmethod
    def create_graph(data=None):
        if data is None:
            df = px.data.iris()

            fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size="petal_length",
                             title="Plotly Graph in PyQt6")
        else:
            fig = px.scatter(data)

        fig.update_layout(
            plot_bgcolor="#181818",
            paper_bgcolor="#2c2c2c",
            font=dict(color="white", size=14, family="Arial"),
            title_font=dict(color="white", size=18, family="Arial"),
            xaxis=dict(
                linecolor="white",
                showgrid=False,
                showline=True,
                showticklabels=True,
                tickcolor="white",
                ticks="outside",
                title=dict(font=dict(color="white", size=14, family="Arial")),
            ),
            yaxis=dict(
                linecolor="white",
                showgrid=False,
                showline=True,
                showticklabels=True,
                tickcolor="white",
                ticks="outside",
                title=dict(font=dict(color="white", size=14, family="Arial")),
            ),
            legend=dict(font=dict(color="white", size=12, family="Arial")),
            showlegend=False,
            autosize=True,
        )

        fig.update_traces(marker=dict(line=dict(width=1, color="white")))

        return fig.to_html(include_plotlyjs='cdn')

    def set_graph(self, graph):
        self.browser.setHtml(graph)

    def show_graph(self):
        self.browser.show()

    def hide_graph(self):
        self.browser.hide()
