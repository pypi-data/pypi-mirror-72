# -*- coding: utf-8 -*-
#!/usr/bin/python3

# urlcounter for Python 3
# by Chris Lindgren <chris.a.lindgren@gmail.com>
# Distributed under the BSD 3-clause license.
# See LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause for details.

# WHAT IS IT?
# A set of functions that tallies full URLs and their domain for periodic, event-defined social-media posting data.
# It assumes you seek an answer to the following questions about link-sharing and circulation:
    # 1. What are the top x full URLs and domain URLs from each group during each period?
    # 2. What are the top x full URLs and domain URLs from each group-module (detected community) in each period?

# It functions only with Python 3.x and is not backwards-compatible.

# Warning: urlcounter performs no custom error-handling, so make sure your inputs are formatted properly. If you have questions, please let me know via email.
import ast
from collections import Counter
import pandas as pd
import re

'''
    regex_lister: Transforms an incoming list of Strings into a regex string
        to facilitate a search.
    
    Arguments:
        -the_list: List. Array of Strings to write as a regex String.
        -key: String. Denotes the group name
    Returns:
        -keyed: Tuple with;
            - 'key' (String) that denotes the group name
            - 'listicle' (regex String) that will be used for a search
'''
def regex_lister(the_list, key):
    # Make group list into regex string
    listicle = ''
    l_len = 1
    if len(the_list) == 1:
        for i in the_list:
            listicle = listicle+'('+i+')'
    elif len(the_list) > 1:
        for i in the_list:
            if listicle == '':
                listicle = listicle+'('+i
                l_len = l_len+1
            elif l_len == len(the_list):
                listicle = listicle+'|'+i+')'
            else:
                listicle = listicle+'|'+i
                l_len = l_len+1
    # Return tuple with group name in first position
    keyed = (key,listicle)
    return keyed

'''
   url_counter: Transforms an incoming list of Strings into a regex string
        to facilitate a search.
    
    Arguments:
        -df: DataFrame. Array of Strings to write as a regex String.
        -columns: a List of 4 column names to use from corpus:
            0. Name of URL column that includes a list of URLs included in post/content.
            1. Integer. Number of times a post was shared, such as Retweets on Twitter.
    Returns:
        -A List that includes:
            - sorted_totals: List of Tuples that contain 2 items:
                - String full URL
                - Integer. Total number of URL instances (including RTs).
            - sorted_domain_totals:
                - String domain URL
                - Integer. Total number of URL instances (including RTs).
'''
def url_counter(df, columns):
    curls = df[columns]
    # Count and sort; append to this list
    cleaned_listed_data = []
    for h in curls.to_dict('records'):
        list_urls = h[columns[0]]
        if isinstance(list_urls, str):
            lu = ast.literal_eval(list_urls)
            if len(lu) > 0:
                # Go through list of urls
                for url in lu:
                    if url != None:
                        # Check for malformed URLs
                        # TODO: Could use some more checks here
                        if (url[0] == '/'):
                            print('=============')
                            print('Cleaning needed for', h[columns[3]]+'\'s', h[columns[0]])
                            print('Problem URL:', url)
                            print('=============')
                            continue
                        else:
                            # Based on shared count, append that amount
                            ranger = int(h[columns[1]])
                            for g in range(0, ranger):
                                cleaned_listed_data.append(url)
    
    # Count up domains
    domain_re = r"://[^.]{1,}\.[^\/]{1,}\/"
    simple_re = r":\/\/[^.]{1,}\..{1,}"
    broken_urls = r":\/\/[^.]{1,}\/"
    domain_list = []
    for domain in cleaned_listed_data:
        domain_match = [(m.start(0), m.end(0)) for m in re.finditer(domain_re, domain)]
        if len(domain_match) == 0:
            s_match = [(s.start(0), s.end(0)) for s in re.finditer(simple_re, domain)]
            broken_check = [(s.start(0), s.end(0)) for s in re.finditer(broken_urls, domain)]
            
            if len(broken_check) > 0:
                continue
            else:
                start = s_match[0][0]+3
                www_check = domain[start:(start+3)]
                end = s_match[0][1]
                if www_check == 'www':
                    domain_list.append(domain[(start+4):end])
                else:
                    domain_list.append(domain[start:end])
        
        else:
            start = domain_match[0][0]+3
            www_check = domain[start:(start+3)]
            end = domain_match[0][1]-1
            if www_check == 'www':
                domain_list.append(domain[(start+4):end])
            else:
                domain_list.append(domain[start:end])
    
    # Count up domains
    domain_totals = list(Counter(domain_list).items())
    sorted_domain_totals = sorted(domain_totals, key=lambda x: x[1], reverse=True) #descending
    
    # Count up URLs
    col_totals = list(Counter(cleaned_listed_data).items())
    sorted_totals = sorted(col_totals, key=lambda x: x[1], reverse=True) #descending
    return [sorted_totals, sorted_domain_totals]

