import pandas as pd
from search_twitter_query import search_twitter_return_ev
from datetime import datetime, timedelta

# Where to save the csv output
file_name = 'training_data.csv'

field_labels = ['company', 'date', 'numTweets', 'avgSubj', 'avgPol', 'medianTime', 'sumRetweet',
                'sumFavorite', 'sumFollowers', 'numVerified']

# Include the twitter handles you would like to collect data for here
companies = ['@microsoft']

# Add dates from 'm' to 'n' days ago to a list
# Change the values in 'range(m, n)' to change the search window
dates = []

for i in range(1, 8):
    dates.append(datetime.today() - timedelta(days=i))

# Create an empty list to collect our training data
tr_data_list = []

# Run search_twitter_return_ev function for each company-date combination in our lists.
for company in companies:
    for date in dates:
        result = search_twitter_return_ev(company,
                                          datetime.strftime(date, '%Y-%m-%d'),
                                          datetime.strftime(date + timedelta(days=1), '%Y-%m-%d'))
        # Append the results to our training data list
        tr_data_list.append(result)

# Transform the training data to a data frame
training_data = pd.DataFrame(tr_data_list, columns=field_labels)

# Output the data frame to csv
training_data.to_csv(file_name, encoding='utf-8', index=False)
