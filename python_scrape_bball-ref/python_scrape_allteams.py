
# coding: utf-8

# In[149]:

import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import time



# In[150]:

salary_df = pd.DataFrame([],columns = ['year','team','salary'])


# In[151]:

# START LOOP HERE
# Loop over the years


teams = ['TOR','GSW']


for team in teams:
	for year in range(2012,2017):

		response = urllib2.urlopen('http://www.basketball-reference.com/teams/{}/{}.html'.format(team,year))
		html = response.read()



		soup = BeautifulSoup(html,'html.parser')

		team_stats=soup.find("table",id="salaries")

		data = team_stats.find_all("tr")

		new_data = []

		for i in data:
		    new_data.append(i.text)


		new_data2 = []
		for i in new_data:
		    new_data2.append((i.replace('\n',',')).split(',', 3))

		new_data3 = [ x[1:] for x in new_data2]

		new_data4 = map(lambda x: [x[0],x[1],(x[2].replace(',','').replace('$',''))], new_data3)

		df = pd.DataFrame(new_data4,columns=new_data4[0])
		df = df.drop(0,axis=0)
		df = df.drop('Rk',axis=1)

		tot_salary = df['Salary'].astype('float32').sum()
		current_entry = pd.DataFrame([[year,team,tot_salary]],columns=['year','team','salary'])

		salary_df = pd.concat([salary_df,current_entry])
		time.sleep(5)



# END LOOP HERE


salary_df.to_csv('all_team_salary.csv')
#salary_df.to_csv('{}_salary.csv'.format(team))




