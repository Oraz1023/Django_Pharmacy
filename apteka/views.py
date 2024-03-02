from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from .models import *
from .serializer import *


# Create your views here.

class ProductAPIView(APIView):

    def get(self, request, pk=None):

        if pk is not None:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            data = serializer.data
            # Получаем имя каталога по его идентификатору
            catalog_title = product.catalog.title
            data['catalog'] = catalog_title
            # Получаем имя категории по его идентификатору
            category_title = product.category.title
            data['category'] = category_title
            # Получаем имя популярного бренда по его идентификатору
            pop_brand_title = product.pop_brand.title
            data['pop_brand'] = pop_brand_title
            return Response(data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            data = serializer.data
            for product_data in data:
                # Получаем имя каталогов
                product_instance = Product.objects.get(pk=product_data['id'])
                catalog_title = product_instance.catalog.title
                product_data['catalog'] = catalog_title
                # Получаем имя категории
                category_title = product_instance.category.title
                product_data['category'] = category_title
                # Получаем имя популярных брендов
                pop_brand_title = product_instance.pop_brand.title
                product_data['pop_brand'] = pop_brand_title
            return Response(data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = get_object_or_404(Product, pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"success": f"Продукт с id {pk} удален"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

        # catalog_pk = request.data['catalog']
        # if catalog_pk is None:
        #     return Response({"error": "Каталог обязательно надо выбрать"}, status=status.HTTP_400_BAD_REQUEST)
        # catalog_instance = Catalog.objects.get(pk=catalog_pk)
        #
        # if catalog_instance is None:
        #     return Response({"error": "Каталог не найден"}, status=status.HTTP_400_BAD_REQUEST)
        #
        # serializer = ProductSerializer(data=request.data)
        #
        # if serializer.is_valid():
        #     # catalog_instance=Catalog.objects.get()
        #     serializer.save(catalog=catalog_instance)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        #
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #


class CatalogAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            catalog = get_object_or_404(Catalog, pk=pk)
            serializer = CatalogSerializer(catalog)
            data = serializer.data
            return Response(data)
        else:
            catalogs = Catalog.objects.all()
            serializer = CatalogSerializer(catalogs, many=True)
            data = serializer.data
            return Response(data)

    def post(self, request):
        serializer = CatalogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = get_object_or_404(Catalog, pk=pk)
        except Catalog.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CatalogSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        catalog = get_object_or_404(data=request.data)
        serializer = CatalogSerializer(instance=catalog, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        catalog = get_object_or_404(pk=pk)
        catalog.delete()
        return Response({"success": f"Каталог с id {pk} удален"}, status=status.HTTP_204_NO_CONTENT)


class CategoryAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            category = get_object_or_404(Category, pk=pk)
            serializer = CategorySerializer(category)
            data = serializer.data
            return Response(data)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            data = serializer.data
            return Response(data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = get_object_or_404(Category, pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({"success": f"Категория с id {pk} удалена"}, status=status.HTTP_204_NO_CONTENT)


class PopularBrandAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            pop_brand = get_object_or_404(Popular_brand, pk=pk)
            serializer = PopularBrandSerializer(pop_brand,)
            data = serializer.data
            return Response(data)
        else:
            pop_brands = Popular_brand.objects.all()
            serializer = PopularBrandSerializer(pop_brands, many=True)
            data = serializer.data
            return Response(data)

    def post(self, request):
        serializer = PopularBrandSerializer(data=request.data,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = get_object_or_404(Popular_brand.objects, pk=pk)
        except Popular_brand.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PopularBrandSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        pop_brand = get_object_or_404(Popular_brand, pk=pk)
        serializer = CatalogSerializer(instance=pop_brand, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        pop_brand = get_object_or_404(Popular_brand, pk=pk)
        pop_brand.delete()
        return Response({"success": f"Бренд с id {pk} удален"}, status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order)
            data = serializer.data
            # Получаем имя клиента по его идентификатору
            customer_name = order.customer.full_name
            data['customer'] = customer_name
            # Получаем список продуктов
            products = order.products.all()
            products = ProductSerializer(products, many=True)
            data['products'] = products.data
            return Response(data)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            data = serializer.data
            for order_data in data:
                # Получаем имя клиента по его идентификатору
                order_instance = Order.objects.get(pk=order_data['id'])
                customer_name = order_instance.customer.full_name
                order_data['customer'] = customer_name
                # Получаем список продуктов
                products = order_instance.products.all()
                products_serializer = ProductSerializer(products, many=True)
                order_data['products'] = products_serializer.data
            return Response(data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data, )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = get_object_or_404(Order, pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({"success": f"Заказ с id {pk} удален"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(instance=order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class HealthBlogAPIView(APIView):
    def get(self, request, pk=None):
        # Если в запросе указан идентификатор записи (pk)
        if pk is not None:
            # Извлекаем запись из базы данных по ее идентификатору
            health_blog = get_object_or_404(Health_blog, pk=pk)
            # Создаем экземпляр сериализатора для одной записи
            serializer = HealthBlogSerializer(health_blog)
            # Возвращаем данные о найденной записи в ответе
            return Response(serializer.data)
        else:
            # Извлекаем все записи блога о здоровье из базы данных
            health_blogs = Health_blog.objects.all()
            # Создаем экземпляр сериализатора для всех записей
            serializer = HealthBlogSerializer(health_blogs, many=True)
            # Возвращаем данные о всех записях в ответе
            return Response(serializer.data)

    def post(self, request):
        # Создаем сериализатор с данными из запроса
        serializer = HealthBlogSerializer(data=request.data)
        # Проверяем валидность данных
        if serializer.is_valid():
            # Сохраняем данные и создаем новую запись в блоге о здоровье
            serializer.save()
            # Возвращаем успешный ответ с данными созданной записи
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Возвращаем ответ с ошибками валидации, если данные неверны
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # Шаг 1: Получаем идентификатор записи блога о здоровье (pk) из URL запроса
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)
        # Шаг 2: Пытаемся найти запись блога о здоровье в базе данных по ее идентификатору
        instance = get_object_or_404(Health_blog, pk=pk)
        # Шаг 3: Создаем экземпляр сериализатора для этой записи с переданными данными из запроса
        serializer = HealthBlogSerializer(instance=instance, data=request.data)
        # Шаг 4: Проверяем валидность данных с помощью сериализатора
        serializer.is_valid(raise_exception=True)
        # Шаг 5: Сохраняем обновленные данные записи
        serializer.save()
        # Шаг 6: Возвращаем обновленные данные записи и код состояния 200 (OK) в ответе
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Извлекаем запись из базы данных по ее идентификатору
        health_blog = get_object_or_404(Health_blog, pk=pk)
        # Удаляем запись
        health_blog.delete()
        # Возвращаем ответ об успешном удалении записи с соответствующим сообщением
        return Response({"success": f"Запись блога о здоровье с id {pk} удалена"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        # Извлекаем запись из базы данных по ее идентификатору
        health_blog = get_object_or_404(Health_blog, pk=pk)
        # Создаем экземпляр сериализатора для обновления записи
        serializer = HealthBlogSerializer(instance=health_blog, data=request.data, partial=True)
        # Проверяем валидность данных
        serializer.is_valid(raise_exception=True)
        # Сохраняем обновленные данные
        serializer.save()
        # Возвращаем ответ с обновленными данными и статусом 200 (OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MonthlyPromotionAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            # Извлекаем запись из базы данных по ее идентификатору
            month_promotion = get_object_or_404(Health_blog, pk=pk)
            # Создаем экземпляр сериализатора для одной записи
            serializer = MonthlyPromotionSerializer(month_promotion)
            # Возвращаем данные о найденной записи в ответе
            return Response(serializer.data)
        else:
            # Извлекаем все записи блога о здоровье из базы данных
            month_promotions = MonthlyPromotion.objects.all()
            # Создаем экземпляр сериализатора для всех записей
            serializer = MonthlyPromotionSerializer(month_promotions, many=True)
            # Возвращаем данные о всех записях в ответе
            return Response(serializer.data)

    def post(self, request, pk=None):
        serializer = MonthlyPromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(MonthlyPromotion, pk=pk)
        serializer = MonthlyPromotionSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        month_promrotion = get_object_or_404(MonthlyPromotion, pk=pk)
        serializer = MonthlyPromotionSerializer(instance=month_promrotion, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Извлекаем запись из базы данных по ее идентификатору
        month_promotion = get_object_or_404(MonthlyPromotion, pk=pk)
        # Удаляем запись
        month_promotion.delete()
        # Возвращаем ответ об успешном удалении записи с соответствующим сообщением
        return Response({"success": f"Запись блога о здоровье с id {pk} удалена"}, status=status.HTTP_204_NO_CONTENT)


class PersonalAccountAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            person = get_object_or_404(Personal_account, pk=pk)
            serializer = PersonalAccountSerializer(person)
            data = serializer.data
            return Response(data)
        else:
            persons = Personal_account.objects.all()
            serializer = PersonalAccountSerializer(persons, many=True)
            data = serializer.data
            return Response(data)
    def post(self, request):
        serializer = PersonalAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        if not pk:
            return Response({"error": "Параметр 'pk' не указан"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = get_object_or_404(Personal_account, pk=pk)
        except Personal_account.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalAccountSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self, request, pk):
        person=get_object_or_404(Personal_account, pk=pk)
        serializer = PersonalAccountSerializer(instance=person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        person=get_object_or_404(Personal_account, pk=pk)
        person.delete()
        return Response({"success": f"Запись блога о здоровье с id {pk} удалена"}, status=status.HTTP_204_NO_CONTENT)



# class ProductApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class OrderApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#
#
# class CatalogApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Catalog.objects.all()
#     serializer_class = CatalogSerializer
#
#
# class MonthlyPromotionApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MonthlyPromotion.objects.all()
#     serializer_class = MonthlyPromotionSerializer
#
#
# class CategoryApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class PopularBrandApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Popular_brand.objects.all()
#     serializer_class = PopularBrandSerializer
#
#
# class PersonApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Personal_account.objects.all()
#     serializer_class = PersonSerializer
#
#
# class HealthBlogApiList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Health_blog.objects.all()
#     serializer_class = HealthBlogSerializer
