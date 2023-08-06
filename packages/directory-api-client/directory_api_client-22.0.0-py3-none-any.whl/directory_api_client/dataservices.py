from directory_api_client.base import AbstractAPIClient

url_corruption_perceptions_index = 'dataservices/corruption-perceptions-index/{country_code}/'
url_ease_of_doing_business = 'dataservices/easeofdoingbusiness/{country_code}/'
url_last_year_import_data = 'dataservices/lastyearimportdata/'
url_historical_import_data = 'dataservices/historicalimportdata/'
url_world_economic_outlook_data = 'dataservices/world-economic-outlook/{country_code}/'


class DataServicesAPIClient(AbstractAPIClient):

    def get_corruption_perceptions_index(self, country_code):
        return self.get(
            url=url_corruption_perceptions_index.format(country_code=country_code),
            use_fallback_cache=True
        )

    def get_ease_of_doing_business(self, country_code):
        return self.get(
            url=url_ease_of_doing_business.format(country_code=country_code),
            use_fallback_cache=True,
        )

    def get_last_year_import_data(self, commodity_code, country):
        return self.get(
            url=url_last_year_import_data,
            params={'commodity_code': commodity_code, 'country': country}
        )

    def get_historical_import_data(self, commodity_code, country):
        return self.get(
            url=url_historical_import_data,
            params={'commodity_code': commodity_code, 'country': country}
        )

    def get_world_economic_outlook_data(self, country_code):
        return self.get(
            url=url_world_economic_outlook_data.format(country_code=country_code),
            use_fallback_cache=True
        )
