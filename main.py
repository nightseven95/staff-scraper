import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict

def scrape_mit_staff() -> Dict[str, List[Dict]]:
    """
    Scrape MIT staff by department.
    Returns a dict with department names as keys and staff lists as values.
    """
    
    # MIT departments/schools base URLs (you'll need to identify the actual structure)
    departments = {
        'School of Engineering': 'https://engineering.mit.edu/faculty-research/',
        'Physics': 'https://physics.mit.edu/faculty/',
        'CSAIL': 'https://csail.mit.edu/people',
        # Add more departments as you discover them
    }
    
    results = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for dept_name, url in departments.items():
        print(f"Scraping {dept_name}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            staff_list = extract_staff(soup, dept_name)
            results[dept_name] = staff_list
            
            # Be polite: wait between requests
            time.sleep(2)
            
        except requests.RequestException as e:
            print(f"  Error scraping {dept_name}: {e}")
            continue
    
    return results

def extract_staff(soup: BeautifulSoup, department: str) -> List[Dict]:
    """
    Extract staff information from a department page.
    This is department-specific and will need adjustment based on actual HTML structure.
    """
    staff = []
    
    # This is a generic example - you'll need to inspect actual HTML
    # and adjust selectors accordingly
    
    # Example: if faculty are in divs with class 'faculty-member'
    for member in soup.find_all('div', class_='faculty-member'):
        name = member.find('h3')
        title = member.find('p', class_='title')
        email = member.find('a', class_='email')
        
        if name:
            staff.append({
                'name': name.get_text(strip=True),
                'title': title.get_text(strip=True) if title else 'N/A',
                'email': email.get_text(strip=True) if email else 'N/A',
                'department': department
            })
    
    return staff

if __name__ == '__main__':
    results = scrape_mit_staff()
    
    # Print results
    for dept, staff in results.items():
        print(f"\n{dept}: {len(staff)} staff members")
        for person in staff[:3]:  # Show first 3
            print(f"  - {person['name']} ({person['title']})")
