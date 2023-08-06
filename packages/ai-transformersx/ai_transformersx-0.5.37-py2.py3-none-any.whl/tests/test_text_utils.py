from ai_transformersx.utils.text_utils import make_sentences_max_length

content = ['斯坦议会上院议长纳扎尔巴耶娃和,',
           '下面一场尼格马图林邀请全国人大常委会委员长栗战书，21号到25号对哈萨克斯坦进行正式友好访问，再努尔苏丹会见首任总统纳扎尔巴耶夫和总统托卡耶夫，与娜扎尔巴耶娃尼格马图林分别举行会谈，与总理马明共同出席相关活动。',
           '中哈',
           '关系实现',
           '中哈关系实现历史性跨越，成为国家间关系的典范。'
           ]


def test_make_sentences_max_length():
    sentences = make_sentences_max_length(content, 30)
    print(sentences)
