import requests
from bs4 import BeautifulSoup



def read_url(url):
    # Initialize main_content to ensure it has a value even if the request fails
    main_content = ''

    def count_tokens(text): return len(text.split())
    
    # Send a GET request to the webpage
    response = requests.get(url)

    if response.status_code == 200:
        # Parsing HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title of the webpage
        title = soup.find('title').text
        
        # Attempt to extract the description, provide a default if not found
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No description found'
        
        # Find all <p> tags and concatenate their text to form the main content
        paragraphs = soup.find_all('p')
        main_content = '\n'.join([para.text for para in paragraphs])

        # Debugging print statements (you might want to remove these for production code)
        print('Token length:', count_tokens(main_content))
        print(f"Title: {title}\nDescription: {description}\n\nMain Content:\n{main_content}")
    else:
        print("Failed to retrieve the webpage")

    

    return main_content

def read_url_with_images(url , need_image = True):
    # Initialize main_content to ensure it has a value even if the request fails
    main_content = ''
    images = []

    def count_tokens(text): return len(text.split())

    # Function to scrape images
    def scrape_images_with_bs4(soup):
        return [img.get('src') for img in soup.find_all('img') if img.get('src')]

    # Send a GET request to the webpage
    response = requests.get(url)

    if response.status_code == 200:
        # Parsing HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title of the webpage
        title = soup.find('title').text
        
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No description found'
        
        # Find all <p> tags and concatenate their text to form the main content
        paragraphs = soup.find_all('p')
        main_content = '\n'.join([para.text for para in paragraphs])


    def download_image(image_url, save_path):
        # Send a GET request to the image URL
        response = requests.get(image_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in binary write mode within the specified path
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded and saved as {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

    # ----------------- // --------------------




    # Scrape images
    images = scrape_images_with_bs4(soup) if need_image else []
    for i , im in enumerate(images[:4]):
        save_path = 'static/docs/images/image{}.jpg'.format(i)

        download_image(im , save_path)

    return main_content, images



    # ----------------- // -------------------- DRIVER CODE

if __name__ =='__main__':
    from response import google_search

    query = 'news on gaza-israel war'
    urls = google_search(query , num_results=1)  

    for url in urls:
        text, images = read_url_with_images(url)


    





# # I should implement a function that adds a webscraping with Selenium in case a webpage is too dynamic to be scraped with Beautiful soup
# def get_content_with_selenium(url):
#     # Setup Selenium WebDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get(url)
    
#     # Wait for the dynamic content to load
#     driver.implicitly_wait(10)  # Adjust based on expected load time
    
#     # Extract the content using Selenium
#     title = driver.title
#     try:
#         description = driver.find_element(By.NAME, 'description').get_attribute('content')
#     except:
#         description = 'No description found'
    
#     # Assuming main content is within <p> tags
#     paragraphs = driver.find_elements(By.TAG_NAME, 'p')
#     main_content = '\n'.join([para.text for para in paragraphs])
    
#     driver.quit()
#     return title, description, main_content


# import asyncio
# from pyppeteer import launch

# async def scrape(url):
#     browser = await launch(headless=True, args=['--no-sandbox'])
#     page = await browser.newPage()
    
#     # Navigate to the page and wait until network is idle
#     await page.goto(url, waitUntil='networkidle0')
    
#     # Extract the content of the page
#     content = await page.content()
    
#     # Optionally, you can extract all text from the <body> element as follows
#     text = await page.evaluate('() => document.body.innerText')
    
#     print(text)  # Prints out all text content of the page
    
#     await browser.close()
