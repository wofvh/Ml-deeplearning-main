import re
import os
import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd


# Json 파일들 상위 디렉토리
input_dir = 'C:\json_to_txt/'

def convert(size, coord_list):
    dw = 1. / size[0]  # 1.0 / 1920 = 0.0005208333333333333 너비 비율
    dh = 1. / size[1] # 1.0 / 1080 = 0.0009259259259259259 높이 비율
    x = (coord_list[0] + coord_list[1]) / 2.0 # x좌표의 평균
    y = (coord_list[2] + coord_list[3]) / 2.0 # y좌표의 평균
    w = coord_list[1] - coord_list[0]  #너비 = x좌표의 차이
    h = coord_list[3] - coord_list[2] # 높이 = y좌표의 차이
    x = x * dw # x좌표의 평균 * 너비 비율
    w = w * dw # 너비 * 너비 비율
    y = y * dh # y좌표의 평균 * 높이 비율
    h = h * dh# 높이 * 높이 비율
    return (x, y, w, h) # x좌표의 평균, y좌표의 평균, 너비, 높이

file_list = os.listdir(input_dir) #input_dir에 있는 파일들을 리스트로 반환
 
json_name_list = [file for file in file_list if file.endswith('.json')] #json 파일만 리스트로 반환

for i in range(len(json_name_list)): #json 파일들의 경로를 리스트로 반환
    json_name_list[i] = input_dir + '/' + json_name_list[i] #json 파일들의 경로를 리스트로 반환

count = 0 #json 파일의 개수

for i in json_name_list: #json 파일들의 경로를 리스트로 반환
    output_file_name = i.split('.')[0] + '.txt' #txt 파일의 경로를 리스트로 반환
    with open(i, 'r', encoding='UTF-8') as file: #json 파일을 읽어옴
        data = file.read().replace('\n', '') #json 파일의 내용을 읽어옴
    count_data = data.count('\"data\"') #data의 개수를 세어줌
    height = re.findall('\d+', data.split('height')[1].split(',')[100]) #findall은 정규식에 맞는 모든 문자열을 리스트로 반환
    width = re.findall('\d+', data.split('width')[1].split(',')[100]) #   너비와 높이를 리스트로 반환
    size = [width[0], height[0]] #size = [width, height]
    size =  list(map(int, size)) #map은 리스트의 요소를 지정된 함수로 처리해주는 함수
    data = data.split("bbox")[1] #bbox를 기준으로 나눔 #bbox가 없는 경우가 있음 
    data_list = data.split("}")
    result = []
    for j in range(count_data):
        temp_data = data_list[j]
        data_name = temp_data.split('\"data\":')[1].split(',')[0]
        x_list = temp_data.split(',      \"y\": ')[0].split('"x": ')[1].replace('[', '').replace(']', '').replace(' ', '').split(',') #x좌표를 리스트로 반환
        y_list = temp_data.split(',      \"y\": ')[1].replace('[', '').replace(']', '').replace(' ', '').split(',')
        coord_list = [x_list[0], x_list[-1], y_list[0], y_list[-1]] #coord_list = [x1, x2, y1, y2]
        coord_list =  list(map(int, coord_list)) #coord_list = [x1, x2, y1, y2]
        yolo_style = list(convert(size, coord_list)) #yolo_style = [x좌표의 평균, y좌표의 평균, 너비, 높이]
        yolo_style.insert(0, data_name) #yolo_style = [data_name, x좌표의 평균, y좌표의 평균, 너비, 높이]
        result.append(' '.join(map(str, yolo_style))) #result = [data_name, x좌표의 평균, y좌표의 평균, 너비, 높이]

    for n in range(len(result)):
        result[n] = result[n].strip()

    #       #txt 파일 새로만든 폴더로 저장
    # with open('C:\\newone/' + output_file_name.split('/')[-1], 'w+') as lf: #새로운 폴더에 txt 파일로 저장
    #     lf.write('\n'.join(result))

    with open(output_file_name, 'w+') as lf:
        lf.write('\n'.join(result))

    with open(output_file_name, 'r') as lf: #txt 파일을 읽어옴
        readList = lf.readlines()

    le = LabelEncoder()
    output_file_name = le.fit_transform([readList] + ['\n']) 