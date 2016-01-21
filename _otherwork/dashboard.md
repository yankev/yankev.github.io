---
title: Plotly Dashboard
layout: default
date: January 21, 2016
---
## Creating a Plotly Dashboard in R

In this example we're going to create two bar graphs containing made-up zoo data. Then we're going to arrange these plots into a dashboard. 


{% highlight r %}
require(plotly)
library(httr)

g1 <- plot_ly(
  x = c("giraffes", "orangutans", "monkeys"),
  y = c(20, 14, 23),
  name = "SF Zoo",
  type = "bar"
)

l1 <- plotly_POST(g1, filename = "r-test/SFzoo", world_readable=TRUE)
#this posts the plot into r-test in our plotly repository
#we then extra the url of the plot
url1 = l1[1] 

g2 <- plot_ly(
  x = c("giraffes", "orangutans", "monkeys"),
  y = c(12, 18, 29),
  name = "LA Zoo",
  type = "bar"
)

l2 <- plotly_POST(g2, filename = "r-test/LAzoo", world_readable=TRUE)

url2 = l2[1]

#here we would have to write the urls ourselves
#this dashboard is is a 2x2 plot

json <- '{"requireauth": false, "rows": [[{"plot_url": "https://plot.ly/~yankev/6"},{"plot_url": "https://plot.ly/~yankev/17"}], [{"plot_url": "https://plot.ly/~yankev/10"}, {"plot_url": "https://plot.ly/~yankev/21"}]], "banner": {"visible": true, "textcolor": "white", "links": [], "backgroundcolor": "#3d4a57", "title": "Quarterly Outlook"}, "auth": {"username": "Acme Corp", "passphrase": ""}}'

#here we use sprintf to fill in the urls for us
#this is going to be slight variation with 2 plots on the top row, and one on the bottom

json2 <- sprintf(
  '{"requireauth": false, "rows": [[{"plot_url": "%s"}, {"plot_url": "%s"}],[{"plot_url": "%s"}]], "banner": {"visible": true, "textcolor": "white", "links": [], "backgroundcolor": "#3d4a57", "title": "Quarterly Outlook"}, "auth": {"username": "Acme Corp", "passphrase": ""}}',
  url1,url2,url1
  )


resp <- POST('https://dashboards.ly/publish', body = list(dashboard=json2),
             encode = "form",
             content_type('application/x-www-form-urlencoded'))
resp
{% endhighlight %}

### The output is the following:

> Response [https://dashboards.ly/publish]  
>  Date: 2016-01-21 20:37  
>  Status: 200  
>  Content-Type: application/json  
>  Size: 41 B  
> {  
>  "url": "/ua-zGQCHrjVoQ5L2MiLLX2Lp6"


<iframe src="https://dashboards.ly/ua-zGQCHrjVoQ5L2MiLLX2Lp6"
         width="100%" height="800px" style="border: none;"></iframe>


