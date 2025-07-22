from urlextract import URLExtract # type: ignore
import re
from wordcloud import WordCloud # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
from collections import Counter # type: ignore
import emoji # type: ignore
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore
def fetch_stats(df, selected_user):
    """
    Fetch statistics for the selected user from the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame containing chat data.
        selected_user (str): The name of the user to fetch statistics for.
        
    Returns:
        tuple: A tuple containing total messages, total words, total media, total links, and total emojis.
    """
    # if selected_user == 'Overall':
    #     num_messages = df.shape[0]
    #     # num_words = df['messages'].str.split().apply(len).sum()
    #     num_words = []
    #     for messages in df['messages']:
    #         num_words.extend(messages.split())
    #     return num_messages, len(num_words)
    # else:
    #     new_df = df[df['users'] == selected_user]
    #     num_messages = new_df.shape[0]  
    #     num_words = []
    #     for messages in new_df['messages']:
    #         num_words.extend(messages.split())
    #     return num_messages, len(num_words)
        
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    num_message = df.shape[0]
    num_words = []
    for message in df['messages']:
        num_words.extend(message.split())

    # count total media messages
    num_media = df[df['messages'] == '<Media omitted>'].shape[0]

    # count total links
    #num_links = df[df['messages'].str.contains('http')].shape[0]
    links = []
    extractor = URLExtract()
    for link in df['messages']:
        links.extend(extractor.find_urls(link))
    num_links = len(links)

    # emoji count
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    return num_message, len(num_words), num_media, num_links, len(emojis)

# most busiest users

def most_busy_users(df):
    X = df['users'].value_counts().head()
    return X

f = open('stop_hinglish.txt', 'r')
stop_words = f.read()
# generaet wordcloud
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    temp = df[df['messages'] != '<Media omitted>']
    def remove_stopwords(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return ' '.join(words)
    wc = WordCloud(width=800, height=400, background_color='white', colormap='Set2')
    temp['messages'].apply(remove_stopwords)
    df_wc = wc.generate(temp['messages'].str.cat(sep=' '))
    return df_wc

# most common words
def fetch_most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    temp = df[df['messages'] != '<Media omitted>']
    words = []
    
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0: 'Common Words', 1: 'Word Frequency'})
    
    if len(most_common_words_df) > 0:
        return most_common_words_df
    else:
        return "Nice Guy, No common words found for the selected user."

    
def fetch_most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']== selected_user]
    
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20)).rename(columns={0:'Emojis', 1:'Emoji Frequency'})

    return emoji_df

# analyse the sentiment of the messages
def sentiment_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    sentiments = SentimentIntensityAnalyzer()
    df['positive'] = [sentiments.polarity_scores(i)['pos'] for i in df['messages']]
    df['negative'] = [sentiments.polarity_scores(i)['neg'] for i in df['messages']]
    df['neutral'] = [sentiments.polarity_scores(i)['neu'] for i in df['messages']]
    pos_sent = round(sum(df['positive']))
    neg_sent = round(sum(df['negative']))
    neu_sent = round(sum(df['neutral']))
    return pos_sent, neg_sent, neu_sent
