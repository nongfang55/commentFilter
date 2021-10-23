class StringKeyUtils:
    """用于存放各种字符串的工具类"""

    """和comment的元素相关，如link, code 等"""
    STR_REPLACE_KEY_TALK = 'cmm_talk'  # 谈话引用
    STR_REPLACE_KEY_LINK = 'cmm_link'  # 超链接
    STR_REPLACE_KEY_ELEMENT = 'cmm_element'  # 小型代码块
    STR_REPLACE_KEY_BLOCK = 'cmm_block'  # 大型代码块
    STR_REPLACE_KEY_AT = 'cmm_at'  # @用户
    STR_REPLACE_KEY_PIC = 'cmm_pic'  # 照片

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
    STR_VALUE_TYPE_DISCRETE = 'type_discrete'  # 离散值变量
    STR_KEY_INDEX = 'index'

    """tsv 文件使用到的"""
    STR_SPLIT_SEP_TSV = '\t'

    """csv 文件使用到的"""
    STR_SPLIT_SEP_CSV = ','

    """做路径分割可能需要的"""
    STR_SPLIT_SEP_ONE = '\\'
    STR_SPLIT_SEP_TWO = '/'

    """过滤日期需要的是"""
    STR_KEY_DATE_RANGE = 'dateRange'

    """ 基本统计信息一些键值 """
    STR_KET_MEAN_NUM = 'mean_num'
    STR_KEY_MAX_NUM = 'max_num'
    STR_KEY_MIN_NUM = 'min_num'
    STR_KEY_WEIGHT_MEAN = 'weight_num'
    STR_KEY_SUM_NUM = 'sum_num'

    """通用过滤需要的一些字段"""
    STR_KEY_FUN_FILTER = 'filter_func'
    STR_KEY_INDICATE = '_indicate'

    """离散值变量映射需要的变量"""
    STR_KEY_LABEL_MAP = 'label_map'

    '''pr timelineItem 可能会使用到的'''
    STR_KEY_PULL_REQUEST_NODE = 'pullrequest_node'
    STR_KEY_TIME_LINE_ITEM_NODE = 'timelineitem_node'
    STR_KEY_TIME_LINE_ITEMS = 'timelineItems'
    STR_KEY_EDGES = 'edges'
    STR_KEY_OID = 'oid'
    STR_KEY_ORIGIN = 'origin'
    STR_FAILED_FETCH = 'Failed to fetch'
    STR_KEY_ACTOR = 'actor'

    '''项目信息使用的key
    '''
    STR_KEY_ID = 'id'
    STR_KEY_NUMBER = 'number'
    STR_KEY_LANG = 'language'
    STR_KEY_OWNER = 'owner'
    STR_KEY_LANG_OTHER = 'Other'
    STR_KEY_NODE_ID = 'node_id'
    STR_KEY_NAME = 'name'
    STR_KEY_FULL_NAME = 'full_name'
    STR_KEY_DESCRIPTION = 'description'
    STR_KEY_CREATE_AT = 'created_at'
    STR_KEY_UPDATE_AT = 'updated_at'
    STR_KEY_STARGAZERS_COUNT = 'stargazers_count'
    STR_KEY_WATCHERS_COUNT = 'watchers_count'
    STR_KEY_LANGUAGE = 'language'
    STR_KEY_FORKS_COUNT = 'forks_count'
    STR_KEY_SUBSCRIBERS_COUNT = 'subscribers_count'
    STR_KEY_OWNER_LOGIN = 'owner_login'
    STR_KEY_PARENT_FULL_NAME = 'parent_full_name'
    STR_KEY_PARENT = 'parent'

    '''用户信息使用到的key '''
    STR_KEY_LOGIN = 'login'
    STR_KEY_SITE_ADMIN = 'site_admin'
    STR_KEY_TYPE = 'type'
    STR_KEY_EMAIL = 'email'
    STR_KEY_FOLLOWERS_URL = 'followers_url'
    STR_KEY_FOLLOWING_URL = 'following_url'
    STR_KEY_STARRED_URL = 'starred_url'
    STR_KEY_SUBSCRIPTIONS_URL = 'subscriptions_url'
    STR_KEY_ORGANIZATIONS_URL = 'organizations_url'
    STR_KEY_REPOS_URL = 'repos_url'
    STR_KEY_EVENTS_URL = 'events_url'
    STR_KEY_RECEVIED_EVENTS_URL = 'received_events_url'
    STR_KEY_COMPANY = 'company'
    STR_KEY_BLOG = 'blog'
    STR_KEY_LOCATION = 'location'
    STR_KEY_HIREABLE = 'hireable'
    STR_KEY_BIO = 'bio'
    STR_KEY_PUBLIC_REPOS = 'public_repos'
    STR_KEY_PUBLIC_GISTS = 'public_gists'
    STR_KEY_FOLLOWERS = 'followers'
    STR_KEY_FOLLOWING = 'following'
    STR_KEY_PARTICIPANTS = 'participants'
    STR_KEY_SITE_ADMIN_V4 = 'isSiteAdmin'
    STR_KEY_HIREABLE_V4 = 'isHireable'
    STR_KEY_WATCHING = 'watching'

    '''pull request可能会使用到的信息'''
    STR_KEY_STATE = 'state'
    STR_KEY_TITLE = 'title'
    STR_KEY_USER = 'user'
    STR_KEY_BODY = 'body'
    STR_KEY_CLOSED_AT = 'closed_at'
    STR_KEY_MERGED_AT = 'merged_at'
    STR_KEY_MERGE_COMMIT_SHA = 'merge_commit_sha'
    STR_KEY_AUTHOR_ASSOCIATION = 'author_association'
    STR_KEY_MERGED = 'merged'
    STR_KEY_COMMENTS = 'comments'
    STR_KEY_REVIEW_COMMENTS = 'review_comments'
    STR_KEY_COMMITS = 'commits'
    STR_KEY_ADDITIONS = 'additions'
    STR_KEY_DELETIONS = 'deletions'
    STR_KEY_CHANGED_FILES = 'changed_files'
    STR_KEY_HEAD = 'head'
    STR_KEY_BASE = 'base'
    STR_KEY_USER_ID = 'user_id'
    STR_KEY_BASE_LABEL = 'base_label'
    STR_KEY_HEAD_LABEL = 'head_label'
    STR_KEY_REPO_FULL_NAME = 'repo_full_name'
    STR_KEY_IS_PR = 'is_pr'
    STR_KEY_PULL_REQUEST = 'PullRequest'
    STR_KEY_ISSUE = 'Issue'
    STR_KEY_CREATE_AT_V4 = 'createdAt'
    STR_KEY_UPDATE_AT_V4 = 'updatedAt'
    STR_KEY_CLOSED_AT_V4 = 'closedAt'
    STR_KEY_MERGED_AT_V4 = 'mergedAt'
    STR_KEY_MERGE_COMMIT = 'mergeCommit'
    STR_KEY_AUTHOR_ASSOCIATION_V4 = 'authorAssociation'
    STR_KEY_REVIEWS = 'reviews'
    STR_KEY_CHANGED_FILES_V4 = 'changedFiles'
    STR_KEY_ISSUE_OR_PULL_REQUEST = 'issueOrPullRequest'
    STR_KEY_OPEN_V4 = 'OPEN'
    STR_KEY_CLOSED_V4 = 'CLOSED'
    STR_KEY_MERGED_V4 = 'MERGED'
    STR_KEY_OPEN_V3 = 'open'
    STR_KEY_CLOSED_V3 = 'closed'

    '''Branch 可能会使用的数据'''
    STR_KEY_LABEL = 'label'
    STR_KEY_REF = 'ref'
    STR_KEY_REPO = 'repo'
    STR_KEY_SHA = 'sha'
    STR_KEY_USER_LOGIN = 'user_login'
    STR_KEY_REPOSITORY = 'repository'
    STR_KEY_NAME_WITH_OWNER = 'nameWithOwner'
    STR_KEY_HEAD_REPOSITORY = 'headRepository'
    STR_KEY_BASE_REPOSITORY = 'baseRepository'
    STR_KEY_HEAD_REF_NAME = 'headRefName'
    STR_KEY_BASE_REF_NAME = 'baseRefName'
    STR_KEY_HEAD_REF_OID = 'headRefOid'
    STR_KEY_BASE_REF_OID = 'baseRefOid'

    '''review可能会使用放日数据'''
    STR_KEY_PULL_NUMBER = 'pull_number'
    STR_KEY_SUBMITTED_AT = 'submitted_at'
    STR_KEY_COMMIT_ID = 'commit_id'
    STR_KEY_SUBMITTED_AT_V4 = 'submittedAt'

    '''reviewThread可能会用到'''
    STR_KEY_REVIEW_THREAD_V4 = 'reviewThreads'

    '''review comment 可能会用到的数据'''
    STR_KEY_PULL_REQUEST_REVIEW_ID = 'pull_request_review_id'
    STR_KEY_DIFF_HUNK = 'diff_hunk'
    STR_KEY_PATH = 'path'
    STR_KEY_POSITION = 'position'
    STR_KEY_ORIGINAL_POSITION = 'original_position'
    STR_KEY_ORIGINAL_COMMIT_ID = 'original_commit_id'
    STR_KEY_START_LINE = 'start_line'
    STR_KEY_ORIGINAL_START_LINE = 'original_start_line'
    STR_KEY_START_SIDE = 'start_side'
    STR_KEY_LINE = 'line'
    STR_KEY_ORIGINAL_LINE = 'original_line'
    STR_KEY_SIDE = 'side'
    STR_KEY_IN_REPLY_TO_ID = 'in_reply_to_id'
    STR_KEY_CHANGE_TRIGGER = 'change_trigger'
    STR_KEY_DIFF_HUNK_V4 = 'diffHunk'
    STR_KEY_ORIGINAL_POSITION_V4 = 'originalPosition'
    STR_KEY_ORIGINAL_COMMIT = 'originalCommit'
    STR_KEY_IN_REPLY_TO_ID_V4 = 'replyTo'
    STR_KEY_PULL_REQUEST_REVIEW_NODE_ID = 'pull_request_review_node_id'

    '''issue comment 可能会使用的数据'''
    STR_KEY_BODY_V4 = 'bodyText'

    '''commit 可能会使用的数据'''
    STR_KEY_COMMIT = 'commit'
    STR_KEY_AUTHOR = 'author'
    STR_KEY_DATE = 'date'
    STR_KEY_AUTHOR_LOGIN = 'author_login'
    STR_KEY_COMMITTER = 'committer'
    STR_KEY_COMMITTER_LOGIN = 'committer_login'
    STR_KEY_COMMIT_AUTHOR_DATE = 'commit_author_date'
    STR_KEY_COMMIT_COMMITTER_DATE = 'commit_committer_date'
    STR_KEY_MESSAGE = 'message'
    STR_KEY_COMMIT_MESSAGE = 'commit_message'
    STR_KEY_COMMENT_COUNT = 'comment_count'
    STR_KEY_COMMIT_COMMENT_COUNT = 'commit_comment_count'
    STR_KEY_STATS = 'stats'
    STR_KEY_STATUS = 'status'  # 一个使用在commit一个使用在file
    STR_KEY_TOTAL = 'total'
    STR_KEY_STATUS_TOTAL = 'status_total'
    STR_KEY_STATUS_ADDITIONS = 'status_additions'
    STR_KEY_STATUS_DELETIONS = 'status_deletions'
    STR_KEY_PARENTS = 'parents'
    STR_KEY_FILES = 'files'
    STR_KEY_MESSAGE_BODY_V4 = 'messageBody'
    STR_KEY_COMMIT_AUTHOR_DATE_V4 = 'authoredDate'
    STR_KEY_COMMIT_COMMITTED_DATE_V4 = 'committedDate'
    STR_KEY_HAS_FILE_FETCHED = 'has_file_fetched'
    STR_KEY_TREE_OID = 'tree_oid'
    STR_KEY_TREE = 'tree'
    STR_KEY_BLOB = 'blob'

    '''v4 接口可能会用到的'''
    STR_KEY_ERRORS = 'errors'
    STR_KEY_TYPE_NAME_JSON = '__typename'
    STR_KEY_EDGE = 'edge'
    STR_KEY_TYPE_NAME = 'typename'
    STR_KEY_DATA = 'data'
    STR_KEY_NODES = 'nodes'
    STR_KEY_NODE = 'node'
    STR_KEY_DATABASE_ID = 'databaseId'
    STR_KEY_CURSOR = 'cursor'

    '''HeadRefForcePushedEvent 可能会使用到的'''
    STR_KEY_AFTER_COMMIT = 'afterCommit'
    STR_KEY_BEFORE_COMMIT = 'beforeCommit'
    STR_KEY_HEAD_REF_PUSHED_EVENT = 'HeadRefForcePushedEvent'

    '''PullRequestCommit 可能会使用到的'''
    STR_KEY_PULL_REQUEST_COMMIT = 'PullRequestCommit'

    '''time line item 可能会碰到的其他类型'''
    STR_KEY_ISSUE_COMMENT = 'IssueComment'
    STR_KEY_MENTIONED_EVENT = 'MentionedEvent'  # 被提及
    STR_KEY_SUBSCRIBED_EVENT = 'SubscribedEvent'  # 订阅事件
    STR_KEY_PULL_REQUEST_REVIEW = 'PullRequestReview'
    STR_KEY_PULL_REQUEST_REVIEW_THREAD = 'PullRequestReviewThread'  # 相当于review
    STR_KEY_PULL_REQUEST_REVISION_MARKER = 'PullRequestRevisionMarker'
    STR_KEY_MERGED_EVENT = 'MergedEvent'
    STR_KEY_CLOSED_EVENT = 'ClosedEvent'
    STR_KEY_REOPENED_EVENT = 'ReopenedEvent'
    STR_KEY_REFERENCED_EVENT = 'ReferencedEvent'  # commit引用，一般在最后merge到主干前做这个动作

    """日期转换用到的"""
    STR_STYLE_DATA_DATE = '%Y-%m-%dT%H:%M:%SZ'

    """计算信息熵用到的"""
    STR_KEY_FILTER_WORD_COUNT = "filter_word_count"
    STR_KEY_CAL_ELEMENT = "cal_element"
    STR_KEY_CAL_UNKNOWN = "cal_unknown"
    STR_KEY_GROUP_UNKNOWN = "group_unknown"
    STR_KEY_KEY_CAL = "key_col"
    STR_KEY_TOKEN_UNKNOWN = "<UNK>"
