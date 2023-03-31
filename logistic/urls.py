from rest_framework.routers import DefaultRouter

from logistic.views import ProductViewSet, StockViewSet, TestView

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('stocks', StockViewSet)


urlpatterns = router.urls
