class TestMovieApi:
    def test_get_10_movie(self, common_user):
        """
        Тест на получение афиши по дефолту
        """
        response = common_user.api.movies_api.receiving_post(expected_status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 10, "По умолчанию Афиш должно быть 10!"

    def test_get_20_movie(self, common_user):
        """
        Тест на получение афиши pageSize": "20
        """
        response = common_user.api.movies_api.receiving_post(params={"pageSize": "20"},expected_status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 20, "В параметрах установили вывод 20 Афиш!"

    def test_get_price(self, common_user):
        """
        Тест на получение афиши по фильтрацие price
        """
        min_price = 1
        max_price = 2
        assert min_price < max_price, "min_price не дожен быть больше либо равен max_price"
        response = common_user.api.movies_api.receiving_post(params={"minPrice": min_price, "maxPrice": max_price},
                                                         expected_status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 10, "По умолчанию Афиш должно быть 10!"
        for number in range(len(response_json['movies'])):
            price = response_json['movies'][number]['price']
            assert min_price <= price <= max_price, "Цена не в указанном деапазоне"

    def test_get_locations(self, common_user):
        """
        Тест на получение афиши по фильтрацие locations [MSK,SPB]
        """
        locations = "SPB"
        response = common_user.api.movies_api.receiving_post(params={"locations": locations},
                                                         expected_status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 10, "По умолчанию Афиш должно быть 10!"
        for number in range(len(response_json['movies'])):
            response_locations = response_json['movies'][number]['location']
            assert response_locations == locations, "Локация не равна указанной"

    def test_get_negative(self, common_user):
        locations = "USA"
        common_user.api.movies_api.receiving_post(params={"locations": locations},
                                              expected_status=400)
        min_price = 100
        max_price = 1
        common_user.api.movies_api.receiving_post(params={"minPrice": min_price, "maxPrice": max_price},
                                                  expected_status=400)
        pagesize = 30
        common_user.api.movies_api.receiving_post(params={"pageSize": pagesize},
                                              expected_status=400)

    from typing import Dict
    min_price = 1
    max_price = 100
    locations = "SPB"
    genreld = 3
    import pytest
    @pytest.mark.parametrize("params, expected_status", [
        ({"minPrice": min_price, "maxPrice": max_price}, 200),
        ({"locations": locations}, 200),
        ({"genreld": genreld}, 200),
    ], ids=["Price", "location", "genreld"])
    def test_filter(self, params, expected_status, api_manager):
         api_manager.movies_api.receiving_post(params=params, expected_status=expected_status)

