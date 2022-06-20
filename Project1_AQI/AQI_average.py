import pandas as pd

def avg_pm25(year):
    average=[]
    for rows in pd.read_csv('Data/AQI/aqi{}.csv'.format(year),chunksize=24):
        add_var=0
        avg=0
        data=[]
        df = pd.DataFrame(data=rows)
        for index,row in df.iterrows():
            data.append(row['PM2.5'])
        for i in data:
            if type(i) is float or type(i) is int:
                add_var = add_var+i
            elif i!='NoData' and i!='PwrFail' and i!='---' and i!='InVld':
                temp = float(i)
                add_var = add_var+temp
        avg= add_var/24
        average.append(avg)
        
    return average
    

if __name__ == "__main__":
    for i in range(2013,2019):
        globals()[f"lst{i}"] = []
        globals()[f"lst{i}"]= avg_pm25(i)
        
    

