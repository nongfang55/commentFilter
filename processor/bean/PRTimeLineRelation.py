import json
from datetime import datetime

from utils.StringKeyUtils import StringKeyUtils


class PRTimeLineRelation():
    """github中pull request的timeline 关系"""

    def __init__(self):
        self.repo_full_name = None
        self.pull_request_node = None
        self.timeline_item_node = None
        self.typename = None
        self.position = None
        self.origin = None
        self.create_at = None

        """可选属性 做简化使用的 实际不进入存储"""
        """force push相关"""
        self.headRefForcePushedEventAfterCommit = None
        self.headRefForcePushedEventBeforeCommit = None

        """review相关"""
        self.comments = []
        self.pull_request_review_commit = None
        self.pull_request_review_original_commit = None

        """issueComment内容"""
        self.body = None

        """pullrequestCommit相关"""
        self.pull_request_commit = None
        self.message = None

        """merge相关"""
        self.merge_commit = None

        """事件author"""
        self.user_login = None

    def parser(item):
        if item is not None and isinstance(item, str):
            item = json.loads(item)
        relation = PRTimeLineRelation()  # 返回结果为一系列关系
        relation.repo_full_name = item.get(StringKeyUtils.STR_KEY_REPO_FULL_NAME, None)
        """依据每个Item的TypeName来判断Item的具体类型"""
        """item的类型种类可以参考 https://developer.github.com/v4/union/pullrequesttimelineitems/"""
        relation.typename = item.get(StringKeyUtils.STR_KEY_TYPE_NAME_JSON, None)
        relation.timeline_item_node = item.get(StringKeyUtils.STR_KEY_ID, None)
        relation.position = item.get(StringKeyUtils.STR_KEY_POSITION, None)
        relation.origin = json.dumps(item)

        """按照感兴趣的类型 依次做出解析"""
        # 注：可能会有疏漏的代表commit的场景没有考虑
        if relation.typename == StringKeyUtils.STR_KEY_HEAD_REF_PUSHED_EVENT:
            """force push"""
            afterCommit = item.get(StringKeyUtils.STR_KEY_AFTER_COMMIT)
            if afterCommit is not None:
                relation.headRefForcePushedEventAfterCommit = afterCommit.get(StringKeyUtils.STR_KEY_OID, None)
            beforeCommit = item.get(StringKeyUtils.STR_KEY_BEFORE_COMMIT)
            if beforeCommit is not None:
                relation.headRefForcePushedEventBeforeCommit = beforeCommit.get(StringKeyUtils.STR_KEY_OID, None)
            if item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4, None) is not None:
                relation.create_at = datetime.strptime(item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4),
                                                                           StringKeyUtils.STR_STYLE_DATA_DATE)
            return relation
        elif relation.typename == StringKeyUtils.STR_KEY_PULL_REQUEST_COMMIT:
            """commit"""
            commit = item.get(StringKeyUtils.STR_KEY_COMMIT)
            if commit is not None and isinstance(commit, dict):
                relation.pull_request_commit = commit.get(StringKeyUtils.STR_KEY_OID, None)
                if commit.get(StringKeyUtils.STR_KEY_COMMIT_COMMITTED_DATE_V4, None) is not None:
                    relation.create_at = datetime.strptime(commit.get(StringKeyUtils.STR_KEY_COMMIT_COMMITTED_DATE_V4),
                                                                        StringKeyUtils.STR_STYLE_DATA_DATE)
            return relation
        elif relation.typename == StringKeyUtils.STR_KEY_MERGED_EVENT:
            """merge"""
            commit = item.get(StringKeyUtils.STR_KEY_COMMIT)
            if commit is not None and isinstance(commit, dict):
                relation.merge_commit = commit.get(StringKeyUtils.STR_KEY_OID, None)
            if item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4, None) is not None:
                relation.create_at = datetime.strptime(item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4),
                                                                        StringKeyUtils.STR_STYLE_DATA_DATE)
            actor = item.get(StringKeyUtils.STR_KEY_ACTOR)
            if actor is not None and isinstance(actor, dict):
                relation.user_login = actor.get(StringKeyUtils.STR_KEY_LOGIN)
            return relation
        elif relation.typename == StringKeyUtils.STR_KEY_PULL_REQUEST_REVIEW:
            """review 需要获取comments, commit和original_commit"""
            comments = item.get(StringKeyUtils.STR_KEY_COMMENTS).get(StringKeyUtils.STR_KEY_NODES)
            relation.comments = comments
            commit = item.get(StringKeyUtils.STR_KEY_COMMIT)
            if commit is not None and isinstance(commit, dict):
                relation.pull_request_review_commit = commit.get(StringKeyUtils.STR_KEY_OID, None)
            author = item.get(StringKeyUtils.STR_KEY_AUTHOR)
            if author is not None and isinstance(author, dict):
                relation.user_login = author.get(StringKeyUtils.STR_KEY_LOGIN)
            if item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4, None) is not None:
                relation.create_at = datetime.strptime(item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4),
                                                                           StringKeyUtils.STR_STYLE_DATA_DATE)
            return relation
        elif relation.typename == StringKeyUtils.STR_KEY_PULL_REQUEST_REVIEW_THREAD:
            """review thread 没有createAt字段，拿第一条comment的时间作为review时间"""
            comments = item.get(StringKeyUtils.STR_KEY_COMMENTS).get(StringKeyUtils.STR_KEY_NODES)
            relation.comments = comments
            if comments is not None and len(comments) > 0 and isinstance(comments, list):
                original_commit = comments[0].get(StringKeyUtils.STR_KEY_ORIGINAL_COMMIT)
                if comments[0].get(StringKeyUtils.STR_KEY_CREATE_AT_V4, None) is not None:
                    relation.create_at = datetime.strptime(comments[0].get(StringKeyUtils.STR_KEY_CREATE_AT_V4),
                                                                       StringKeyUtils.STR_STYLE_DATA_DATE)
                relation.user_login = comments[0].get(StringKeyUtils.STR_KEY_AUTHOR).get(
                    StringKeyUtils.STR_KEY_LOGIN)
                if original_commit is not None and isinstance(original_commit, dict):
                    relation.pull_request_review_commit = original_commit.get(StringKeyUtils.STR_KEY_OID, None)
            return relation
        elif relation.typename == StringKeyUtils.STR_KEY_ISSUE_COMMENT:
            """issueComment（也算做review的一种）"""
            author = item.get(StringKeyUtils.STR_KEY_AUTHOR)
            if author is not None:
                relation.user_login = author.get(StringKeyUtils.STR_KEY_LOGIN)
            relation.body = item.get(StringKeyUtils.STR_KEY_BODY_V4)
            if item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4, None) is not None:
                relation.create_at = datetime.strptime(item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4),
                                                                      StringKeyUtils.STR_STYLE_DATA_DATE)
            return relation
        elif relation.typename == StringKeyUtils.STR_KEY_CLOSED_EVENT:
            """pull request的closed事件"""
            if item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4, None) is not None:
                relation.create_at = datetime.strptime(item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4),
                                                                       StringKeyUtils.STR_STYLE_DATA_DATE)
                actor = item.get(StringKeyUtils.STR_KEY_ACTOR)
                if actor is not None and isinstance(actor, dict):
                    relation.user_login = actor.get(StringKeyUtils.STR_KEY_LOGIN)
            return relation
        elif relation.typename == StringKeyUtils.STR_KEY_REOPENED_EVENT:
            """pull request的reopen事件"""
            if item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4, None) is not None:
                relation.create_at = datetime.strptime(item.get(StringKeyUtils.STR_KEY_CREATE_AT_V4),
                                                                       StringKeyUtils.STR_STYLE_DATA_DATE)
            return relation
        else:
            """修改 不管如何都会返回relation"""
            return relation
