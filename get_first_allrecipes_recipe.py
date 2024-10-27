from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Set Chrome driver path
chrome_service = Service('H:\\chromedriver-win64\\chromedriver.exe')  # Replace with your ChromeDriver path

# Launch Chrome browser in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=chrome_service, options=options)

def get_first_allrecipes_recipe():
    url = "https://www.allrecipes.com/"
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Parse the homepage to find the first recipe link
    soup = BeautifulSoup(driver.page_source, "html.parser")
    first_recipe_card = soup.find('a', class_="comp mntl-card-list-items mntl-document-card mntl-card card--image-top card card--no-image")
    
    if not first_recipe_card:
        print("Unable to find the first recipe link.")
        return {
            "Title": "No Recipe Found",
            "Link": "",
            "Description": "",
            "Ingredients": ["No Ingredients"],
            "Steps": ["No Steps"]
        }

    recipe_url = first_recipe_card['href']
    recipe_title = first_recipe_card.get_text(strip=True) if first_recipe_card else "No Title"
    
    # Visit the recipe link and extract details
    driver.get(recipe_url)
    time.sleep(5)  # Wait for the page to load

    # Parse the recipe page content
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract description, if available
    description_tag = soup.find("div", class_="recipe-summary")
    description = description_tag.get_text(strip=True) if description_tag else "No Description"

    # Extract ingredients
    ingredients = []
    ingredients_list = soup.find_all("li", class_="mm-recipes-structured-ingredients__list-item")
    for item in ingredients_list:
        quantity = item.find("span", {"data-ingredient-quantity": "true"})
        unit = item.find("span", {"data-ingredient-unit": "true"})
        name = item.find("span", {"data-ingredient-name": "true"})

        quantity_text = quantity.get_text(strip=True) if quantity else ""
        unit_text = unit.get_text(strip=True) if unit else ""
        name_text = name.get_text(strip=True) if name else ""
        
        ingredient = f"{quantity_text} {unit_text} {name_text}".strip()
        ingredients.append(ingredient)

        steps = []
        directions_section = soup.find("div", class_="mm-recipes-steps")
        if directions_section:
            content_section = directions_section.find("div", class_="mm-recipes-steps__content")
            if content_section:
                directions_list = content_section.find("ol", class_="mntl-sc-block-startgroup")
                if directions_list:
                    steps_items = directions_list.find_all("li", class_="mntl-sc-block-startgroup")
                    for i, step in enumerate(steps_items, 1):
                        step_text = step.find("p", class_="mntl-sc-block-html")
                        if step_text:
                            steps.append(f"Step {i}: {step_text.get_text(strip=True)}")
                        else:
                            steps.append(f"Step {i}: Text not found")
                else:
                    print("No ordered list found for steps.")
            else:
                print("No content section found within directions.")
        else:
            steps.append("No Steps")

        # Print the steps
        for step in steps:
            print(step)

    # Close the browser
    driver.quit()

    # Return the recipe details
    return {
        "Title": recipe_title,
        "Link": recipe_url,
        "Description": description,
        "Ingredients": ingredients if ingredients else ["No Ingredients"],
        "Steps": steps if steps else ["No Steps"]
    }

# Example of calling the function and printing results
if __name__ == "__main__":
    recipe = get_first_allrecipes_recipe()
    print(f"Title: {recipe['Title']}")
    print(f"Link: {recipe['Link']}")
    print(f"Description: {recipe['Description']}")
    print("Ingredients:")
    for ingredient in recipe['Ingredients']:
        print(f"- {ingredient}")
    print("Steps:")
    for step in recipe['Steps']:
        print(step)
