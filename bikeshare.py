import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    #Asks user to specify a city, month, and day to analyze.
    """
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('Would you like to see data for Chicago, New York or Washignton? ').lower()
        if city =='chicago' or city=='new york' or city=='washington':
            if city == 'new york':
                city='new york city'
            break
        else:
            print('Invalid selection!! Please enter a valid option from the list\n')
            continue  
    
    # TO DO: get user input for month (all, january, february, ... , june)
    
    while True:
        time_filter=input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time ')
        if time_filter.lower() =='month' or time_filter.lower()=='day' or time_filter.lower()=='both' or time_filter.lower()=='none':
            break
        else:
            print('Invalid selection!! Please enter a valid option from the list\n')
            continue
    if time_filter == 'month' or time_filter=='both':
        while True:
            mnth=input('Which month? January, February, March, April,May or June? ').lower()
            if mnth=='january' or mnth=='february' or mnth=='march' or mnth=='april' or mnth=='may' or mnth=='june':
                mnth_def=mnth
                break
            else:
                print('Invalid selection!! Please enter a valid option from the list\n')
                continue    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
  
    if time_filter == 'day' or time_filter=='both':
        try:
            while True:
                dy=int(input('Which day? Please type your response as an integer (e.g., 1= Sunday) '))
                if dy<=7 and dy >= 1:
                    day_def=dy
                    break
                else:
                    print('Invalid selection!! Please enter a valid option\n')
                    continue
        except ValueError:
            print('Thats not a valid number')
            #print('-'*40)
    if time_filter == 'month':
        day_def=0
    if time_filter == 'day':
        mnth_def='none'
    if time_filter== 'none':
        day_def = 0
        mnth_def= 'none'
        
            
    return city,mnth_def,day_def

    
def load_data(city, mnth, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df= pd.read_csv(CITY_DATA[city])
    #Create a column for month and weekday#
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #print(day)
    if mnth != 'none':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(mnth.lower()) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    if day != 0:
        # use the index of the weeks list to get the corresponding day
        days = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day_temp=day-1
        dy=days[day_temp]
        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == dy]
    #print(df.head())
    return df


def time_stats(df,mnth,day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (str) city - Identify the user selection 
        (str) month - Identify user selection
        df - Filtered Dataframe
    Returns:
        Nothing returned
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['start_hour'] = df['Start Time'].dt.hour
    #print(df.head())
    #print(list(df.columns))
    # TO DO: display the most common month
    if  mnth == 'none':
        ## find the most popular month
        popular_month = df['month'].mode()[0] 
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month_desc= months[popular_month-1]
        print('Most popular month:',popular_month_desc )
    # TO DO: display the most common day of week
    if day == 0:
        ## find the most popular day week
        popular_week = df['day_of_week'].mode()[0] 
        print('Most popular day of week:',popular_week )

    # TO DO: display the most common start hour
    ## find the most popular hour
    popular_hour = df['start_hour'].mode()[0] 
    print('Most popular Start Hour:',popular_hour )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
       df - Filtered Dataframe
    Returns:
        Nothing returned
    """
    
    #print(list(df.columns))
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0] 
    print('Most popular Start Station:',popular_start_station )

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0] 
    print('Most popular End Station:',popular_end_station )

    # TO DO: display most frequent combination of start station and end station trip
    df2=df.groupby(['Start Station','End Station'])
    most_frequent_combination = df2.size().sort_values(ascending=False).head(1)
    print('The most frequent combination if start station and end station is :\n', most_frequent_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #print(df.columns)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration

    Args:
       df - Filtered Dataframe
    Returns:
        Nothing returned
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    trip_sum= df['Trip Duration'].sum()
    hours,seconds=divmod(trip_sum,3600)
    minutes,sec = divmod(seconds,60)
    print(trip_sum)
    print('Total travel time:',hours,'Hours',minutes, 'Minutes',sec, 'seconds')
    # TO DO: display mean travel time
    trip_avg= df['Trip Duration'].mean()
    mn,sc = divmod(trip_avg,60)
    print('Average travel time:',mn ,'minutes')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users

    Args:
       df - Filtered Dataframe
    Returns:
        Nothing returned
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    #rint(df.head())
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types \n', user_types)
    
    # TO DO: Display counts of gender
    #Only available for chicago
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Count of user types \n', gender_count)
        #noprint(df.columns)

    # TO DO: Display earliest, most recent, and most common year of birth
    #Earliest year of birth
    #Only available for chicago
    if 'Birth Year' in df.columns:
        yob = df.sort_values(by=['Birth Year'], ascending = False)
        yob_earliest = yob['Birth Year'].loc[yob.index[0]]
        print('Youngest person taken the trip has a Birth year', int(yob_earliest))
    
        #Latest year of birth
        yob = df.sort_values(by=['Birth Year'])
        yob_latest = yob['Birth Year'].loc[yob.index[0]]
        print('Older person taken the trip has a Birth year', int(yob_latest))
    
        #Common year of birth
        common_yob =df['Birth Year'].mode()[0]
        print("People with birth year {} has travelled the most".format(int(common_yob)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_raw_data(df):
    """
    Displays raw data until user inputs 'no'

    Args:
       df - Filtered Dataframe
    Returns:
        Nothing returned
    """
    start_row=0
    #Show 10 rows at a time"""
    end_row=10
    max_row = df.size
    print_row = 'yes'
    #Continue display until user said no or end of data reached.
    while end_row < max_row or print_row == 'yes' :
        if print_row != 'yes':
            break
        else:
            print_row = input('\n Would you like to see the raw data? Enter yes or no. \n').lower()
            if print_row != 'yes':
                break
            print((df[start_row:end_row]).to_string(index=False))
            print_row = input('\n Would you like to see more? Enter yes to see more, otherwise say no. \n').lower()
            if print_row != 'yes':
                break
            else:
            #Increment counter to show next 10 rows
                start_row += 10
                end_row += 10
                print((df[start_row:end_row]).to_string(index=False))
                start_row += 10
                end_row += 10

def main():
    while True:
        """get_filters()"""
        city,mnth,day=get_filters()
        
        """Load data based on the input parameters recevied"""
        df = load_data(city,mnth,day)
        
        """Find statistics on time"""
        time_stats(df,mnth,day)
        
        """Find statistics on station"""
        station_stats(df)
        
        """Find statistics on trip duration"""
        trip_duration_stats(df)
        
        """Find statistics on user types"""
        user_stats(df)
        
        """After displaying statistics, ask user if they would like to see the raw data"""
        display_raw_data(df)
                   
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
