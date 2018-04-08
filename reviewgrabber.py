# -*- coding: utf-8 -*-

'''
@author      : Anton
@date        : 04/08/2018
'''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                              EXAMPLE URLS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
https://www.amazon.com/Google-Wifi-system-set-replacement/product-reviews/B01MAW2294/
ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews
'''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                              LIBRARY IMPORTS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import signal
import requests
import pandas as pd
from cmd import Cmd
from pyfiglet import Figlet
from urlparse import urlparse
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from sqlalchemy import create_engine
from tqdm import tqdm

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                              CMDLET COMMANDS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
# AmazonReviewGrabber: Provides terminal like interface for the Python script.
    Commands:
        preloop    : Show logo and version at first launch
        do_get     : Retrieves reviews from Amazon via url
        help_get   : Show help options for get command
        do_save    : Save df of reviews to a sqlalchemy database
        help_save  : Show help options for save command
        do_batch   : Do a batch extract of reviews from multiple urls
        help_batch : Show help options for batch command
        do_exit    : Exit the application
        help_exit  " Show help options for exit command
'''
class AmazonReviewGrabber(Cmd):
    
    '''
    # Initial logo and version display
    '''
    def preloop(self):
        fig = Figlet(font='big')
        print(fig.renderText('ReviewGrabber'))
        print('Version 1.0a')
        
    '''
    # Retrieve reviews from an Amazon product via user-provided url
    Usage:
        get <url>   : Retrieve reviews from url
        url example : https://www.amazon.com/Google-Wifi-system-set-replacement/
                      product-reviews/B01MAW2294/ref=cm_cr_dp_d_show_all_top?ie=
                      UTF8&reviewerType=all_reviews   
    '''
    def do_get(self, url):
        global all_reviews_df
        
        # Print the product id of the product being queried
        product_id = get_item_id(url)
        print('\n# REVIEWS FOR PRODUCT ID: {}\n'.format(product_id))
        
        # Get the page number, and make the initial query
        page_number = 1
        pre_grab = make_query(url, page_number)
        
        # Pre-grab allows to determine the number of reviews available to pull
        if pre_grab.status_code == 200:
            reviews = []
            processed_reviews = 0
            total_reviews = get_num_reviews(pre_grab.text)
            pbar = tqdm(total=total_reviews)
             
            # Continue to pull reviews until they are all extracted
            while (processed_reviews <= total_reviews):
                results = make_query(url, page_number)
                page_number+=1
                
                # Only process the page if status_code == 200
                if (results.status_code == 200):
                    clean = get_reviews(results.text, product_id)
                    
                    # Don't process pages with no results
                    if clean is not None:
                        if len(clean) > 0:
                            processed_reviews+=len(clean)
                            pbar.update(len(clean))
                            for review in clean:
                                reviews.append(review)
                    else:
                        break
                else:
                    print('[!] Received Error: {}'.format(results.status_code))
                    break
            
            # Put all results in a pandas dataframe if data exists
            pbar.close()
            if len(reviews) > 0:
                df = pd.DataFrame(reviews)
                all_reviews_df = all_reviews_df.append(df, ignore_index=True)
                all_reviews_df.reset_index(drop=True)
                print('\n[+] Recovered {} reviews from {} pages'.format(len(reviews), page_number-2))
            else:
                print('\n[!] Error recovering reviews')
        else:
            print('\n[!] Reviews not available for {}'.format(product_id))

    '''
    # Help command for go_get 
    Usage:
        help get   : show usage and description to console
    '''                
    def help_get(self):
         print('Get reviews from Amazon using a url to the reviews page')
         print('Usage:\n  get <url>')

    '''
    # Save reviews on user demand to the local sqlalchmey database. 
    Usage:
        save <table_name>   : Save all past retrieved reviews into a database
                              called reviews.db in a table called <table_name>
    '''          
    def do_save(self, table_name):
        global all_reviews_df
        
        engine = create_engine('sqlite:///reviews.db')
        con = engine.connect()
        all_reviews_df.to_sql(name=table_name, index=False, con=con, 
                               if_exists='append')
        all_reviews_df = pd.DataFrame(columns=columns)
        con.close()
        
        print('\n[+] Save complete!')

    '''
    # Help command for do_save 
    Usage:
        help save   : show usage and description to console
    '''    
    def help_save(self):
         print('Save reviews from Amazon to a local SQL database')
         print('Usage:\n  save <table-name>')

    '''
    # Batch process products by using a local text file of urls pointing to reviews
    Usage:
        batch auto <file_name>   : process each url, auto-save to default table
        batch manual <file_name> : process each url, manual save to user-defined table                     
    '''            
    def do_batch(self, args):
        # Split the args variable        
        x = args.split(' ')
        if len(x) != 2:
            print('\n[!] Invalid arguments')
            return
        
        code = x[0]
        file_name = x[1]
        
        # Process the file line by line. If code == auto, save the data to
        # sqlalchemy using 'default' table name
        path = os.getcwd()
        if os.path.isfile(os.path.join(path, file_name)):
            with open(file_name) as fp:
                line = fp.readline()
                if line is not None:
                    while line:
                        self.do_get(line)
                        line = fp.readline()
            
            if code == 'auto':
                self.do_save('default')
        else:
            print('\n[!] File not found!')

    '''
    # Help command for do_save 
    Usage:
        help batch : show usage and description to console
    Notes:
        manual     : user must manually run save post processing
        auto       : reviews are automatically saved to default table
    '''                
    def help_batch(self):
        print('Batch extract and process product reviews by reading a text file of urls')
        print('Usage:\n  batch manual <file_name>')
        print('  batch auto <file_name>')
 
    '''
    # Exit the application
    Usage:
        exit : exit the application                     
    '''          
    def do_exit(self, now):
        print('\nYou stay classy San Diego!')
        os.kill(os.getpid(), signal.SIGINT)

    '''
    # Help command for do_exit 
    Usage:
        help exit : show usage and description to console
    '''           
    def help_exit(self):
        print('Exit the application')
        print('Usage:\n  exit')
         
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                               MAIN SCRIPT
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Define global dataframe for storting reviews. Updated after each query,
# and cleared after each save.
columns = ['author', 'author_profile', 'helpful', 'image_available', 'link', 
           'product_id', 'rating', 'review', 'review_date', 'review_id' ]
