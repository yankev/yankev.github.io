

    import json
    import requests
    from requests.auth import HTTPBasicAuth
    import pandas as pd

Let's now setup the authentication, so that the Plotly web api can identify us.


    username = 'your username'    #however in this example the account will be 'yankev'
    api_key = 'fill in with your own'
    
    auth = HTTPBasicAuth(username, api_key)
    headers = {'Plotly-Client-Platform': 'python'}
    page_size = 500

Perhaps now we would like to see a list of all the folders that are present in our Plotly repository. So below we've written a function that takes in an argument called `file` which takes either the value `plot` or `fold` in order to perform this task.


    def get_files(file):
        '''
        This function will the name, fid, and path of all the files in your
        plotly repository with the file type you choose
        -----
        Arguments
        file: the type of file we want to retrieve and takes on values ['plot','fold']
        
        Returns: A list of lists, containing the information required
        
        '''
        
        url = 'https://api.plot.ly/v2/folders/all?user='+username+'&filetype='+file+'&page_size='+str(page_size)
        response = requests.get(url, auth=auth, headers=headers)
        page = json.loads(response.content)
        temp = []
        for i in range(page['children']['count']):
            path = requests.get('https://api.plot.ly/v2/files/{}/path'.format(page['children']['results'][i]['fid']), auth=auth, headers=headers)
            #print('Filename: {}, fid: {}, path: {}'.format(page['children']['results'][i]['filename'],page['children']['results'][i]['fid'],str.split(path.content,":")[1][1:-2]))
            temp.append([page['children']['results'][i]['filename'],page['children']['results'][i]['fid'],str.split(path.content,":")[1][1:-2]])
        return temp 
    
    folders = get_files('fold')


We can now turn this information into a pandas data frame(just because). We write a function called `files2df` in order to do this, and the argument `data` will refer to the output of the `get_files` function call.


    def files2df(data):
        '''
        This function will turn your data into a dataframe
        -----
        Arguments
        data: Output of get_files call
        
        Returns: a data frame containing information in "data"
        '''
        return pd.DataFrame(data,columns=['name','fid','path'])
    
    files2df(folders)  # can also just call folders2df(get_folders())




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>fid</th>
      <th>path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>r-docs</td>
      <td>yankev:0</td>
      <td>/r-docs</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dashboard</td>
      <td>yankev:5</td>
      <td>/dashboard</td>
    </tr>
    <tr>
      <th>2</th>
      <td>r-test</td>
      <td>yankev:12</td>
      <td>/r-test</td>
    </tr>
  </tbody>
</table>
</div>



Now let's move our attention towards **plots**, which may be of more interest to you.
So below we will retrive a list of all the plots, and simultaneously turn them into a dataframe.


    plots_df = files2df(get_files('plot'))


    plots_df




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>fid</th>
      <th>path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>usamap</td>
      <td>yankev:1</td>
      <td>/r-docs/usamap</td>
    </tr>
    <tr>
      <th>1</th>
      <td>nycflights</td>
      <td>yankev:3</td>
      <td>/r-docs/nycflights</td>
    </tr>
    <tr>
      <th>2</th>
      <td>earnings</td>
      <td>yankev:6</td>
      <td>/dashboard/earnings</td>
    </tr>
    <tr>
      <th>3</th>
      <td>growth</td>
      <td>yankev:8</td>
      <td>/dashboard/growth</td>
    </tr>
    <tr>
      <th>4</th>
      <td>performance</td>
      <td>yankev:10</td>
      <td>/dashboard/performance</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SFzoo</td>
      <td>yankev:13</td>
      <td>/r-test/SFzoo</td>
    </tr>
    <tr>
      <th>6</th>
      <td>new_1</td>
      <td>yankev:19</td>
      <td>/dashboard/new_1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>LAzoo (1)</td>
      <td>yankev:21</td>
      <td>/r-test/LAzoo (1)</td>
    </tr>
    <tr>
      <th>8</th>
      <td>chart</td>
      <td>yankev:24</td>
      <td>/chart</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SFzoo (1)</td>
      <td>yankev:40</td>
      <td>/r-test/SFzoo (1)</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SFzoo (2)</td>
      <td>yankev:41</td>
      <td>/r-test/SFzoo (2)</td>
    </tr>
  </tbody>
