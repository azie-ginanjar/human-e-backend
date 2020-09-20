class EmailTypes:
    COUPON_EMAIL = "coupon_email"
    FOLLOWUP_EMAIL = "followup_email"
    WAIT_NEXT_COUPON_EMAIL = "wait_next_coupon_email"


class PromoCustomerStatuses:
    COUPON_SENT = "coupon_sent"
    WAIT_NEXT_COUPON = "wait_next_coupon"
    LINK_OPENED = "link_opened"
    FOLLOWED_UP = "followed_up"
    WAITLIST_SENT = "waitlist_sent"



INDONESIA_MARKETPLACE = "indonesia_mp"
PHILIPPINES_MARKETPLACE = "philippines_mp"

SUPPORTED_MARKETPLACES = [INDONESIA_MARKETPLACE, PHILIPPINES_MARKETPLACE]

LAZADA_PLATFORM = "lazada"
SHOPEE_PLATFORM = "shopee"


# Email related constants
class FollowupEmailDefaults:
    DEFAULT_EMAIL_SUBJECT = "How is your {{ campaign_product_name }}?"
    DEFAULT_EMAIL_HEADLINE = 'We Hope You Loved Our Product!'
    DEFAULT_EMAIL_BODY = """
        Hey there! Thanks so much for being a part of our {{ campaign_product_name }} promo campaign.
        We hope you are enjoying it! Could you please take 2 minutes and leave us a product review?
        Reviews really help our small family business, and other customers could really benefit by 
        learning from your experience. Click the button below to leave a review. Thank you for doing business with us. 
        We would not be able to provide these awesome products if it weren't for our customers :)
        All the best!
        """


class CouponEmailDefaults:
    DEFAULT_EMAIL_SUBJECT = 'Claim your coupon code'
    DEFAULT_EMAIL_HEADLINE = 'Hey {{ customer_first_name }},\nYou just requested a {{ campaign_percent_discount }}% coupon!'
    DEFAULT_EMAIL_BODY = """
    You just received a {{ campaign_percent_discount }}% coupon. Please click the button below to claim your offer. 
    Please claims in 24 hrs before link expired.
    """

class WaitlistEmailDefaults:
    DEFAULT_EMAIL_SUBJECT = 'Claim your coupon code'
    DEFAULT_EMAIL_HEADLINE = 'Hey {{ customer_first_name }},\nYour voucher for {{ campaign_product_name }} just available!'
    DEFAULT_EMAIL_BODY = """
        Please click the button below to claim your offer before no voucher left!!
        """

class DefaultUserSetting:
    DEFAULT_EMAIL_FROM = "Agilascout Coupon Mailer"
    DEFAULT_BLOCKED_EMAIL_DOMAINS = ['trash-mail.com']
    DEFAULT_ONE_PROMO_PER_EMAIL = True
    DEFAULT_ONE_PROMO_PER_IP = False

BASE_URL_TO_CLAIM_VOUCHER = 'https://www.agilascout.com/voucher_claim'
CAMPAIGN_EXPIRATION_MIN = 30
