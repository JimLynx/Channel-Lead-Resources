<p align="center">
<img src="static/img/ms3-logo.png" />
</p>

SITE DEPLOYED LIVE ON HEROKU [HERE](https://channel-lead-resources.herokuapp.com/)

## Table of Contents

> - [Overview](#overview)
> - [User Stories](#user-stories)
> - [UX](#ux)
> - [Features](#features)
> - [Technologies Used](#technologies-used)
> - [References for learning](#references-for-learning)
> - [Testing](#testing)
> - [Project barriers and solutions](#project-barriers-and-solutions)
> - [Code validity](#code-validity)
> - [Version Control](#version-control)
> - [Deployment](#deployment)
> - [Credits](#credits)
> - [Acknowledgments](#acknowledgments)
> - [Support](#support)

(TBA - make gif for responsive view)

**Please note: To open any links in this document in a new browser tab, please press `CTRL + Click`.**

## Overview

> Every 6 weeks a current student from each of the four main sections of the course is selected to act as a Channel Lead for that respective channel.
>
> Up until now, the Channel Leads have been posting their slideshows, videos and PDF lessons/presentations in respective Slack Channels and 'Pinning' them in the channels. However, this procedure has proven that the information is not intuitive to find and students are asking many questions daily that are answered in these resources.
>
> The aim of this project is to provide a single resource platform for the Code Institute Slack community to easily access these valuable and helpful resources. Not only will this increase learning process for students, but also aims to minimise the amount of questions raised in Slack Channels, and relieve congestion on the Tutor Support platform.
>

## User Stories

> ### :man_student: :woman_student: Users _(Code Institute Students)_
>
> - As a user I would like to **have access to past Channel Lead presentations** in one place, so that I can:
>   - **periodically refer to them after the live presentations**
>   - **refer to them if I cannot make the live presentations** 
> - As a user I would like to **be able to search the site**, so that I can **easily find resources that I am looking for**
> - As a user I would like to **leave a comment** so that I can **recommend future topics to cover**
> - As a user I would like to **rate a post** (like/dislike-emojis) so that I can **visibly show how valuable the particular resource is to me**
> - As a user I would like to **access the information from anywhere**, so that I can **watch and read presentations on my mobile phone/tablet**
>
> ### :white_circle: Admin _(Code institute Slack Channel Leads)_
>
> - As an Admin I would like the ability to **log into an admin account**, so that I can **create resource posts**
> - As an Admin I would like the ability to **upload my presentations**, so that I can **add new material to the site**
> - As an Admin I would like the ability to **update my presentations**, so that I can **maintain material previously uploaded to most recent versions**
> - As an Admin I would like the ability to **delete my presentations**, so that I can **remove outdated information, which may become irrelevant due to technological advances**
> - As an Admin I would like the **ability for users to review my presentations**, so that I can **be informed of how useful they are and if anything can be improved upon**
>
> ### :red_circle: Superuser _(Developer-Site Creator)_
>
> In addition to the above,
> - As a Superuser I would like to be able to **keep information aimed at Code Institute Students**, so that **material posted is not directly available to the general public**
> - As a Superuser I would like to be able to **Create Admin accounts**, so that I can **assign them to ----------------------------**
> - As a Superuser I would like to be able to **Delete User accounts**, so that I can **keep the site secure**
> - As a Superuser I would like to be able to **Update Category names**, so that I can **ensure the site is kept neat**
> - As a Superuser I would like to be able to **Delete Categories**, so that I can **keep the site clean and clutter free**
>
>
> ### :large_blue_circle: Assessor (_Milestone Project Assessor account_)
>
> - As an Assessor, I will require full access to all Superuser privileges, so that I can gain full access in order to assess all aspects of the project

---

## UX

> This website project will target Code Institute Students undertaking the Diploma in Full Stack Software Development. The priority focus is on providing a fluent and structured resource and catalogue of current and past Channel Lead presentations.

---

### 1. Strategy

> #### Project and User Goals:
>
> - Provide an easy to navigate resource platform for hosting Channel Lead presentations and videos
>
> - Provide a pre-determined student User account for Code Institute students to be able to log in and access the resources
> - Provide Admin account for Channel Leads, to enable them to log in and post and manage presentations
> - Provide Superuser account for Site owner to enable frontend login accounts management
> - Provide Assessor account to enable an assessor to gain full access to all functionality in order to grade the project
> - Design backend functionality focussed on defensive design
> - Design frontend UX for:
>   - Clean and intuitive navigation
>   - Familiarity, using Slack and Code Institute 'look and feel'
>   - Responsiveness for use on mobile phone and tablet devices
>
> #### Main Sections to cover:
>
> - **:file_folder: Milestone 1** - Main focus in HTML, CSS (& Bootstrap)
> - **:file_folder: Milestone 2** - Main focus in JavaScript (& jQuery) and API's
> - **:file_folder: Milestone 3** - Main focus in Python, Databases and CRUD
> - **:file_folder: Milestone 4** - Focus on Django Full Stack Frameworks
> - **:file_folder: Version Control** - All topics relating to Git, IDE's, Repositories and Deployment
> - **:file_folder: General** - All other topics
>

### 2. Scope

> - Fits in with my current skill-set of HTML, CSS, JavaScript, Python, Flask and MongoDB
> - Implement platform for **links** to PDF  content (Channel Leads can host files on Cloudinary Account)
> - Implement platform for **links** to Video (Channel Leads can videos host on YouTube Brand Channel)
> - Allow Users to Read material posted
> - Allow Admin to Create, Read, Update and Delete material
> - Allow Superuser to Create, Read, Update and Delete material
> - Allow Superuser to Create, Read, Update and Delete Login Credentials
> - Allow separate Assessor Login, with full rights to investigate all aspects and functionality
>
> #### Stretch Goals:
>
> - :film_strip: Implement YouTube API to display videos on site
>
> - :+1: 'Like' or 'Starring' functionality for users to review posts
>
> - :calendar: Events Calendar - Displaying upcoming Channel Lead events and webinars
>
> - :clipboard: Review Page - Comments section for users to request topics to be covered

### 3. Structure

> The overall structure is for ease of navigation to each section
>
> - Top navigation menu for general public displays only Home and Login links
> - Logged in Users have access to various topic pages
>   - Each topic page is the same format to ensure consistency
>   - Top Navigation menu allows for easy navigation to desired sections
> - Logged in Superuser and Assessor have further access to superuser page where account management is possible

### 4. Skeleton

> - [Wireframes](static/wireframes/wireframes.pdf): #### TBA - link to wireframes
> - Navigation bar - Menu with links pointing to each page.
>   - Home - Intro image/video
>     - Brief information on the site
>   - Login (user types)
>     - Student (User) Login
>     - Admin (Channel Lead) Login
>     - Superuser Login
>     - Assessor Login
>   - Resource page with links to each topic (or direct link to each topic page from menu dropdown)
>   - Topic pages displaying content
>   - Contact page
> - Footer with Copyright info, Useful Links and Social Media icons

---

### 5. Surface

> The overall UX is clean and coordinates well with the official Code Institute and Slack themes for consistency and relatability.
>
> #### Colours
>
> Colour palette has been chosen to align with the Code Institute and Slack UX for familiarity
>
> [Colour Palette - Coolors.co](https://coolors.co/ffffff-4a4a4a-007cba-e84610-efb920)
> ![Image](static/img/colour-palette.png)
>
> #### Typography
>
> - "Montserrat" font (with fall-back font of Sans-Serif) is used for heading and body content, which aligns with the Code Institute format
>
> #### Images
>
> -
>
> #### Design Choices
>
> - 123
> - 456

---

## Features

### Existing Features

> - Designed with HTML5, CSS3, JavaScript, Python3, Flask, MongoDB and Bootstrap
> - Home/Landing page with ___________ pages in total
> - Responsive Bootstrap Navigation bar
> - Footer with useful links and social media links
> - Contact Form
>
> ### Features Left to Implement when skills develop
>
> - Integrate with Slack
> - Scalability

---

## Technologies Used

1. ### Languages

> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1593529419/Logos/html5-50_groo6o.png) [HTML5](https://en.wikipedia.org/wiki/HTML5)
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1593529419/Logos/CSS3-50_slrv0x.png) [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1597668963/Logos/js50_fcj8kt.png) [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
>
>  ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1605958609/Logos/python50.png) [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

2. ### Integration

> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1593528776/Logos/Bootstrap-50_khpj57.png) [Bootstrap](https://getbootstrap.com/) - by linking via [Bootstrap CDN](https://www.bootstrapcdn.com/) to HTML Doc
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1593528776/Logos/fontawesome-50_r5df5h.png) [FontAwesome](https://fontawesome.com/) Icons for Social Media links
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1593528776/Logos/GoogleFonts-50_mx57p6.png) [Google Fonts](https://fonts.google.com/) - Overall Typography import
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1600683635/Logos/jquery-50.png) [jQuery](https://jquery.com/) - JavaScript library
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1605958236/Logos/flask50.png) [Flask](https://flask.palletsprojects.com/en/1.1.x/) Micro web framework written in Python
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1605958236/Logos/mongo50.png) [MongoDB](https://www.mongodb.com/) NoSQL database program, using JSON-like documents

3. ### Dependencies:
> - [Flask Mail](https://pythonhosted.org/Flask-Mail/) For connecting the application to my mail account to receive communication from users
> - [Pymongo](https://pypi.org/project/pymongo/) and [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) To connect Python and Flask to the MongoDB database
> - [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) WSGI (Web Server Gateway Interface) for Python
> - [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) Templating language for Python
> - [dnspython](https://www.dnspython.org/) DNS toolkit for Python
> - [autopep8](https://pypi.org/project/autopep8/) Python Code formatter
> - [blinker](https://pythonhosted.org/blinker/) Object-to-object and broadcast signaling for Python objects
> - [click](https://click.palletsprojects.com/en/7.x/) Command Line Interface creation kit
> - [itsdangerous](https://readthedocs.org/projects/itsdangerous/) Various helpers to pass data to untrusted environments and to get it back safely
> - [MarkupSafe](https://pypi.org/project/MarkupSafe/) Implements a text object that escapes characters so it is safe to use in HTML and XML
>

4. ### Workspace, Version Control, Repository storage and Deployment

> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1600764509/Logos/VS-50.png) [VSCode](https://code.visualstudio.com/) - Main workspace IDE (Integrated Development Environment)
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1593518772/Logos/git-50_znskan.png) [Git](https://git-scm.com/) - Distributed Version Control tool to store versions of files and track changes
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1593518773/Logos/github-50_ixwpch.png) [GitHub](https://github.com/) - A cloud-based hosting service to manage Git repositories
>
> ![Image](https://res.cloudinary.com/jimlynx/image/upload/v1605957602/Logos/heroku50.png) [Heroku](https://heroku.com) - Container-based cloud platform for deployment and running of apps

5. ### Other

> - [Autoprefixer](https://autoprefixer.github.io/) Parses CSS and adds vendor prefixes.
> - [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly) Mobile-friendly check on site.
> - [Website Page Test](https://www.webpagetest.org/) Runs a website speed test from multiple locations around the globe using real browsers (IE and Chrome) and at real consumer connection speeds.
> - [Online-Spellcheck](https://www.online-spellcheck.com/) Online spelling and grammar checks.

6. ### IDE Extensions used in VSCode

> - Auto Close Tag
> - Auto Rename Nametag
> - Bracket Pair Colorizer 2
> - Code Spellchecker
> - Beautify - Code Formatter
> - Indent-Rainbow
> - Bootstrap 4 CDN Snippet
> - Markdown Lint
> - Python
> - JSHint

---

## Resources

> - [Code Institute Course Content](https://courses.codeinstitute.net/) - Main source of fundamental knowledge.
> - Code Institute **SLACK Community** - Main source of assistance
> - [Stack Overflow](https://stackoverflow.com/) - General resource.
> - [Youtube](https://www.youtube.com/) - General resource.
> - [CSS-Tricks](https://css-tricks.com/) - General resource.
> - [W3.CSS](https://www.w3schools.com/w3css/4/w3.css) - General resource.
> - [CommonMark](https://commonmark.org/help/) - For Markdown language reference.
> - [Colour Palette - Coolors.co](https://coolors.co/ffffff-4a4a4a-007cba-e84610-efb920)
> - [TinyPNG](https://tinypng.com/) - Efficient compression of images for site.
> - [Am I Responsive](http://ami.responsivedesign.is/) - Responsive website mockup image generator.
> - [Balsamiq](https://balsamiq.com/wireframes/) - Wireframing design tool.

---

## Testing

> Testing documentation can be found on a separate document [HERE](static/testing/TESTING.md)

## Project barriers and solutions

> - Created a branch for the modal confirmations. Modal templates for 'Add', 'Edit', 'Delete' and 'Add User' placed in base.html. The Add buttons on the modals work fine, but the Edit and Delete submit buttons will not work. Assumed issue stems from it being on the same page as the Add modal, causing a submit conflict with that form. Resolved by creating seperate ID's for the template modals, which relate to the form value on each modal, and then wrapping buttons/a tags in form elements, using 'form' attribute on modals to target the ID of the relevant forms. The Delete modals were still deleting the first item on the list, rather than  the specific item selected. Rectified this by moving the delete modal code from the base.html to each relevant file and providing id-targeting via Jinja.
> - Videos in iframes in modals continued playing after modal closed. Solution found on Stack Overflow - See [Credits](#credits)

---

## Code validity

> HTML - [W3C](https://validator.w3.org/) - Markup Validation
>
> CSS - [W3C](https://jigsaw.w3.org/css-validator/) - Jigsaw CSS Validation
>
> JavaScript - [JSHINT](https://jshint.com/) - JavaScript code warning & error check
>
> Python - [Pyton Tester](https://extendsclass.com/python-tester.html) Python code syntax checker
>
> TAGS - [Closing Tag Checker for HTML5](https://www.aliciaramirez.com/closing-tags-checker/) - Validates all tags are opening and closing correctly.

---

## Version Control

> - Used Git for version control.
> - Branches were created to work on alternative layout and buttons.
>   - user-confirmation branch > for implementing and testing confirmation modal dialogues.
> - The branches were then merged with the master branch after any conflicts were addressed.

---

## Deployment

This project has been deployed on GitHub Pages with the following process:

> ### IDE
>
> - All code was written on [Visual Studio Code](https://code.visualstudio.com/), a local IDE (Integrated Development Environment).
> - A virtual environment was created on VSCode to ensure that the packages installed are only installed in the virtual environment folder.
> - Sensitive information (passwords etc) is stored in an env.py file, which is added to the .gitignore file, to ensure this information is not pushed to the repository.
> - a requirements.txt file was created to store updated depenecies of installed packages for the project.
> - A Procfile was created to declare what commands are run by the application's dynos on the Heroku platform.
> - The code was then pushed to GitHub where it is stored in my [Repository](https://github.com/JimLynx/Channel-Lead-Resources).
>
> ### Heroku
>
> This project is deployed and hosted on [Heroku](https://www.heroku.com) - a Cloud Application Platform that enables developers to build, run, and operate applications in the cloud.
> Deployment process is as follows:
>
> - Register for a free account on the Heroku [Signup](https://signup.heroku.com/login) page.
> - On the Dashboard, click the 'New' button and select 'Create new app'.
> - Choose a name and region.
> - Under the 'Settings' tab, click on 'Config Vars' to add Configuration Variables from the env.py file. This includes the IP, Port, Secret key, [MongoDB](https://www.mongodb.com/) name and URI, as well as mail settings for Flask Mail.
> - Select the 'Deploy' option from the menu.
> - Under 'Deployment method' select the GitHub option to connect to your GitHub repository. Ensure GitHub Username is selected and use the search function to find the relevant repository. It is recommended using a 'main' branch as default, due to GitHub depreciating the 'master' branch name.
> - Select Automatic deploys from the main branch and click 'Deploy Branch'.
> - Click on the 'Open App' button on the top-right to open the deployed app.
> - There is no difference between the deployed version and the development version.
>
> ### Cloning
>
> - The code can be run locally through clone or download from the repository on [GitHub](https://github.com/JimLynx/Channel-Lead-Resources).
> - You can do this by opening the repository, clicking on the green 'Code' button and selecting either 'clone or download'.
> - The Clone option provides a URL, which you can use on your CLI with `git clone <url>`.
> - The Download ZIP option provides a link to download a ZIP file which can be unzipped on your local machine. The files can then be.uploaded to your IDE

## Credits

> ### Media
>
> - Code Institute logo downloaded from [official website](https://codeinstitute.net/)
> - Slack logo downloaded from [official website](https://slack.com/)
> - 404 error page image created on [Meme Generator](https://memegenerator.net/)
>
> #### Content
>
> - Logo created by me, but using downloaded Code Institute and Slack logos
>
> #### Bootstrap 4 CDN Boilerplate
>
> - I've taken advantage of _Simen Daehlin's_ template boilerplate from his [Marketplace](https://marketplace.visualstudio.com/items?itemName=eventyret.bootstrap-4-cdn-snippet)
>
> #### Code Snippets
>
> - Setting active class to navigation items in Flask, adapted from post on Stack Overflow found [HERE](https://stackoverflow.com/a/55895621)
> - Animation for 404 page images adjsacent to button, adapted from post on CSS Tricks found [HERE](https://css-tricks.com/making-css-animations-feel-natural/)
> - Prevent spaces in username and password entries, adapted from post on Stack Overflow found [HERE](https://stackoverflow.com/a/14236954)
> - Javascript solution for cancelling video playback after closing modal from Stack Overflow found [HERE](https://stackoverflow.com/a/54845883)
> - Regex code solution for capturing only the hosted Youtube video ID written by [Sean Murphy](https://github.com/nazarja)
>
> -
---

## Acknowledgments
>
> I would like to thank:
>
> - My mentor, **Aaron Sinnott** for his guidance and advice.
> - **[Tim Nelson](https://github.com/TravelTimN)**, **[Bim Williams](https://github.com/mrbim)**, **[John Traas](https://github.com/Jays-T)**, **[Anthony O'Brien](https://github.com/auxfuse)** and **[Sean Murphy](https://github.com/nazarja)** for always being open to discussing, helping and generally being awesome people.
> - Everyone in Tutor support for always being patient and friendly when approaching with assistance during course material.
> - **CI staff** and **Slack Community** for always being on-hand with questions posted and assistance requests.
> - Everyone that takes part in the Slack calls, specifically from the **#In-It-Together** and **#Study-Group** channels.

## Support

> For any issue resolution or assistance, please email  Jim Morel :e-mail: jim.lynx@gmail.com :e-mail:

---

## Known Bugs
> - 
