---
layout: post
title:  "Analysing nycflights13 Using Relational Structure of its DataFrames (Updated) "
date:   2016-01-18 18:46:00 -0500

---

### Introduction
In this post we'll be usig the `nycflights13` data again, and this is because it has many other dataframes within it, so that we can use some of dplyr's relational function.

In fact there are the following datasets within this package:

1. `flights` which contains information about all the flights out of New York, and is the most central df

2. `airports` which gives us information regarding the airports, ie:the name and location
3. `planes` which gives us information regarding particular planes, used in `flights`
4. `airlines` gives information regarding airlines
5. `weather` which gives us the weather conditions at the departing city/aiport in New York.

In this post we'll take a look at `flights, planes, and airports` in the following 2 questions.

#### Let's begin


So the first question we'll take a look at is:

* Compute the average delay by destination, then join on the airports data frame so you can show the spatial distribution of delays. 


{% highlight r %}
flights2 <- mutate(flights, tot_delay = arr_delay + dep_delay)
flights2 <- flights2 %>% group_by(dest) %>% 
  summarise(avg_delay = mean(tot_delay, na.rm = T)) %>% 
  left_join(airports, c("dest"="faa")) %>%
  arrange(desc(avg_delay))

head(flights2)
{% endhighlight %}



{% highlight text %}
## Source: local data frame [6 x 8]
## 
##    dest avg_delay                  name      lat        lon   alt    tz
##   (chr)     (dbl)                 (chr)    (dbl)      (dbl) (int) (dbl)
## 1   CAE  75.57547 Columbia Metropolitan 33.93883  -81.11953   236    -5
## 2   TUL  68.54762            Tulsa Intl 36.19839  -95.88811   677    -6
## 3   OKC  59.80000     Will Rogers World 35.39309  -97.60073  1295    -6
## 4   JAC  55.57143  Jackson Hole Airport 43.60733 -110.73775  6451    -7
## 5   TYS  52.45156         Mc Ghee Tyson 35.81097  -83.99403   981    -5
## 6   BHM  45.89219       Birmingham Intl 33.56294  -86.75355   644    -6
## Variables not shown: dst (chr)
{% endhighlight %}

Now we're ready to visualize this information. First let's make a plot of the United States, as it seems the flights only include flights to other American cities. We use the map data included with the `ggplot2` package, and we we set the variable `states` to the dataframe that includes the coordinates to plot each state.
We then use `geom_polygon` in order to plot the map using the coordinate information. 


{% highlight r %}
library(ggplot2)
states = map_data("state")

g <- ggplot(data=states)
g2 <- g + geom_polygon(mapping=aes(x=long,y=lat,group=group),color="white",fill="grey")
g2 <- g2 + ggtitle("Map of the USA minus Alaska")
g2
{% endhighlight %}

