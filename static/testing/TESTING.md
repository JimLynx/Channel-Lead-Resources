## Table of Contents

> - [User Stories](#user-stories)
> - [Code validity](#code-validity)
> - [Contact Form](#contact-form)
> - [Search Function](#search-function)
> - [Responsive](#responsive)
> - [Deployment](#deployment)

---

## User Stories

> ### Users _(Code Institute Students)_
>
> 1. As a user I would like to **have access to past Channel Lead presentations** in one place, so that I can:
>
> - **periodically refer to them after the live presentations**.
> - **refer to them if I cannot make the live presentations**.
>
> #### **TESTING:** After logging in with a user (**'student'**) account, resource material is available on the Resources page. Users can read description of the material posted and view PDF and Videos on modals within each section
>
> 2. As a user I would like to **be able to search the site**, so that I can **easily find resources that I am looking for**.
>
> #### **TESTING:** The search function allows the user to search by keyword, category or both, which makes it easy for the user to source relevant material easily. testing is covered in more detail under [Search Function](#search-function)
>
> 3. As a user I would like to **leave a comment** so that I can **recommend future topics to cover**.
>
> #### **TESTING:** The Contact Page has functionality allowing the user to submit a review and/or suggestion, which is delivered to my email inbox. I cna then copy and paste the informaiton in the 'Channel Lead' Slack channel to highlight the interest of the topic needing to be covered
>
> 4. As a user I would like to **rate a post** (like/dislike-emojis) so that I can **visibly show how valuable the particular resource is to me**.
>
> #### **TESTING:** The rating functionality has been moved to 'Features Left to Implement' due to time constraints
>
> 5. As a user I would like to **access the information from anywhere**, so that I can **watch and read presentations on my mobile phone/tablet**.
>
> #### **TESTING:** Site designed with mobile-first responsive approach, allowing the user to easily access the information provided on mobile and tablet devices
>
> ### Admin _(Code institute Slack Channel Leads)_
>
> 1. As an Admin I would like the ability to **log into an admin account**, so that I can **create resource posts**.
>
> #### **TESTING:** The **'Lead'** username and dedicated password was added for Channel leads with access to the Manage Resources dashboard page, whereby they can Create new material with the Add Resources button, which redirects to the Add Resources page. This page presents a form for all relevant fields for a post, seperated by categories
>
> 2. As an Admin I would like the ability to **upload my presentations**, so that I can **add new material to the site**.
>
> #### **TESTING:** On the above Add Resources page, various options were attempted fopr PDF and Video uploads, but without a paid hosting service, admin users are requested to host these resources themselves and paste a link into the inputs for each instead. The upload functionality will need to be implemented at a later stage once skills develop
>
> 3. As an Admin I would like the ability to **update my presentations**, so that I can **maintain material previously uploaded to most recent versions**.
>
> #### **TESTING:** On the Manage Resources page, admin users have the Edit Resources
>
> 4. As an Admin I would like the ability to **delete my presentations**, so that I can **remove outdated information, which may become irrelevant due to technological advances**.
>
> #### **TESTING:** > #### **TESTING:** On the Manage Resources page, admin users have the Delete Resources
>
> - As an Admin I would like the **ability for users to review my presentations**, so that I can **be informed of how useful they are and if anything can be improved upon**
>
> #### **TESTING:** Users are able to review posts from the Contact Page by submitting a review and/or suggestion. The 'rate/review' functionality for individual posts has been moved to 'Features Left to Implement' due to time constraints
>
> ### Superuser _(Developer-Site Creator)_
>
> In addition to the above,
>
> 1. As a Superuser I would like to be able to **keep information aimed at Code Institute Students**, so that **material posted is not directly available to the general public**.
>
> #### **TESTING:** Only assigned Student, Lead, Superuser and Assessor accounts have access to the site via pre-added usernames and passwords. The general public does only has access to the Home & Login screens
>
> 2. As a Superuser I would like to be able to **Create Admin accounts**, so that I can **assign them to users**.
>
> #### **TESTING:** On the Manage Users page, the Superuser account has the ability to Add usernames and passwords
>
> 3. As a Superuser I would like to be able to **Delete User accounts**, so that I can **maintain control of user accounts**.
>
> #### **TESTING:** On the Manage Users page, the Superuser account has the ability to Delete usernames
>
> 4. As a Superuser I would like to be able to **Update Category names**, so that I can **ensure the site is kept neat**.
>
> #### **TESTING:** On the Manage Categories page, the Superuser account has the ability to Add new categories and Edit existing categories names
>
> 5. As a Superuser I would like to be able to **Delete Categories**, so that I can **keep the site clean and clutter free**.
>
> #### **TESTING:** On the Manage Categories page, the Superuser account has the ability to Delete existing categories
>
> ### Assessor (_Milestone Project Assessor_)
>
> 1. As an Assessor, I will require full access to all Superuser privileges, so that I can gain full access in order to assess all aspects of the project.
>
> #### **TESTING:** The **'Assessor'** username and password created to allow a Project Assessor full access to the project with all priveledges of a Superuser, but with dedicated login details

---

## Code Validity

> ### HTML
>
> Passed code through [Nu Html Checker](https://validator.w3.org/#validate_by_uri) by entering the 'Validate by URI method.
> - (----------removed direct input as too many errors from templating language - HTML tyo be tested again after final deployment-------------------)
>
> ### CSS
>
> Passed code through [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input) by pasting code in by direct input method
>
> - No errors found
> - 8 warnings relating to custom colour variables - safely ignored.
>
> ![Image](../testing/css-validation.png)
>
> ### JavaScript
> Passed code through [JSHint](https://jshint.com/)
> - Two warnings for missing semi-colons(resolved)
> - Warning for ''let' is available in ES6 (use 'esversion: 6') or Mozilla JS extensions (use moz).' - Safely ignored.
> - JSHint flags Jquery $ symbol as undefined variable - safely ignored.
> ### Python
>
> Autopepe8 installed as a dependency for checking code as written
> All Python code passed through [ExtendsClass Python Syntax Checker](https://extendsclass.com/python-tester.html)
>
> - app
>   ![Image](../testing/app-check.png)
> - routes
>   ![Image](../testing/routes-check.png)
> - errors
>   ![Image](../testing/errors-check.png)
> - mail_settings
>   ![Image](../testing/mail_settings-check.png)

---

## Search Function (Resources, Manage Categories and Manage Resources pages)

> #### **TESTING:**
>
> - Clicked submit with no entries in fields - page resets to show all resources.
> - Entered valid keyword and page returns relevant resource(s) containing that keyword.
> - Entered invalid keyword and page returns the message: 'No results found, please try another search'.
> - Entered keyword and selected category:
>   - If keyword is valid and category is valid, page returns relevant resource(s) containing that keyword within the category selected.
>   - If keyword is valid but not in the selected category, page returns the message: 'No results found, please try another search'.
> - Selected category only with no keyword entered, page returns a list of resources of the selected category.
> - Clicked Reset button and this resets the page to default view as expected.

---

## Contact Form

> #### **TESTING:**
>
> - All required fields are working fine. When Submit button is clicked and 'required' fields are empty, the user receives a notification to fill in the relevant field.
> - When submitting a completed form, user receives a flash message notification that the feedback/suggestion has been sent.
> - After submission, checked email inbox and message from the site is successfully recieved.
>
> ![Image](../testing/email-test.png)

---

## Responsive Tests

> When select element is viewed on mobile in DevTools, the option elements extend offscreen. However, this is not an issue on physical mobile devices as the browser renders it's own native form elements.

![Image](../testing/test-select-devtools.png)
![Image](../testing/test-select-mobile-device.png)

---

## Deployment

>
