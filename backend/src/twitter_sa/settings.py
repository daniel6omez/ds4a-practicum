TRACK_WORDS = ['sttmed', '@sttmed', 'movilidadmedellin', 'movilidad medellin', 'movilidad medellín']
TABLE_NAME = "twitter_mta"
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at timestamp, text VARCHAR(255), \
            polarity INT, subjectivity INT, user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count INT, longitude double precision, latitude double precision, \
            retweet_count INT, favorite_count INT"
