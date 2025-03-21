import requests
from bs4 import BeautifulSoup
import hashlib
import time

def get_character_names(url):
    """
    Scrapes the given LOTR Fandom category page for character names.
    Returns a tuple: (names_on_this_page, next_page_url)
    """
    names = []
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page:", url)
        return names, None

    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all("a", class_="category-page__member-link"):
        name = a.get_text(strip=True)
        if name and "Category:" not in name:
            names.append(name)
    
    next_link = soup.find("a", class_="category-page__pagination-next")
    next_page_url = next_link['href'] if next_link and next_link.has_attr('href') else None
    
    if next_page_url and next_page_url.startswith("/"):
        base_url = "https://lotr.fandom.com"
        next_page_url = base_url + next_page_url

    return names, next_page_url

def get_all_character_names(start_url):
    """
    Follows pagination links to scrape character names from all pages.
    Returns a complete list of character names.
    """
    all_names = []
    current_url = start_url
    page = 1
    while current_url:
        print(f"Scraping page {page}: {current_url}")
        names, next_page = get_character_names(current_url)
        print(f"Found {len(names)} names on page {page}")
        all_names.extend(names)
        current_url = next_page
        page += 1
        time.sleep(1)
    return all_names

def generate_password(names, target_hash):
    """
    Iterates over the list of names and generates every possible password candidate
    by concatenating 3 consecutive names (without any separator).
    Computes the MD5 hash and compares it with target_hash.
    Returns the matching password candidate if found.
    """
    for i in range(len(names) - 2):
        candidate = names[i] + names[i + 1] + names[i + 2]
        candidate_hash = hashlib.md5(candidate.encode()).hexdigest()
        if candidate_hash == target_hash:
            return candidate
    return None

if __name__ == "__main__":
    start_url = "https://lotr.fandom.com/wiki/Category:The_Lord_of_the_Rings_characters"
    target_hash = "5c5408e1f41c8a2ce6343ed0899eecb0"
    
    character_names = get_all_character_names(start_url)
    print("\nTotal character names scraped:", len(character_names))
    
    password = generate_password(character_names, target_hash)
    
    if password:
        flag = f"rootaccess{{{password}}}"
        print("\nPassword found:", password)
        print("Flag:", flag)
    else:
        print("\nPassword not found. Consider expanding or verifying the scraped data.")