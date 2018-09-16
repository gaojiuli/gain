
from gain import Css, Item, Parser, Xpath


html = """
<!DOCTYPE html>
   <html>
   <head>
   <meta charset="UTF-8">
    <title>Title of the document</title>
    <meta name="twitter:title" property="og:title" itemprop="element dict" content="python, lxml retrieving all elements in a dict">
   </head>
   <body>
       <div id="breadcrumb">
           <span>Home</span>
           <span>Categories</span>
           <span>Deals</span>
           <span>
               <p id="end"></br><a href="/personal-deal" target="_blank">Here is your deal</a></br></p>
           </span>
       </div
       <div class="deal-page">
           <h1 class="deal-page-title">
               <strong>Today 20% off for the weekend special, now for 200€</strong>
           </h1>
           <div>
               <img src="/images/branding/googlelogo/2x/googlelogo_color_120x44dp.png" alt="Google" data-atf="3" width="120" height="44">
               <div class="map_canvas" data-address="263 Prinsengracht, Amsterdam">
                   Google Map
               </div>
           </div>
           <div style="float:right; text-align:left;width:340px;" class="info">
              <ul>
                 <li><strong>General</strong></li>
                 <li>
                    Location:
                    England
                 </li>
                 <li>
                    Type of building:
                    Historical
                 </li>
                 <li>
                    Amount of people:
                    Less than 100
                 </li>
                 <li>
                    Price range:
                    € 450 - € 600
                 </li>
                 <li>
                    Occasion:
                    Ceremony, Business, Cultural,
                 </li>
                 <li>
                   Location:
                   City district
                 </li>
                 <li>
                    Number of Rooms:
                    8
                 </li>
              </ul>
              <br>
              <ul>
                 <li><strong>Opportunities &amp; Services</strong></li>
                 <li>Audio and Visual</li>
                 <li>Kitchen</li>
                 <li>Wheelchair accessible</li>
              </ul>
           </div>
           <div class="contact" style="margin-bottom:10px;padding:10px;line-height:160%;color:#002a50;">
               <strong style="color:#002a50;">
               Prime Minister's residence</strong><br>
               <span style="color:#002a50;">10 Downing Street</span><br><span style="color:#002a50;">SW1A 2AA&nbsp;London, England</span>
               <br><br><strong>Contactperson</strong><br>
               Mr.
               C.J.
               Carlson
               <br><br><span style="color:#51a4d9;">T: </span> +36 074-21292733
               <br>
               <span style="color:#51a4d9;">W:</span> <a href="http://www.stjames.uk" target="_blank">www.stjames.uk</a>
           </div>
       </div>
   </body>
   </html>
"""


def test_parse():
    html = '<title class="username">tom</title><div class="karma">15</div>'

    class User(Item):
        username = Xpath('//title')
        karma = Css('.karma')

    parser = Parser(html, User)

    user = parser.parse_item(html)
    assert user.results == {
        'username': 'tom',
        'karma': '15'
    }


def test_parse_urls():
    html = ('<a href="item?id=14447885">64comments</a>'
            '<a href="item?id=14447886">64comments</a>')

    class User(Item):
        username = Xpath('//title')
        karma = Css('.karma')

    parser = Parser('item\?id=\d+', User)
    parser.parse_urls(html, 'https://blog.scrapinghub.com')
    assert parser.pre_parse_urls.qsize() == 2


def test_parse_css_text():
    class Test(Item):
        item = Css('.deal-page-title strong') # Default method=text and index=0

    parser = Parser(html, Test)
    extract = parser.parse_item(html)

    assert extract.item == 'Today 20% off for the weekend special, now for 200€'


def test_parse_css_text_content():
    class Test(Item):
        item = Css('#breadcrumb span', **{"method":'text_content', "index":'3', "manipulate": ["clean_string"] })

    parser = Parser(html, Test)
    extract = parser.parse_item(html)

    assert extract.item == 'Here is your deal' 


def test_parse_css_get():
    class Test(Item):
        attr = Css('.map_canvas', 'data-address')
        get = Css('.map_canvas', **{"method":'get', "attr":'data-address'})
        gmap = Css('[data-address]', **{"manipulate": ["clean_string"]})

    parser = Parser(html, Test)
    extract = parser.parse_item(html)

    assert extract.get == "263 Prinsengracht, Amsterdam"
    assert extract.attr == "263 Prinsengracht, Amsterdam"
    assert extract.gmap == "Google Map"


def test_parse_css_itertext():
    class Test(Item):
        ul = Css('.info', **{"method":"itertext"})

    parser = Parser(html, Test)
    extract = parser.parse_item(html)

    assert isinstance(extract.ul, list)
    assert len(extract.ul) == 12
    assert extract.ul[11] == 'Wheelchair accessible'


def test_parse_css_dict():
    class Test(Item):
        content = Css('meta[property="og:title"]', **{"method":"get", "attr":"content"})
        attrib_dict = Css('meta[property="og:title"]', **{"method":"dict"})

    parser = Parser(html, Test)
    extract = parser.parse_item(html)

    assert isinstance(extract.attrib_dict, dict)
    assert extract.content == 'python, lxml retrieving all elements in a dict'
    assert extract.attrib_dict["property"] == 'og:title'


if __name__ == "__main__":
    test_parse()
    test_parse_urls()
    test_parse_css_text()
    test_parse_css_text_content()
    test_parse_css_get()
    test_parse_css_itertext()
    test_parse_css_dict()