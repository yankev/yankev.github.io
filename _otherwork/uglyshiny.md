---
title: Ugly Shiny Demo with Plotly graphs
date: January 21, 2016
layout: default
---

## Shiny Dashboard Demo and Thoughts

Below is a dashboard style shiny project that includes Plotly graphs. This dashboard is hosted on shinyapps.io.
In order to create the layout I used the `fluidRow` and `column` function in the shiny library. However this didn't seem to work to well when putting the Plotly graphs side by side, hence their reduced size. 

It appears that using Shiny to create Plotly dashboards may be less visually appealing, (at least without some html css touchups that you may have to include yourself) compared to using the Dashboard.ly web API. 

However an issue that I found when using this web API in R was the ability to properly format my data into a json string. 
That had to be done using the `json.dump` function found in the `json` library in Python. 

<iframe src="https://yankev.shinyapps.io/Movies/" style="border: none; width: 1000px; height: 800px"></iframe>