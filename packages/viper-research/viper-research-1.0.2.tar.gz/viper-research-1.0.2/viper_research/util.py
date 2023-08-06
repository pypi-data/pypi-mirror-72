from datetime import datetime


def try_parsing_date(text):
    """
    字符串转换为datetime对象
    :param text:时间的字符串格式
    :return:datetime
    """
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y%m%d'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')
