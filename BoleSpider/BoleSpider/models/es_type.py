from elasticsearch_dsl import Document, Date, Keyword, Text, Integer, Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class JobboleType(Document):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    preview_img = Keyword()
    preview_img_path = Keyword()
    votes = Integer()
    comments = Integer()
    bookmarks = Integer()
    tags = Text(analyzer="ik_max_word")
    body = Text(analyzer="ik_max_word")

    class Index:
        name = "jobbole"
        settings = {
            "number_of_shards": 2,
        }

    class Meta:
        doc_type = "article"


class LagouType(Document):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    salary = Keyword()
    job_city = Keyword()
    work_years = Keyword()
    degree_need = Keyword()
    job_type = Keyword()
    publish_time = Keyword()
    job_advantage = Keyword()
    job_desc = Text(analyzer="ik_max_word")
    job_addr = Keyword()
    company_name = Keyword()
    company_url = Keyword()
    tags = Text(analyzer="ik_max_word")
    crawl_time = Date()

    class Index:
        name = "lagou"
        settings = {
            "number_of_shards": 2,
        }

    class Meta:
        doc_type = "job"


if __name__ == "__main__":
    # JobboleType.init()
    LagouType.init()