---
layout: post
title:  "Intro to Dplyr on nycflights13"
date:   2016-01-11 8:30:55 -0500
---

### Introduction
In this entry I'm going to work through a sequence of analysis that will cover some of the main operations in dplyr. Dplyr is a tool in R that will frame our data into a data-structure called a dataframe(different than the standard on in R). It will allow us to query the dataframe similar to what is possible in SQL.
  
> The main operations in dplyr are:  
>
> 1. Select
2. Filter
3. Arrange
4. Mutate
5. Summarise


#### Let's begin
We're going to be looking at the nycflights13 dataset, which contains records of all the flights departing from NYC airports in 2013. 
Let's take a look at the data:



{% highlight r %}
library(nycflights13)
head(flights)
{% endhighlight %}



{% highlight text %}
## Source: local data frame [6 x 16]
## 
##    year month   day dep_time dep_delay arr_time arr_delay carrier tailnum
##   (int) (int) (int)    (int)     (dbl)    (int)     (dbl)   (chr)   (chr)
## 1  2013     1     1      517         2      830        11      UA  N14228
## 2  2013     1     1      533         4      850        20      UA  N24211
## 3  2013     1     1      542         2      923        33      AA  N619AA
## 4  2013     1     1      544        -1     1004       -18      B6  N804JB
## 5  2013     1     1      554        -6      812       -25      DL  N668DN
## 6  2013     1     1      554        -4      740        12      UA  N39463
## Variables not shown: flight (int), origin (chr), dest (chr), air_time
##   (dbl), distance (dbl), hour (dbl), minute (dbl)
{% endhighlight %}
  
To get started with the `select` function, let's figure out a few ways select dep_time, dep_delay, arr_time, and arr_delay from flights.


{% highlight r %}
#because they are side by side, we can do the following
select(flights, 4:7)
#if they weren't,  we could create a list:
select(flights, c(4,5,6,7))
#we can also list them out individually
select(flights, dep_time,dep_delay,arr_time,arr_delay)
#or using starts_with/ends_with
select(flights, starts_with("dep"),starts_with("arr"))
#or
select(flights, ends_with("delay"),ends_with("time"))
{% endhighlight %}

Let's now try `mutate`. We can use this function in order to create new variables in our data frame.
Perhaps we can create a variable that will give us the total delay of the flights.


{% highlight r %}
temp <- mutate(flights, total_delay= dep_delay + arr_delay) 
select(temp, ends_with("delay"))
{% endhighlight %}



{% highlight text %}
## Source: local data frame [336,776 x 3]
## 
##    dep_delay arr_delay total_delay
##        (dbl)     (dbl)       (dbl)
## 1          2        11          13
## 2          4        20          24
## 3          2        33          35
## 4         -1       -18         -19
## 5         -6       -25         -31
## 6         -4        12           8
## 7         -5        19          14
## 8         -3       -14         -17
## 9         -3        -8         -11
## 10        -2         8           6
## ..       ...       ...         ...
{% endhighlight %}


{% highlight r %}
g<-ggplot(data=temp)
g + geom_bar(map=aes(x=total_delay), fill="maroon") + xlim(-100,1000) + labs(title="A look at the distribution of delays")
{% endhighlight %}



{% highlight text %}
## Warning: Removed 9482 rows containing non-finite values (stat_count).
{% endhighlight %}

![center](http://yankev.github.io/figs/dplyr_flights/unnamed-chunk-4-1.png)

What we see is a right-skewed distribution. We can confirm this because the **mean** is: `19.4505325` which is larger than the **median**: `-6`, which indicates a right-skewed distribution.

Perhaps now we can look at all the flights with reasonable arrival and departing delays (e.g. let's assume that 2 hrs is reasonable). We will do this by using the `filter` function supplied with dplyr. 


{% highlight r %}
ok_flights <- temp %>% filter(arr_delay<=2, dep_delay<=2)
{% endhighlight %}

Moreover, you may have notice we used something new (`%>%`). This symbol tells us that we are using what's on the left of it as the first parameter for the expression on the right, and is thus equivalent to:

{% highlight r %}
ok_flights <- filter(temp, arr_delay<=2, dep_delay<=2)
{% endhighlight %}

Now an interesting question we could ask is: `Which airlines on average have the most delays?`.


{% highlight r %}
ok_flights %>%
group_by(carrier) %>%
summarise(avg_tot_delay = mean(total_delay, na.rm=TRUE)) %>%
arrange(desc(avg_tot_delay))
{% endhighlight %}



{% highlight text %}
## Source: local data frame [16 x 2]
## 
##    carrier avg_tot_delay
##      (chr)         (dbl)
## 1       FL     -15.52893
## 2       WN     -17.51483
## 3       F9     -18.04911
## 4       MQ     -18.32812
## 5       B6     -18.65148
## 6       US     -18.81534
## 7       EV     -19.07062
## 8       DL     -21.07224
## 9       UA     -21.18221
## 10      OO     -21.94444
## 11      YV     -22.96654
## 12      AA     -23.31697
## 13      VX     -23.74205
## 14      9E     -24.38127
## 15      HA     -27.57265
## 16      AS     -32.29764
{% endhighlight %}

In this example we made use of multiple pipes. Moreover, we introduced the `group_by()` function, which was used to the dataframe into subsets based on the carrier. We then looked at the average total delay for all the flights for each different airline using the `summarise()` function. Lastly, we used the `arrange()` function in order to look at the flights with the most delays, and to our surprise, they happen to be negative. 

#### In closing

We took a brief look at the operations included in the dplyr package, and how simple it was for us to do some initial exploratory analysis on the data set. 

