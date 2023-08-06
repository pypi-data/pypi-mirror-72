"""User class.

User class created from firestore website clickstream data.

Created: 2020-03-0? (Merijn)
Updated: 2020-06-29 (Merijn, DAT-1583)
"""

# TODO: add ppcVisitorAcco, which is a funnel event.
# TODO: date in SearchPageSearchQuery can still be '2019-09-02|±2', split this in two variables.


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
import dataclasses
import json
import re
import operator

import google.auth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import vaknl_user.Event as EventDataclass
from datetime import datetime, timedelta
import json
import requests


# ----------------------------------------------------------------------------------------------------------------------
# User defined functions
# ----------------------------------------------------------------------------------------------------------------------
def _create_firestore_client(project_id: str):
    """Sets up Firestore client."""
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {'projectId': project_id})
    return firestore.client()


def safe_list_get(lst: list, idx: int, default=None):
    """Safely get element with given index from list. A default value is returned when exceptions are raised."""
    if isinstance(lst, list):
        try:
            return lst[idx]
        except IndexError:
            return default
    else:
        return default


# ----------------------------------------------------------------------------------------------------------------------
# Default input variables
# ----------------------------------------------------------------------------------------------------------------------
_, _project_id = google.auth.default()
_firestore_collection_source = u'in_website_clickstream'
_firestore_collection_destination = u'dmp_users'
_firestore_client = _create_firestore_client(_project_id)


