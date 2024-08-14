# Advertising Campaigns Analysis Dashboard

![Dashboard Screenshot](images/Screenshot.png)  <!https://adsdashboard.streamlit.app -->

## Overview

The **Advertising Campaigns Analysis Dashboard** is a live analytical tool built using Streamlit and Python. It retrieves data from a MySQL database hosted in the cloud and visualizes performance metrics for various advertising campaigns. This dashboard allows users to filter campaign data, assess key performance indicators (KPIs), and gain insights into their advertising strategies.

## Features

- Data retrieval from a MySQL database
- Dynamic filtering options for Campaign ID and Platform Type
- Metrics visualization including Audience Reach, Average Frequency, Audience Efficiency Rate, and more
- Interactive data tables and charts
- Customizable date range for analytics (Daily, Weekly, Monthly)

## Technologies Used

- [Streamlit](https://streamlit.io/) - For building the dashboard
- [Pandas](https://pandas.pydata.org/) - For data manipulation and analysis
- [Plotly](https://plotly.com/python/) - For creating interactive charts and graphs
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) - For visualizing data in static charts
- [Altair](https://altair-viz.github.io/) - For declarative statistical visualization
- [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/) - For connecting to a MySQL database
- [Streamlit Option Menu](https://streamlit-option-menu.streamlitapp.com/) - For the sidebar navigation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Yass01b/AdsDashboard

2 - Navigate to the project directory:

cd AdsDashboard

3 - Install the required Python packages:

pip install -r requirements.txt
Update .env file (if applicable) with your database connection details.

4 - Usage

Run the Streamlit application:

streamlit run app.py

Open your web browser and go to http://localhost:8501.

Use the sidebar to filter by:

Campaign ID: Select one or more campaign IDs from the list.
Platform Type: Choose one or more advertising platforms.
Date Range: Select the time frame for analysis (Daily, Weekly, Monthly).


5 - Deployment
This dashboard is deployed on Streamlit Cloud. You can access it through the following link: < !https://adsdashboard.streamlit.app -->


6 - Acknowledgments
Thanks to the Streamlit community for their great resources and support.
Special thanks to the developers of the libraries and tools used in this project.