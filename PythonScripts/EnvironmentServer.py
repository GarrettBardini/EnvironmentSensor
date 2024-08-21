#!/usr/bin/env python3
#################################################################
#####     ENVIRONMENT SERVER | HOST DATA FOR USERS          #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)               #####
#####     CREATE_DATE: 2022/10/11                           #####
#####     LAST_MODIFIED: 2024/08/21                         #####
#################################################################
import os
import time
import glob
import socket
import pandas as pd
from http.server import BaseHTTPRequestHandler, HTTPServer
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import cv2
import base64

# DEFINE WEBSERVER #
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
hostName = (s.getsockname()[0]) # '10.0.0.7'
s.close()

serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # LOAD DATA # 
        df = pd.read_csv(r"/mnt/usb0/EnvironmentData/EnvironmentResults.csv")
        # CREATE PLOTS #
        div1 = temp_humid_plot(df)
        div2 = temp_lumen_plot(df)
        # LOAD IMAGES # 
        img1 = get_recent_image()
        img2 = get_current_image()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<body><center>", "utf-8"))
        self.wfile.write(bytes(div1, "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))
        # self.wfile.write(bytes("<body><center>", "utf-8"))
        self.wfile.write(bytes(div2, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        # self.wfile.write(bytes("<body><center>", "utf-8"))
        self.wfile.write(bytes(img1, "utf-8")) # TITLE?
        # self.wfile.write(bytes("</body></html>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))
        # self.wfile.write(bytes("<body><center>", "utf-8"))
        self.wfile.write(bytes(img2, "utf-8")) # TITLE?
        self.wfile.write(bytes("</body></html>", "utf-8"))

def temp_humid_plot(df):
    # PLOT TEMP AND HUMIDITY # 
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(x = df['DateTime'],y = df['Temperature_F'], name="Temperature Fahrenheit",marker_color='rgb(0, 0, 255)'),secondary_y=False,)
    fig1.add_trace(go.Scatter(x = df['DateTime'],y = df['Humidity'], name="Humidity %",marker_color='rgb(255, 0, 0)'),secondary_y=True,)
    fig1.update_layout(title_text="Temperature (F) and Humidity (%)", title_x=0.5)
    fig1.update_xaxes(title_text="Date Time")
    fig1.update_yaxes(title_text="Temperature Fahrenheit", secondary_y=False)
    fig1.update_yaxes(title_text="Humidity Percent", secondary_y=True)

    fig1.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1h",
                        step="hour",
                        stepmode="backward"),
                    dict(count=1,
                        label="1d",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    # fig1.show()
    div1 = fig1.to_html(full_html=False)
    return (div1)

def temp_lumen_plot(df):
    # PLOT TEMP AND LUMENS # 
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Scatter(x = df['DateTime'],y = df['Temperature_F'], name="Temperature Fahrenheit",marker_color='rgb(0, 0, 255)'),secondary_y=False,)
    fig2.add_trace(go.Scatter(x = df['DateTime'],y = df['Lux'], name="Lumens",marker_color='rgb(0, 128, 64)'),secondary_y=True,)
    fig2.update_layout(title_text="Temperature (F) and Lumens", title_x=0.5)
    fig2.update_xaxes(title_text="Date Time")
    fig2.update_yaxes(title_text="Temperature Fahrenheit", secondary_y=False)
    fig2.update_yaxes(title_text="Lumens", secondary_y=True)

    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1h",
                        step="hour",
                        stepmode="backward"),
                    dict(count=1,
                        label="1d",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    # fig2.show()
    div2 = fig2.to_html(full_html=False)
    return (div2)

def get_recent_image():
    imageDir = '/mnt/usb0/TimelapseImages'
    commonName = 'ImageCapture.jpg'
    images = glob.glob(os.path.join(imageDir, '*' + commonName))
    imgDates = []
    for img in images:
        imDate = int((os.path.basename(img)).strip(commonName))
        imgDates.append(imDate)
    recentImage = (os.path.join(imageDir,str(max(imgDates))+commonName))
    uri = base64.b64encode(open(recentImage, 'rb').read()).decode('utf-8')
    rImg = '<img src="data:image/png;base64,{0}">'.format(uri)
    return (rImg)

def get_current_image():
    tempDir = '/home/GPI/Documents/EnvironmentSensor'
    cam = cv2.VideoCapture(0)
    attempts = 0
    while attempts < 75:
        ret, image = cam.read()
        attempts += 1
    cv2.imwrite(os.path.join(tempDir,'temp.jpg'), image)
    cam.release()
    cv2.destroyAllWindows()
    uri = base64.b64encode(open(os.path.join(tempDir,'temp.jpg'), 'rb').read()).decode('utf-8')
    cImg = '<img src="data:image/png;base64,{0}">'.format(uri)
    return (cImg)

if __name__ == "__main__":   
    # SPIN UP WEBSERVER # 
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    webServer.serve_forever()  