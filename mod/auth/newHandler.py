# -*- coding: utf-8 -*-
# @Date    : 2016-07-25 15:34:57
# @Author  : jerry.liangj@qq.com
from PIL import Image
import io
import urllib,json
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient,HTTPError


divideInfo = {
	'w': {'all': [51, 52, 53, 54], 'select': 51} ,
	'p': {'all': [35,36, 37,38], 'select': 36} ,
	's': {'all': [], 'select': []} ,
	'v': {'all': [], 'select': []} ,
	'y': {'all': [33, 34,35, 36, 37], 'select': 33} ,
	'x': {'all': [32,33, 34, 35,36], 'select': 33} ,
	'r': {'all': [], 'select': []} ,
	'u': {'all': [], 'select': []} ,
	'a': {'all': [], 'select': []} ,
	'q': {'all': [], 'select': []} ,
	'c': {'all': [30, 31,32,33], 'select': 30} ,
	'b': {'all': [35,36, 37,38], 'select': 36} ,
	'e': {'all': [33, 34], 'select': 33} ,
	'd': {'all': [36, 37], 'select': 36} ,
	'g': {'all': [], 'select': []} ,
	'f': {'all': [24, 25, 26, 27, 28], 'select': 24} ,
	'i': {'all': [], 'select': []} ,
	'h': {'all': [], 'select': []} ,
	'k': {'all': [], 'select': []} ,
	'j': {'all': [], 'select': []} ,
	'm': {'all': [56, 52, 53, 54, 55], 'select': 52} ,
	'l': {'all': [], 'select': []} ,
	'o': {'all': [], 'select': []} ,
	'n': {'all': [31,32, 33, 34,35], 'select': 32} ,
	'1': {'all': [], 'select': []} ,
	'0': {'all': [], 'select': []} ,
	'3': {'all': [32, 33], 'select': 32} ,
	'2': {'all': [33, 34], 'select': 33} ,
	'5': {'all': [29, 30], 'select': 29} ,
	'4': {'all': [36, 37, 38, 39], 'select': 36} ,
	'7': {'all': [32, 33, 34,35], 'select': 32} ,
	'6': {'all': [36,37, 38], 'select': 37} ,
	'9': {'all': [], 'select': []} ,
	'8': {'all': [37], 'select': 37} ,
	'z': {'all': [], 'select': []} ,
	't': {'all': [], 'select': []} ,
}

