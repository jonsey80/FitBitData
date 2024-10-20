import pandas as pd
import matplotlib as plt
#load data from 2 CSV
User_steps_rate = pd.read_csv(r'C:\FITBITDATA RAW\dailyActivity_merged.csv')
User_weight_data = pd.read_csv(r'C:\FITBITDATA RAW\weightLogInfo_merged.csv')
#need to ensure date values are in datetime format
User_steps_rate['Date'] = pd.to_datetime(User_steps_rate['ActivityDate'], errors='coerce')
#Select columns needed from data set 
User_steps_select = User_steps_rate[['Id','Date','TotalSteps','Calories']]
User_weight_data['Date'] = pd.to_datetime(User_weight_data['Date'], errors='coerce')
#convert a date time columns to individual date and time columns for join purpose
User_weight_data['Time'] = User_weight_data['Date'].dt.time
User_weight_data['Date'] = User_weight_data['Date'].dt.date
#join both Data frames together 
User_weight_data['Date'] = pd.to_datetime(User_weight_data['Date'],errors='coerce')
#select out columns and merge data frames 
User_weight_select = User_weight_data[['Id','Date','Time','WeightKg']]
User_Data = pd.merge(User_steps_select,User_weight_select, on=['Id','Date'],how='left')
#sort the data frame by ID and Date 
User_Data= User_Data.sort_values(by=['Id','Date'])
#remove NaN values with known good values by using forward and back fill
User_Data['WeightKg'] = User_Data.groupby('Id')['WeightKg'].fillna(method='ffill')
User_Data['WeightKg'] = User_Data.groupby('Id')['WeightKg'].fillna(method='bfill')
#collates average steps, Average calories burnt and where recorded the weight of participants
user_data_calories = User_Data.groupby('Id').mean(['TotalSteps','Calories'])
user_data_calories = user_data_calories.rename(columns={'TotalSteps':'AvgSteps','Calories':'AvgCalories'})
#add in the heart rate data 
heart_rate_data = pd.read_csv(r'C:\FITBITDATA RAW\heartrate_seconds_merged.csv')
heart_rate_data['Time'] = pd.to_datetime(heart_rate_data['Time'],errors='coerce')
heart_rate_data['Time'] = heart_rate_data['Time'].dt.date
heart_rate_avg = heart_rate_data.groupby('Id').mean('value')
heart_rate_avg = heart_rate_avg.rename(columns={'value':'AvgHR'})
Final_user_data = pd.merge(user_data_calories,heart_rate_avg,on=['Id'],how='left')
print(Final_user_data)
                              