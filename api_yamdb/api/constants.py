URL_COMMENTS = r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'

URL_REVIEW = r'titles/(?P<title_id>\d+)/reviews'

ERROR_REVIEW_AUTHOR_UNIQUE = (
    'Нельзя оставлять несколько отзывов на одно произведение'
)