Standard = {
	'w': {'select': ['4.80', '8.10', '11.80', '15.70', '19.75', '23.10', '26.75', '30.75', '33.95', '34.20', '31.10', '27.20', '23.15', '19.85', '16.15', '11.85', '13.75', '17.10', '20.05', '22.40', '22.95', '23.00', '22.95', '22.30', '19.85', '16.85', '13.20', '14.65', '18.10', '21.75', '25.10', '28.70', '30.45', '31.00', '29.45', '26.05', '22.85', '19.20', '15.90', '12.10', '13.75', '17.10', '20.80', '24.80', '26.00', '25.95', '26.00', '24.55', '21.20', '17.20', '13.90']} ,
	'p': {'select': ['52.11', '52.11', '52.11', '52.06', '52.06', '52.06', '52.00', '52.00', '51.89', '51.72', '12.00', '12.94', '13.00', '11.89', '12.94', '12.00', '12.00', '12.94', '14.00', '13.94', '15.00', '16.00', '16.94', '19.00', '23.00', '27.89', '37.78', '38.00', '37.00', '35.00', '33.94', '33.00', '30.00', '27.00', '23.83', '20.00']} ,
	's': {'select': ''} ,
	'v': {'select': ''} ,
	'y': {'select': ['5.52', '8.09', '10.57', '13.57', '16.61', '20.13', '24.43', '29.00', '33.00', '36.48', '38.91', '40.43', '41.35', '40.83', '37.87', '33.35', '28.78', '24.30', '19.17', '16.35', '16.91', '16.52', '16.43', '17.00', '16.96', '16.57', '16.48', '16.96', '16.57', '16.39', '15.96', '13.91', '11.43']} ,
	'x': {'select': ['4.00', '7.00', '9.95', '13.00', '16.45', '19.00', '22.00', '24.00', '24.95', '27.00', '28.50', '29.00', '28.00', '25.00', '22.00', '19.50', '18.00', '18.00', '19.00', '22.00', '25.00', '27.50', '29.50', '30.50', '29.50', '28.00', '25.80', '23.00', '20.00', '16.95', '14.00', '10.50', '7.50']} ,
	'r': {'select': ''} ,
	'u': {'select': ''} ,
	'a': {'select': ''} ,
	'q': {'select': ''} ,
	'c': {'select': ['11.63', '18.79', '22.47', '25.63', '28.26', '30.42', '32.21', '33.21', '34.37', '36.00', '34.42', '27.89', '23.16', '19.68', '18.79', '17.58', '16.00', '15.58', '13.89', '14.00', '14.00', '14.00', '14.00', '14.00', '13.74', '13.16', '14.00', '14.00', '13.79', '13.16']} ,
	'b': {'select': ['53.75', '53.75', '53.69', '53.75', '53.75', '53.75', '53.69', '53.62', '52.62', '49.12', '12.06', '12.94', '12.94', '12.06', '12.88', '12.00', '12.06', '13.00', '14.00', '14.06', '15.00', '16.06', '17.12', '19.25', '23.31', '28.56', '37.75', '37.94', '36.81', '34.81', '33.88', '32.75', '29.81', '26.81', '23.62', '19.50']} ,
	'e': {'select': ['11.22', '17.92', '22.53', '25.50', '28.39', '30.36', '32.19', '33.19', '34.39', '36.19', '35.81', '30.00', '25.42', '22.81', '21.75', '20.78', '20.00', '19.97', '19.81', '19.19', '20.14', '21.58', '24.67', '27.94', '28.00', '27.78', '26.61', '25.11', '25.75', '24.58', '22.58', '20.58', '18.03']} ,
	'd': {'select': ['12.00', '20.17', '24.04', '27.00', '30.08', '32.96', '33.96', '35.08', '37.04', '37.96', '37.58', '28.75', '22.83', '18.88', '16.79', '15.96', '14.96', '14.00', '13.96', '12.92', '12.00', '12.04', '12.92', '12.00', '13.00', '12.96', '13.62', '52.88', '53.00', '53.04', '53.04', '52.96', '52.96', '52.96', '52.92', '52.92']} ,
	'g': {'select': ''} ,
	'f': {'select': ['5.90', '5.79', '6.00', '7.38', '11.59', '44.97', '47.55', '49.76', '50.69', '51.69', '52.59', '53.31', '53.45', '52.14', '48.69', '16.21', '14.45', '12.17', '11.31', '11.28', '11.21', '11.14', '11.17', '10.34']} ,
	'i': {'select': ''} ,
	'h': {'select': ''} ,
	'k': {'select': ''} ,
	'j': {'select': ''} ,
	'm': {'select': ['38.00', '37.93', '37.93', '38.00', '38.00', '38.00', '38.00', '37.93', '38.00', '33.50', '7.00', '6.93', '7.00', '7.00', '7.00', '7.00', '7.00', '7.00', '7.07', '8.00', '8.14', '9.29', '15.00', '38.93', '38.93', '38.86', '38.00', '38.00', '37.86', '36.86', '35.79', '34.71', '29.29', '7.00', '6.86', '6.00', '6.14', '7.00', '6.86', '6.14', '7.00', '7.14', '8.00', '8.07', '9.29', '15.00', '39.00', '39.00', '38.93', '38.79', '38.00', '37.86']} ,
	'l': {'select': ''} ,
	'o': {'select': ''} ,
	'n': {'select': ['37.95', '38.00', '37.95', '38.00', '38.00', '37.95', '38.00', '38.00', '38.00', '37.95', '7.00', '6.95', '7.00', '7.00', '7.00', '7.00', '7.00', '7.00', '7.00', '8.00', '8.00', '8.00', '8.89', '11.00', '39.00', '39.00', '38.89', '38.00', '37.95', '37.00', '36.00', '35.00']} ,
	'1': {'select': ''} ,
	'0': {'select': ''} ,
	'3': {'select': ['6.23', '12.00', '11.91', '11.86', '11.23', '17.82', '17.82', '17.77', '16.77', '17.73', '17.77', '17.77', '18.77', '18.77', '19.82', '20.91', '22.91', '24.95', '28.05', '33.09', '40.05', '43.23', '47.95', '46.86', '44.91', '43.86', '40.82', '36.77', '33.82', '29.41', '21.50', '12.73']} ,
	'2': {'select': ['9.91', '16.04', '17.09', '18.91', '19.83', '20.70', '20.91', '22.65', '23.61', '24.43', '24.43', '24.09', '23.17', '22.30', '22.26', '22.26', '22.30', '22.39', '23.30', '24.52', '26.48', '28.65', '32.09', '36.30', '35.30', '34.48', '33.35', '31.57', '30.43', '28.57', '26.52', '23.57', '20.26']} ,
	'5': {'select': ['6.96', '29.84', '29.80', '29.88', '29.80', '29.84', '29.68', '24.72', '19.84', '19.96', '20.96', '20.96', '21.04', '22.92', '22.08', '24.04', '25.00', '27.08', '30.32', '37.76', '36.96', '35.92', '34.00', '33.84', '31.88', '29.92', '27.84', '25.76', '21.40']} ,
	'4': {'select': ['9.14', '10.19', '11.19', '12.38', '14.14', '15.19', '16.38', '17.95', '18.00', '18.00', '18.19', '18.76', '18.00', '18.00', '18.19', '18.81', '18.00', '18.19', '18.81', '18.00', '17.95', '18.14', '18.76', '24.14', '50.81', '51.00', '51.00', '51.00', '50.95', '51.00', '51.00', '51.00', '42.81', '8.00', '8.00', '8.00']} ,
	'7': {'select': ['8.00', '8.19', '11.25', '15.12', '18.06', '20.06', '21.00', '23.12', '25.06', '26.12', '28.12', '30.06', '30.81', '27.75', '24.94', '23.94', '22.94', '21.94', '21.00', '20.94', '20.06', '20.88', '20.00', '19.94', '19.94', '19.81', '17.88', '16.81', '15.75', '13.81', '12.75', '10.81']} ,
	'6': {'select': ['14.20', '22.08', '28.16', '32.08', '35.12', '38.12', '41.08', '43.00', '44.00', '45.00', '46.12', '32.68', '27.64', '23.76', '21.64', '19.64', '19.68', '18.60', '17.72', '18.60', '17.72', '17.68', '17.80', '19.80', '20.80', '21.88', '24.84', '28.00', '35.80', '35.72', '33.68', '31.84', '30.72', '28.80', '26.44', '17.80', '14.68']} ,
	'9': {'select': ''} ,
	'8': {'select': ['6.82', '12.00', '14.95', '23.91', '31.00', '34.91', '38.00', '41.95', '44.95', '47.91', '42.95', '39.91', '32.00', '28.00', '25.00', '23.91', '21.95', '20.95', '22.00', '20.95', '21.95', '23.00', '26.95', '27.86', '30.91', '35.95', '43.95', '47.95', '44.91', '42.95', '39.91', '35.86', '31.95', '27.00', '20.95', '12.00', '6.95']} ,
	'z': {'select': ''} ,
	't': {'select': ''} ,	
}
URL = "http://my.seu.edu.cn/captchaGenerate.portal"
LOGIN_URL = "http://my.seu.edu.cn/userPasswordValidate.portal"
CAPTCHA_URL = "http://my.seu.edu.cn/captchaValidate.portal?captcha=%s&what=captcha&_=&value=%s"
MAX_N = 30
WHITE = 0
BLACK = 255

