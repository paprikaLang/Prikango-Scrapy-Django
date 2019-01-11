from django.shortcuts import render
from django.views.generic import TemplateView
from search.models import JobboleType
from django.http import HttpResponse
import json
from elasticsearch import Elasticsearch
from datetime import datetime
import redis

client = Elasticsearch(hosts=["127.0.0.1"])
redis_client = redis.StrictRedis()

class SearchSuggest(TemplateView):
    def get(self, request):
        key_words = request.GET.get('s', '')
        re_data = []
        if key_words:
            s = JobboleType.search()
            s = s.suggest('my-suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute()

            for match in getattr(suggestions.suggest, "my-suggest")[0].options:
                source = match._source
                re_data.append(source["title"])
        return HttpResponse(json.dumps(re_data), content_type="application/json")


class SearchView(TemplateView):
    def get(self, request):
        key_words = request.GET.get('q', "")
        page_id = request.GET.get('p', "")
        try:
            page = int(page_id)
        except:
            page = 1

        start_time = datetime.now()
        response = client.search(
            index="jobbole",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["tags", "title", "body"]
                    }
                },
                "from": (page - 1)*10,
                "size": 10,
                "highlight": {
                    "pre_tags": ["<span class='keyWord'>"],
                    "post_tags": ["</span>"],
                    "fields": {
                        "title": {},
                        "body": {}
                    }
                }
            }
        )
        end_time = datetime.now()
        jobbole_count = int(redis_client.get("jobbole_total_count"))
        durine_time = (end_time - start_time).total_seconds()
        total_hits = response["hits"]["total"]
        if (page % 10) > 0:
            page_nums = int(total_hits / 10) + 1
        else:
            page_nums = int(total_hits / 10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "body" in hit["highlight"]:
                hit_dict["content"] = "".join(hit["highlight"]["body"])[:1000]
            else:
                hit_dict["content"] = hit["_source"]["body"][:1000]

            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)

        return render(request, "result.html", {"all_hits": hit_list,
                                               "total_nums": total_hits,
                                               "page": page,
                                               "page_nums": page_nums,
                                               "jobbole_count": jobbole_count,
                                               "last_seconds": durine_time,
                                               "key_words": key_words})

