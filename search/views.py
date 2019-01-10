from django.shortcuts import render
from django.views.generic import TemplateView
from search.models import JobboleType
from django.http import HttpResponse
import json
from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=["127.0.0.1"])


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
        response = client.search(
            index="jobbole",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["tags", "title", "body"]
                    }
                },
                "from": 0,
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
        total_hits = response["hits"]["total"]
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "body" in hit["highlight"]:
                hit_dict["content"] = "".join(hit["highlight"]["body"])[:500]
            else:
                hit_dict["content"] = hit["_source"]["body"][:500]

            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)

        return render(request, "result.html", {"all_hits": hit_list,
                                               "total_nums": total_hits,
                                               "key_words": key_words})

