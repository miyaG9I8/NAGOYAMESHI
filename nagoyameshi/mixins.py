from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect



#ログイン済みか、有料会員かをチェック
class PremiumMemberMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # customerフィールドが空なら非会員扱い
        if not request.user.customer:
            return redirect("nagoyameshi:index")

        return super().dispatch(request, *args, **kwargs)








    """
    def dispatch(self,request,*args,**kwargs):

        if not request.user.is_authenticated:
            #return redirect("login")と同じ
            return self.handle_no_permission()

        #カスタマーIDの確認
        try:
            subscriptions = stripe.Subscription.list(customer=request.user.customer)
        except:
            print("このカスタマーIDは無効です。")
            request.user.customer = ""
            request.user.save()
            return redirect("nagoyameshi:index")

    #サブスクの確認
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です")
                return super().dispatch(request,*args,**kwargs)
            else:
                print("サブスクリプションが無効です。再度登録をお願いします。")
            request.user.customer = ""
            request.user.save()
            return redirect("nagoyameshi:index")
    """