</table>
</div>



So it appears that we might have some extra plots with the name SFzoo. So let's create a new folder in r-test called `backups`, and then move plots 13 and 40 into it assuming that 41 is the newest rendition.


    response = requests.post('https://api.plot.ly/v2/folders', data={"path": "/r-test/backups"}, headers=headers, auth=auth)
    response.raise_for_status()


    #Check for the new list of folders
    files2df(get_files('fold'))




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>fid</th>
      <th>path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>r-docs</td>
      <td>yankev:0</td>
      <td>/r-docs</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dashboard</td>
      <td>yankev:5</td>
      <td>/dashboard</td>
    </tr>
    <tr>
      <th>2</th>
      <td>r-test</td>
      <td>yankev:12</td>
      <td>/r-test</td>
    </tr>
    <tr>
      <th>3</th>
      <td>backups</td>
      <td>yankev:39</td>
      <td>/r-test/backups</td>
    </tr>
  </tbody>
</table>
</div>




    response = requests.patch('https://api.plot.ly/v2/files/yankev:13', data={"parent": 39}, auth=auth, headers=headers)
    response.raise_for_status()


    response = requests.patch('https://api.plot.ly/v2/files/yankev:40', data={"parent": 39}, auth=auth, headers=headers)
    response.raise_for_status




    <bound method Response.raise_for_status of <Response [200]>>




    files2df(get_files('plot'))




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>fid</th>
      <th>path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>usamap</td>
      <td>yankev:1</td>
      <td>/r-docs/usamap</td>
    </tr>
    <tr>
      <th>1</th>
      <td>nycflights</td>
      <td>yankev:3</td>
      <td>/r-docs/nycflights</td>
    </tr>
    <tr>
      <th>2</th>
      <td>earnings</td>
      <td>yankev:6</td>
      <td>/dashboard/earnings</td>
    </tr>
    <tr>
      <th>3</th>
      <td>growth</td>
      <td>yankev:8</td>
      <td>/dashboard/growth</td>
    </tr>
    <tr>
      <th>4</th>
      <td>performance</td>
      <td>yankev:10</td>
      <td>/dashboard/performance</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SFzoo</td>
      <td>yankev:13</td>
      <td>/r-test/backups/SFzoo</td>
    </tr>
    <tr>
      <th>6</th>
      <td>new_1</td>
      <td>yankev:19</td>
      <td>/dashboard/new_1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>LAzoo (1)</td>
      <td>yankev:21</td>
      <td>/r-test/LAzoo (1)</td>
    </tr>
    <tr>
      <th>8</th>
      <td>chart</td>
      <td>yankev:24</td>
      <td>/chart</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SFzoo (1)</td>
      <td>yankev:40</td>
      <td>/r-test/backups/SFzoo (1)</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SFzoo (2)</td>
      <td>yankev:41</td>
      <td>/r-test/SFzoo (2)</td>
    </tr>
  </tbody>
</table>
</div>



We see that we've successfully moved the two plots over to the newly created duplicates folder.

Assuming that we only need one backup copy of our plot, let's throw one of these into the trash (e.g 13), and rename 40 into SFzoo_duplicate. 


    response = requests.patch('https://api.plot.ly/v2/files/yankev:40', data={"filename": "SFzoo_duplicate"}, auth=auth, headers=headers)
    response




    <Response [200]>




    response = requests.post('https://api.plot.ly/v2/files/yankev:13/trash', auth=auth, headers=headers)
    response




    <Response [200]>



There we go, we've now used the REST API via Python in order to perform operations on files hosted on the Plotly servers.
