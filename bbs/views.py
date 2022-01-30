from rest_framework.views import APIView
#from django.views import View

#APIで使うレスポンスオブジェクトとステータスコード
from rest_framework.response import Response
from rest_framework import status


from django.shortcuts import render

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from .models import Topic
from .serializer import TopicSerializer

class IndexView(APIView):

    def create_context(self):
        context     = {}
        context["topics"]       = Topic.objects.all()

        return context

    def get(self, request, *args, **kwargs):
        context     = self.create_context()

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):
        print("POST")

        serializer      = TopicSerializer(data=request.data)

        if serializer.is_valid():
            print("バリデーションOK")
            serializer.save()
        else:
            print("バリデーションNG")
            

        context                 = self.create_context()
        content_data_string     = render_to_string('bbs/comment.html', context ,request)
        json_data               = { "content" : content_data_string }

        return JsonResponse(json_data)

    def delete(self, request, *args, **kwargs):

        topic   = Topic.objects.filter(id=kwargs["pk"]).first()

        if topic:
            print("削除")
            topic.delete()

        context                 = self.create_context()
        content_data_string     = render_to_string('bbs/comment.html', context ,request)
        json_data               = { "content" : content_data_string }

        return JsonResponse(json_data)

index   = IndexView.as_view()



#上記IndexViewをAPI対応にしたApiIndexViewを作る。
class ApiIndexView(APIView):

    def get(self, request, *args, **kwargs):

        #トピックの一覧を全て返却する。ただし、形式はJsonとステータスコードをセットで返却する。
        topics      = Topic.objects.all()

        #TopicSerializerを経由して、JSON形式に変換。モデルオブジェクト複数であればmany=Trueも指定する。
        serializer  = TopicSerializer(data=topics, many=True)

        #ステータスコードは下記URLから選ぶ
        #https://www.django-rest-framework.org/api-guide/status-codes/
        
        #シリアライズされたデータ(JSON)とステータスコードを同時に返却する
        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        print("POST")

        serializer      = TopicSerializer(data=request.data)

        if serializer.is_valid():
            print("バリデーションOK")
            serializer.save()
            #JSONとステータスコードを同時に返却する
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            print("バリデーションNG")
            #バリデーションNGなら、この時点でレスポンスを返却する
            return Response(request.data, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        topic   = Topic.objects.filter(id=kwargs["pk"]).first()

        if topic:
            print("削除")
            topic.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            return Response(status.HTTP_404_NOT_FOUND)

api_index   = ApiIndexView.as_view()



"""
下記を実行してみる。DELETE以外はボディとステータスコードが返却される。


curl -X GET "http://localhost:8000/api/index/" -w " %{http_code}\n"
curl -X POST -d "comment=テスト" "http://localhost:8000/api/index/" -w " %{http_code}\n"
curl -X DELETE "http://localhost:8000/api/index/1/" -w " %{http_code}\n"

"""

