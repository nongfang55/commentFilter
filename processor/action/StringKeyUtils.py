

class StringKeyUtils:
    """用于存放各种字符串的工具类"""

    """和comment的元素相关，如link, code 等"""
    STR_REPLACE_KEY_TALK = 'cmm_talk'  # 谈话引用
    STR_REPLACE_KEY_LINK = 'cmm_link'  # 超链接
    STR_REPLACE_KEY_ELEMENT = 'cmm_element'  # 小型代码块
    STR_REPLACE_KEY_BLOCK = 'cmm_block' # 大型代码块
    STR_REPLACE_KEY_AT = 'cmm_at'  # @用户
    STR_REPLACE_KEY_PIC = 'cmm_pic' # 照片

    STR_INDICATE_TALK = 'talk'
    STR_INDICATE_LINK = 'link'
    STR_INDICATE_ELEMENT = 'element'
    STR_INDICATE_BLOCK = 'block'
    STR_INDICATE_AT = 'at'
    STR_INDICATE_PIC = 'pic'

    """统计元素所用的行"""
    STR_COUNT_TALK = 'count_talk'
    STR_COUNT_LINK = 'count_link'
    STR_COUNT_ELEMENT = 'count_element'
    STR_COUNT_BLOCK = 'count_block'
    STR_COUNT_AT = 'count_at'
    STR_COUNT_PIC = 'count_pic'

    """断句分词所用的行"""
    STR_INDICATE_SENTENCE = 'sentence'
    STR_INDICATE_TOKEN = 'token'

    STR_COUNT_SENTENCE = 'count_sentence'
    STR_COUNT_TOKEN = 'count_token'

    """punkt分割器的加载路径"""
    STR_PATH_PUNTK = 'tokenizers/punkt/english.pickle'

    """统计分布所需要的字段"""
    STR_KEY_GROUP_BY = 'key_group_by'
    STR_KEY_EXCEL_NAME = 'key_excel_name'
    STR_KEY_SHEET_NAME = 'key_sheet_name'
    STR_KEY_DEFAULT_EXCEL_NAME = 'distribution.xls'

    STR_KEY_VALUE_TYPE = 'value_type'
    STR_VALUE_TYPE_CONTINUOUS = 'type_continuous'  # 连续值变量
    STR_VALUE_TYPE_DISCRETE = 'type_discrete' # 离散值变量
    STR_KEY_INDEX = 'index'
