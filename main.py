from requests_html import HTMLSession


class JianShu(object):

    def __init__(self, root_url):
        self.url = root_url
        self.session = HTMLSession()

    @property
    def response(self):
        return self.session.get(self.url)

    @property
    def get_author(self):
        return self.response.html.find(".main-top .title", first=True).text

    @property
    def get_url(self):
        return self.url

    @property
    def get_description(self):
        return self.response.html.find(".js-intro", first=True).text.replace(" ", "").replace("\n", "").replace("\t", "")

    @property
    def get_weibo(self):
        flag = self.response.html.find("div.description > a[target=_blank]", first=True)
        if not flag:
            return "no found weibo info"
        else:
            return flag.absolute_links

    def get_list_passage(self):
        pass

    @property
    def get_follower_number(self):
        number = self.response.html.find("div.main-top > div.info > ul > li > div")[0].text
        return number.replace(" ", "").replace("\n", "").replace("\t", "")

    @property
    def get_following_number(self):
        number = self.response.html.find("div.main-top > div.info > ul > li > div")[1].text
        return number.replace(" ", "").replace("\n", "").replace("\t", "")

    @property
    def get_passage_number(self):
        number = self.response.html.find("div.main-top > div.info > ul > li > div")[2].text
        return number.replace(" ", "").replace("\n", "").replace("\t", "")

    @property
    def get_writer_number(self):
        number = self.response.html.find("div.main-top > div.info > ul > li > div")[3].text
        return number.replace(" ", "").replace("\n", "").replace("\t", "")

    @property
    def get_liked_number(self):
        number = self.response.html.find("div.main-top > div.info > ul > li > div")[4].text
        return number.replace(" ", "").replace("\n", "").replace("\t", "")


if __name__ == "__main__":
    jianshu = JianShu("https://www.jianshu.com/u/ad01cece21e2")
    # jianshu = JianShu("https://www.jianshu.com/u/58f0817209aa")
    print(jianshu.get_author, jianshu.get_description, jianshu.get_url, jianshu.get_weibo,
          jianshu.get_follower_number,
          jianshu.get_following_number,
          jianshu.get_liked_number,
          jianshu.get_writer_number)