# ----------------------------------------------------------------------------------------------------------------------
# User class
# ----------------------------------------------------------------------------------------------------------------------
class User(object):
    """User class where user object is identified by dmp_user_id user."""

    def __init__(self, dmp_user_id):
        self.dmp_user_id = dmp_user_id
        self.events = []
        self.statistics = {
            'acco_city_freq': dict(),
            'acco_city_list': list(),
            'acco_city_mode': None,
            'acco_country_freq': dict(),
            'acco_country_list': list(),
            'acco_country_mode': None,
            'acco_region_freq': dict(),
            'acco_region_list': list(),
            'acco_region_mode': None,
            'acco_city_code_freq': dict(),
            'acco_city_code_list': list(),
            'acco_city_code_mode': None,
            'acco_country_code_freq': dict(),
            'acco_country_code_list': list(),
            'acco_country_code_mode': None,
            'acco_region_code_freq': dict(),
            'acco_region_code_list': list(),
            'acco_region_code_mode': None,
            'acco_theme_freq': dict(),
            'acco_theme_list': list(),
            'acco_theme_mode': None,
            'activity_first': None,
            'activity_last': None,
            'booked_acco_freq': dict(),
            'booked_acco_last': None,
            'booked_cnt': 0,
            'dmp_session_ids': list(),
            'event_cnt': 0,
            'funnel_step': 'visitor',
            'image_click_cnt': 0,
            'pageview_cnt': 0,
            'party_composition': dict(),
            'price_click_cnt': 0,
            'productpage_freq': dict(),
            'productpage_last': None,
            'productpage_list': list(),
            'productpage_mode': None,
            'search_departure_airport_freq': dict(),
            'search_departure_airport_list': list(),
            'search_departure_airport_mode': None,
            'search_departure_date_freq': dict(),
            'search_departure_date_last': None,
            'search_departure_date_list': list(),
            'search_departure_date_mode': None,
            'search_country_freq': dict(),
            'search_country_list': list(),
            'search_country_mode': None,
            'search_page_filter_selection_cnt': 0,
            'search_party_composition_freq': dict(),
            'search_region_freq': dict(),
            'search_region_list': list(),
            'search_region_mode': None,
            'search_theme_freq': dict(),
            'search_theme_list': list(),
            'search_theme_mode': None,
            'session_cnt': 0,
            'session_day_of_week_freq': dict(),
            'session_day_of_week_list': list(),
            'session_day_of_week_mode': None,
            'session_hour_freq': dict(),
            'session_hour_list': list(),
            'session_hour_mode': None,
            'user_identifiers': dict(),
        }

    @staticmethod
    def create_event(clickstream_event_json):
        """Assigns event to a (event-)dataclass based on event clickstream json.
        Args:
            clickstream_event_json: str, clickstream event json string
        Return:
            dataclass, event dataclass.
        """
        event_value_type = clickstream_event_json.get('eventValueType')
        event_trigger = clickstream_event_json.get('info', {}).get('eventTrigger')
        standard_event_arguments = {
            'event_id': clickstream_event_json.get('eventId'),
            'timestamp': clickstream_event_json.get('timestamp'),
            'dmp_session_id': clickstream_event_json.get('info', {}).get('dmpSessionId')
        }
        if event_value_type == 'undefined':
            pass
        else:
            event_value_json = json.loads(clickstream_event_json.get('eventValueJson'))
            if event_value_type == 'session':
                event = EventDataclass.Session(
                    ip=clickstream_event_json.get('remoteIp'),
                    time_zone=clickstream_event_json.get('timeZone'),
                    continent=clickstream_event_json.get('continent'),
                    country=clickstream_event_json.get('country'),
                    region=clickstream_event_json.get('mostSpecificSubdivision'),
                    device=event_value_json.get(event_value_type, {}).get('userAgent', {}).get('uaDeviceType'),
                    **standard_event_arguments
                )
            elif event_value_type == 'pageview':
                page_type = event_value_json.get(event_value_type, {}).get('pageType')
                if page_type == 'homePage':
                    event = EventDataclass.PageviewHomePage(
                        **standard_event_arguments
                    )
                elif page_type == 'productPage':
                    event = EventDataclass.PageviewProductPage(
                        giataid=safe_list_get(
                            re.findall(r"hotelId=(\d+)", event_value_json[event_value_type].get('url')),
                            idx=0
                        ),
                        **standard_event_arguments
                    )
                elif page_type in ('brandedSearchPage', 'Search', 'nonBrandedSearchPage', 'Branded Search'):
                    event = EventDataclass.PageviewSearch(
                        **standard_event_arguments
                    )
                elif page_type == 'bookingForm':
                    event = EventDataclass.PageviewBookingStep(
                        **standard_event_arguments
                    )
                elif page_type == 'dealPage':
                    event = EventDataclass.PageviewDealPage(
                        **standard_event_arguments
                    )
                elif page_type == 'searchAssistantPage':
                    event = EventDataclass.PageviewKeuzehulp(
                        **standard_event_arguments
                    )
                elif page_type == 'content':
                    event = EventDataclass.PageviewContent(
                        **standard_event_arguments
                    )
                elif page_type == 'newsPage':
                    event = EventDataclass.PageviewBlog(
                        **standard_event_arguments
                    )
                elif page_type in ('errorPage', '404Page'):
                    event = EventDataclass.PageviewError(
                        **standard_event_arguments
                    )
                else:
                    event = EventDataclass.PageviewOther(
                        **standard_event_arguments
                    )
            elif event_value_type == 'reservation':
                reservation_status = event_value_json.get(event_value_type, {}).get('reservationStatus')
                giataid = event_value_json['reservation']['packages'][0]['productCode']
                if event_trigger == 'ibe-extras':
                    event = EventDataclass.ReservationExtras(
                        giataid=giataid,
                        **standard_event_arguments
                    )
                elif event_trigger == 'ibe-personaldata':
                    event = EventDataclass.ReservationPersonalData(
                        giataid=giataid,
                        **standard_event_arguments
                    )
                elif event_trigger == 'ibe-overview-payment':
                    event = EventDataclass.ReservationOverview(
                        giataid=giataid,
                        **standard_event_arguments
                    )
                elif event_trigger == 'ibe-confirmation' and reservation_status == 'Booked':
                    event = EventDataclass.ReservationBooked(
                        giataid=giataid,
                        reservation_id=event_value_json.get(event_value_type, {}).get('reservationId'),
                        **standard_event_arguments
                    )
                else:
                    event = EventDataclass.ReservationOther(
                        reservation_status=reservation_status,
                        giataid=giataid,
                        **standard_event_arguments
                    )
            elif event_value_type == 'priceClick':
                event = EventDataclass.PriceClick(
                    giataid=event_value_json.get('packagePrice', {}).get('productCode'),
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'imgClick':
                event = EventDataclass.ImageClick(
                    giataid=event_value_json.get('value'),
                    **standard_event_arguments
                )
            elif event_value_type == 'search' and event_trigger == 'search':
                filters = event_value_json.get(event_value_type, {}).get('filters')
                departure_date = \
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == "departure"),
                         [None])[0]
                geo = next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == "geo"), None)
                theme = \
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'theme'),
                         None)[0]
                departure_airports = next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == "airports"), None)
                distance_to_beach = \
                    next((list(item['filterValues'].keys()) for item in filters if
                          item['filterName'] == 'distanceToBeach'),
                         [0])[0]
                if distance_to_beach == '0':
                    distance_to_beach = None
                elif distance_to_beach == 'on-beach':
                    distance_to_beach = 0
                else:
                    distance_to_beach = int(distance_to_beach)
                mealplans = next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == "mealplans"), None)
                hotel_ratings = int(next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'hotelRatings'),
                    [-1])[0])
                star_rating = int(
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'rating'),
                         [0])[0])
                budget = int(
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'budget'),
                         [0])[0])
                party_composition = next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'partyComposition'),
                    [None])[0]
                event = EventDataclass.SearchPageSearchQuery(
                    departure_date=departure_date,
                    geo=geo,
                    theme=theme if theme != '0' else None,
                    departure_airports=departure_airports,
                    distance_to_beach=distance_to_beach if distance_to_beach != 0 else None,
                    mealplans=mealplans,
                    hotel_ratings=hotel_ratings if hotel_ratings != -1 else None,
                    star_rating=star_rating if star_rating != 0 else None,
                    budget=budget if budget != 0 else None,
                    party_composition=party_composition,
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'selectFilter':
                event = EventDataclass.SearchPageFilter(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterDepartureDate':
                event = EventDataclass.ProductPageFilterDepDate(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterAirport':
                event = EventDataclass.ProductPageFilterAirport(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterMealplan':
                event = EventDataclass.ProductPageFilterMealPlan(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'selectFlightFilter':
                event = EventDataclass.ProductPageFilterFlight(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterDurationRange':
                event = EventDataclass.ProductPageFilterDurationRange(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'partyCompositionFilter':
                event = EventDataclass.GlobalFilterPartyComposition(
                    label=clickstream_event_json.get('label'),
                    **standard_event_arguments
                )
            elif event_value_type == 'packageAvailability':
                event = EventDataclass.ProductAvailability(
                    **standard_event_arguments
                )
            elif event_value_type == 'productService':
                event = EventDataclass.ProductService(
                    giataid=event_value_json.get('package', {}).get('productCode'),
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger in \
                    ('changeTransfer', 'changeInsurance', 'changeLuggage'):
                event = EventDataclass.SelectExtrasBookingStep(
                    type=re.findall(r"change(.+)", event_trigger.lower())[0],
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'showTop10':
                event = EventDataclass.KeuzehulpShowTop10(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'sfmcId':
                event = EventDataclass.SfmcId(
                    email=event_value_json.get('value', {}).get('email'),
                    **standard_event_arguments
                )
            else:
                event = EventDataclass.EventOther(
                    event_value_type=event_value_type,
                    event_trigger=event_trigger,
                    **standard_event_arguments
                )

            return event

    @staticmethod
    def update_funnel_step(statistics, event):
        """Updates the funnel step the user is in.
        For speed: only trigger if event.funnel_event == True.
        Args:
            statistics: dict, user statistics dictionary.
            event: dataclass, clickstream event.
        Return:
            str, name of funnel step the user is in.
        """
        funnel_step = statistics['funnel_step']
        if isinstance(event, EventDataclass.ReservationBooked):
            funnel_step = 'booked'
        elif funnel_step != 'in_market':
            if isinstance(event, (EventDataclass.ReservationPersonalData, EventDataclass.ReservationOverview,
                                  EventDataclass.SelectExtrasBookingStep)):
                funnel_step = 'in_market'
            elif funnel_step != 'active_plus':
                if (
                        isinstance(event, (EventDataclass.ProductService, EventDataclass.ProductPageFilterFlight,
                                           EventDataclass.ProductPageFilterAirport,
                                           EventDataclass.ProductPageFilterMealPlan,
                                           EventDataclass.ProductAvailability, EventDataclass.ReservationExtras)) or
                        len(statistics['productpage_freq'].keys()) >= 5
                ):
                    funnel_step = 'active_plus'
                elif funnel_step != 'active':
                    if (
                            (isinstance(event, EventDataclass.SearchPageSearchQuery) and event.departure_date) or
                            isinstance(event, (
                                    EventDataclass.ProductPageFilterDepDate,
                                    EventDataclass.GlobalFilterPartyComposition,
                                    EventDataclass.KeuzehulpShowTop10, EventDataclass.PriceClick)) or
                            statistics['image_click_cnt'] >= 3 or
                            statistics['search_page_filter_selection_cnt'] >= 2
                            # OR landing from ppc campaign on product page
                    ):
                        funnel_step = 'active'
        return funnel_step

    def update_statistics(self, event):
        """Update user statistics with event.
        Args:
            event: dataclass, clickstream event.
        """
        date_time = datetime.fromtimestamp(event.timestamp / 1e3)

        if self.statistics['event_cnt'] == 0:
            self.statistics['activity_first'] = event.timestamp
            self.statistics['activity_last'] = event.timestamp
        else:
            self.statistics['activity_first'] = min(self.statistics['activity_first'], event.timestamp)
            self.statistics['activity_last'] = max(self.statistics['activity_last'], event.timestamp)
        self.statistics['event_cnt'] += 1

        if isinstance(event, EventDataclass.Pageview):
            self.statistics['pageview_cnt'] += 1
            if isinstance(event, EventDataclass.PageviewProductPage):
                giataid = event.giataid
                if giataid:
                    giataid_counter = self.statistics['productpage_freq']
                    giataid_counter[giataid] = giataid_counter[giataid] + 1 if giataid in giataid_counter else 1
                    self.statistics['productpage_freq'] = giataid_counter
                    self.statistics['productpage_last'] = giataid
                    self.statistics['productpage_mode'] = max(giataid_counter, key=giataid_counter.get)
                    self.statistics['productpage_list'] = sorted(
                        giataid_counter,
                        key=giataid_counter.get,
                        reverse=True
                    )

                # TODO: NBC API part needs to be revised.
                # # Data from NBC content
                # if giataid:
                #     nbc = "https://nbc-dot-vaknl-website-dev.appspot.com/api/v1/accommodations/" + giataid
                #     api_call_response = requests.get(nbc)
                #     if api_call_response.status_code == 200:
                #         json_data = api_call_response.json()
                #         accommodation = json_data.get('accommodation', {})
                #         country_code = accommodation.get('country_code')
                #         country_code = "g" + country_code
                #         country_code_counter = self.statistics['acco_country_code_freq']
                #         country_code_counter[country_code] = country_code_counter[country_code] + 1 \
                #             if country_code in country_code_counter else 1
                #         self.statistics['acco_country_code_freq'] = country_code_counter
                #         self.statistics['acco_country_code_mode'] = max(
                #             country_code_counter,
                #             key=country_code_counter.get
                #         )
                #         self.statistics['acco_country_code_list'] = sorted(
                #             country_code_counter,
                #             key=country_code_counter.get,
                #             reverse=True
                #         )
                #         region_code = accommodation.get('region_id')
                #         region_code = country_code + "+r" + str(region_code)
                #         region_code_counter = self.statistics['acco_region_code_freq']
                #         region_code_counter[region_code] = region_code_counter[region_code] + 1 \
                #             if region_code in region_code_counter else 1
                #         self.statistics['acco_region_code_freq'] = region_code_counter
                #         self.statistics['acco_region_code_mode'] = max(
                #             region_code_counter,
                #             key=region_code_counter.get
                #         )
                #         self.statistics['acco_region_code_list'] = sorted(
                #             region_code_counter,
                #             key=region_code_counter.get,
                #             reverse=True
                #         )
                #         city_code = accommodation.get('city_id')
                #         city_code = region_code + "+c" + str(city_code)
                #         city_code_counter = self.statistics['acco_city_code_freq']
                #         city_code_counter[city_code] = city_code_counter[city_code] + 1 \
                #             if city_code in city_code_counter else 1
                #         self.statistics['acco_city_code_freq'] = city_code_counter
                #         self.statistics['acco_city_code_mode'] = max(city_code_counter, key=city_code_counter.get)
                #         self.statistics['acco_city_code_list'] = sorted(
                #             city_code_counter,
                #             key=city_code_counter.get,
                #             reverse=True
                #         )
                #         country = accommodation.get('country')
                #         country_counter = self.statistics['acco_country_freq']
                #         country_counter[country] = country_counter[country] + 1 if country in country_counter else 1
                #         self.statistics['acco_country_freq'] = country_counter
                #         self.statistics['acco_country_mode'] = max(
                #             country_counter,
                #             key=country_counter.get
                #         )
                #         self.statistics['acco_country_list'] = sorted(
                #             country_counter,
                #             key=country_counter.get,
                #             reverse=True
                #         )
                #         region = accommodation.get('region')
                #         region_counter = self.statistics['acco_region_freq']
                #         region_counter[region] = region_counter[region] + 1 if region in region_counter else 1
                #         self.statistics['acco_region_freq'] = region_counter
                #         self.statistics['acco_region_mode'] = max(
                #             region_counter,
                #             key=region_counter.get
                #         )
                #         self.statistics['acco_region_list'] = sorted(
                #             region_counter,
                #             key=region_counter.get,
                #             reverse=True
                #         )
                #         city = accommodation.get('city')
                #         city_counter = self.statistics['acco_city_freq']
                #         city_counter[city] = city_counter[city] + 1 if city in city_counter else 1
                #         self.statistics['acco_city_freq'] = city_counter
                #         self.statistics['acco_city_mode'] = max(city_counter, key=city_counter.get)
                #         self.statistics['acco_city_list'] = sorted(
                #             city_counter,
                #             key=city_counter.get,
                #             reverse=True
                #         )
                #
                #         theme_counter = self.statistics['acco_theme_freq']
                #         themes_to_add = [key for key, value in accommodation.items() if 'theme_' in key and value]
                #         for theme in themes_to_add:
                #             theme_counter[theme] = theme_counter[theme] + 1 if theme in theme_counter else 1
                #         self.statistics['acco_theme_freq'] = theme_counter
                #         self.statistics['acco_theme_mode'] = max(theme_counter, key=theme_counter.get)
                #         self.statistics['acco_theme_list'] = sorted(
                #             theme_counter,
                #             key=theme_counter.get,
                #             reverse=True
                #         )

        elif isinstance(event, EventDataclass.PriceClick):
            self.statistics['price_click_cnt'] += 1

        elif isinstance(event, EventDataclass.ImageClick):
            self.statistics['image_click_cnt'] += 1

        elif isinstance(event, EventDataclass.ReservationBooked):
            giataid = event.giataid
            self.statistics['booked_acco_last'] = giataid
            self.statistics['booked_cnt'] += 1
            booked_acco_counter = self.statistics['booked_acco_freq']
            booked_acco_counter[giataid] = booked_acco_counter[giataid] + 1 if giataid in booked_acco_counter else 1
            self.statistics['booked_acco_freq'] = booked_acco_counter

        elif isinstance(event, EventDataclass.SearchPageFilter):
            self.statistics['search_page_filter_selection_cnt'] += 1

        elif isinstance(event, EventDataclass.SearchPageSearchQuery):
            # Search on departure airport
            airports = event.departure_airports
            if airports:
                dep_air_counter = self.statistics['search_departure_airport_freq']
                for airport in airports:
                    if airport in dep_air_counter:
                        dep_air_counter[airport] += 1
                    else:
                        dep_air_counter[airport] = 1
                    dep_air_counter[airport] = dep_air_counter[airport] + 1 if airport in dep_air_counter else 1
                self.statistics['search_departure_airport_freq'] = dep_air_counter
                self.statistics['search_departure_airport_mode'] = max(dep_air_counter, key=dep_air_counter.get)
                self.statistics['search_departure_airport_list'] = sorted(
                    dep_air_counter,
                    key=dep_air_counter.get,
                    reverse=True
                )
            search_theme = event.theme
            if search_theme:
                search_theme_counter = self.statistics['search_theme_freq']
                search_theme_counter[search_theme] = search_theme_counter[search_theme] + 1 \
                    if search_theme in search_theme_counter else 1
                self.statistics['search_theme_freq'] = search_theme_counter
                self.statistics['search_theme_mode'] = max(search_theme_counter, key=search_theme_counter.get)
                self.statistics['search_theme_list'] = sorted(
                    search_theme_counter,
                    key=search_theme_counter.get,
                    reverse=True
                )
            search_geo = event.geo
            if search_geo:
                search_country_counter = self.statistics['search_country_freq']
                search_country_counter[search_geo[0]] = search_country_counter[search_geo[0]] + 1 \
                    if search_geo[0] in search_country_counter else 1
                self.statistics['search_country_freq'] = search_country_counter
                self.statistics['search_country_mode'] = max(
                    search_country_counter,
                    key=search_country_counter.get
                )
                self.statistics['search_country_list'] = sorted(
                    search_country_counter,
                    key=search_country_counter.get,
                    reverse=True
                )
                try:
                    if search_geo[1]:
                        search_geo[1] = search_geo[0] + "+" + search_geo[1]
                        search_region_counter = self.statistics['search_region_freq']
                        search_region_counter[search_geo[1]] = search_region_counter[search_geo[1]] + 1 \
                            if search_geo[1] in search_region_counter else 1
                        self.statistics['search_region_freq'] = search_region_counter
                        self.statistics['search_region_mode'] = (
                            max(search_region_counter, key=search_region_counter.get)
                        )
                        self.statistics['search_region_list'] = sorted(
                            search_region_counter,
                            key=search_region_counter.get,
                            reverse=True
                        )
                except:
                    pass
            search_party_composition = event.party_composition
            search_party_composition_counter = self.statistics['search_party_composition_freq']
            search_party_composition_counter[search_party_composition] = \
                search_party_composition_counter[search_party_composition] + 1 \
                    if search_party_composition in search_party_composition_counter else 1
            self.statistics['search_party_composition_freq'] = search_party_composition_counter

            # Search on departure date
            dep_date = event.departure_date
            if dep_date:
                dep_date = dep_date[:10]
                dep_date_counter = self.statistics['search_departure_date_freq']
                dep_date_counter[dep_date] = dep_date_counter[dep_date] + 1 if dep_date in dep_date_counter else 1
                self.statistics['search_departure_date_freq'] = dep_date_counter
                self.statistics['search_departure_date_mode'] = max(dep_date_counter, key=dep_date_counter.get)
                self.statistics['search_departure_date_last'] = dep_date
                self.statistics['search_departure_date_list'] = sorted(
                    dep_date_counter,
                    key=dep_date_counter.get,
                    reverse=True
                )

        elif isinstance(event, EventDataclass.GlobalFilterPartyComposition):
            party = event.label
            party_counter = self.statistics['party_composition']
            party_counter[party] = party_counter[party] + 1 if party in party_counter else 1
            self.statistics['party_composition'] = party_counter

        elif isinstance(event, EventDataclass.Session):
            # Number of session and list of unique dmp_session_ids
            dmp_user_id_set = set(self.statistics['dmp_session_ids'] + [event.dmp_session_id])
            self.statistics['dmp_session_ids'] = list(dmp_user_id_set)
            self.statistics['session_cnt'] = len(dmp_user_id_set)

            # Day of week
            # Ordered tuple where weekdays[0] returns '0', where 0 = Monday:
            weekdays = ("0", "1", "2", "3", "4", "5", "6")
            day = date_time.weekday()
            day_string = weekdays[day]
            day_counter = self.statistics['session_day_of_week_freq']
            day_counter[day_string] = day_counter[day_string] + 1 if day_string in day_counter else 1
            self.statistics['session_day_of_week_freq'] = day_counter
            self.statistics['session_day_of_week_mode'] = max(day_counter, key=day_counter.get)
            self.statistics['session_day_of_week_list'] = sorted(
                day_counter,
                key=day_counter.get,
                reverse=True
            )

            # Hour of day
            hour = str(date_time.hour)
            hour_counter = self.statistics['session_hour_freq']
            hour_counter[hour] = hour_counter[hour] + 1 if hour in hour_counter else 1
            self.statistics['session_hour_freq'] = hour_counter
            self.statistics['session_hour_mode'] = max(hour_counter, key=hour_counter.get)
            self.statistics['session_hour_list'] = sorted(
                hour_counter,
                key=hour_counter.get,
                reverse=True
            )

        elif isinstance(event, EventDataclass.SfmcId):
            # List of unique email-addresses (or hashes)
            emails = self.statistics['user_identifiers'].get('emails', [])
            if event.email and event.email != 'undefined':
                self.statistics['user_identifiers']['emails'] = list(set(emails + [event.email]))

        # Update funnel step
        if self.statistics['funnel_step'] != 'booked' and event.funnel_event:
            self.statistics['funnel_step'] = self.update_funnel_step(self.statistics, event)

    def add_event(self, clickstream_event_json):
        """Adds event to user based on clickstream json, updates statistics.
        Args:
            clickstream_event_json: str, clickstream event json string
        """
        event = self.create_event(clickstream_event_json)
        if event:
            self.events.append(event)
            self.update_statistics(event)

    def add_multiple_events(self, clickstream_event_json_list):
        """Adds multiple events to event_list at a time.
        Args:
            clickstream_event_json_list: [str], list of clickstream event json strings
        """
        for clickstream_event_json in clickstream_event_json_list:
            self.add_event(clickstream_event_json)

    def sort_events_by_timestamp(self):
        """Sort self.events (event list) ascending on timestamp."""
        self.events = sorted(self.events, key=operator.attrgetter('timestamp'))

    def events_to_dict(self):
        """Outputs list of event dicts (decoded from the list of event dataclasses).
        Return:
            [dict], list of events as dictionaries
        """
        return [{'event_name': event.__class__.__name__, 'values': dataclasses.asdict(event)} for event in self.events]

    def to_firestore(self):
        """Writes user to firestore."""
        global _firestore_client, _firestore_collection_destination
        doc_ref = _firestore_client.collection(_firestore_collection_destination).document(self.dmp_user_id)
        doc_ref.set({
            'statistics': self.statistics,
            # 'event_list': self.events_to_dict()
        })

    def create_user_from_clickstream(self):
        """Gets all available website clickstream data from Firestore for the given dmp_user_id and fills the User class
        with information."""
        global _firestore_client, _firestore_collection_source
        doc_ref = _firestore_client.collection(_firestore_collection_source).document(self.dmp_user_id) \
            .collection(u'sessions').stream()
        sessions = [doc.id for doc in doc_ref]

        event_list = []
        for session in sessions:
            event_list += _firestore_client.collection(_firestore_collection_source).document(self.dmp_user_id) \
                .collection(u'sessions').document(session) \
                .collection(u'events').document(u'event_list').get().to_dict()['event_list']

        self.add_multiple_events(event_list)
        self.sort_events_by_timestamp()
