class TestMovieApi:
    def test_get_10_movie(self, api_manager):
        """
        Тест на получение афиши по дефолту
        """
        response = api_manager.movies_api.receiving_post(status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 10, "По умолчанию Афиш должно быть 10!"

    def test_get_20_movie(self, api_manager):
        """
        Тест на получение афиши pageSize": "20
        """
        response = api_manager.movies_api.receiving_post(params={"pageSize": "20"},status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 20, "В параметрах установили вывод 20 Афиш!"

    def test_get_price(self, api_manager):
        """
        Тест на получение афиши по фильтрацие price
        """
        min_price = 1
        max_price = 2
        assert min_price < max_price, "min_price не дожен быть больше либо равен max_price"
        response = api_manager.movies_api.receiving_post(params={"minPrice": min_price, "maxPrice": max_price},status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 10, "По умолчанию Афиш должно быть 10!"
        for number in range(len(response_json['movies'])):
            price = response_json['movies'][number]['price']
            assert min_price <= price <= max_price, "Цена не в указанном деапазоне"

    def test_get_locations(self, api_manager):
        """
        Тест на получение афиши по фильтрацие locations [MSK,SPB]
        """
        locations = "SPB"
        response = api_manager.movies_api.receiving_post(params={"locations": locations},status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 10, "По умолчанию Афиш должно быть 10!"
        for number in range(len(response_json['movies'])):
            response_locations = response_json['movies'][number]['location']
            assert response_locations == locations, "Локация не равна указанной"

    def test_get_negative(self, api_manager):
        locations = "USA"
        api_manager.movies_api.receiving_post(params={"locations": locations}, status=400)
        min_price = 100
        max_price = 1
        api_manager.movies_api.receiving_post(params={"minPrice": min_price, "maxPrice": max_price},status=400)
        pagesize = 30
        api_manager.movies_api.receiving_post(params={"pageSize": pagesize},status=400)

    # def test_creation_movie(self, api_manager, generate_movies):
    #     api_manager.movies_api.update_headers()
    #     response = api_manager.movies_api.created_movie(generate_movies, 201)
    #     response_json = response.json()