'''
top_urls: Tallies up URLs in corpus.
    
    Arguments:
        -df= DataFrame. Corpus to query from.
        -columns= A List of 5 column names (String) to reference in DF corpus:
            0. Column with URLs (String) that includes a list of URLs included in post/content: 
                - Example: ['https://time.com','https://and-time-again.com']. The List can also be a String, '[]' since the function converts literals.
            1. Column with number of times a post was shared (Integer), such as Retweets on Twitter.
            2. Column with group data (String), such as hashtags from tweets.
            3. Column with usernames (String), such as tweet usernames
            4. Column with target content data (String), such as tweets with targeted users from module, 
                or stringified list of targeted people like tweet mentions.
        -url_sample_size= Integer. Desired sample limit.
        -periods= Tuple. Contains 2 Integers, which define the range of periods, e.g., (1,10)
        -hubs= Tuple. Contains 2 Integers, which define the range of module/hubs, e.g., (1,10)
        -period_dates= Dict of Lists with dates per period: pd['1'] => ['2018-01-01','2018-01-01',...] 
        -list_of_regex= List. Contains:
            1. list of regex patterns with group identifiers, such as hashtags
            2. String. Key identifier for group.
        -hl= Dict. Contains lists of community-detected usernames
        -verbose= Boolean. True prints out status messages (recommended), False prints nothing
    Returns:
        -Dict. See documentation for output details for data access.
'''
def top_urls(**kwargs):
    verboseprint = print if kwargs['verbose']==True else lambda *a, **k: None
    output = {}
    url_sample_size = kwargs['url_sample_size']
    group_col = kwargs['columns'][2]
    username_col = kwargs['columns'][3]
    content_col = kwargs['columns'][4]
    
    #1. LOOP THROUGH EACH GROUP
    for htg in kwargs['list_of_regex']:
        
        #2. LOOP THROUGH DESIRED PERIOD
        for p in range (kwargs['periods'][0], (kwargs['periods'][1]+1)):
            if str(p) not in output:
                output.update({ str(p): {} })
                
                #2a Retrieve all period tweets from df
                period_df = kwargs['df'][kwargs['df']['date'].isin(kwargs['period_dates'][str(p)])]
                
                #2b GROUP TOTALS FOR PERIOD 
                #2c Search periodic content with group regex string (htg[1])
                df_group = period_df[period_df[group_col].str.contains(htg[1], na=False)]
                c_url_counts_perperiod = url_counter(df_group, kwargs['columns'])
                verboseprint('\nPeriod',p,': ', htg ,':', len(c_url_counts_perperiod[0]))

                #2d Append per period to dict
                urlp = htg[0]+'_urls_per_period'
                urld = htg[0]+'_domains_per_period'
                output[str(p)].update( { urlp: c_url_counts_perperiod[0][:url_sample_size] } )
                output[str(p)].update( { urld: c_url_counts_perperiod[1][:url_sample_size] })
                output[str(p)].update( { htg[0]: {} })

                #3. LOOP THROUGH DESIRED GROUP MODULE/HUB FOR PERIOD
                for h in range(kwargs['hubs'][0], (kwargs['hubs'][1]+1)):
                    #3a If post targets hub user
                    if str(p) in kwargs['hl'][htg[0]]:
                        # Verify hub length greater than 0
                        if len(kwargs['hl'][htg[0]][str(p)][str(h)]) > 0:
                            #3b Create regex search string with every hub/module username
                            h_search_list = regex_lister(kwargs['hl'][htg[0]][str(p)][str(h)], htg[0])

                            #3c Search for tweets by module user
                            hut = period_df[period_df[username_col].str.contains(h_search_list[1], na=False)]
                            
                            #3d Xref hu for tweets that only mention module users
                            hm = hut[hut[content_col].str.contains(h_search_list[1], na=False)]

                            verboseprint('Period',p,'Hub',h,'Size:',len(kwargs['hl'][htg[0]][str(p)][str(h)]))
                            verboseprint('Period',p,'Hub',h,'# of Tweets:',len(hm))
                            
                            #3e Count up URLs from found content
                            h_url_counts_perperiod_perhub = url_counter(hm, kwargs['columns'])

                            verboseprint('Period',p,'Hub',h,'URLS:\n', h_url_counts_perperiod_perhub[0][:3])        
                            verboseprint('Period',p,'Hub',h,'DOMAINS:\n', h_url_counts_perperiod_perhub[1][:3])        
                            
                            #3f Assign to output Dict
                            output[str(p)][htg[0]].update({str(h):{}})
                            output[str(p)][htg[0]][str(h)].update({ 'hub_sample_size': len(kwargs['hl'][htg[0]][str(p)][str(h)]) })
                            output[str(p)][htg[0]][str(h)].update({ 'hub_tweet_sample_size': len(hm) })
                            output[str(p)][htg[0]][str(h)].update({ 'hub_url_counts': h_url_counts_perperiod_perhub[0][:url_sample_size] })
                            output[str(p)][htg[0]][str(h)].update({ 'hub_domain_counts': h_url_counts_perperiod_perhub[1][:url_sample_size] })
            else:
                #2a Retrieve all period tweets from df
                period_df = kwargs['df'][kwargs['df']['date'].isin(kwargs['period_dates'][str(p)])]

                #2b GROUP TOTALS FOR PERIOD 
                #2c Search periodic content with group regex string (htg[1])
                df_group = period_df[period_df[group_col].str.contains(htg[1], na=False)]
                c_url_counts_perperiod = url_counter(df_group, kwargs['columns'])
                verboseprint('\nPeriod',p,': ', htg ,':', len(c_url_counts_perperiod[0]))

                #2d Append per period to dict
                urlp = htg[0]+'_urls_per_period'
                urld = htg[0]+'_domains_per_period'
                output[str(p)].update( { urlp: c_url_counts_perperiod[0][:url_sample_size] } )
                output[str(p)].update( { urld: c_url_counts_perperiod[1][:url_sample_size] })
                output[str(p)].update( { htg[0]: {} })

                #3. Loop through period's hub_lists
                for h in range(kwargs['hubs'][0], (kwargs['hubs'][1]+1)):
                    #3a Find hub content for period 
                    if str(p) in kwargs['hl'][htg[0]]:
                        # Verify hub length greater than 0
                        if len(kwargs['hl'][htg[0]][str(p)][str(h)]) > 0:
                            #3b Create regex search string with every hub/module username
                            h_search_list = regex_lister(kwargs['hl'][htg[0]][str(p)][str(h)], htg[0])

                            #3c Search for tweets by module user
                            hut = period_df[period_df[username_col].str.contains(h_search_list[1], na=False)]
                            
                            #3d Xref hu for tweets that only mention module users
                            hm = hut[hut[content_col].str.contains(h_search_list[1], na=False)]

                            verboseprint('Period',p,'Hub',h,'Size:',len(kwargs['hl'][htg[0]][str(p)][str(h)]))
                            verboseprint('Period',p,'Hub',h,'# of Tweets:',len(hm))
                            
                            #3e Count up URLs from found content
                            h_url_counts_perperiod_perhub = url_counter(hm, kwargs['columns'])

                            verboseprint('Period',p,'Hub',h,'URLS:\n', h_url_counts_perperiod_perhub[0][:3])        
                            verboseprint('Period',p,'Hub',h,'DOMAINS:\n', h_url_counts_perperiod_perhub[1][:3])        
                            
                            #3f Assign to output Dict
                            output[str(p)][htg[0]].update({str(h):{}})
                            output[str(p)][htg[0]][str(h)].update({ 'hub_sample_size': len(kwargs['hl'][htg[0]][str(p)][str(h)]) })
                            output[str(p)][htg[0]][str(h)].update({ 'hub_tweet_sample_size': len(hm) })
                            output[str(p)][htg[0]][str(h)].update({ 'hub_url_counts': h_url_counts_perperiod_perhub[0][:url_sample_size] })
                            output[str(p)][htg[0]][str(h)].update({ 'hub_domain_counts': h_url_counts_perperiod_perhub[1][:url_sample_size] })
                        
    return output
