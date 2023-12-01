# Testing

## Manual Testing

## User Stories (click path)

### First time user

| Story | Site Path | Image |
|:---:|:---:|:---:|

### Registered user

| Story | Site Path | Image |
|:---:|:---:|:---:|

### Super user

| Story | Site Path | Image |
|:---:|:---:|:---:|

### Admin user

| Story | Site Path | Image |
|:---:|:---:|:---:|

## Code Validators

### HTML

### CSS

### JavaScript

### Python

## Lighthouse

I used Google Chrome Dev Tools Lighthouse function to check the performance, accessibility and search engine optimization with scores documented below and notes to explain reduced scores in certain areas.

Home

![Home Lighthouse Screenshot](/static/images/readme/testing/homelh.webp)

Register

![Register Lighthouse Screenshot](/static/images/readme/testing/registerlh.webp)

Sign In

![Sign In Lighthouse Screenshot](/static/images/readme/testing/signinlh.webp)

Recipes

![Recipe Lighthouse Screenshot](/static/images/readme/testing/recipeslh.webp)

Recipe Details

![Recipe Details Lighthouse Screenshot](/static/images/readme/testing/recipedetailslh.webp)

Add Recipe

![Add Recipe Lighthouse Screenshot](/static/images/readme/testing/addrecipelh.webp)

Edit Recipe

![Edit Recipe Lighthouse Screenshot](/static/images/readme/testing/editrecipelh.webp)

Categories

![Categories Lighthouse Screenshot](/static/images/readme/testing/categorylh.webp)

Add Category

![Add Category Lighthouse Screenshot](/static/images/readme/testing/addcategorylh.webp)

Edit Category

![Edit Category Lighthouse Screenshot](/static/images/readme/testing/editcategorylh.webp)

Profile

![Profile Lighthouse Screenshot](/static/images/readme/testing/profilelh.webp)

Edit Details

![Edit Details Lighthouse Screenshot](/static/images/readme/testing/editdetailslh.webp)

Users

![Users Lighthouse Screenshot](/static/images/readme/testing/userslh.webp)

Messages

![Messages Lighthouse Screenshot](/static/images/readme/testing/messageslh.webp)

Contact

![Contact Lighthouse Screenshot](/static/images/readme/testing/contactlh.webp)

### Notes

The below were noted during the Lighthouse testing as suggestions for improvements in the scores.

- add_recipe.html - lower accessibility score due to dynamic instructions and ingredients sections which do not have individual labels for the inputs, rather a group label

- Cards reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

- Performance score reduction due to the images being URL linked rather than appropriately sized and formatted uploads direct from the user.

- Best Practices score reduction due to one of the linked image URLS causing Cookie issues in Chrome Devtools.

- SEO reduction (Recipe Details) due to the floating more options Materialize button not being crawlable.

[Back to README](README.md)