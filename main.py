import requests
import datetime as dt
import smtplib
import time


###############################MAIL INFORMATION#############################
MY_EMAIL= "pythonermail@gmail.com"
APP_PASSWORD_GMAIL ="guzkxmnkxvcwwzen"

#######################################MY LOCATION###########################
#Gdańsk
MY_LAT = 54.350340
MY_LNG = 18.593380

##############################ISS POSITION################################
def is_iss_overhead():
    response1 = requests.get(url="http://api.open-notify.org/iss-now.json")
    response1.raise_for_status() # wyłapuje error i opisuje problem
    data1 = response1.json()
    # data = response.json()["iss_position"]
    # print(data)

    iss_latitude = float(data1["iss_position"]["latitude"])
    iss_longitude = float(data1["iss_position"]["longitude"])


    iss_position = (iss_latitude, iss_longitude)
    print(f"ISS location is {iss_position}")

#############My position is within +5 or -5 degrees of the ISS position.####
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True



######################SUNRISE AND SUNSET IN MY LOCATION#####################
def is_night():
    parameters ={
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response2 = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response2.raise_for_status()
    data2 = response2.json()
    # print(data2)

    sunrise_info = data2["results"]["sunrise"]
    sunset_info = data2["results"]["sunset"]
    print(f"Sunrise in Gdańsk: {sunrise_info}")
    print(f"Sunset in Gdańsk: {sunset_info}")


    sunrise_hour = int(sunrise_info.split("T")[1].split(":")[0])
    sunset_hour = int(sunset_info.split("T")[1].split(":")[0])
    print(f"Sunrise hour in Gdańsk: {sunrise_hour}")
    print(f"Sunset hour in Gdańsk: {sunset_hour}")

############################TIME NOW######################################
    time_now = dt.datetime.now()
    # print(f"Now is time: {time_now}")
    now_hour = time_now.hour
    print(f"Now hour is: {now_hour}")
    print(type(now_hour))
    # 03<=05sunrise  and 23>=21sunset (night between 21-05)
    if now_hour <= sunrise_hour and now_hour >= sunset_hour:
        return True
        



######################If the ISS is close to my current position#########


while True:
    time.sleep(30)
    if is_iss_overhead()is True and is_night() is True:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=APP_PASSWORD_GMAIL)
            connection.sendmail(
                from_addr=MY_EMAIL, 
                to_addrs=MY_EMAIL, 
                msg="Subject: Look up \n\nThe ISS is above your head.")
    else:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=APP_PASSWORD_GMAIL)
            connection.sendmail(
                from_addr=MY_EMAIL, 
                to_addrs=MY_EMAIL, 
                msg="Subject: No ISS \n\nThe ISS is not above your head.")




# ##########EXTRACT HOURS FROM SUNRISE AND SUNSET############################
# print(f"Sunrise in Gdańsk: {sunrise_info}")
# #return 2023-05-11T02:46:11+00:00 - string

# print(sunrise_info.split("T"))
# #return list with 2 items['2023-05-11', '02:46:11+00:00']

# print(sunrise_info.split("T")[1].split(":"))
# #return list with 4 items['02', '46', '11+00', '00']

# print(sunrise_info.split("T")[1].split(":")[0])
# #return item 02