import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Setup Selenium WebDriver with Popup Blocking
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
print("Initialized Selenium WebDriver.")

# Step 2: Login to Twitter
def login_to_twitter(username, password):
    """
    Logs into Twitter using provided credentials.
    
    Args:
        username (str): Twitter username.
        password (str): Twitter password.
    """
    
    print("Attempting to log in to Twitter...")
    driver.get("https://x.com/login/")
    print('I accessed login page')
    time.sleep(5)
    username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
    print('I found username filed.')
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(3)
    print("Entered username.")
    password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
    print('I found password filed.')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(4)
    print("Logged in successfully!")

# Replace with your Twitter credentials
username = 'safirantandis'
password = 'Gharibvand82'
login_to_twitter(username, password)

# Step 3: Search on Twitter
def search_twitter(query):
    """
    Searches Twitter for a specific query and sorts results by latest.

    Args:
        query (str): The search query for Twitter.
    """
    
    print(f"Searching for query: {query}")
    search_box = driver.find_element(By.XPATH, '//input[@aria-label="Search query"]')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    print("Search results are ready.")
    driver.find_element(By.LINK_TEXT, "Latest").click()  # Click on "Latest" tab (sorting)
    time.sleep(3)
    print("Sorted by latest tweets.")

# Replace with your search query
query = '"السودانی" until:2024-12-22 since:2024-12-20'
search_twitter(query)
print(f"Searched for the query: {query}")

def status(tweet):
    """
    Determine the type of a tweet: reply, retweet, quote, or regular tweet.

    Args:
        tweet (WebElement): A Selenium WebElement representing the tweet.

    Returns:
        str: The status of the tweet ("Reply", "Retweet", "Quote", "Regular").
    """
    try:
        # Check if the tweet is a reply
        is_reply = tweet.find_elements(By.XPATH, '//*[contains(text(), "Replying to")]')
        if is_reply:
            return "Reply"

        # Check if the tweet is a retweet
        is_retweet = tweet.find_elements(By.XPATH, '//*[contains(text(), "Retweeted")]')
        if is_retweet:
            return "Retweet"

        # Check if the tweet is a quote
        is_quote = tweet.find_elements(By.XPATH, '//*[contains(text(), "Quote Tweet")]')
        if is_quote:
            return "Quote"

        # If none of the above, it is a regular tweet
        return "Regular"
    except Exception as e:
        print(f"Error determining tweet status: {e}")
        return "Unknown"

# Step 4: Scrape Extended Tweet Details
def scrape_tweets_extended(max_tweets):
    print(f"Starting to scrape tweets. Target: {max_tweets} tweets.")
    tweets_data = []
    while len(tweets_data) <= max_tweets:
        print(f"Currently collected tweets: {len(tweets_data)}. Fetching more...")
        tweets = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
        print(f"Found {len(tweets)} tweets on the page.")
        
        # getting options of every post.
        for tweet in tweets:
            try:
                try:
                    caption = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"] span').text
                    print('i found caption button')
                except Exception:
                    caption = None  # Handle tweets without text
                    print("No caption found.")    
                print('i found caption button')
                
                # Extract author
                try:
                    author = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"] > div > div > a > div > div > span > span').text
                except Exception:
                    author = None
                    print("No author found.") 
                print('i found author button')
                
                # Extract timestamp
                try:
                    timestamp = tweet.find_element(By.CSS_SELECTOR, 'time').get_attribute("datetime")
                except Exception:
                    timestamp = None
                    print("No timestamp found.")

                # Media link
                try:
                    media = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] img').get_attribute("src")
                    print(f"Found media link: {media}")
                except Exception:
                    media = None
                    print("No media found for this tweet.")

                try:
                    views_element = tweet.find_element(By.CSS_SELECTOR, 'div[class*="r-1iusvr4 r-16y2uox"]') 
                    views_count = views_element.text.strip() if views_element.text.strip() else None
                except Exception:
                    views_count = None
                    print("No views count found.")

                # Counts for comments, retweets
                stats = tweet.find_elements(By.XPATH, '//*[@id="id__t8t6golzzq"]/div[1]/button/div/div[2]/span/span/span')
                comments_count = stats[0].text if stats else "0"

                stats = tweet.find_elements(By.XPATH, '//*[@id="id__b7pqhb6zde"]/div[2]/button/div/div[2]/span/span/span')
                retweets_count = stats[0].text if stats else "0"
                
                # Extract stats: likes
                try:
                    stats = tweet.find_elements(By.CSS_SELECTOR, 'div[data-testid="like"] span')
                    likes_count = stats[0].text if stats else "0"
                except Exception:
                    likes_count = "0"
                    print("Error retrieving likes count.")
                status_of_tweet = status(tweet)    
                    
                # Append data to the list
                tweets_data.append({
                    "Author": author,   
                    "Caption": caption,  
                    "Timestamp": timestamp,  
                    "Media Link": media,   
                    "Comments Count": comments_count,   
                    "Retweets Count": retweets_count,   
                    "Views Count": views_count,  
                    "Likes Count": likes_count, 
                    "Status": status_of_tweet   
                    })
                print("Successfully added tweet data to the list.")

                if len(tweets_data) >= max_tweets:
                    print("Reached the target number of tweets. Stopping scraping.")
                    break
            except Exception as e:
                print(f"Error retrieving tweet: {e}")

        # Scroll down to load more tweets
        print("Scrolling down to load more tweets...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        print("Scroll completed.")
        
        
    print(f"Scraping completed. Collected {len(tweets_data)} tweets.")
    return tweets_data

try:
    print("Starting the scraping process.")
    tweets_data = scrape_tweets_extended(max_tweets=50)
    print(f"Collected {len(tweets_data)} tweets.")
    # Save to CSV
    df = pd.DataFrame(tweets_data)
    csv_file = "twitter_search_results.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"Saved tweets to {csv_file}")
    # Display dataframe
    print("Here is the collected data:")
    print(df)
finally:
    driver.quit()  # Ensure the browser is closed properly
    print("Browser closed.")
