import json 
import requests
import itertools

# def page_generator(no_of_posts):
#     no_of_pages = no_of_posts//12 + 1
#     return no_of_pages

def generator(account_name):
    user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    headers = {'User-Agent':user_agent}
    json_data_list = []
    account_dict = {}
    post_count=0
    for page_number in range(7):
        json_data = requests.get('https://www.instagram.com/{}/?__a=1&page={}'.format(account_name, page_number), headers = headers)
        profileData = json.loads(json_data.text)
        json_data_list.append(profileData)

    pre_account_json = json_data_list[0]['graphql']['user']
    username = pre_account_json['username']
    account_no_of_followers = pre_account_json['edge_followed_by']['count']
    account_no_of_following = pre_account_json['edge_follow']['count']
    account_no_of_post = pre_account_json['edge_owner_to_timeline_media']['count']
    account_url = 'https://www.instagram.com/{}'.format(account_name)
    account_info = {
        'username': username,
        'no_of_followers' : account_no_of_followers,
        'no_of_following' : account_no_of_following,
        'no_of_post' : account_no_of_post,
        'account_url' : account_url,
    }


    for pre_data in json_data_list:
        pre_JsonData = pre_data['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for i in range(12):
            post_image_url = pre_JsonData[i]['node']['thumbnail_src']
            post_shortcode = pre_JsonData[i]['node']['shortcode']
            post_url = 'https://www.instagram.com/p/'+post_shortcode
            post_like_count = pre_JsonData[i]['node']['edge_liked_by']['count']
            post_comment_count = pre_JsonData[i]['node']['edge_media_to_comment']['count']
            account_dict[post_like_count] = {
                                        'post_url' : post_url ,
                                        'post_like':post_like_count,
                                        'post_comment':post_comment_count,
                                        'post_image_url': post_image_url,
                                        
                                        }
            post_count+= 1
            if post_count == 60:
                print('Reached {} posts.'.format(post_count))
                break
    print(account_dict)
    sorted_account_dict = dict(sorted(account_dict.items(), reverse=True))
    final_account = dict(itertools.islice(sorted_account_dict.items(), 20))
    return (account_info ,final_account)