![center](http://yankev.github.io/figs/relationalmap_plotly/unnamed-chunk-3-1.png)

Let's now add the information regarding which destination airports are the cause of most delay. Let's remove the points that are too west to be plotted onto this map, (ie: all airports in Alaska).


{% highlight r %}
flights3 <- filter(flights2, lon > -140)
g3 <- g2 + geom_point(data=flights3, mapping = aes(x = lon, y = lat, color = avg_delay), 
                position = "jitter",size=2.5) + labs(color = "Average Delay") +
                scale_colour_gradient(low = "white",high = "dark red")
g3
{% endhighlight %}

![center](http://yankev.github.io/figs/relationalmap_plotly/unnamed-chunk-4-1.png)

Let's make this even more detailed by adding some labels to the worst, and best destinations.


{% highlight r %}
#let's remove the na terms, because they will cause some trouble for the tail function later on.
#note: probably should've removed the na terms far earlier on.

flights3 <- filter(flights3, !is.na(avg_delay))
worst_flights <- head(flights3,5)
best_flights <- tail(flights3,5)

g4 <- g3 + geom_text(data=worst_flights, mapping=aes(x = lon, y = lat, label = dest), color="red", nudge_y = -0.5) 

g4 + geom_text(data=best_flights, mapping=aes(x = lon, y = lat , label = dest), angle=20,nudge_y=-0.5)
{% endhighlight %}

![center](http://yankev.github.io/figs/relationalmap_plotly/unnamed-chunk-5-1.png)

#### As an added bonus, we'll plot this information(including those points too Western for the ggplot map of the USA) using `plotly`.




{% highlight r %}
flights2$hover <- with(flights2, paste0(name,', Avg. Delay: ',avg_delay))

m <- list(
  colorbar = list(title = "Average Delay"),
  size = 9, opacity = 0.7, symbol = 'circle'
)

# geo styling
g <- list(
  scope = 'usa',
  projection = list(type = 'albers usa'),
  showland = TRUE,
  landcolor = toRGB("gray95"),
  subunitcolor = toRGB("gray85"),
  countrycolor = toRGB("gray85"),
  countrywidth = 1,
  subunitwidth = 0.5
)



usa <- plot_ly(flights2, lat = lat, lon = lon, text = hover, color = avg_delay,
        type = 'scattergeo', locationmode = 'USA-states', mode = 'markers',
        marker = m) %>% layout(title = 'Delays of US airports, flying out of NYC', geo = g)

usa
{% endhighlight %}

<!--html_preserve--><div id="htmlwidget-1943" style="width:720px;height:432px;" class="plotly"></div>
<script type="application/json" data-for="htmlwidget-1943">{"x":{"data":[{"type":"scattergeo","inherit":true,"lat":[33.938833,36.198389,35.393089,43.607333333,35.810972,33.562942,41.533972,37.505167,43.139858,40.9160833,41.732581,42.748267,42.880833,42.932556,34.895556,41.303167,39.048836,39.297606,44.741445,32.127583,36.09775,42.947222,41.785972,38.138639,38.373147,38.695417,38.944533,39.902375,38.1740858,36.894611,30.494056,43.646161,43.118866,36.124472,41.708661,29.533694,44.807444,38.748697,39.175361,35.042417,32.898647,41.938889,34.270615,39.717331,33.636719,39.861656,43.111187,39.997972,44.471861,41.411689,35.877639,42.940525,39.871944,39.642556,34.200667,26.683161,45.588722,29.645419,40.491467,26.072583,29.993389,null,44.881956,33.67975,27.975472,38.509794,41.978603,38.852083,45.777643,30.194528,35.0402222,null,42.212444,28.429394,35.214,37.721278,35.436194,37.618972,29.984433,40.481181,32.733556,37.3626,36.2818694,33.434278,null,42.364347,26.536167,41.253053,33.817722,61.174361,27.395444,24.556111,33.942536,36.080056,47.449,40.788389,25.79325,32.896828,21.318681,41.391667,null,33.675667,33.829667,38.0365,40.777245],"lon":[-81.119528,-95.888111,-97.600733,-110.73775,-83.994028,-86.75355,-93.663083,-77.319667,-89.337514,-81.4421944,-71.420383,-73.801692,-85.522806,-71.435667,-82.218889,-95.894069,-84.667822,-94.713905,-85.582235,-81.202139,-79.937306,-87.896583,-87.752417,-78.452861,-81.593189,-121.590778,-77.455811,-84.219375,-85.7364989,-76.201222,-81.687861,-70.309281,-77.672389,-86.678194,-86.31725,-98.469778,-68.828139,-90.370028,-76.668333,-89.976667,-80.040528,-72.683222,-77.902569,-86.294383,-84.428067,-104.673178,-76.106311,-82.891889,-73.153278,-81.849794,-78.787472,-78.732167,-75.241139,-106.917694,-118.358667,-80.095589,-122.5975,-95.278889,-80.232872,-80.15275,-90.258028,null,-93.221767,-78.928333,-82.53325,-107.894242,-87.904842,-77.037722,-111.160151,-97.669889,-106.6091944,null,-83.353389,-81.308994,-80.943139,-122.220722,-82.541806,-122.374889,-95.341442,-107.21766,-117.189667,-121.929022,-94.3068111,-112.011583,null,-71.005181,-81.755167,-70.060181,-118.151611,-149.996361,-82.554389,-81.759556,-118.408075,-115.15225,-122.309306,-111.977772,-80.290556,-97.037997,-157.922428,-70.615278,null,-117.868222,-116.506694,-84.605889,-73.872608],"text":["Columbia Metropolitan, Avg. Delay: 75.5754716981132","Tulsa Intl, Avg. Delay: 68.5476190476191","Will Rogers World, Avg. Delay: 59.8","Jackson Hole Airport, Avg. Delay: 55.5714285714286","Mc Ghee Tyson, Avg. Delay: 52.4515570934256","Birmingham Intl, Avg. Delay: 45.8921933085502","Des Moines Intl, Avg. Delay: 45.1453154875717","Richmond Intl, Avg. Delay: 43.7314578005115","Dane Co Rgnl Truax Fld, Avg. Delay: 43.7086330935252","Akron Canton Regional Airport, Avg. Delay: 40.5439429928741","Theodore Francis Green State, Avg. Delay: 38","Albany Intl, Avg. Delay: 37.8444976076555","Gerald R Ford Intl, Avg. Delay: 37.5741758241758","Manchester Regional Airport, Avg. Delay: 35.8122317596567","Greenville-Spartanburg International, Avg. Delay: 35.0367088607595","Eppley Afld, Avg. Delay: 34.889840881273","Cincinnati Northern Kentucky Intl, Avg. Delay: 34.7664429530201","Kansas City Intl, Avg. Delay: 34.7480106100796","Cherry Capital Airport, Avg. Delay: 34.5052631578947","Savannah Hilton Head Intl, Avg. Delay: 33.2136181575434","Piedmont Triad, Avg. Delay: 33.0435656836461","General Mitchell Intl, Avg. Delay: 32.9409376153562","Chicago Midway Intl, Avg. Delay: 31.0139130434783","Charlottesville-Albemarle, Avg. Delay: 30.8913043478261","Yeager, Avg. Delay: 30.865671641791","Sacramento Intl, Avg. Delay: 30.8014184397163","Washington Dulles Intl, Avg. Delay: 30.7529258777633","James M Cox Dayton Intl, Avg. Delay: 30.2080057183703","Louisville International Airport, Avg. Delay: 28.6983695652174","Norfolk Intl, Avg. Delay: 28.3061366806137","Jacksonville Intl, Avg. Delay: 28.2203583682806","Portland Intl Jetport, Avg. Delay: 27.9501748251748","Greater Rochester Intl, Avg. Delay: 27.7989821882952","Nashville Intl, Avg. Delay: 27.7031558185404","South Bend Rgnl, Avg. Delay: 27.6","San Antonio Intl, Avg. Delay: 27.3232169954476","Bangor Intl, Avg. Delay: 27.1843575418994","Lambert St Louis Intl, Avg. Delay: 26.9835828102366","Baltimore Washington Intl, Avg. Delay: 26.8340248962656","Memphis Intl, Avg. Delay: 26.1162514827995","Charleston Afb Intl, Avg. Delay: 25.2051467923161","Bradley Intl, Avg. Delay: 24.7694174757282","Wilmington Intl, Avg. Delay: 23.803738317757","Indianapolis Intl, Avg. Delay: 23.771327612317","Hartsfield Jackson Atlanta Intl, Avg. Delay: 23.7252479657896","Denver Intl, Avg. Delay: 23.6511368391686","Syracuse Hancock Intl, Avg. Delay: 23.2325717633275","Port Columbus Intl, Avg. Delay: 22.8199037883343","Burlington Intl, Avg. Delay: 22.5752988047809","Cleveland Hopkins Intl, Avg. Delay: 22.5628129267183","Raleigh Durham Intl, Avg. Delay: 22.4512226512227","Buffalo Niagara Intl, Avg. Delay: 22.2969365426696","Philadelphia Intl, Avg. Delay: 21.9085009733939","Eagle Co Rgnl, Avg. Delay: 21.768115942029","Bob Hope, Avg. Delay: 21.6513513513514","Palm Beach Intl, Avg. Delay: 21.575304455064","Portland Intl, Avg. Delay: 21.2630402384501","William P Hobby, Avg. Delay: 21.2539606337014","Pittsburgh Intl, Avg. Delay: 21.2490895848507","Fort Lauderdale Hollywood Intl, Avg. Delay: 20.7659073716063","Louis Armstrong New Orleans Intl, Avg. Delay: 20.7658142664872","NA, Avg. Delay: 20.5551801801802","Minneapolis St Paul Intl, Avg. Delay: 20.3665752633858","Myrtle Beach Intl, Avg. Delay: 20.3620689655172","Tampa Intl, Avg. Delay: 19.4826792963464","Montrose Regional Airport, Avg. Delay: 19.4285714285714","Chicago Ohare Intl, Avg. Delay: 19.3094289508632","Ronald Reagan Washington Natl, Avg. Delay: 19.2055756777522","Gallatin Field, Avg. Delay: 19.0571428571429","Austin Bergstrom Intl, Avg. Delay: 19.0369141435089","Albuquerque International Sunport, Avg. Delay: 18.1220472440945","NA, Avg. Delay: 17.9720670391061","Detroit Metro Wayne Co, Avg. Delay: 17.1474919720961","Orlando Intl, Avg. Delay: 16.7199828166392","Charlotte Douglas Intl, Avg. Delay: 16.5567500365657","Metropolitan Oakland Intl, Avg. Delay: 16.3851132686084","Asheville Regional Airport, Avg. Delay: 16.1532567049808","San Francisco Intl, Avg. Delay: 15.4115994837926","George Bush Intercontinental, Avg. Delay: 15.012420606916","Yampa Valley, Avg. Delay: 14.4285714285714","San Diego Intl, Avg. Delay: 14.2565522332964","Norman Y Mineta San Jose Intl, Avg. Delay: 13.5518292682927","NW Arkansas Regional, Avg. Delay: 13.2661290322581","Phoenix Sky Harbor Intl, Avg. Delay: 12.4576639166305","NA, Avg. Delay: 12.3339684739304","General Edward Lawrence Logan Intl, Avg. Delay: 11.576421248835","Southwest Florida Intl, Avg. Delay: 11.4683038263849","Nantucket Mem, Avg. Delay: 11.2992424242424","Long Beach, Avg. Delay: 11.0937972768533","Ted Stevens Anchorage Intl, Avg. Delay: 10.375","Sarasota Bradenton Intl, Avg. Delay: 10.3555370524563","Key West Intl, Avg. Delay: 10","Los Angeles Intl, Avg. Delay: 9.89835267690004","Mc Carran Intl, Avg. Delay: 9.63272849462366","Seattle Tacoma Intl, Avg. Delay: 9.5009009009009","Salt Lake City Intl, Avg. Delay: 9.203182374541","Miami Intl, Avg. Delay: 9.16785991546623","Dallas Fort Worth Intl, Avg. Delay: 8.92596566523605","Honolulu Intl, Avg. Delay: 7.95007132667618","Martha\\\\'s Vineyard, Avg. Delay: 6.6047619047619","NA, Avg. Delay: 0.777992277992278","John Wayne Arpt Orange Co, Avg. Delay: -1.08743842364532","Palm Springs Intl, Avg. Delay: -15.6666666666667","Blue Grass, Avg. Delay: -31","La Guardia, Avg. Delay: NaN"],"locationmode":"USA-states","mode":"markers","marker":{"colorbar":{"title":"Average Delay"},"colorscale":[[0,"#440154"],[0.111111111111111,"#482878"],[0.222222222222222,"#3E4A89"],[0.333333333333333,"#31688E"],[0.444444444444444,"#26838E"],[0.555555555555556,"#1F9D89"],[0.666666666666667,"#35B779"],[0.777777777777778,"#6CCE59"],[0.888888888888889,"#B4DD2C"],[1,"#FDE725"]],"color":[75.5754716981132,68.5476190476191,59.8,55.5714285714286,52.4515570934256,45.8921933085502,45.1453154875717,43.7314578005115,43.7086330935252,40.5439429928741,38,37.8444976076555,37.5741758241758,35.8122317596567,35.0367088607595,34.889840881273,34.7664429530201,34.7480106100796,34.5052631578947,33.2136181575434,33.0435656836461,32.9409376153562,31.0139130434783,30.8913043478261,30.865671641791,30.8014184397163,30.7529258777633,30.2080057183703,28.6983695652174,28.3061366806137,28.2203583682806,27.9501748251748,27.7989821882952,27.7031558185404,27.6,27.3232169954476,27.1843575418994,26.9835828102366,26.8340248962656,26.1162514827995,25.2051467923161,24.7694174757282,23.803738317757,23.771327612317,23.7252479657896,23.6511368391686,23.2325717633275,22.8199037883343,22.5752988047809,22.5628129267183,22.4512226512227,22.2969365426696,21.9085009733939,21.768115942029,21.6513513513514,21.575304455064,21.2630402384501,21.2539606337014,21.2490895848507,20.7659073716063,20.7658142664872,20.5551801801802,20.3665752633858,20.3620689655172,19.4826792963464,19.4285714285714,19.3094289508632,19.2055756777522,19.0571428571429,19.0369141435089,18.1220472440945,17.9720670391061,17.1474919720961,16.7199828166392,16.5567500365657,16.3851132686084,16.1532567049808,15.4115994837926,15.012420606916,14.4285714285714,14.2565522332964,13.5518292682927,13.2661290322581,12.4576639166305,12.3339684739304,11.576421248835,11.4683038263849,11.2992424242424,11.0937972768533,10.375,10.3555370524563,10,9.89835267690004,9.63272849462366,9.5009009009009,9.203182374541,9.16785991546623,8.92596566523605,7.95007132667618,6.6047619047619,0.777992277992278,-1.08743842364532,-15.6666666666667,-31,null],"size":9,"opacity":0.7,"symbol":"circle"}}],"layout":{"title":"Delays of US airports, flying out of NYC","geo":{"scope":"usa","projection":{"type":"albers usa"},"showland":true,"landcolor":"rgb(242,242,242)","subunitcolor":"rgb(217,217,217)","countrycolor":"rgb(217,217,217)","countrywidth":1,"subunitwidth":0.5},"margin":{"b":40,"l":60,"t":25,"r":10}},"url":null,"width":null,"height":null,"base_url":"https://plot.ly","layout.1":{"title":"Delays of US airports, flying out of NYC","geo":{"scope":"usa","projection":{"type":"albers usa"},"showland":true,"landcolor":"rgb(242,242,242)","subunitcolor":"rgb(217,217,217)","countrycolor":"rgb(217,217,217)","countrywidth":1,"subunitwidth":0.5}},"filename":"Delays of US airports, flying out of NYC"},"evals":[]}</script><!--/html_preserve-->

#### Second Question now is:

* Is there a relationship between the age of a plane and its delays?

So for this we are using the year the plane is made as a proxy for age, ie: latest models are the youngest planes.
Answering this question now requires us to join the `planes` table with the flights table in a similar fashion as we did before:


{% highlight r %}
flights_planes <- mutate(flights, tot_delay = arr_delay + dep_delay)

flights_planes <- flights_planes %>% group_by(tailnum) %>% 
  summarise(avg_delay = mean(tot_delay, na.rm = T), num_of_flights = n() ) %>% 
  left_join(planes, by="tailnum") %>%
  arrange(desc(avg_delay))

head(flights_planes)
{% endhighlight %}



{% highlight text %}
## Source: local data frame [6 x 11]
## 
##   tailnum avg_delay num_of_flights  year                    type
##     (chr)     (dbl)          (int) (int)                   (chr)
## 1  N844MH       617              1  2002 Fixed wing multi engine
## 2  N911DA       562              1  1995 Fixed wing multi engine
## 3  N922EV       550              1  2003 Fixed wing multi engine
## 4  N587NW       536              1  2002 Fixed wing multi engine
## 5  N851NW       452              1  2004 Fixed wing multi engine
## 6  N654UA       412              1  1992 Fixed wing multi engine
## Variables not shown: manufacturer (chr), model (chr), engines (int), seats
##   (int), speed (int), engine (chr)
{% endhighlight %}



{% highlight r %}
#let's remove all the planes that haven't flown more than 100 times, and any missing values.

flights_planes2 <- filter(flights_planes, num_of_flights>=100, !is.na(avg_delay), !is.na(year))

g_planes <- ggplot()
g_planes + geom_jitter(data=flights_planes2, mapping = aes(x=year,y=avg_delay)) + geom_smooth(data=flights_planes2, mapping = aes(x=year, y=avg_delay), method = "lm") + xlab("Year") + ylab("Average Delay") + ggtitle("Year of Plane vs Average Delay") + geom_smooth(data=flights_planes2, mapping=aes(x=year,y=avg_delay), color="red", se=F)
{% endhighlight %}

![center](http://yankev.github.io/figs/relationalmap_plotly/unnamed-chunk-8-1.png)

From the looks of the plot, it doesn't really seem like there's a relationship. The average delay times are all fairly spread out for all the years with a lot of planes, there does seem to be a lot more variation in the early 2000s compared to the years following however. 

However I plotted the blue line, which represents a linear model (avg_delay ~ year), and it seems to signal a positive relationship between the two variables. We can further examine the model to see if this is valid.


{% highlight r %}
model <- lm(avg_delay~year,data=flights_planes2)
summary(model)
{% endhighlight %}



{% highlight text %}
## 
## Call:
## lm(formula = avg_delay ~ year, data = flights_planes2)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -29.065  -9.303  -1.536   7.916  42.411 
## 
## Coefficients:
##               Estimate Std. Error t value Pr(>|t|)  
## (Intercept) -318.72454  139.19931  -2.290   0.0222 *
## year           0.16929    0.06954   2.434   0.0151 *
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 12.73 on 1097 degrees of freedom
## Multiple R-squared:  0.005373,	Adjusted R-squared:  0.004466 
## F-statistic: 5.926 on 1 and 1097 DF,  p-value: 0.01508
{% endhighlight %}

We see that the p-value for the coefficient for year is actually significant, and is equal to `0.16929`, which is again quite negligile in practical terms. In addition, the r-squared of the model is: `summary(model)$r.squared` which indicates an extremely poor model, and thus it's evidence against a linear relationship between year of the plane and average delay. In addition we also tried a polynomial model(indicated in red), but that returned a poor r-squared as well. Thus I don't believe that there's a practical relationship between the age of the plane the delays they face, at least for the data that is present in the nycflights13 dataset. 

#### Conclusion

In this post we used `join functions` in the `dplyr` package in order to generate new data frames for our analysis. We were able to use this information to visualize delays by airports via a map of the USA, and we were able to answer the question of whether or not the age of the plane had an influence of the average delay time of the plane.