all_reviews_df = pd.DataFrame(columns=columns)

'''
# Extract total number of pages. Used for testing and debugging.  
    Args: 
        page  : Raw HTML returned from requests
    Return:
        pages : Total pages of reviews available for a given product
'''
def get_num_pages(page):
    soup = bs(page, 'html.parser')
    pages = soup.find_all('span', attrs={'data-hook': 'cm_cr_arp_d_paging_btm'})
    
    if pages is not None:
        pages = pages[-1].text      # Last tag contains the total
    else:
        pages = 1
        
    return pages

'''
# Extract total number of reviews for a given product
    Args: 
        page        : Raw HTML returned from requests
    Return:
        num_reviews : Number of reviews total for a product
'''
def get_num_reviews(page):
    soup = bs(page, 'html.parser')
    num_reviews = soup.find('span', attrs={'data-hook': 'total-review-count'})
    if num_reviews is not None:
        num_reviews = num_reviews.text.replace(',', '')   # Remove , from 1000+
        num_reviews = int(num_reviews)
    else:
        num_reviews = 0
        
    return num_reviews

'''
# Extract all reviews on a given page. Store each review as a dictionary, and
  append each dictionary to a list.
    Args: 
        page            : Raw HTML returned from requests
        product_id      : Product id to be associated with the review
    Return:
        cleaned_reviews : List of dicts containing reviews
'''
def get_reviews(page, product_id):
    cleaned_reviews = []  
    
    # Find all reviews using html parser.
    soup = bs(page, 'html.parser')
    reviews = soup.find_all('div', attrs={'data-hook': 'review'})
    
    # Verify reviews exist before processing
    if len(reviews) > 0:
        for review in reviews:
            # Create a clean dict for each review
            clean = {}  
            
            # Get review id
            clean['review_id'] = review['id']
            
            # Add the product id
            clean['product_id'] = product_id
            
            # Get product rating (out of 5 stars)
            rating = review.div.a.text
            clean['rating'] = rating[0:3]
            
            clean['link'] = review.div.a['href']
            
            # Get review title from author
            title = review.div.div.find('a',attrs={'data-hook': 'review-title'})
            if title is not None:
                clean['title'] = title.text
            else:
                clean['title'] = "None"
            
            # Get author and their profile link
            author = review.div.find('a', attrs={'class': 
                'a-size-base a-link-normal author'})
            
            if author is not None:
                clean['author'] = author.text
                clean['author_profile'] = author['href']
            else:
                clean['author'] = 'Anonymous'
                clean['author_provile'] = 'Anonymous'
                 
            # Review date
            dat = review.div.find('span', attrs={'data-hook': 
                'review-date'}).text
            date = dt.strptime(dat[3:], '%B %d, %Y')
            date = dt.strftime(date, '%m/%d/%Y')
            clean['review_date'] = date
            
            # Review body
            body = review.div.find('span', attrs={'data-hook': 
                'review-body'}).text
            body = body.rstrip('\n')
            clean['review'] = body
            
            # Get image, if exists
            img = review.div.find('img', attrs={'data-hook': 
                'review-image-tile'})
            
            if img is not None:
                clean['image_available'] = True
            else:
                clean['image_available'] = False
            
            # Get number of people who say review was helpful
            helpful = review.div.find('span', attrs={'data-hook': 
                'helpful-vote-statement'})
            
            if helpful is not None:
                helpful = helpful.text.strip()
                helpful = helpful.partition(' ')[0]
                
                if helpful == 'One':                    # First is One, not 1
                    clean['helpful'] = 1
                else:
                    helpful = helpful.replace(',', '')  # Remove , from 1,000+
                    clean['helpful'] = int(helpful) 
            else:
                clean['helpful'] = 0
            
            # Append the review to the list
            cleaned_reviews.append(clean)
        
        return cleaned_reviews

'''
# Extract the product id from the url
    Args: 
        url     : Obtained from the get command
    Return: 
        item_id : Product id that is being examined
'''
def get_item_id(url):
    parts = urlparse(url)
    item_id = parts.path.split('/')
    return item_id[3]

'''
# Perform the query to the webpage. Iterate pages and include a user-agent string
  Max results per page for Amazon is 50.
    Args: 
        url          : Obtained from the get command
        page_number  : Start with page 1 and go to x
    Return: 
        requests     : Requests object, including status_code and html of page
'''
def make_query(url, page_number):
    headers = {'user-agent': 
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    url = url + '&pageNumber=' + str(page_number) + '&pageSize=50'
    return requests.get(url, headers=headers) 

'''
# Main application prompt
'''
def main():
    print()
    prompt = AmazonReviewGrabber()
    prompt.prompt = '> '
    prompt.cmdloop('\nThey\'ve done studies you know. Sixty percent of the ' +
                   'time it works every time....')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

