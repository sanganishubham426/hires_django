# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'yash108.rejoice@gmail.com'
# EMAIL_HOST_PASSWORD = 'ogyizehsfblgswzp'
# EMAIL_PORT = 587

from decouple import config

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'yashpp5545@gmail.com'
# EMAIL_HOST_PASSWORD = 'jyixqsmsdrbgyvsv'
# EMAIL_PORT = 587

EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')