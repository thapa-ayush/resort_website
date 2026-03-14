"""
Currency conversion utilities for Diamond Hill Resort.

Provides automatic currency detection based on user location and conversion.
"""

import requests
from django.core.cache import cache
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Exchange rates (can be updated via API or manually)
EXCHANGE_RATES = {
    'NPR': Decimal('1.0'),
    'USD': Decimal('0.00756'),  # 1 NPR = 0.00756 USD (approx)
    'EUR': Decimal('0.00718'),  # 1 NPR = 0.00718 EUR (approx)
}

CURRENCY_SYMBOLS = {
    'NPR': 'Rs.',
    'USD': '$',
    'EUR': '€',
}

COUNTRY_TO_CURRENCY = {
    'NP': 'NPR',  # Nepal
    'US': 'USD',  # United States
    'GB': 'GBP',  # UK
    'DE': 'EUR',  # Germany
    'FR': 'EUR',  # France
    'IT': 'EUR',  # Italy
    'ES': 'EUR',  # Spain
    'NL': 'EUR',  # Netherlands
    'BE': 'EUR',  # Belgium
    'AT': 'EUR',  # Austria
    'CH': 'CHF',  # Switzerland
    'SE': 'EUR',  # Sweden
    'NO': 'EUR',  # Norway
    'DK': 'EUR',  # Denmark
    'FI': 'EUR',  # Finland
    'PL': 'EUR',  # Poland
    'CZ': 'EUR',  # Czech Republic
    'HU': 'EUR',  # Hungary
    'RO': 'EUR',  # Romania
    'UA': 'EUR',  # Ukraine
    'RU': 'EUR',  # Russia
    'IN': 'INR',  # India
    'BD': 'BDT',  # Bangladesh
    'PK': 'PKR',  # Pakistan
    'LK': 'LKR',  # Sri Lanka
    'CN': 'CNY',  # China
    'JP': 'JPY',  # Japan
    'TH': 'THB',  # Thailand
    'SG': 'SGD',  # Singapore
    'MY': 'MYR',  # Malaysia
    'PH': 'PHP',  # Philippines
    'ID': 'IDR',  # Indonesia
    'VN': 'VND',  # Vietnam
    'KR': 'KRW',  # South Korea
    'AU': 'AUD',  # Australia
    'NZ': 'NZD',  # New Zealand
    'CA': 'CAD',  # Canada
    'MX': 'MXN',  # Mexico
    'BR': 'BRL',  # Brazil
    'ZA': 'ZAR',  # South Africa
    'EG': 'EGP',  # Egypt
    'AE': 'AED',  # United Arab Emirates
    'SA': 'SAR',  # Saudi Arabia
    'IL': 'ILS',  # Israel
    'TW': 'TWD',  # Taiwan
}


def get_user_country(request):
    """
    Detect user's country from request.
    
    Uses IP geolocation API to determine country.
    Falls back to 'NP' (Nepal) if unable to detect.
    
    Args:
        request: Django request object
        
    Returns:
        str: Country code (e.g., 'US', 'NP', 'GB')
    """
    try:
        # Check cache first
        client_ip = get_client_ip(request)
        cache_key = f'country_{client_ip}'
        cached_country = cache.get(cache_key)
        if cached_country:
            return cached_country
        
        # Try to get country from IP geolocation
        try:
            response = requests.get(f'https://ipapi.co/{client_ip}/json/', timeout=2)
            if response.status_code == 200:
                country_code = response.json().get('country_code', 'NP')
                # Cache for 24 hours
                cache.set(cache_key, country_code, 60 * 60 * 24)
                return country_code
        except Exception as e:
            logger.warning(f"IP geolocation failed: {e}")
        
        return 'NP'  # Default to Nepal
    except Exception as e:
        logger.error(f"Error detecting country: {e}")
        return 'NP'


def get_client_ip(request):
    """
    Get client IP address from request.
    
    Args:
        request: Django request object
        
    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or '127.0.0.1'


def get_user_currency(request):
    """
    Get currency for user based on location.
    
    Args:
        request: Django request object
        
    Returns:
        str: Currency code (e.g., 'USD', 'NPR', 'EUR')
    """
    country = get_user_country(request)
    currency = COUNTRY_TO_CURRENCY.get(country, 'NPR')
    return currency


def convert_price(price_npr, from_currency='NPR', to_currency='USD'):
    """
    Convert price from one currency to another.
    
    Args:
        price_npr: Price in NPR (Decimal)
        from_currency: Source currency code (default: NPR)
        to_currency: Target currency code (default: USD)
        
    Returns:
        Decimal: Converted price
    """
    if from_currency == to_currency:
        return price_npr
    
    # If source is not NPR, convert to NPR first
    if from_currency != 'NPR':
        rate = EXCHANGE_RATES.get(from_currency, Decimal('1.0'))
        if rate > 0:
            price_npr = price_npr / rate
    
    # Convert from NPR to target currency
    rate = EXCHANGE_RATES.get(to_currency, Decimal('1.0'))
    return price_npr * rate


def format_price(price, currency='NPR'):
    """
    Format price with currency symbol.
    
    Args:
        price: Price amount (Decimal or float)
        currency: Currency code (default: NPR)
        
    Returns:
        str: Formatted price string (e.g., "Rs. 5,000" or "$50.00")
    """
    symbol = CURRENCY_SYMBOLS.get(currency, 'Rs.')
    
    # Format based on currency
    if currency in ['USD', 'EUR']:
        return f"{symbol} {price:,.2f}"
    else:
        return f"{symbol} {price:,.0f}"


def get_room_price_for_currency(room, currency='NPR'):
    """
    Get room price in specified currency.
    
    Args:
        room: Room model instance
        currency: Currency code
        
    Returns:
        Decimal: Price in specified currency
    """
    currency = currency.upper()
    
    if currency == 'USD':
        if room.price_usd and room.price_usd > 0:
            return room.price_usd
        return convert_price(room.price, 'NPR', 'USD')
    
    elif currency == 'EUR':
        if room.price_eur and room.price_eur > 0:
            return room.price_eur
        return convert_price(room.price, 'NPR', 'EUR')
    
    else:
        return room.price


def update_exchange_rates():
    """
    Update exchange rates from external API.
    Can be called periodically via management command or celery task.
    """
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/NPR', timeout=5)
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            
            if 'USD' in rates:
                EXCHANGE_RATES['USD'] = Decimal(str(rates['USD']))
            if 'EUR' in rates:
                EXCHANGE_RATES['EUR'] = Decimal(str(rates['EUR']))
            
            logger.info("Exchange rates updated successfully")
            return True
    except Exception as e:
        logger.error(f"Failed to update exchange rates: {e}")
    
    return False
