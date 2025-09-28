from django.views.generic import ListView, DetailView, CreateView
from nagoyameshi.models import Restaurant,Category, Review, Reservation
from nagoyameshi.forms import CategoryForm,ReviewForm,RestaurantCategorySearchForm,ReservationForm
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
#from nagoyameshi.mixins import PremiumMemberMixin  #検証用に一旦コメントアウト
from django.contrib.auth.mixins import LoginRequiredMixin



###トップページに検索機能検索
class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        query   =Q()


        if "search" in request.GET:
            print(request.GET["search"]) #デバッグ
            context["restaurants"]   = Restaurant.objects.filter(name__icontains=request.GET["search"])
            print( request.GET["search"].replace(" ","　").split("　") ) #デバッグ
            
            #split = 文字分割、スペースも文字とみなす
            words =request.GET["search"].replace(" ","　").split("　")
            #nameをモデル名に変更すれば他条件での検索も可能になる
            for word in words:
                query &= Q(name__icontains=word)
        
        #restaurant内でフィルターをかけた結果をだす
        context["restaurants"] = Restaurant.objects.filter(query)

        #Categoryモデルを全て表示
        context["categories"]  = Category.objects.all()

        # render関数は指定したテンプレートのレンダリングをしている。
        # 第一引数はrequestオブジェクト、第2引数はテンプレート、第3引数はコンテキスト(DBなどから読み込みしたデータ(辞書型))
        return render(request, "nagoyameshi/index.html", context)

    def post(self, request, *args, **kwargs):
        # POSTメソッドを使用してリクエストが送られた場合、この部分の処理が実行される。
        pass

index   = IndexView.as_view()

###トップページに店舗を表示　→あとからトップ３の店舗を表示してもいい
class IndexListView(ListView):
    model = Restaurant
    template_name = 'pages/index.html'



###店舗一覧ページ
class RestaurantListView(View):
     def get(self, request, *args, **kwargs):

        context = {}
        query   = Q()

        context["categories"] = Category.objects.all()

        if "search" in request.GET:
            words = request.GET["search"].replace(" ","　").split("　")
            for word in words:
                #AND検索：&=
                #OR検索 ：!=
                #OR検索で空文字を含むと全件が検索結果として表示されるため、空文字がない場合は検索条件を追加という定義をする（if word !="":）
                if word   != "": 
                    query &= Q( Q(name__icontains=word) | Q(address__icontains=word) | Q(category__name__icontains=word) )


        #TODO : ここにカテゴリでの検索にも対応させる。
        # RestaurantCategorySearchForm で実在するカテゴリのidかをチェックする。
        form    = RestaurantCategorySearchForm(request.GET)

        if form.is_valid():
            # このManyToManyFieldのオブジェクトは直接指定して検索はできない。
            print( form.cleaned_data["category_name"] )
            # そのため、request.GETからidをセット
            query &= Q(category_name=request.GET["category_name"])



        print(query)

        # TODO:カテゴリも含めて検索する。
        restaurants = Restaurant.objects.filter(query)
        #ページネーション
        #第一引数：オブジェクト、第二引数：1ページに表示するオブジェクト数
        paginator = Paginator(restaurants,6)

        if "page" in request.GET:
            restaurants = paginator.get_page(request.GET["page"])
        else:
            restaurants = paginator.get_page(1)

        #検索ワードを引き継いだままページ遷移できるようにする
        copied = request.GET.copy()

        #パラメータ
        print("?" + copied.urlencode())

        #前にページがある場合
        if restaurants.has_previous():
            copied["page"]                 = restaurants.previous_page_number()
            restaurants.previous_page_link = "?" + copied.urlencode()

            copied["page"]                 = 1
            restaurants.first_page_link = "?" + copied.urlencode()

        #次にページがある場合
        if restaurants.has_next():
            copied["page"]                 = restaurants.next_page_number()
            restaurants.next_page_link = "?" + copied.urlencode()

            copied["page"]                 = restaurants.paginator.num_pages
            restaurants.end_page_link = "?" + copied.urlencode()
        
        context["restaurants"]  = restaurants

        return render(request,"pages/restaurant_list.html",context)

restaurant_list = RestaurantListView.as_view()




###店舗の詳細ページ
class RestaurantDetailView(DetailView):
    
    model = Restaurant
    template_name = 'pages/restaurant_detail.html'
    context_object_name = "restaurant"   #objectをrestaurantで定義し直し


    def get(self, request, pk, *args, **kwargs):
        restaurant = Restaurant.objects.get(id=pk)
        reviews = Review.objects.filter(restaurant=restaurant).order_by("-created_date")
        form = ReviewForm()

        return render(request, "pages/restaurant_detail.html", {
            "restaurant": restaurant,
            "reviews": reviews,
            "form": form,
        })

    def post(self, request, pk, *args, **kwargs):
        restaurant = Restaurant.objects.get(id=pk)
        copied = request.POST.copy()
        copied["user"] = request.user
        copied["restaurant"] = restaurant.id
        form = ReviewForm(copied)

        if form.is_valid():
            form.save()
            messages.success(request, "レビューを投稿しました")
        else:
            messages.error(request, "投稿に失敗しました")

        return redirect("nagoyameshi:restaurant_detail", pk=restaurant.id)


###予約ビュー
class ReservationView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = "pages/reservation_form.html"
    fields = ["date", "people"]  # CreateViewでuser, restaurant は自動設定

    def form_valid(self, form):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs["pk"])
        form.instance.restaurant = restaurant
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs["pk"])
        context["restaurant"] = restaurant
        return context

    def get_success_url(self):
        return reverse_lazy("nagoyameshi:restaurant_detail", kwargs={"pk": self.kwargs["pk"]})

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "pages/reservation_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by("date")
    









       