def newAuthApi(username,password):
	data = {
		'Login.Token1':username,
		'Login.Token2':password
	}
	result = {'code':200,'content':''}
	try:
		client = HTTPClient()
		request = HTTPRequest(
			url = URL,
			method='GET')
		response = client.fetch(request)
		img = Image.open(io.BytesIO(response.body))
		img.save("test.jpg")
		cookie = response.headers['Set-Cookie']
		cookieTemp = cookie.split(";")
		cookie = cookieTemp[0] + ";" + cookieTemp[1].split(",")[1]
		vercode = recognize(img)
		data['captcha'] = vercode
		request = HTTPRequest(
			url = LOGIN_URL,
			method='POST',
			body=urllib.urlencode(data),
			headers = {'Cookie':cookie},
			request_timeout=8
		)
		response = client.fetch(request)
		result['content'] = response.headers['Set-Cookie']
	except HTTPError as e:
		result['code'] = 400
	except Exception,e:
		result['code'] = 500
	return result

def recognize(img):
    recognize_result = ""
    tempImg = img.load()
    size = img.size
    arrange = []
    arrangeTemp = []
    for i in xrange(0,size[0]):
        ylength = 0
        for j in xrange(0,size[1]):
            if tempImg[i,j][0] == 0:
                ylength = ylength+1
        if ylength>1:
            arrangeTemp.append(i)
        arrange.append([i,ylength])
    length = len(arrangeTemp)
    start = 0
    result = []
    for x in range(1,length):
        if(arrangeTemp[x]-arrangeTemp[x-1]>2 and x-start>2):
            result.append([arrangeTemp[start],arrangeTemp[x-1],x-start])
            start = x
    result.append([arrangeTemp[start],arrangeTemp[length-1],length-start])
    # print "divide result",result
    length = len(result)
    if(length!=4):
        recognize_result = "0000"
    else:
        for i in range(length):
            sample = []
            for x in xrange(result[i][0],result[i][1]):
                temp = 0
                for y in xrange(100):
                    temp += (tempImg[x,y][1] < 40)
                sample.append(temp)
            min_score = 1000
            max_match = 0
            sample_length = len(sample)
            for (x,y) in divideInfo.iteritems():
                diff = []
                if result[i][2] in y['all']:
                    min_length = min(y['select'],sample_length)
                    for m in xrange(min_length):
                        diff.append(abs(sample[m]-float(Standard[x]['select'][m])))
                    avg = float(sum(diff)) / min_length
                    for m in xrange(min_length):
                        diff[i] = abs(diff[i] - avg)
                    score = sum(diff)
                    if score < min_score:
                        min_score = score
                        max_match = x
            recognize_result += str(max_match)
    return recognize_result
